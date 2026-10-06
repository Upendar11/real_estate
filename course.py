"""Template-driven builder for the Spark & Databricks episode series.

Scene coordinates are 1280 x 720. Pip lives bottom-right (x > 1120, y > 520), subtitles cover y > 680,
so content stays inside x 50-1100 / y 100-670 (or up to 1230 above y 520).
"""
import json, os, textwrap
from gen import text, box, line
from gen2 import T, merge

ROOT = os.path.dirname(os.path.abspath(__file__))
SERIES = "Apache Spark & Databricks"
OUT = "series"
END_LINE = "That's the end of the series. Thanks for watching, and happy Sparking!"
EPISODES = {}            # filled by each episode module: num -> title (for "next episode" cards)
BUBBLES = {}             # extra bubble sprites needed: name -> text

COLORS = ["teal", "blue", "orange", "violet", "green", "yellow", "red", "grey"]

def B(say, steps=(), acts=(), sfx=(), focus=None, host=None, dur=None, quiet=False):
    return {"say": say, "steps": [s for s in steps if s], "acts": list(acts), "sfx": list(sfx),
            "focus": focus, "host": host, "dur": dur, "quiet": quiet}

def A(aid, sprite, *kfs):
    return {"id": aid, "sprite": sprite, "kf": [dict(t=k[0], x=k[1], y=k[2], **(k[3] if len(k) > 3 else {})) for k in kfs]}

def bubble(name, txt):
    BUBBLES[name] = txt
    return name

def wrap(s, width, fs):
    n = max(8, int(width / (fs * 0.56)))
    out = []
    for para in s.split("\n"):
        out += textwrap.wrap(para, n, break_long_words=False, break_on_hyphens=False) or [""]
    return out

def card(x, y, w, s, color="teal", fs=24, fill="hachure", center=False, minh=60):
    lines = wrap(s, w - 40, fs)
    h = max(minh, len(lines) * fs * 1.3 + 26)
    els = box(x, y, w, h, "", color, fill=fill)
    for i, l in enumerate(lines):
        if center:
            els += text(x + w / 2, y + 13 + i * fs * 1.3, l, fs, align="center")
        else:
            els += text(x + 20, y + 13 + i * fs * 1.3, l, fs)
    return els, h

def code_lines(x, y, lines, fs, color_comment="green"):
    out = []
    for i, ln in enumerate(lines):
        if not ln.strip():
            out.append([])
            continue
        col = color_comment if ln.strip().startswith(("#", "--", "//")) else "ink"
        els = text(x, y + i * fs * 1.45, ln, fs, col)
        for e in els:
            e["fontFamily"] = 3; e["width"] = len(ln) * fs * 0.6
        out.append(els)
    return out


def split_code(ln, limit=82):
    """Break a long code line after a comma that sits inside brackets (valid Python/SQL continuation)."""
    out = []
    indent = len(ln) - len(ln.lstrip())
    cur = ln
    while len(cur) > limit:
        depth, best, dot, quote = 0, -1, -1, None
        for i, ch in enumerate(cur):
            if quote:
                if ch == quote: quote = None
                continue
            if ch in "\"'": quote = ch
            elif ch in "([{": depth += 1
            elif ch in ")]}": depth -= 1
            elif ch == "," and depth > 0 and i < limit: best = i
            elif ch == "." and depth == 0 and 20 < i < limit and cur[i + 1:i + 2].isalpha(): dot = i
        if dot > 0 and (best < 0 or dot > best):
            out.append(cur[:dot] + "\\")
            cur = " " * (indent + 4) + cur[dot:]
        elif best > 0:
            out.append(cur[: best + 1])
            cur = " " * (indent + 6) + cur[best + 1:].lstrip()
        else:
            break
    out.append(cur)
    return out


def split_sql(ln, limit=82):
    """Break a long SQL line after a comma (outside quotes), or before a keyword."""
    import re as _re
    out = []; indent = len(ln) - len(ln.lstrip()); cur = ln
    while len(cur) > limit:
        quote, best = None, -1
        for i, ch in enumerate(cur[:limit]):
            if quote:
                if ch == quote: quote = None
                continue
            if ch == "'": quote = ch
            elif ch == "," and i > indent + 8: best = i
        if best < 0:
            dep, d_ = [], 0
            for ch in cur:
                d_ += (ch == "(") - (ch == ")"); dep.append(d_)
            m = [x.start() for x in _re.finditer(r" (AND|OR|ON|FROM|WHERE|GROUP|ORDER|JOIN|HAVING) ", cur[:limit]) if x.start() > indent + 8 and dep[x.start()] == 0]
            if not m: break
            out.append(cur[:m[-1]]); cur = " " * (indent + 4) + cur[m[-1] + 1:]
        else:
            out.append(cur[:best + 1]); cur = " " * (indent + 4) + cur[best + 1:].lstrip()
    out.append(cur)
    return out


class Episode:
    def __init__(self, num, title, chapters_note=""):
        self.num, self.title = num, title
        self.S = []
        EPISODES[num] = title
        self._chap = 0

    # -------------------------------------------------------------- scaffolding
    def add(self, name, beats, chapter=None):
        self.S.append({"name": f"{len(self.S):02d}_{name}", "beats": beats, "chapter": chapter})

    def intro(self, agenda, say_hello=None):
        hi = bubble("b_hi", "Hi, I'm Pip!") if self.num == 1 else bubble("b_welcome", "Welcome back!")
        beats = [B(say_hello or (f"Hi! I'm Pip. Welcome to episode {self.num} of our {SERIES} series: {self.title}."
                                 if self.num == 1 else f"Welcome back! This is episode {self.num}: {self.title}."), [
            text(640, 100, f"{SERIES} · Episode {self.num}", 30, "grey", align="center"),
            box(140, 150, 1000, 150, "", "blue", fill="hachure"),
            text(640, 190, self.title, 46 if len(self.title) < 34 else (38 if len(self.title) < 42 else 32), align="center"),
        ], acts=[A("hi", hi, (0.2, 1000, 520, {"pop": 1, "flip": 1}), (0.95, 1000, 520, {"o": 0, "flip": 1}))], host="happy")]
        items = []
        for i, a in enumerate(agenda):
            items.append(card(170, 340 + i * 62, 900, f"{i+1}.  {a}", COLORS[i % len(COLORS)], fs=24, minh=52)[0])
        beats.append(B("In this episode: " + "; ".join(agenda) + ".", items, host="point"))
        self.add("intro", beats)

    def chapter(self, title, say=None):
        self._chap += 1
        n = self._chap
        words = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
        self.add(f"chapter{n}", [B(say or f"Part {words[n-1]}. {title}.", [
            text(830, 250, f"Part {n}", 40, "grey", align="center"),
            *card(560, 310, 540, title, "blue", fs=32, center=True, minh=110)[:1],
        ], sfx=[("chime", 0.05)], host="happy")], chapter=f"Part {n}")

    # -------------------------------------------------------------- templates
    def bullets(self, title, items, intro=None, fs=24, name="bullets", host=None):
        """items: (text, say[, color])"""
        W = 1030
        heights = [len(wrap(it[0], W - 40, fs)) * fs * 1.3 + 26 for it in items]
        cols = 1
        if sum(max(60, h) for h in heights) + 14 * len(items) > 560:
            cols, fs = 2, min(fs, 21)
        beats = []
        steps_title = [T(title)]
        if intro:
            beats.append(B(intro, steps_title, host=host)); steps_title = []
        y = [110, 110]; colw = W if cols == 1 else 505
        for i, it in enumerate(items):
            c = it[2] if len(it) > 2 else COLORS[i % len(COLORS)]
            col = 0 if cols == 1 else (0 if y[0] <= y[1] else 1)
            x = 60 + col * (colw + 20)
            els, h = card(x, y[col], colw, it[0], c, fs=fs)
            y[col] += h + 14
            beats.append(B(it[1], steps_title + [els], host=host if i == 0 else None)); steps_title = []
        self.add(name, beats)

    def code(self, title, src, beats, name="code", lang=None):
        """beats: (lines_revealed_cumulative, say[, output_text])"""
        raw = src.strip("\n").split("\n"); lines = []; remap = []
        import re as _re
        is_sql = bool(_re.search(r"\b(SELECT|CREATE|INSERT|UPDATE|DELETE|ALTER)\b", src)) and "spark." not in src and "import " not in src
        for ln_ in raw:
            st_ = ln_.lstrip()
            if st_.startswith(("#", "--")) and len(ln_) > 72:
                pre = ln_[: len(ln_) - len(st_)]; mark = "#" if st_.startswith("#") else "--"
                parts = textwrap.wrap(st_.lstrip("#-").strip(), 66)
                lines += [pre + mark + " " + p for p in parts]
            elif len(ln_) > 86:
                lines += split_sql(ln_) if is_sql else split_code(ln_)
            else:
                lines.append(ln_)
            remap.append(len(lines))
        beats = [(remap[min(b[0], len(remap)) - 1] if b[0] > 0 else 0,) + tuple(b[1:]) for b in beats]
        L, M = len(lines), max(len(l) for l in lines)
        maxw = 1180 if L * 22 * 1.45 + 132 < 480 else 1060
        fs = min(26, (maxw - 60) / (M * 0.6), 515 / (L * 1.45))
        w = min(maxw, max(420, M * fs * 0.6 + 44)); h = L * fs * 1.45 + 28
        px, py = 50, 104
        panel = box(px, py, w, h, "", "grey", fill="solid")
        cl = code_lines(px + 22, py + 14, lines, fs)
        out_y = py + h + 18; out_x = px
        right = (px + w + 30 < 760)
        tot = sum(card(0, 0, 900, bt[2], fs=22, minh=46)[1] + 12 for bt in beats if len(bt) > 2 and bt[2])
        if not right and out_y + tot > 662:
            fs_r = min(26, (820 - 44) / (M * 0.6), 515 / (L * 1.45))
            fs_s = min(fs, (662 - 18 - tot - py - 28) / (L * 1.45))
            if px + w + 30 < 820:
                right = True
            elif fs_r > fs_s + 0.5:
                fs = fs_r
                w = min(maxw, max(420, M * fs * 0.6 + 44)); h = L * fs * 1.45 + 28
                panel = box(px, py, w, h, "", "grey", fill="solid")
                cl = code_lines(px + 22, py + 14, lines, fs)
                right = True
            else:
                h_allowed = 662 - 18 - tot - py
                fs = min(fs, (h_allowed - 28) / (L * 1.45))
                w = min(maxw, max(420, M * fs * 0.6 + 44)); h = L * fs * 1.45 + 28
                panel = box(px, py, w, h, "", "grey", fill="solid")
                cl = code_lines(px + 22, py + 14, lines, fs)
                out_y = py + h + 18
                right = False
        if right:
            out_x, out_y = px + w + 30, py
        res = []; shown = 0; first = True
        zoom = fs < 15.5
        for bi, bt in enumerate(beats):
            k, say = bt[0], bt[1]
            steps = ([T(title), panel] if first else [])
            steps += [e for e in cl[shown:k] if e]
            focus = None
            if zoom:
                a = py + 14 + shown * fs * 1.45; b = py + 14 + k * fs * 1.45
                fw = min(1180, max(640, w + 60)); fh = fw * 9 / 16
                cy = min(max((a + b) / 2, fh / 2 + 60), 720 - fh / 2)
                focus = [20, cy - fh / 2, fw, fh]
            if len(bt) > 2 and bt[2]:
                ow = (1240 - out_x if out_x > 760 else 1100 - out_x) if right else min(1050, max(300, len(max(bt[2].split("\n"), key=len)) * 22 * 0.62 + 60))
                els, oh = card(out_x, out_y, ow, bt[2], "green", fs=22, fill="solid", minh=46)
                if not right and out_y + oh > 662:
                    if px + w + 30 < 820:
                        right = True; out_x, out_y = px + w + 30, py
                        ow = 1100 - out_x
                    else:
                        out_y = py + h - oh - 12; out_x = px + w - ow - 12
                    els, oh = card(out_x, out_y, ow, bt[2], "green", fs=22, fill="solid", minh=46)
                steps.append(els); out_y += oh + 12
            shown = max(shown, k)
            res.append(B(say, steps, focus=focus, quiet=not first))
            first = False
        self.add(name, res)

    def compare(self, title, cards, intro=None, fs=21, name="compare"):
        """cards: (heading, body, color, say)"""
        n = len(cards); gap = 22; W = 1040
        cw = (W - gap * (n - 1)) / n
        beats = []; steps_title = [T(title)]
        if intro:
            beats.append(B(intro, steps_title)); steps_title = []
        hmax = max(len(wrap(c[1], cw - 36, fs)) * fs * 1.3 + len(wrap(c[0], cw - 30, 28 if n <= 3 else 22)) * (28 if n <= 3 else 22) * 1.2 + 70 for c in cards)
        for i, (hd, body, color, say) in enumerate(cards):
            x = 55 + i * (cw + gap); y = 120
            els = box(x, y, cw, hmax, "", color, fill="hachure")
            hfs = 28 if n <= 3 else 22
            hl = wrap(hd, cw - 30, hfs)
            for j, l in enumerate(hl):
                els += text(x + cw / 2, y + 16 + j * hfs * 1.2, l, hfs, color, align="center")
            for j, l in enumerate(wrap(body, cw - 36, fs)):
                els += text(x + 18, y + 26 + len(hl) * hfs * 1.2 + j * fs * 1.3, l, fs)
            beats.append(B(say, steps_title + [els])); steps_title = []
        self.add(name, beats)

    def flow(self, title, steps, intro=None, note=None, name="flow", fs=22):
        """steps: (label, say[, color]) - boxes with arrows, 4 per row."""
        beats = []; steps_title = [T(title)]
        if intro:
            beats.append(B(intro, steps_title)); steps_title = []
        per = 4 if len(steps) > 4 else len(steps)
        bw = min(240, (1040 - (per - 1) * 50) / per)
        ml = max(len(wrap(st[0], bw - 24, fs)) for st in steps)
        bh = max(110, ml * fs * 1.3 + 30); rs = bh + 65
        for i, st in enumerate(steps):
            r, c = divmod(i, per)
            x = 60 + c * (bw + 50); y = 140 + r * rs
            col = st[2] if len(st) > 2 else COLORS[i % len(COLORS)]
            els = box(x, y, bw, bh, "\n".join(wrap(st[0], bw - 24, fs)), col, fs=fs)
            if c > 0:
                els = line([(x - 44, y + bh / 2), (x - 6, y + bh / 2)], sw=3) + els
            elif r > 0:
                px = 60 + (per - 1) * (bw + 50) + bw / 2
                els = line([(px, y - 65), (px, y - 35), (60 + bw / 2, y - 35), (60 + bw / 2, y - 4)], "grey", style="dashed") + els
            beats.append(B(st[1], steps_title + [els])); steps_title = []
        if note:
            rows = (len(steps) - 1) // per + 1
            beats.append(B(note[1], [card(160, 140 + rows * rs, 860, note[0], "yellow", fs=24, fill="solid", center=True)[0]]))
        self.add(name, beats)

    def table_els(self, x, y, header, rows, colw, rh=44, fs=20, color="teal", hl=None):
        hl = hl or {}
        els = []
        for j, hcell in enumerate(header):
            els += box(x + sum(colw[:j]), y, colw[j], rh, str(hcell), color, fs=fs, fill="solid", rounded=False)
        for i, r in enumerate(rows):
            c = hl.get(i, color); f = "solid" if i in hl else "hachure"
            for j, cell in enumerate(r):
                els += box(x + sum(colw[:j]), y + (i + 1) * rh, colw[j], rh, str(cell), c if i in hl else color, fs=fs, fill=f, rounded=False)
        return els

    def quiz(self, qas):
        for i, (q, a, short) in enumerate(qas):
            th = bubble("b_think", "Hmm…")
            self.add(f"quiz{i+1}", [
                B(f"Quick quiz! Question {['one','two','three','four'][i]}. {q} Pause and think.", [
                    T(f"Quiz · Question {i+1} of {len(qas)}"), card(110, 130, 1000, q, "violet", fs=28, center=True, minh=110)[0]],
                  acts=[A("th", th, (0.6, 1060, 520, {"pop": 1, "flip": 1}), (0.98, 1060, 520, {"o": 0, "flip": 1}))]),
                B("", [merge(box(430 + k * 160, 330, 100, 100, str(3 - k), "yellow", t="ellipse", fs=40, fill="solid")) for k in range(3)],
                  sfx=[("tick", 0.0), ("tick", 0.33), ("tick", 0.66)], dur=3.2),
                B(a, [card(170, 480, 940, short, "green", fs=30, fill="solid", center=True, minh=80)[0]], sfx=[("ding", 0.02)], host="happy"),
            ])

    def outro(self, points, next_title=None):
        beats = [B("Let's recap.", [T("Recap")])]
        y = 110
        for i, (p, say) in enumerate(points):
            els, h = card(140, y, 960, p, COLORS[i % len(COLORS)], fs=24, center=True, minh=56)
            y += h + 12
            beats.append(B(say, [els]))
        nxt = next_title
        if nxt:
            beats.append(B(f"Next time: {nxt}. See you there!", [
                text(620, y + 20, f"Next: {nxt}", 30, "blue", align="center")], host="happy", sfx=[("chime", 0.6)]))
        else:
            beats.append(B(END_LINE, [
                text(620, y + 20, "Thanks for watching!", 34, "blue", align="center")], host="happy", sfx=[("chime", 0.5)]))
        self.add("outro", beats)

    # -------------------------------------------------------------- output
    def build(self):
        out = os.path.join(ROOT, f"{OUT}/ep{self.num:02d}")
        os.makedirs(out, exist_ok=True)
        for sc in self.S:
            els = [e for b in sc["beats"] for s in b["steps"] for e in s]
            json.dump({"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": els,
                       "appState": {"viewBackgroundColor": "#ffffff"}, "files": {}}, open(os.path.join(out, sc["name"] + ".excalidraw"), "w"))
        json.dump(self.S, open(os.path.join(out, "plan.json"), "w"))
        bfile = os.path.join(ROOT, "series/bubbles.json")
        allb = json.load(open(bfile)) if os.path.exists(bfile) else {}
        allb.update(BUBBLES); json.dump(allb, open(bfile, "w"), indent=1)
        words = sum(len(b["say"].split()) for s in self.S for b in s["beats"])
        print(f"ep{self.num:02d}: {len(self.S)} scenes, {sum(len(s['beats']) for s in self.S)} beats, {words} words (~{words/140:.1f} min)")
        with open(os.path.join(out, "script.md"), "w") as f:
            f.write(f"# Episode {self.num}: {self.title}\n\n")
            for s in self.S:
                say = " ".join(b["say"] for b in s["beats"] if b["say"])
                f.write(f"## {s['name'][3:].replace('_', ' ').title()}\n\n{say}\n\n")
