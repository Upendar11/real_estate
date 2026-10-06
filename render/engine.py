"""Animated explainer engine: static Excalidraw steps + keyframed sprite actors + host + zoom + sfx + music."""
import asyncio, hashlib, json, math, os, re, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN_PATH = os.path.join(ROOT, os.environ.get("PLAN", "../scenes4/plan.json"))
WORK = os.path.join(ROOT, os.environ.get("WORK", "work4"))
OUTFILE = os.path.join(ROOT, os.environ.get("OUTFILE", "../Iceberg_Project009_animated.mp4"))
VOICE = os.path.expanduser("~/voices/en_US-ryan-high.onnx")
os.makedirs(WORK, exist_ok=True)
PLAN = json.load(open(PLAN_PATH))

W, H, FPS = 1920, 1080, 30
SW, SH, SX, SY = 1653, 930, 133, 8
K = SW / 1280
FADE, GAP, LEAD, HOLD, OUT = 0.45, 0.45, 0.6, 1.0, 0.5
HOME = (1205, 708)
SR = 22050

import make_video as mv          # reuse spoken(), sentences(), wrap(), sub_img()

def h(s):
    return hashlib.md5(s.encode()).hexdigest()[:12]

# ------------------------------------------------------------------ 1. TTS
def tts():
    from piper import PiperVoice, SynthesisConfig
    v = PiperVoice.load(VOICE); cfg = SynthesisConfig(length_scale=1.06)
    n = 0
    for sc in PLAN:
        for b in sc["beats"]:
            if not b["say"]:
                continue
            p = f"{WORK}/v_{h(b['say'])}.wav"
            if not os.path.exists(p):
                with wave.open(p, "wb") as wf:
                    v.synthesize_wav(mv.spoken(b["say"]), wf, syn_config=cfg); n += 1
    print("tts new:", n)

# ------------------------------------------------------------------ 2. static steps
async def render_steps():
    from playwright.async_api import async_playwright
    JS = open(os.path.join(ROOT, "bundle.js")).read()
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(); await pg.set_content("<html><body></body></html>"); await pg.add_script_tag(content=JS)
        shot = await br.new_page(viewport={"width": SW, "height": SH})
        for si, sc in enumerate(PLAN):
            steps = [s for b in sc["beats"] for s in b["steps"]]
            if not steps:
                continue
            anchor = {**steps[0][0], "id": "anchor", "type": "rectangle", "x": 0, "y": 0, "width": 1280, "height": 720, "angle": 0,
                      "strokeColor": "transparent", "backgroundColor": "transparent", "groupIds": [], "boundElements": None}
            cur = [anchor]
            for k, st in enumerate(steps):
                cur = cur + st
                p_ = f"{WORK}/i_{sc['name']}_{k:03d}.png"
                if os.path.exists(p_):
                    continue
                svg = await pg.evaluate("""async ([els,w,h])=>{const s=await window.exportToSvg({data:{elements:els,
                    appState:{exportBackground:true,viewBackgroundColor:'#fff'},files:{}},config:{padding:0}});
                    s.setAttribute('width',w);s.setAttribute('height',h);return s.outerHTML}""", [cur, SW, SH])
                await shot.set_content("<html><body style='margin:0;background:#fff'>" + svg + "</body></html>")
                await shot.screenshot(path=p_)
            print("rendered", sc["name"], len(steps), flush=True)
        await br.close()

# ------------------------------------------------------------------ 3. timeline
def wav(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def timeline():
    t = 0.0; scenes = []; voice = []; subs = []; sfx = []; host_kf = [(0.0, 1420, HOME[1], 1.0, 0)]; poses = []
    chapters = []
    for si, sc in enumerate(PLAN):
        s0 = t
        if sc.get("chapter"):
            chapters.append(s0)
        S = {"name": sc["name"], "start": s0, "events": [], "actors": {}, "focus": [], "si": si}
        t += LEAD
        if si == 0:
            host_kf.append((t + 0.1, 1420, HOME[1], 1.0, 0)); host_kf.append((t + 2.2, HOME[0], HOME[1], 1.0, 1))
        if sc.get("chapter"):
            host_kf.append((s0 + 0.05, HOME[0], HOME[1], 1.0, 0)); host_kf.append((s0 + 1.4, 380, 690, 1.9, 1))
        k = 0
        for bi, b in enumerate(sc["beats"]):
            if b["say"]:
                a = wav(f"{WORK}/v_{h(b['say'])}.wav"); d = len(a) / SR
                voice.append((t, a))
                chunks = mv.sentences(b["say"]); tot = sum(len(c) for c in chunks); tt = t
                for c in chunks:
                    cd = d * len(c) / tot; subs.append((tt, tt + cd, c)); tt += cd
            else:
                d = b["dur"] or 2.0
            n = len(b["steps"])
            for j in range(n):
                te = t + j * (0.75 * d) / max(n, 1)
                S["events"].append((te, k)); k += 1
                if not b.get("quiet"): sfx.append((te, "pop", 0.18))
            for name, f in b["sfx"]:
                sfx.append((t + f * d, name, 1.0))
            poses.append((t, b["host"] or ("point" if bi % 2 == 1 else "stand")))
            S["focus"].append((t, b["focus"]))
            for act in b["acts"]:
                A = S["actors"].setdefault(act["id"], [])
                for kf in act["kf"]:
                    kk = dict(kf); kk["T"] = t + kf["t"] * d; kk.setdefault("sprite", act["sprite"])
                    A.append(kk)
                    if kk.get("pop"): sfx.append((kk["T"], "pop", 0.5))
                    if kk.get("whoosh"):
                        prev = [q for q in A[:-1]]
                        sfx.append(((prev[-1]["T"] if prev else kk["T"]), "whoosh", 0.45))
            t += d + GAP
        t += HOLD
        if sc.get("chapter"):
            host_kf.append((t - 0.3, 380, 690, 1.9, 0)); host_kf.append((t + OUT + 1.0, HOME[0], HOME[1], 1.0, 1))
        S["end"] = t + OUT; S["nsteps"] = k
        scenes.append(S); t += OUT
    for S in scenes:
        for A in S["actors"].values():
            A.sort(key=lambda q: q["T"])
    return {"total": t, "scenes": scenes, "voice": voice, "subs": subs, "sfx": sfx, "host": host_kf, "poses": poses, "chapters": chapters}

# ------------------------------------------------------------------ 4. audio
def synth(name):
    n = lambda s: int(s * SR)
    tt = lambda s: np.arange(n(s)) / SR
    if name == "pop":
        t = tt(0.09); f = 900 * np.exp(-t * 25) + 300
        return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45)
    if name == "whoosh":
        t = tt(0.45); noise = np.random.default_rng(1).standard_normal(len(t))
        y = np.zeros_like(noise); a = 0.0
        for i in range(len(noise)):
            c = 0.02 + 0.25 * math.sin(math.pi * i / len(noise)); a += c * (noise[i] - a); y[i] = a
        return 0.9 * y * np.sin(np.pi * t / t[-1])
    if name == "ding":
        t = tt(1.2)
        return 0.35 * (np.sin(2 * np.pi * 1318.5 * t) + 0.6 * np.sin(2 * np.pi * 1975.5 * t) * np.exp(-t * 3)) * np.exp(-t * 4)
    if name == "buzz":
        t = tt(0.35); sq = np.sign(np.sin(2 * np.pi * 110 * t))
        return 0.18 * sq * np.minimum(1, (0.35 - t) * 12)
    if name == "chime":
        t = tt(1.6); out = np.zeros(len(t))
        for i, f in enumerate([784, 988, 1175]):
            s = n(i * 0.12); tt2 = t[: len(t) - s]
            out[s:] += 0.22 * np.sin(2 * np.pi * f * tt2) * np.exp(-tt2 * 3.5)
        return out
    if name == "tick":
        t = tt(0.06)
        return 0.45 * np.sin(2 * np.pi * 2000 * t) * np.exp(-t * 80)
    raise ValueError(name)

def music(total):
    """Gentle procedural lo-fi bed: Cmaj7 - Am7 - Fmaj7 - G6, 76 bpm."""
    beat = 60 / 76; bar = 4 * beat
    chords = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 64]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    N = int(total * SR) + SR; out = np.zeros(N)
    t_bar = np.arange(int(bar * SR)) / SR
    env = np.minimum(1, t_bar / 0.6) * np.minimum(1, (bar - t_bar) / 0.6)
    b = 0
    while b * bar < total + 1:
        ch = chords[b % 4]; s = int(b * bar * SR); seg = np.zeros(len(t_bar))
        for m in ch:
            f = hz(m - 12)
            seg += np.sin(2 * np.pi * f * t_bar) + 0.3 * np.sin(2 * np.pi * f * 1.003 * t_bar)
        seg *= env * 0.05
        for i in range(8):                                    # soft arpeggio, eighth notes
            m = ch[[0, 2, 1, 3, 2, 1, 3, 2][i]] + 12
            ps = int(i * beat / 2 * SR); tl = t_bar[: len(t_bar) - ps]
            seg[ps:] += 0.035 * np.sin(2 * np.pi * hz(m) * tl) * np.exp(-tl * 5)
        e = min(N, s + len(seg)); out[s:e] += seg[: e - s]; b += 1
    from scipy.signal import lfilter
    return lfilter([0.18], [1, -0.82], out)

def mix(TL):
    total = TL["total"]; N = int(total * SR) + SR
    v = np.zeros(N); fx = np.zeros(N)
    for st, a in TL["voice"]:
        i = int(st * SR); v[i:i + len(a)] += a
    cache = {}
    for st, name, vol in TL["sfx"]:
        if name not in cache: cache[name] = synth(name)
        s = cache[name]; i = int(st * SR); e = min(N, i + len(s)); fx[i:e] += vol * 0.5 * s[: e - i]
    m = music(total)[:N]
    # duck music under the voice
    env = np.abs(v); k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = np.where(env > 0.01, 0.45, 1.0)
    duck = np.convolve(duck, np.ones(k) / k, mode="same")
    m = m / (np.abs(m).max() + 1e-9) * 0.16 * duck
    fade = np.minimum(1, np.arange(N) / (2 * SR)) * np.minimum(1, (N - np.arange(N)) / (3 * SR))
    y = v + fx + m * fade
    y = y / max(1.0, np.abs(y).max() / 0.95)
    with wave.open(f"{WORK}/mix.wav", "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((y * 32767).astype(np.int16).tobytes())
    # talk envelope per video frame
    hop = SR // FPS; nf = int(total * FPS) + 2
    rms = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) if i * hop < N else 0 for i in range(nf)])
    np.save(f"{WORK}/talk.npy", rms > 0.025)

# ------------------------------------------------------------------ 5. frames
SPR = {}
META = json.load(open(os.path.join(ROOT, "sprites/meta.json")))
def sprite(name):
    if name not in SPR:
        SPR[name] = Image.open(os.path.join(ROOT, f"sprites/{name}.png")).convert("RGBA")
    return SPR[name]

def ease(p):
    p = max(0.0, min(1.0, p)); return p * p * (3 - 2 * p)

def actor_state(kfs, t):
    """Return dict(sprite,x,y,s,o,flip,angle,bob) or None."""
    if not kfs or t < kfs[0]["T"]:
        return None
    i = 0
    while i + 1 < len(kfs) and kfs[i + 1]["T"] <= t:
        i += 1
    a = kfs[i]
    st = {"sprite": a["sprite"], "x": a["x"], "y": a["y"], "s": a.get("s", 1.0), "o": a.get("o", 1.0),
          "flip": a.get("flip", 0), "angle": 0.0, "bob": 0.0, "cycle": a.get("cycle"), "period": a.get("period", 0.4)}
    # carry sprite/scale forward from earlier keys when not overridden
    for q in kfs[: i + 1]:
        if "cycle" in q: st["cycle"], st["period"] = q["cycle"], q.get("period", 0.4)
    if "s" not in a:
        for q in kfs[: i + 1][::-1]:
            if "s" in q: st["s"] = q["s"]; break
    if i + 1 < len(kfs):
        b = kfs[i + 1]; dur = b["T"] - a["T"]; p = (t - a["T"]) / dur if dur > 0 else 1
        e = ease(p)
        st["x"] = a["x"] + (b["x"] - a["x"]) * e; st["y"] = a["y"] + (b["y"] - a["y"]) * e
        if "o" in b: st["o"] = a.get("o", 1.0) + (b["o"] - a.get("o", 1.0)) * e
        if b.get("flip") is not None and (b["x"] - a["x"]) != 0: st["flip"] = b.get("flip", 0)
        if (b.get("walk")) and 0 < p < 1:
            ph = (t - a["T"]) * 3.2
            st["angle"] = 7 * math.sin(2 * math.pi * ph); st["bob"] = 6 * abs(math.sin(2 * math.pi * ph))
        if b.get("slide") and 0 < p < 1:
            st["bob"] = 2 * abs(math.sin(2 * math.pi * (t - a["T"]) * 1.2))
    if a.get("pop"):
        p = (t - a["T"]) / 0.35
        if p < 1:
            st["s"] *= max(0.05, 0.3 + 0.7 * ease(p) + 0.25 * math.sin(math.pi * p))
    if st["cycle"]:
        st["sprite"] = st["cycle"][int(t / st["period"]) % len(st["cycle"])]
    return st

SCALES = {"ant": 1.2, "turtle": 1.4, "squirrel": 1.4, "pip": 1.15, "sheep": 1.4, "dog": 1.4, "duck": 1.8, "owl": 1.5, "parrot": 1.7, "snail": 1.3, "eng": 1.3, "asha": 1.15, "mira": 1.15,
          "b_": 1.6, "stamp": 1.6, "cube": 1.0}
def base_scale(name):
    for k, v in SCALES.items():
        if name.startswith(k): return v
    return 1.0

def draw_sprite(canvas, st, ox=0, oy=0):
    if st is None or st["o"] <= 0.01:
        return
    nm = st["sprite"]
    if st["flip"] and nm + "_L" in META:
        nm = nm + "_L"
    im = sprite(nm); m = META[nm]
    if st["flip"] and nm == st["sprite"]:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    s = st["s"] * base_scale(st["sprite"])
    if abs(s - 1) > 0.01:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    if abs(st["angle"]) > 0.2:
        im = im.rotate(st["angle"], resample=Image.BILINEAR, center=(im.width / 2, im.height * 0.9))
    if st["o"] < 0.99:
        a = im.getchannel("A").point(lambda v: int(v * st["o"])); im = im.copy(); im.putalpha(a)
    px = ox + st["x"] * K - (m["m"] + m["w"] / 2) * K * s
    py = oy + (st["y"] - st["bob"]) * K - (m["m"] + m["h"]) * K * s
    canvas.alpha_composite(im, (int(px), int(py))) if canvas.mode == "RGBA" else canvas.paste(im, (int(px), int(py)), im)

def focus_rect(S, t):
    full = (0, 0, 1280, 720)
    def norm(r):
        if not r: return full
        x, y, w, hh = r; cx, cy = x + w / 2, y + hh / 2
        w = min(1280, max(w, hh * 16 / 9)); hh = w * 9 / 16
        return (min(max(0, cx - w / 2), 1280 - w), min(max(0, cy - hh / 2), 720 - hh), w, hh)
    def at(a, b, t0, tt):
        e = ease((tt - t0) / 0.9)
        return tuple(a[i] + (b[i] - a[i]) * e for i in range(4))
    frm, to, tc = full, full, -99.0
    for (tb, r) in S["focus"]:
        if tb > t: break
        new = norm(r)
        if new != to:
            frm = at(frm, to, tc, tb); to = new; tc = tb
    return at(frm, to, tc, t)

def host_state(TL, t, talk, fi):
    kf = TL["host"]; i = 0
    while i + 1 < len(kf) and kf[i + 1][0] <= t: i += 1
    t0, x0, y0, s0, _ = kf[i]
    x, y, s, ang, bob = x0, y0, s0, 0.0, 0.0
    if i + 1 < len(kf):
        t1, x1, y1, s1, walk = kf[i + 1]; p = (t - t0) / (t1 - t0); e = ease(p)
        x, y, s = x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, s0 + (s1 - s0) * e
        if walk and 0 < p < 1:
            ph = (t - t0) * 3.0; ang = 7 * math.sin(2 * math.pi * ph); bob = 6 * abs(math.sin(2 * math.pi * ph))
    bob += 2.5 * (1 + math.sin(2 * math.pi * t * 0.8))
    pose = "stand"
    for (tp, ps) in TL["poses"]:
        if tp <= t: pose = ps
        else: break
    flip = 0
    if i + 1 < len(kf) and kf[i + 1][1] > x0 and kf[i + 1][4] and t < kf[i + 1][0]:
        flip = 1
    name = f"pip_{pose}"
    if talk and (fi // 3) % 2 == 0:
        name += "_talk"
    elif not talk and (t % 3.3) < 0.13:
        name += "_blink"
    return {"sprite": name, "x": x, "y": y, "s": s, "o": 1, "flip": flip, "angle": ang, "bob": bob, "cycle": None}

def render_scene(args):
    si, TL = args
    S = TL["scenes"][si]; name = S["name"]
    talk = np.load(f"{WORK}/talk.npy")
    f0, f1 = round(S["start"] * FPS), round(S["end"] * FPS)
    seg = f"{WORK}/seg_{si:02d}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-tune", "animation", "-crf", os.environ.get("CRF", "19"), "-pix_fmt", "yuv420p", seg], stdin=subprocess.PIPE)
    white_scene = Image.new("RGB", (SW, SH), "white")
    imgs = {}
    def step_img(k):
        if k < 0: return white_scene
        if k not in imgs:
            imgs[k] = Image.open(f"{WORK}/i_{name}_{k:03d}.png").convert("RGB")
        return imgs[k]
    subs = TL["subs"]; sub_cache = {}
    font_ch = TL["chapters"]; total = TL["total"]
    for fi in range(f0, f1):
        t = fi / FPS
        done, fading, alpha = -1, None, 0
        for (te, k) in S["events"]:
            if t >= te + FADE: done = k
            elif t >= te: fading, alpha = k, (t - te) / FADE
        sc = step_img(done)
        if fading is not None:
            sc = Image.blend(sc, step_img(fading), ease(alpha))
        sc = sc.copy()
        for kfs in S["actors"].values():
            draw_sprite(sc, actor_state(kfs, t))
        fx, fy, fw, fh = focus_rect(S, t)
        if fw < 1279:
            sc = sc.crop((int(fx * K), int(fy * K), int((fx + fw) * K), int((fy + fh) * K))).resize((SW, SH), Image.BILINEAR)
        frame = Image.new("RGB", (W, H), "white"); frame.paste(sc, (SX, SY))
        if t > S["end"] - OUT:
            frame = Image.blend(frame, Image.new("RGB", (W, H), "white"), ease((t - (S["end"] - OUT)) / OUT))
        draw_sprite(frame, host_state(TL, t, bool(talk[min(fi, len(talk) - 1)]), fi), SX, SY)
        d = ImageDraw.Draw(frame)
        d.rectangle([0, 0, W, 7], fill="#e9ecef"); d.rectangle([0, 0, int(W * t / total), 7], fill="#20c997")
        for c in font_ch:
            xc = int(W * c / total); d.rectangle([xc - 1, 0, xc + 1, 7], fill="#495057")
        for (a, b, c) in subs:
            if a <= t < b:
                if c not in sub_cache:
                    sub_cache.clear(); rgb, al = mv.sub_img(c)
                    im = Image.fromarray(np.concatenate([rgb, al * 255], axis=2).astype(np.uint8), "RGBA"); sub_cache[c] = im
                frame.paste(sub_cache[c], (0, H - 195), sub_cache[c]); break
        ff.stdin.write(frame.tobytes())
    ff.stdin.close(); ff.wait()
    return si

def compose(TL, only=None):
    idx = only if only is not None else list(range(len(TL["scenes"])))
    with Pool(2) as p:
        TLs = {k: v for k, v in TL.items() if k != "voice"}
        for si in p.imap_unordered(render_scene, [(i, TLs) for i in idx]):
            print("segment", si, TL["scenes"][si]["name"], flush=True)

def final(TL):
    with open(f"{WORK}/segs.txt", "w") as f:
        for si in range(len(TL["scenes"])):
            f.write(f"file 'seg_{si:02d}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/segs.txt", "-i", f"{WORK}/mix.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", OUTFILE], check=True)
    def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x*1000%1000):03d}"
    with open(f"{WORK}/subtitles.srt", "w") as f:
        for i, (a, b, c) in enumerate(TL["subs"], 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n")
    if os.path.getsize(OUTFILE) > 29.3 * 1024 * 1024:
        small = OUTFILE + ".small.mp4"
        subprocess.run([os.path.join(ROOT, "shrink2p.sh"), OUTFILE, small], check=True)
        os.replace(small, OUTFILE)
    print("done", OUTFILE, os.path.getsize(OUTFILE) // 1024 // 1024, "MB")

if __name__ == "__main__":
    st = sys.argv[1]
    if st == "tts": tts()
    elif st == "steps": asyncio.run(render_steps())
    else:
        TL = timeline(); print(f"total {TL['total']/60:.1f} min")
        if st in ("audio", "all"): mix(TL)
        if st == "scene": compose(TL, [int(x) for x in sys.argv[2].split(",")])
        if st in ("frames", "all"): compose(TL)
        if st in ("final", "all"): final(TL)
