"""Story layer: Episode subclass with student/mentor dialogue scenes, auto-fit tables, practice and memory hooks.
Series settings come from series.json in the project folder (name, out, end_line, groups)."""
import hashlib, json, os
import course
_CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "series.json")))
course.SERIES = _CFG["name"]
course.OUT = _CFG["out"]
course.END_LINE = _CFG.get("end_line", "That's the end of the series. Thanks for watching!")
from course import *          # noqa: F401,F403  (B, A, card, wrap, bubble, COLORS, Episode)
from gen import text, box, line
from gen2 import T, merge

ASHA = (165, 668)
MIRA = (1010, 668)
WHO = {"A": ("Asha", "orange"), "M": ("Mira", "violet"), "N": ("", "yellow")}


def sb(txt):
    """Short speech-bubble sprite (keep under ~18 chars a line)."""
    return bubble("b_" + hashlib.md5(txt.encode()).hexdigest()[:8], txt)


def _ml(c):
    return max(len(l) for l in str(c).split("\n"))


def colw_for(header, rows, fs, minw=60, maxw=2000):
    ws = []
    for j, h in enumerate(header):
        m = max([_ml(h)] + [_ml(r[j]) for r in rows])
        ws.append(int(min(maxw, max(minw, m * fs * 0.62 + 28))))
    return ws


def fit_table(header, rows, fs, limit=1160):
    import textwrap
    rows = [[str(c) for c in r] for r in rows]
    for _ in range(8):
        ws = colw_for(header, rows, fs)
        if sum(ws) <= limit:
            break
        j = max(range(len(ws)), key=lambda k: ws[k])
        target = int(max(_ml(r[j]) for r in rows) * 0.62)
        if target < 14:
            break
        rows = [r[:j] + ["\n".join(textwrap.wrap(r[j].replace("\n", " "), target))] + r[j + 1:] for r in rows]
    while fs > 13 and sum(colw_for(header, rows, fs)) > limit:
        fs -= 1
    return fs, colw_for(header, rows, fs), rows


class StoryEp(Episode):
    # ------------------------------------------------------------ story scene with the two characters
    def story(self, title, lines, name="story"):
        """lines: (who, on_screen, say[, pose]) ; who in A / M / N. Splits into scenes so cards never overlap the actors."""
        chunks, cur, hsum = [], [], 0
        for ln in lines:
            who = ln[0]
            w = 620 if who == "N" else 600
            h = card(0, 0, w, ln[1], fs=22)[1] + 12
            if cur and hsum + h > 520:
                chunks.append(cur); cur, hsum = [], 0
            cur.append(ln); hsum += h
        if cur:
            chunks.append(cur)
        for ci, ch in enumerate(chunks):
            beats, y = [], 108
            for bi, ln in enumerate(ch):
                who, scr, say = ln[0], ln[1], ln[2]
                pose = ln[3] if len(ln) > 3 else None
                nm, col = WHO[who]
                if who == "N":
                    x, w = 280, 620
                    els, h = card(x, y, w, scr, "yellow", fs=22, fill="solid", center=True, minh=50)
                elif who == "A":
                    x, w = 270, 600
                    els, h = card(x, y, w, f"{nm}: {scr}", col, fs=22, minh=50)
                else:
                    x, w = 320, 600
                    els, h = card(x, y, w, f"{nm}: {scr}", col, fs=22, minh=50)
                y += h + 12
                steps = [els]
                acts = []
                if bi == 0:
                    steps = [T(title)] + steps
                    if ci == 0:
                        acts += [A("asha", "asha", (0.0, -120, ASHA[1], {"o": 1}), (0.25, ASHA[0], ASHA[1], {"walk": 1})),
                                 A("mira", "mira_L", (0.0, 1400, MIRA[1]), (0.25, MIRA[0], MIRA[1], {"walk": 1}))]
                    else:
                        acts += [A("asha", "asha", (0.0, ASHA[0], ASHA[1])), A("mira", "mira_L", (0.0, MIRA[0], MIRA[1]))]
                if who == "A":
                    acts.append(A("asha", "asha" + ("_" + pose if pose else ""), (0.02, ASHA[0], ASHA[1])))
                    acts.append(A("mira", "mira_L", (0.02, MIRA[0], MIRA[1])))
                elif who == "M":
                    acts.append(A("mira", "mira" + ("_" + pose if pose else "") + "_L", (0.02, MIRA[0], MIRA[1])))
                    acts.append(A("asha", "asha", (0.02, ASHA[0], ASHA[1])))
                beats.append(B(say, steps, acts=acts, host="stand"))
            self.add(f"{name}{ci+1}" if len(chunks) > 1 else name, beats)

    # ------------------------------------------------------------ tables
    def tables(self, title, items, name="tables", fs=19, rh=38):
        """items: (label, header, rows, say[, hl dict, x, y]) - placed left→right, then below."""
        beats, x, y, rowh = [], 60, 112, 0
        first = True
        for it in items:
            label, header, rows, say = it[:4]
            hl = it[4] if len(it) > 4 else None
            tfs, cw, rows = fit_table(header, rows, fs)
            nl = max(len(str(c).split("\n")) for r in rows for c in r)
            trh = max(rh, nl * tfs * 1.3 + 12)
            if len(items) == 1 and len(it) <= 6:          # lone table: grow to use the space
                while tfs < 28:
                    f2 = tfs + 1; r2 = max(rh * f2 / fs, nl * f2 * 1.3 + 12)
                    if sum(colw_for(header, rows, f2)) > 1120 or (len(rows) + 1) * r2 > 530:
                        break
                    tfs, trh = f2, r2
                cw = colw_for(header, rows, tfs)
            W = sum(cw); Hh = (len(rows) + 1) * trh + (34 if label else 0)
            if len(it) > 6:
                x, y = it[5], it[6]
            elif x + W > 1220 and x > 60:
                x, y = 60, y + rowh + 22; rowh = 0
            els = []
            if label:
                els += text(x, y, label, 22, "blue")
            els += self.table_els(x, y + (34 if label else 0), header, rows, cw, rh=trh, fs=tfs, hl=hl)
            steps = ([T(title)] if first else []) + [els]
            beats.append(B(say, steps)); first = False
            x += W + 40; rowh = max(rowh, Hh)
        self.add(name, beats)

    # ------------------------------------------------------------ practice: question first, pause, then answer code
    def practice(self, n, q, sql, beats, total=None, name="practice", atitle=None):
        th = sb("Try it first!")
        lab = f"Practice {n}" + (f" of {total}" if total else "")
        self.add(f"{name}{n}_q", [
            B(f"{lab}. {q} Pause the video and write your query.", [T(lab), card(110, 140, 1000, q, "violet", fs=28, center=True, minh=110)[0]],
              acts=[A("th", th, (0.55, 1040, 520, {"pop": 1, "flip": 1}), (0.98, 1040, 520, {"o": 0, "flip": 1}))]),
            B("", [merge(box(430 + k * 160, 360, 100, 100, str(3 - k), "yellow", t="ellipse", fs=40, fill="solid")) for k in range(3)],
              sfx=[("tick", 0.0), ("tick", 0.33), ("tick", 0.66)], dur=3.2)])
        self.code(atitle or f"{lab} · answer", sql, beats, name=f"{name}{n}_a")

    def hook(self, hook, pause_q, pause_a, short):
        """Memory hook card + pause-and-predict question."""
        self.add("hook", [B(f"Memory hook: {hook}", [T("Memory hook"),
                 card(140, 200, 1000, f"“{hook}”", "yellow", fs=36, fill="solid", center=True, minh=140)[0]],
                 sfx=[("chime", 0.05)], host="happy")])
        self.quiz([(pause_q, pause_a, short)])

    def warn(self, title, items, name="mistakes"):
        """Common mistakes / teacher corrections: red-bordered cards. items: (text, say)"""
        self.bullets(title, [(t, s, "red") for t, s in items], name=name)
