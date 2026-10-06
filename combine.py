"""Merge episode plans (OUT/epNN/plan.json) into long videos, ~4 episodes each, per series.json groups. Usage: python3 combine.py 1 2 3"""
import json, os, copy, shutil, glob
from gen import text, box
from gen2 import T, merge
from course import card, COLORS

ROOT = os.path.dirname(os.path.abspath(__file__))
_CFG = json.load(open(os.path.join(ROOT, "series.json")))
SER = _CFG["out"]
GROUPS = [(g[0], g[1]) for g in _CFG["groups"]]
WORDS = ["one", "two", "three", "four"]

def ep_title(n):
    first = open(os.path.join(ROOT, f"{SER}/ep{n:02d}/script.md")).readline()
    return first.split(":", 1)[1].strip()

def B(say, steps, **k):
    d = {"say": say, "steps": steps, "acts": [], "sfx": [], "focus": None, "host": None, "dur": None, "quiet": False}
    d.update(k); return d

def build(vi):
    name, eps = GROUPS[vi]
    titles = [ep_title(n) for n in eps]
    out = []
    # video intro
    hi = {"id": "hi", "sprite": "b_hi" if vi == 0 else "b_welcome",
          "kf": [dict(t=0.2, x=1000, y=520, pop=1, flip=1), dict(t=0.95, x=1000, y=520, o=0, flip=1)]}
    intro_steps = [text(640, 100, f"{_CFG['name']} · Video {vi+1} of {len(GROUPS)}", 30, "grey", align="center"),
                   box(140, 150, 1000, 150, "", "blue", fill="hachure"),
                   text(640, 195, name, 46 if len(name) < 30 else 38, align="center")]
    greet = (_CFG.get("welcome", f"Hi! I'm Pip, and welcome to {_CFG['name']}. ") if vi == 0 else f"Welcome back to {_CFG['name']}! ") + f"This is video {vi+1} of {len(GROUPS)}: {name}."
    agenda = [card(170, 340 + i * 62, 900, f"Topic {i+1}.  {t}", COLORS[i], fs=24, minh=52)[0] for i, t in enumerate(titles)]
    out.append({"name": "v_intro", "chapter": None, "beats": [
        B(greet, intro_steps, acts=[hi], host="happy"),
        B(f"It covers {len(eps)} topics: " + "; ".join(titles) + ".", agenda, host="point")]})
    for ti, n in enumerate(eps):
        plan = json.load(open(os.path.join(ROOT, f"{SER}/ep{n:02d}/plan.json")))
        intro, body, outro = plan[0], plan[1:-1], plan[-1]
        # topic card replaces the episode intro
        tc = copy.deepcopy(intro)
        tc["name"] = f"t{ti+1}_00_topic"; tc["chapter"] = f"Topic {ti+1}"
        tc["beats"][0] = B(f"Topic {WORDS[ti]}: {titles[ti]}.", [
            text(640, 110, f"Topic {ti+1} of {len(eps)}", 34, "grey", align="center"),
            box(140, 150, 1000, 150, "", COLORS[ti], fill="hachure"),
            text(640, 200, titles[ti], 44 if len(titles[ti]) < 34 else 34, align="center")],
            sfx=[("chime", 0.05)], host="happy")
        tc["beats"][1]["say"] = tc["beats"][1]["say"].replace("In this episode", "In this topic")
        out.append(tc)
        for s in body:
            s = copy.deepcopy(s); s["name"] = f"t{ti+1}_{s['name']}"
            if s.get("chapter"): s["chapter"] = None
            out.append(s)
        oc = copy.deepcopy(outro); oc["name"] = f"t{ti+1}_{oc['name']}"
        oc["beats"][0]["say"] = f"Let's recap topic {WORDS[ti]}."
        last = oc["beats"][-1]
        if ti < len(eps) - 1:
            oc["beats"] = oc["beats"][:-1]           # drop "next time"
        elif vi < len(GROUPS) - 1:
            nxt = GROUPS[vi + 1][0]
            last["say"] = f"That's the end of video {vi+1}. Next video: {nxt}. See you there!"
            last["steps"] = [[e for e in st if e.get("type") != "text"] + text(620, e0y(st), f"Next video: {nxt}", 30, "blue", align="center")
                             for st in last["steps"]]
        out.append(oc)
    d = os.path.join(ROOT, f"{SER}/v{vi+1}")
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, "plan.json"), "w"))
    words = sum(len(b["say"].split()) for s in out for b in s["beats"])
    print(f"video {vi+1}: {name} · {len(out)} scenes · ~{words/140:.0f} min")
    # reuse narration already generated
    w = os.path.join(ROOT, f"render/work_{SER}_v{vi+1}"); os.makedirs(w, exist_ok=True)
    for n in eps:
        for f in glob.glob(os.path.join(ROOT, f"render/work_ep{n:02d}/v_*.wav")):
            t = os.path.join(w, os.path.basename(f))
            if not os.path.exists(t): shutil.copy(f, t)

def e0y(st):
    ys = [e["y"] for e in st if e.get("type") == "text"]
    return ys[0] if ys else 600

if __name__ == "__main__":
    import sys
    for a in sys.argv[1:]:
        build(int(a) - 1)
