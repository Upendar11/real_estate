"""Stage 1: TTS per beat + render cumulative step images.  Stage 2: compose frames + audio into one MP4."""
import asyncio, json, os, re, sys, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(os.path.join(ROOT, os.environ.get("PLAN", "../scenes2/plan.json"))))
WORK = os.path.join(ROOT, os.environ.get("WORK", "work")); os.makedirs(WORK, exist_ok=True)
# Changed to female voice (amy-medium) for a young adult female narrator (age 21-25)
VOICE = os.path.expanduser("~/voices/en_US-amy-medium.onnx")
W, H, FPS = 1920, 1080, 30
SW, SH, SX, SY = 1653, 930, 133, 8           # scene area
FADE, GAP, LEAD, HOLD, OUT = 0.45, 0.45, 0.5, 1.2, 0.5

SPOKEN = [("PostgreSQL", "Postgres"), ("PostgresSQL", "Postgres"), ("pgAdmin", "P G admin"), ("psql", "P S Q L"), ("TIMESTAMPTZ", "timestamp T Z"), ("VARCHAR", "var char"), ("varchar", "var char"), ("BIGINT", "big int"), ("SMALLINT", "small int"), ("NULLIF", "null if"), ("ILIKE", "I like"), ("DATE_TRUNC", "date trunc"), ("plpgsql", "P L P G sequel"), ("1NF", "first normal form"), ("2NF", "second normal form"), ("3NF", "third normal form"), ("snake_case", "snake case"), ("updated_at", "updated at"), ("is_deleted", "is deleted"), ("SCD", "S.C.D."), ("JDBC", "J.D.B.C."),
          ("AUTO CDC", "auto C.D.C."), ("CDC", "C.D.C."), ("WAL", "W.A.L."), ("binlog", "bin log"),
          ("PySpark", "Pie Spark"), ("SQL", "sequel"), ("JSON", "jason"), ("op D", "op 'D'"),
          ("Debezium", "Dee-BEE-zee-um"), ("E00000001", "E, zero zero zero zero zero zero zero one"), ("E00000002", "E, zero zero zero zero zero zero zero two"), ("E_NEW_0001", "E new zero zero zero one"), ("E_NEW_0002", "E new zero zero zero two"), ("/p/2-fixed", "slash P slash two fixed"), ("event_id", "event I.D."), ("event_time", "event time"), ("ingested_at", "ingested at"), ("event_date", "event date"), ("device_type", "device type"), ("event_name", "event name"), ("event_type", "event type"), ("EXCEPT", "except"), ("DESCRIBE", "describe"), ("IDs", "I.D.s"), ("ID", "I.D.")]

ACR = {"DDL": "D D L", "DML": "D M L", "DCL": "D C L", "TCL": "T C L", "DQL": "D Q L", "CTEs": "C T Es", "CTE": "C T E", "CTAS": "C TAS", "DBMS": "D B M S", "UTC": "U T C", "OLTP": "O L T P", "ISBN": "I S B N", "SKU": "S K U", "ER": "E R", "FK": "F K", "PK": "P K", "SSN": "S S N", "RDDs": "R D Ds", "RDD": "R D D", "JVMs": "J V Ms", "JVM": "J V M", "UDFs": "U D Fs", "UDF": "U D F", "APIs": "A P Is",
       "API": "A P I", "DBFS": "D B F S", "UI": "U I", "ORC": "O R C", "TSV": "T S V", "CSV": "C S V", "HDFS": "H D F S",
       "AQE": "A Q E", "ML": "M L", "BI": "B I", "ETL": "E T L", "ETLs": "E T Ls", "GPUs": "G P Us", "CPU": "C P U", "OS": "O S",
       "VMs": "V Ms", "S3": "S three", "ADLS": "A D L S", "I/O": "I O", "ODBC": "O D B C", "DDDM": "D D D M", "SaaS": "sass",
       "PMC": "P M C", "EECS": "E E C S", "UC": "U C", "OOM": "out of memory", "ANSI": "ansi", "TB": "terabytes",
       "dbutils": "D B utils", "df": "D F", "DF": "D F", "DFs": "D Fs", "AWS": "A W S", "GCP": "G C P", "OBT": "O B T",
       "YARN": "yarn", "JAR": "jar", "SparkR": "Spark R", "sparklyr": "sparkly R", "HiveQL": "Hive Q L", "MLflow": "M L flow",
       "Z-Ordering": "Z ordering", "ZORDER": "Z order", "VACUUM": "vacuum", "ACID": "acid", "NaN": "not a number",
       "explain()": "explain", "%fs": "percent F S", "sc": "S C", "SQL": "sequel", "JSON": "jason", "PySpark": "Pie Spark"}

def spoken(s):
    for a, b in SPOKEN:
        s = re.sub((r"\b" if a[0].isalnum() else "") + re.escape(a) + (r"\b" if a[-1].isalnum() else ""), b, s)
    for a, b in ACR.items():
        s = re.sub((r"(?<![\w])" ) + re.escape(a) + r"(?![\w])", b, s)
    s = re.sub(r"([A-Za-z])\.([A-Za-z])", r"\1 dot \2", s)
    s = s.replace("()", "").replace("_", " ").replace("`", "")
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    return s

def tts():
    from piper import PiperVoice, SynthesisConfig
    v = PiperVoice.load(VOICE)
    cfg = SynthesisConfig(length_scale=1.08)
    for si, sc in enumerate(PLAN):
        for bi, b in enumerate(sc["beats"]):
            p = f"{WORK}/a_{si:02d}_{bi:02d}.wav"
            if os.path.exists(p):
                continue
            with wave.open(p, "wb") as wf:
                v.synthesize_wav(spoken(b["say"]), wf, syn_config=cfg)
    print("tts done")

async def render_steps():
    from playwright.async_api import async_playwright
    JS = open(os.path.join(ROOT, "bundle.js")).read()
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(); await pg.set_content("<html><body></body></html>"); await pg.add_script_tag(content=JS)
        shot = await br.new_page(viewport={"width": SW, "height": SH})
        for si, sc in enumerate(PLAN):
            steps = [s for b in sc["beats"] for s in b["steps"]]
            anchor = {**steps[0][0], "id": "anchor", "type": "rectangle", "x": 0, "y": 0, "width": 1280, "height": 720,
                      "strokeColor": "transparent", "backgroundColor": "transparent", "groupIds": [], "boundElements": None}
            cur = [anchor]
            for k, st in enumerate(steps):
                cur = cur + st
                p_ = f"{WORK}/i_{si:02d}_{k:03d}.png"
                if os.path.exists(p_):
                    continue
                svg = await pg.evaluate("""async (els)=>{const s=await window.exportToSvg({data:{elements:els,
                    appState:{exportBackground:true,viewBackgroundColor:'#fff'},files:{}},config:{padding:0}});
                    s.setAttribute('width','%d');s.setAttribute('height','%d');return s.outerHTML}""" % (SW, SH), cur)
                await shot.set_content("<html><body style='margin:0;background:#fff'>" + svg + "</body></html>")
                await shot.screenshot(path=p_)
            print("rendered", sc["name"], len(steps), flush=True)
        await br.close()

def wav_read(p):
    with wave.open(p) as w:
        sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    return sr, a

def sentences(s):
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z])", s.strip())
    out = []
    for p in parts:   # keep subtitles to 2 lines of ~58 chars
        words, cur = p.split(), ""
        chunks = []
        for w_ in words:
            if len(cur) + len(w_) + 1 > 100 and cur:
                chunks.append(cur); cur = w_
            else:
                cur = (cur + " " + w_).strip()
        chunks.append(cur)
        out += chunks
    return out

def wrap(s, n=58):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 > n and cur:
            lines.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    lines.append(cur)
    return lines

FONT = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 40)
def sub_img(s):
    lines = wrap(s)
    im = Image.new("RGBA", (W, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tw = max(d.textlength(l, font=FONT) for l in lines); th = 50 * len(lines)
    x0 = (W - tw) / 2 - 28; y0 = 190 - th - 24
    d.rounded_rectangle([x0, y0, x0 + tw + 56, y0 + th + 16], 14, fill=(20, 20, 24, 215))
    for i, l in enumerate(lines):
        d.text(((W - d.textlength(l, font=FONT)) / 2, y0 + 6 + i * 50), l, font=FONT, fill=(255, 255, 255, 255))
    a = np.array(im).astype(np.float32)
    return a[..., :3], a[..., 3:4] / 255.0

def compose():
    events, subs, audio_parts, scenes_t = [], [], [], []
    t = 0.0; sr = None
    for si, sc in enumerate(PLAN):
        s0 = t; t += LEAD; k = 0
        for bi, b in enumerate(sc["beats"]):
            sr, a = wav_read(f"{WORK}/a_{si:02d}_{bi:02d}.wav")
            d = len(a) / sr
            audio_parts.append((t, a))
            n = len(b["steps"])
            for j in range(n):
                events.append((t + j * (0.75 * d) / max(n, 1), si, k)); k += 1
            chunks = sentences(b["say"]); tot = sum(len(c) for c in chunks); tt = t
            for c in chunks:
                cd = d * len(c) / tot
                subs.append((tt, tt + cd, c)); tt += cd
            t += d + GAP
        t += HOLD
        scenes_t.append((s0, t + OUT, si, k)); t += OUT
    total = t
    print(f"total {total/60:.1f} min, {len(events)} steps", flush=True)
    # audio track
    track = np.zeros(int(total * sr) + sr, np.int16)
    for st, a in audio_parts:
        i = int(st * sr); track[i:i + len(a)] = a
    with wave.open(f"{WORK}/voice.wav", "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(track.tobytes())
    # srt
    def ts(x): return f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(x*1000%1000):03d}"
    with open(f"{WORK}/subtitles.srt", "w") as f:
        for i, (a, b, c) in enumerate(subs, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n")
    # frames
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", f"{WORK}/voice.wav", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest",
                           os.path.join(ROOT, os.environ.get("OUTFILE", "../CDC_explainer.mp4"))], stdin=subprocess.PIPE)
    white = np.full((H, W, 3), 255, np.uint8)
    cache, sub_cache = {}, {}
    def img(si, k):
        key = (si, k)
        if key not in cache:
            if len(cache) > 80: cache.clear()
            fr = white.copy()
            if k >= 0:
                fr[SY:SY + SH, SX:SX + SW] = np.array(Image.open(f"{WORK}/i_{si:02d}_{k:03d}.png").convert("RGB"))
            cache[key] = fr
        return cache[key]
    ev_by_scene = {}
    for (te, si, k) in events:
        ev_by_scene.setdefault(si, []).append((te, k))
    nframes = int(total * FPS)
    si_idx = 0; si_cur = scenes_t[0]; sub_i = 0
    for fi in range(nframes):
        tf = fi / FPS
        while si_idx < len(scenes_t) - 1 and tf >= scenes_t[si_idx][1]:
            si_idx += 1
        s0, s1, si, nst = scenes_t[si_idx]
        evs = ev_by_scene[si]
        # last fully shown step and current fading step
        done, fading, alpha = -1, None, 0
        for (te, k) in evs:
            if tf >= te + FADE: done = k
            elif tf >= te: fading, alpha = k, (tf - te) / FADE
        frame = img(si, done).astype(np.float32) if fading is None else \
            img(si, done).astype(np.float32) * (1 - alpha) + img(si, fading).astype(np.float32) * alpha
        if tf > s1 - OUT:                                   # fade out to white at scene end
            a = min(1, (tf - (s1 - OUT)) / OUT)
            frame = frame * (1 - a) + 255 * a
        while sub_i < len(subs) and tf >= subs[sub_i][1]:
            sub_i += 1
        if sub_i < len(subs) and subs[sub_i][0] <= tf < subs[sub_i][1]:
            c = subs[sub_i][2]
            if c not in sub_cache:
                sub_cache.clear(); sub_cache[c] = sub_img(c)
            rgb, al = sub_cache[c]
            band = frame[H - 195:H - 5]
            frame[H - 195:H - 5] = band * (1 - al) + rgb * al
        ff.stdin.write(frame.astype(np.uint8).tobytes())
        if fi % 1800 == 0: print(f"frame {fi}/{nframes}", flush=True)
    ff.stdin.close(); ff.wait()
    print("video done")

if __name__ == "__main__":
    stage = sys.argv[1]
    if stage == "tts": tts()
    elif stage == "render": asyncio.run(render_steps())
    elif stage == "compose": compose()
