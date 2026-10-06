"""Original hand-drawn characters as Excalidraw elements. Each sprite fits in a (w, h) box with origin top-left."""
import random
from gen import base, nid

random.seed(11)
INK = "#1e1e1e"

def el(t, x, y, w, h, stroke=INK, fill="transparent", fs="solid", sw=2, angle=0.0, rough=1, rounded=False):
    e = base(t, x, y, w, h, "ink", fill="solid")
    e.update({"strokeColor": stroke, "backgroundColor": fill, "fillStyle": fs, "strokeWidth": sw,
              "angle": angle, "roughness": rough, "roundness": {"type": 3} if rounded else None})
    return e

def ell(x, y, w, h, fill="transparent", stroke=INK, **k):
    return el("ellipse", x, y, w, h, stroke, fill, **k)

def rect(x, y, w, h, fill="transparent", stroke=INK, **k):
    return el("rectangle", x, y, w, h, stroke, fill, **k)

def poly(pts, fill="transparent", stroke=INK, closed=True, sw=2):
    if closed and pts[0] != pts[-1]:
        pts = pts + [pts[0]]
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs = [p[0] for p in rel]; ys = [p[1] for p in rel]
    e = el("line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke, fill, sw=sw)
    e.update({"points": rel, "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
              "startArrowhead": None, "endArrowhead": None, "elbowed": False})
    return e

def ln(pts, stroke=INK, sw=2):
    return poly(pts, closed=False, stroke=stroke, sw=sw)

def txt(x, y, s, fs=16, color=INK, center=True):
    w = len(s) * fs * 0.56
    e = el("text", x - (w / 2 if center else 0), y, w, fs * 1.25, color)
    e.update({"text": s, "originalText": s, "fontSize": fs, "fontFamily": 1, "textAlign": "center" if center else "left",
              "verticalAlign": "top", "containerId": None, "lineHeight": 1.25, "autoResize": True,
              "backgroundColor": "transparent"})
    return e

# ------------------------------------------------------------------ Pip the penguin (box 130 x 165) - Enhanced with vibrant colors
def penguin(pose="stand", talk=False, blink=False):
    E = []
    E += [ell(33, 148, 26, 12, "#ff8c42", "#fd7e14"), ell(71, 148, 26, 12, "#ff8c42", "#fd7e14")]
    # flippers
    if pose == "point":
        E.append(ell(-2, 52, 20, 52, "#343a40", "#212529", angle=0.95))
    else:
        E.append(ell(14, 78, 20, 52, "#343a40", "#212529", angle=0.3))
    if pose == "happy":
        E.append(ell(96, 52, 20, 52, "#343a40", "#212529", angle=-0.95))
    else:
        E.append(ell(96, 78, 20, 52, "#343a40", "#212529", angle=-0.3))
    E.append(ell(25, 30, 80, 125, "#343a40", "#212529"))
    E.append(ell(40, 62, 50, 88, "#ffffff", "#dee2e6"))
    # eyes
    if pose == "happy":
        E += [ln([(45, 54), (51, 47), (57, 54)], sw=3), ln([(67, 54), (73, 47), (79, 54)], sw=3)]
    elif blink:
        E += [ln([(45, 52), (57, 52)], sw=3), ln([(67, 52), (79, 52)], sw=3)]
    else:
        E += [ell(44, 43, 15, 18, "#ffffff", INK, sw=1), ell(66, 43, 15, 18, "#ffffff", INK, sw=1),
              ell(49, 49, 7, 8, INK, INK), ell(70, 49, 7, 8, INK, INK)]
    # beak
    if talk:
        E += [poly([(53, 64), (77, 64), (65, 71)], "#ffb84d", "#f59f00"), poly([(56, 75), (74, 75), (65, 83)], "#ffb84d", "#f59f00")]
    else:
        E.append(poly([(53, 65), (77, 65), (65, 77)], "#ffb84d", "#f59f00"))
    # scarf - vibrant teal/cyan
    E += [rect(36, 88, 58, 13, "#3bc9db", "#1098ad", rounded=True), rect(72, 94, 13, 28, "#3bc9db", "#1098ad", rounded=True)]
    return E, (130, 165)

# ------------------------------------------------------------------ sheep (box 120 x 105) - Enhanced with vibrant colors
def sheep(tag=None):
    E = [ln([(35, 75), (33, 98)], sw=3), ln([(52, 78), (52, 100)], sw=3), ln([(72, 78), (72, 100)], sw=3), ln([(88, 75), (90, 98)], sw=3)]
    for (x, y, d) in [(20, 40, 36), (40, 30, 40), (62, 32, 38), (78, 44, 34), (30, 52, 40), (55, 52, 42), (20, 55, 30)]:
        E.append(ell(x, y, d, d, "#ffffff", "#adb5bd"))
    E += [ell(88, 30, 28, 34, "#868e96", "#495057"), ell(96, 40, 5, 6, "#ffffff", "#ffffff")]
    if tag:
        E += [rect(2, 2, 116, 26, "#ff8787", "#ff6b6b", rounded=True), txt(60, 5, tag, 15, "#e03131")]
    return E, (120, 105)

# ------------------------------------------------------------------ sheepdog (box 150 x 110)
def dog():
    br, dk = "#d9a066", "#8c5a2b"
    E = [ln([(40, 70), (36, 104)], dk, 4), ln([(58, 72), (58, 106)], dk, 4), ln([(98, 72), (100, 106)], dk, 4), ln([(114, 70), (118, 104)], dk, 4)]
    E.append(ln([(22, 52), (6, 30), (2, 22)], dk, 5))
    E.append(ell(20, 40, 110, 46, br, dk))
    E.append(ell(98, 50, 30, 30, "#ffffff", "#adb5bd"))
    E.append(ell(104, 10, 46, 44, br, dk))
    E += [ell(100, 6, 18, 30, dk, dk, angle=0.4), ell(130, 26, 22, 14, "#f1f3f5", dk), ell(144, 28, 8, 7, INK, INK),
          ell(122, 20, 7, 8, INK, INK), ln([(134, 40), (140, 44)], INK, 2)]
    return E, (152, 110)

# ------------------------------------------------------------------ duck (box 110 x 110)
def duck(label=None):
    E = [ell(10, 40, 80, 50, "#ffe066", "#e67700"), ell(28, 52, 40, 24, "#ffd43b", "#e67700", angle=-0.2),
         ell(58, 10, 40, 40, "#ffe066", "#e67700"), poly([(94, 26), (110, 30), (94, 36)], "#ff922b", "#e8590c"),
         ell(80, 22, 6, 7, INK, INK), ln([(40, 90), (38, 98)], "#e8590c", 3), ln([(60, 90), (62, 98)], "#e8590c", 3)]
    if label:
        E.append(txt(55, 96, label, 15, "#1971c2"))
    return E, (115, 118)

# ------------------------------------------------------------------ owl with sign (box 120 x 175) - Enhanced with vibrant colors
def owl(sign, color="#fd7e14"):
    br, dk = "#e8ac6f", "#d9822b"
    E = [poly([(28, 22), (36, 2), (46, 20)], br, dk), poly([(74, 20), (84, 2), (92, 22)], br, dk),
         ell(15, 10, 90, 110, br, dk), ell(28, 22, 64, 50, "#fff4e6", dk),
         ell(32, 28, 26, 28, "#ffffff", INK), ell(62, 28, 26, 28, "#ffffff", INK),
         ell(40, 37, 11, 12, INK, INK), ell(70, 37, 11, 12, INK, INK),
         poly([(54, 56), (66, 56), (60, 66)], "#ffb84d", "#fd7e14"),
         ell(22, 70, 22, 40, "#d9822b", dk, angle=0.3), ell(76, 70, 22, 40, "#d9822b", dk, angle=-0.3)]
    E += [rect(14, 104, 92, 50, "#ffffff", color, rounded=True), txt(60, 114, sign, 24, color)]
    E += [ln([(46, 154), (44, 166)], "#fd7e14", 3), ln([(74, 154), (76, 166)], "#fd7e14", 3)]
    return E, (120, 175)

# ------------------------------------------------------------------ parrot (box 110 x 160) - Enhanced with vibrant colors
def parrot():
    E = [ln([(48, 112), (40, 156)], "#339af0", 6), ln([(56, 112), (56, 158)], "#ff6b6b", 6), ln([(64, 112), (72, 156)], "#ffd43b", 6),
         ell(26, 40, 62, 82, "#69db7c", "#37b24d"), ell(30, 60, 30, 50, "#51cf66", "#37b24d", angle=0.25),
         ell(40, 6, 52, 50, "#ff8787", "#ff6b6b"), ell(64, 18, 14, 14, "#ffffff", INK), ell(68, 22, 6, 6, INK, INK),
         poly([(86, 24), (104, 30), (98, 46), (88, 38)], "#ffe066", "#ffd43b"),
         ln([(46, 120), (44, 128)], "#868e96", 3), ln([(62, 120), (64, 128)], "#868e96", 3)]
    return E, (110, 160)

# ------------------------------------------------------------------ snail carrying column blocks (box 300 x 260)
def snail(cols):
    E = [ell(10, 200, 280, 50, "#d8f5a2", "#5c940d"), ell(220, 150, 60, 70, "#d8f5a2", "#5c940d"),
         ln([(238, 156), (230, 118)], "#5c940d", 3), ln([(262, 156), (270, 118)], "#5c940d", 3),
         ell(224, 108, 13, 13, INK, INK), ell(264, 108, 13, 13, INK, INK), ln([(240, 196), (252, 202), (264, 196)], INK, 2)]
    bh = 26
    for i, (c, color) in enumerate(cols):
        y = 200 - (i + 1) * bh
        fill = {"grey": "#e9ecef", "green": "#b2f2bb", "orange": "#ffd8a8"}[color]
        stroke = {"grey": "#868e96", "green": "#2f9e44", "orange": "#e8590c"}[color]
        E += [rect(40, y, 160, bh, fill, stroke), txt(120, y + 4, c, 15)]
    return E, (300, 260)

# ------------------------------------------------------------------ stick-figure engineer with laptop (box 140 x 190)
def engineer(wave=False):
    E = [ell(48, 4, 44, 44, "#fff3bf", INK), ell(60, 20, 5, 6, INK, INK), ell(76, 20, 5, 6, INK, INK),
         ln([(62, 34), (70, 38), (78, 34)], INK, 2), ln([(70, 48), (70, 118)], INK, 3),
         ln([(70, 118), (52, 182)], INK, 3), ln([(70, 118), (88, 182)], INK, 3),
         ln([(70, 70), (100, 96)], INK, 3)]
    E.append(ln([(70, 70), (28, 34)], INK, 3) if wave else ln([(70, 70), (36, 98)], INK, 3))
    E += [rect(76, 86, 56, 36, "#a5d8ff", "#1971c2"), rect(70, 120, 70, 6, "#dee2e6", "#495057")]
    return E, (145, 190)

def cube(color):
    f, s = {"green": ("#b2f2bb", "#2f9e44"), "blue": ("#a5d8ff", "#1971c2"), "red": ("#ffc9c9", "#e03131"),
            "orange": ("#ffd8a8", "#e8590c"), "grey": ("#e9ecef", "#868e96")}[color]
    return [rect(2, 2, 30, 30, f, s)], (34, 34)

def bubble(s, fs=22):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * fs * 0.6 + 36; h = len(lines) * fs * 1.3 + 26
    E = [rect(2, 2, w, h, "#ffffff", INK, rounded=True), poly([(w * 0.25, h + 1), (w * 0.2, h + 22), (w * 0.4, h + 1)], "#ffffff", INK)]
    for i, l in enumerate(lines):
        E.append(txt(2 + w / 2, 14 + i * fs * 1.3, l, fs))
    return E, (w + 6, h + 26)

def stamp(s, color="#e03131"):
    w = len(s) * 30 * 0.62 + 40
    return [rect(4, 4, w, 52, "#ffffff", color, sw=4, angle=-0.15), txt(4 + w / 2, 14, s, 30, color)], (w + 10, 64)

def mirror(els, W):
    import copy
    out = []
    for e in els:
        e = copy.deepcopy(e)
        if e["type"] in ("line", "arrow"):
            pts = [[e["x"] + px, e["y"] + py] for px, py in e["points"]]
            pts = [[W - px, py] for px, py in pts]
            x0, y0 = pts[0]
            e["points"] = [[px - x0, py - y0] for px, py in pts]; e["x"], e["y"] = x0, y0
        else:
            e["x"] = W - e["x"] - e["width"]; e["angle"] = -e.get("angle", 0)
        e["id"] = e["id"] + "m"
        out.append(e)
    return out

def ant(load=None):
    E = [ln([(30, 70), (18, 92)], INK, 3), ln([(50, 72), (50, 94)], INK, 3), ln([(70, 70), (84, 92)], INK, 3),
         ell(8, 50, 38, 32, "#5c3d2e", "#2b1d14"), ell(40, 52, 30, 26, "#5c3d2e", "#2b1d14"), ell(66, 40, 34, 34, "#5c3d2e", "#2b1d14"),
         ell(84, 48, 8, 9, "#ffffff", INK), ln([(84, 42), (92, 22)], INK, 2), ln([(92, 44), (104, 26)], INK, 2)]
    if load:
        f, s_ = {"green": ("#b2f2bb", "#2f9e44"), "blue": ("#a5d8ff", "#1971c2"), "orange": ("#ffd8a8", "#e8590c")}[load]
        E.append(rect(30, 8, 40, 40, f, s_))
    return E, (110, 100)

def turtle():
    E = [ell(10, 70, 26, 22, "#8ce99a", "#2b8a3e"), ell(96, 70, 26, 22, "#8ce99a", "#2b8a3e"),
         ell(100, 40, 44, 36, "#8ce99a", "#2b8a3e"), ell(126, 50, 8, 9, INK, INK),
         ell(14, 20, 110, 66, "#a9e34b", "#5c940d"), ln([(40, 30), (54, 80)], "#5c940d", 2), ln([(84, 28), (74, 82)], "#5c940d", 2),
         ln([(18, 52), (120, 52)], "#5c940d", 2)]
    return E, (150, 95)

def squirrel():
    br, dk = "#d9822b", "#8c4a12"
    E = [ell(0, 10, 60, 100, br, dk, angle=-0.3), ell(50, 50, 56, 66, br, dk), ell(70, 18, 44, 40, br, dk),
         poly([(78, 22), (84, 4), (92, 22)], br, dk), ell(98, 30, 8, 9, INK, INK), ell(62, 70, 26, 30, "#fff4e6", dk),
         ell(84, 82, 20, 18, "#a0522d", "#5c3317")]
    return E, (120, 120)

# ------------------------------------------------------------------ cat (box 130 x 100)
def cat():
    E = [ln([(40, 90), (38, 112)], INK, 3), ln([(58, 92), (58, 114)], INK, 3), ln([(74, 92), (76, 114)], INK, 3), ln([(92, 90), (94, 112)], INK, 3)]
    E += [ell(20, 30, 90, 48, "#ff6b6b", "#c92a2a"), ell(84, 12, 24, 32, "#ff6b6b", "#c92a2a"), ell(106, 12, 24, 32, "#ff6b6b", "#c92a2a")]
    E += [ell(42, 38, 12, 14, "#ffffff", INK), ell(72, 38, 12, 14, "#ffffff", INK)]
    E += [ell(46, 42, 5, 6, INK, INK), ell(76, 42, 5, 6, INK, INK)]
    E += [poly([(54, 52), (60, 58), (66, 52)], "#ff6b6b", "#c92a2a")]
    E += [ln([(40, 58), (20, 54)], INK, 2), ln([(46, 62), (26, 64)], INK, 2), ln([(74, 58), (94, 54)], INK, 2), ln([(80, 62), (100, 64)], INK, 2)]
    return E, (130, 120)

# ------------------------------------------------------------------ rabbit (box 100 x 140)
def rabbit():
    E = [ell(20, 96, 16, 12, "#868e96", INK, sw=2), ell(64, 96, 16, 12, "#868e96", INK, sw=2)]
    E += [ell(12, 20, 18, 70, "#f8f9fa", "#868e96"), ell(62, 20, 18, 70, "#f8f9fa", "#868e96")]
    E += [ell(20, 54, 60, 52, "#f8f9fa", "#868e96"), ell(32, 68, 36, 30, "#ffffff", "#adb5bd")]
    E += [ell(38, 74, 8, 9, INK, INK), ell(58, 74, 8, 9, INK, INK)]
    E += [poly([(48, 86), (50, 92), (52, 86)], "#ff8787", "#e03131")]
    E += [ell(78, 68, 12, 16, "#f8f9fa", "#868e96")]
    return E, (100, 110)

# ------------------------------------------------------------------ elephant (box 160 x 130)
def elephant():
    E = [ln([(36, 110), (30, 150)], "#868e96", 5), ln([(64, 114), (64, 154)], "#868e96", 5), ln([(96, 114), (96, 154)], "#868e96", 5), ln([(124, 110), (130, 150)], "#868e96", 5)]
    E += [ell(20, 50, 120, 74, "#adb5bd", "#868e96"), ell(110, 32, 46, 56, "#adb5bd", "#868e96")]
    E += [ell(130, 46, 10, 11, INK, INK)]
    E += [poly([(124, 72), (142, 78), (150, 96), (146, 110), (138, 108), (134, 96), (136, 80)], "#adb5bd", "#868e96")]
    E += [ell(92, 2, 18, 30, "#adb5bd", "#868e96", angle=0.4), ell(126, 2, 18, 30, "#adb5bd", "#868e96", angle=-0.4)]
    return E, (160, 160)

# ------------------------------------------------------------------ giraffe (box 110 x 200)
def giraffe():
    E = [ln([(32, 130), (32, 194)], "#f59f00", 5), ln([(78, 130), (78, 194)], "#f59f00", 5)]
    E += [ell(24, 190, 18, 10, INK, INK), ell(70, 190, 18, 10, INK, INK)]
    E += [ell(20, 90, 70, 50, "#ffd43b", "#f59f00"), ln([(55, 50), (55, 96)], "#f59f00", 6)]
    E += [ell(40, 32, 32, 36, "#ffd43b", "#f59f00"), ell(54, 16, 12, 20, "#ffd43b", "#f59f00", angle=-0.3)]
    E += [ell(44, 38, 7, 8, INK, INK), ell(60, 38, 7, 8, INK, INK)]
    E += [ln([(58, 54), (64, 58)], INK, 2)]
    for (x, y) in [(28, 100), (52, 98), (76, 102), (42, 114), (64, 116)]:
        E.append(ell(x, y, 10, 10, "#e67700", "#e67700"))
    return E, (110, 205)

# ------------------------------------------------------------------ fish (box 100 x 60)
def fish():
    E = [ell(16, 16, 62, 40, "#339af0", "#1864ab"), poly([(16, 36), (2, 26), (2, 46)], "#339af0", "#1864ab")]
    E += [poly([(48, 6), (70, 18), (48, 18)], "#339af0", "#1864ab"), poly([(48, 38), (70, 38), (48, 50)], "#339af0", "#1864ab")]
    E += [ell(54, 26, 8, 9, "#ffffff", INK), ell(58, 28, 4, 5, INK, INK)]
    E += [ln([(74, 36), (96, 28), (96, 44), (74, 36)], "#74c0fc", "#1864ab")]
    return E, (100, 60)

# ------------------------------------------------------------------ butterfly (box 90 x 80)
def butterfly():
    E = [ln([(45, 10), (45, 70)], INK, 3)]
    E += [ell(8, 20, 32, 26, "#ff6b6b", "#c92a2a"), ell(6, 42, 28, 24, "#ff8787", "#e03131")]
    E += [ell(50, 20, 32, 26, "#ffd43b", "#f59f00"), ell(54, 42, 28, 24, "#ffe066", "#f59f00")]
    E += [ell(42, 6, 5, 5, INK, INK), ln([(40, 4), (34, 0)], INK, 2), ln([(50, 4), (56, 0)], INK, 2)]
    for (x, y) in [(18, 28), (16, 48), (60, 28), (62, 48)]:
        E.append(ell(x, y, 6, 6, "#ffffff", "#ffffff"))
    return E, (90, 80)

# ================================================================== VEHICLES

# ------------------------------------------------------------------ car (box 140 x 80)
def car(color="blue"):
    colors = {"blue": ("#339af0", "#1864ab"), "red": ("#ff6b6b", "#c92a2a"), "green": ("#51cf66", "#2b8a3e"), "orange": ("#ff922b", "#e8590c")}
    fill, stroke = colors.get(color, colors["blue"])
    E = [ell(22, 64, 26, 26, "#343a40", "#212529"), ell(92, 64, 26, 26, "#343a40", "#212529")]
    E += [rect(4, 32, 132, 38, fill, stroke, rounded=True), rect(24, 10, 48, 28, "#74c0fc", "#1864ab", rounded=True)]
    E += [rect(76, 10, 48, 28, "#74c0fc", "#1864ab", rounded=True)]
    E += [ell(28, 70, 14, 14, "#868e96", "#343a40"), ell(98, 70, 14, 14, "#868e96", "#343a40")]
    E += [rect(6, 44, 20, 8, "#ffd43b", "#f59f00"), rect(114, 44, 20, 8, "#ffd43b", "#f59f00")]
    return E, (140, 90)

# ------------------------------------------------------------------ truck (box 180 x 100)
def truck():
    E = [ell(28, 84, 28, 28, "#343a40", "#212529"), ell(142, 84, 28, 28, "#343a40", "#212529")]
    E += [rect(4, 42, 80, 48, "#e03131", "#c92a2a", rounded=True), rect(88, 28, 88, 62, "#ff6b6b", "#e03131", rounded=True)]
    E += [rect(22, 16, 48, 32, "#74c0fc", "#1864ab", rounded=True)]
    E += [ell(34, 90, 16, 16, "#868e96", "#343a40"), ell(148, 90, 16, 16, "#868e96", "#343a40")]
    E += [rect(96, 48, 72, 32, "#f8f9fa", "#adb5bd")]
    return E, (180, 112)

# ------------------------------------------------------------------ bus (box 200 x 110)
def bus():
    E = [ell(36, 94, 24, 24, "#343a40", "#212529"), ell(164, 94, 24, 24, "#343a40", "#212529")]
    E += [rect(4, 18, 192, 82, "#ffd43b", "#f59f00", rounded=True)]
    E += [ell(42, 100, 14, 14, "#868e96", "#343a40"), ell(170, 100, 14, 14, "#868e96", "#343a40")]
    for x in [16, 56, 96, 136, 176]:
        E += [rect(x, 28, 32, 28, "#74c0fc", "#1864ab", rounded=True)]
    E += [rect(8, 72, 24, 14, "#e03131", "#c92a2a", rounded=True)]
    return E, (200, 118)

# ------------------------------------------------------------------ bicycle (box 140 x 90)
def bicycle():
    E = [ell(14, 64, 32, 32, "transparent", INK, sw=3), ell(94, 64, 32, 32, "transparent", INK, sw=3)]
    E += [ln([(46, 80), (70, 38)], INK, 3), ln([(30, 80), (70, 38)], INK, 3), ln([(70, 38), (110, 80)], INK, 3)]
    E += [ln([(56, 38), (84, 38)], INK, 3), ln([(70, 38), (70, 60)], INK, 3)]
    E += [ell(18, 68, 24, 24, "#343a40", "#212529"), ell(98, 68, 24, 24, "#343a40", "#212529")]
    E += [rect(54, 32, 32, 12, "#ff6b6b", "#e03131", rounded=True)]
    return E, (140, 96)

# ------------------------------------------------------------------ airplane (box 180 x 100)
def airplane():
    E = [ell(40, 44, 100, 32, "#74c0fc", "#1864ab"), poly([(20, 60), (2, 70), (2, 50)], "#74c0fc", "#1864ab")]
    E += [poly([(24, 44), (4, 24), (46, 48)], "#a5d8ff", "#1864ab"), poly([(24, 62), (4, 82), (46, 58)], "#a5d8ff", "#1864ab")]
    E += [poly([(118, 44), (166, 32), (176, 54), (134, 60)], "#a5d8ff", "#1864ab")]
    E += [rect(48, 16, 36, 20, "#74c0fc", "#1864ab", rounded=True)]
    E += [rect(56, 22, 8, 8, "#1864ab", "#1864ab"), rect(68, 22, 8, 8, "#1864ab", "#1864ab")]
    return E, (180, 100)

# ------------------------------------------------------------------ rocket (box 100 x 140)
def rocket():
    E = [poly([(30, 100), (44, 6), (56, 6), (70, 100)], "#ff6b6b", "#e03131")]
    E += [poly([(30, 100), (20, 130), (36, 106)], "#e03131", "#c92a2a"), poly([(70, 100), (80, 130), (64, 106)], "#e03131", "#c92a2a")]
    E += [ell(42, 44, 16, 16, "#74c0fc", "#1864ab")]
    E += [rect(44, 18, 12, 20, "#ffd43b", "#f59f00", rounded=True)]
    for y in [110, 120]:
        E += [ell(36, y, 8, 8, "#ffd43b", "#f59f00"), ell(56, y, 8, 8, "#ffe066", "#f59f00")]
    return E, (100, 140)

# ================================================================== COMPUTER COMPONENTS

# ------------------------------------------------------------------ laptop (box 160 x 100)
def laptop(screen_color="#51cf66"):
    E = [rect(4, 62, 152, 10, "#495057", "#343a40"), rect(10, 8, 140, 60, "#343a40", "#212529")]
    E += [rect(18, 14, 124, 46, screen_color, "#2b8a3e")]
    E += [rect(76, 66, 8, 4, "#868e96", "#495057")]
    return E, (160, 76)

# ------------------------------------------------------------------ desktop monitor (box 140 x 120)
def monitor(screen_color="#339af0"):
    E = [rect(44, 96, 52, 8, "#495057", "#343a40"), rect(62, 102, 16, 12, "#495057", "#343a40")]
    E += [rect(4, 4, 132, 96, "#343a40", "#212529"), rect(12, 10, 116, 78, screen_color, "#1864ab")]
    E += [ell(70, 92, 6, 6, "#51cf66", "#2b8a3e")]
    return E, (140, 114)

# ------------------------------------------------------------------ keyboard (box 180 x 60)
def keyboard():
    E = [rect(2, 2, 176, 56, "#495057", "#343a40", rounded=True)]
    for row in range(3):
        for col in range(8):
            x, y = 10 + col * 20, 10 + row * 16
            E += [rect(x, y, 16, 12, "#f8f9fa", "#868e96", rounded=True)]
    return E, (180, 60)

# ------------------------------------------------------------------ mouse (box 60 x 80)
def mouse():
    E = [ell(8, 12, 44, 62, "#495057", "#343a40"), ln([(30, 14), (30, 40)], "#343a40", 2)]
    E += [rect(18, 18, 10, 18, "#868e96", "#495057", rounded=True)]
    return E, (60, 80)

# ------------------------------------------------------------------ cpu chip (box 100 x 100)
def cpu_chip():
    E = [rect(20, 20, 60, 60, "#343a40", "#212529")]
    E += [rect(28, 28, 44, 44, "#868e96", "#495057")]
    E += [txt(50, 42, "CPU", 16, "#ffd43b")]
    for i in range(6):
        y = 26 + i * 8
        E += [rect(12, y, 6, 4, "#ffd43b", "#f59f00"), rect(82, y, 6, 4, "#ffd43b", "#f59f00")]
        x = 26 + i * 8
        E += [rect(x, 12, 4, 6, "#ffd43b", "#f59f00"), rect(x, 82, 4, 6, "#ffd43b", "#f59f00")]
    return E, (100, 100)

# ------------------------------------------------------------------ ram stick (box 140 x 60)
def ram_stick():
    E = [rect(4, 16, 132, 40, "#2f9e44", "#2b8a3e")]
    for x in [20, 48, 76, 104]:
        E += [rect(x, 24, 16, 24, "#343a40", "#212529")]
    E += [txt(70, 6, "RAM", 12, "#343a40")]
    for x in [40, 96]:
        E += [rect(x, 4, 8, 16, "#ffd43b", "#f59f00")]
    return E, (140, 60)

# ------------------------------------------------------------------ hard drive (box 140 x 80)
def hard_drive():
    E = [rect(4, 4, 132, 72, "#495057", "#343a40", rounded=True)]
    E += [rect(12, 12, 116, 56, "#343a40", "#212529")]
    E += [txt(70, 28, "HDD", 20, "#74c0fc")]
    E += [ell(112, 64, 10, 10, "#51cf66", "#2b8a3e"), ell(124, 64, 10, 10, "#ffd43b", "#f59f00")]
    return E, (140, 80)

# ------------------------------------------------------------------ server rack (box 120 x 180)
def server_rack():
    E = [rect(4, 4, 112, 172, "#343a40", "#212529")]
    for i in range(4):
        y = 14 + i * 40
        E += [rect(10, y, 100, 32, "#495057", "#343a40", rounded=True)]
        E += [rect(16, y + 8, 80, 16, "#1864ab", "#1864ab")]
        for j in range(3):
            E += [ell(94 + j * 6, y + 12, 4, 4, "#51cf66", "#2b8a3e")]
    return E, (120, 180)

# ------------------------------------------------------------------ router (box 160 x 80)
def router():
    E = [rect(4, 32, 152, 44, "#343a40", "#212529", rounded=True)]
    for i in range(5):
        E += [ell(20 + i * 26, 64, 6, 6, "#51cf66", "#2b8a3e")]
    E += [ln([(32, 32), (32, 12)], "#868e96", 3), ln([(72, 32), (72, 8)], "#868e96", 3), ln([(112, 32), (112, 12)], "#868e96", 3)]
    for x in [28, 68, 108]:
        E += [ell(x, 4, 8, 8, "#343a40", "#212529")]
    return E, (160, 80)

# ------------------------------------------------------------------ usb drive (box 60 x 80)
def usb_drive():
    E = [rect(16, 44, 28, 32, "#1864ab", "#1864ab", rounded=True)]
    E += [rect(20, 24, 20, 24, "#74c0fc", "#1864ab", rounded=True)]
    E += [txt(30, 32, "USB", 10, "#ffffff")]
    E += [rect(24, 12, 12, 14, "#868e96", "#495057")]
    return E, (60, 80)


# ------------------------------------------------------------------ Asha the student (box 130 x 205) - Enhanced with vibrant colors
def asha(pose="stand"):
    skin, hair, top, dk = "#ffc078", "#3b2414", "#ff6b6b", "#e03131"
    E = [rect(18, 70, 34, 56, "#a5d8ff", "#339af0", rounded=True)]                      # backpack - brighter blue
    E += [ln([(58, 150), (48, 200)], INK, 4), ln([(74, 150), (84, 200)], INK, 4)]          # legs
    E += [ell(38, 196, 18, 8, INK, INK), ell(78, 196, 18, 8, INK, INK)]
    E.append(poly([(40, 76), (92, 76), (100, 154), (32, 154)], top, dk))                   # tunic - vibrant coral
    if pose == "happy":
        E += [ln([(44, 84), (14, 40)], INK, 4), ln([(88, 84), (118, 40)], INK, 4)]
    elif pose == "think":
        E += [ln([(44, 84), (26, 128)], INK, 4), ln([(88, 84), (104, 104), (82, 62)], INK, 4)]
        E.append(txt(118, 0, "?", 34, "#7950f2"))
    else:
        E += [ln([(44, 84), (26, 128)], INK, 4), ln([(88, 84), (106, 128)], INK, 4)]
    E += [ell(40, 4, 26, 52, hair, hair, angle=0.5)]                                       # ponytail
    E += [ell(42, 14, 50, 56, skin, "#f59f00"), poly([(42, 34), (50, 12), (80, 8), (94, 30), (70, 22)], hair, hair)]
    E += [ell(56, 38, 6, 7, INK, INK), ell(76, 38, 6, 7, INK, INK)]
    E.append(ln([(60, 54), (67, 58), (74, 54)], INK, 2) if pose != "think" else ln([(61, 56), (73, 56)], INK, 2))
    return E, (130, 205)

# ------------------------------------------------------------------ Mira the mentor (box 140 x 215) - Enhanced with vibrant colors
def mira(pose="stand"):
    skin, hair, coat, dk = "#fab005", "#212529", "#da77f2", "#862e9c"
    E = [ln([(62, 150), (56, 208)], INK, 4), ln([(80, 150), (86, 208)], INK, 4),
         ell(44, 203, 18, 8, INK, INK), ell(80, 203, 18, 8, INK, INK)]
    E.append(poly([(44, 78), (98, 78), (104, 156), (38, 156)], coat, dk))
    E.append(poly([(64, 78), (78, 78), (71, 100)], "#ffffff", dk))
    if pose == "point":
        E += [ln([(46, 86), (30, 132)], INK, 4), ln([(96, 86), (128, 44)], INK, 4), rect(124, 30, 8, 22, "#51cf66", "#37b24d")]
    elif pose == "happy":
        E += [ln([(46, 86), (16, 44)], INK, 4), ln([(96, 86), (126, 44)], INK, 4)]
    else:
        E += [ln([(46, 86), (30, 132)], INK, 4), ln([(96, 86), (112, 132)], INK, 4), rect(108, 126, 8, 22, "#51cf66", "#37b24d")]
    E += [ell(56, 0, 30, 24, hair, hair)]                                                   # bun
    E += [ell(46, 16, 50, 58, skin, "#f59f00"), poly([(46, 40), (52, 18), (90, 18), (96, 40), (72, 28)], hair, hair)]
    E += [ell(52, 38, 16, 14, "transparent", INK, sw=2), ell(74, 38, 16, 14, "transparent", INK, sw=2), ln([(68, 44), (74, 44)], INK, 2),
          ell(57, 42, 5, 6, INK, INK), ell(79, 42, 5, 6, INK, INK)]
    E.append(ln([(64, 60), (71, 64), (78, 60)], INK, 2))
    return E, (140, 215)

def board(lines, w=300):
    h = len(lines) * 30 + 30
    E = [rect(2, 2, w, h, "#ffffff", "#495057", sw=3)]
    for i, l in enumerate(lines):
        E.append(txt(2 + w / 2, 16 + i * 30, l, 20, "#1971c2"))
    return E, (w + 6, h + 6)

def sprite_defs():
    D = _defs()
    import json as _j, os as _o
    bf = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "series/bubbles.json")
    if _o.path.exists(bf):
        for k, v in _j.load(open(bf)).items():
            D[k] = bubble(v)
    fc = [("DEST_COUNTRY_NAME", "grey"), ("ORIGIN_COUNTRY_NAME", "grey"), ("count", "grey")]
    D["snail_f3"] = snail(fc); D["snail_f4"] = snail(fc + [("count2", "green")])
    D["ant"] = ant(); D["ant_green"] = ant("green"); D["ant_blue"] = ant("blue"); D["ant_orange"] = ant("orange")
    D["turtle"] = turtle(); D["squirrel"] = squirrel()
    
    # New animals
    D["cat"] = cat(); D["rabbit"] = rabbit(); D["elephant"] = elephant()
    D["giraffe"] = giraffe(); D["fish"] = fish(); D["butterfly"] = butterfly()
    
    # Vehicles
    D["car_blue"] = car("blue"); D["car_red"] = car("red"); D["car_green"] = car("green"); D["car_orange"] = car("orange")
    D["truck"] = truck(); D["bus"] = bus(); D["bicycle"] = bicycle()
    D["airplane"] = airplane(); D["rocket"] = rocket()
    
    # Computer components
    D["laptop"] = laptop("#51cf66"); D["laptop_blue"] = laptop("#339af0"); D["laptop_orange"] = laptop("#ff922b")
    D["monitor"] = monitor("#339af0"); D["monitor_green"] = monitor("#51cf66"); D["monitor_purple"] = monitor("#9775fa")
    D["keyboard"] = keyboard(); D["mouse"] = mouse()
    D["cpu_chip"] = cpu_chip(); D["ram_stick"] = ram_stick(); D["hard_drive"] = hard_drive()
    D["server_rack"] = server_rack(); D["router"] = router(); D["usb_drive"] = usb_drive()
    
    for p in ("stand", "think", "happy"):
        D["asha" + ("" if p == "stand" else "_" + p)] = asha(p)
    for p in ("stand", "point", "happy"):
        D["mira" + ("" if p == "stand" else "_" + p)] = mira(p)
    D["stamp_6rows"] = stamp("6 ROWS?!", "#e03131"); D["stamp_trusted"] = stamp("TRUSTED", "#2f9e44")
    D["stamp_error"] = stamp("ERROR", "#e03131"); D["stamp_rejected"] = stamp("REJECTED", "#e03131")
    D["stamp_null"] = stamp("NULL", "#868e96"); D["stamp_commit"] = stamp("COMMIT", "#2f9e44"); D["stamp_rollback"] = stamp("ROLLBACK", "#e8590c")
    for k in list(D):
        if not k.startswith("pip_"):
            els, (w, h) = D[k]
            D[k + "_L"] = (mirror(els, w), (w, h))
    return D

def _defs():
    D = {}
    for pose in ("stand", "point", "happy"):
        for talk in (False, True):
            D[f"pip_{pose}{'_talk' if talk else ''}"] = penguin(pose, talk)
        D[f"pip_{pose}_blink"] = penguin(pose, False, True)
    D["sheep"] = sheep(); D["sheep_noid"] = sheep("no ID"); D["sheep_mars"] = sheep("MARS")
    D["dog"] = dog(); D["sheep_17850"] = sheep("17850"); D["sheep_12583"] = sheep("12583")
    D["duck_a"] = duck("E00000001"); D["duck_b"] = duck("E00000001"); D["duck"] = duck("E00000001 ✓")
    D["owl_old"] = owl("09:00", "#868e96"); D["owl_new"] = owl("11:00", "#2f9e44")
    D["parrot"] = parrot()
    base_cols = [("event_id", "grey"), ("user_id", "grey"), ("event_name", "grey"), ("event_time", "grey"), ("region", "grey")]
    D["snail5"] = snail(base_cols)
    renamed = [("event_id", "grey"), ("user_id", "grey"), ("event_type", "orange"), ("event_time", "grey"), ("region", "grey")]
    D["snail5r"] = snail(renamed)
    D["snail6"] = snail(renamed + [("device_type", "green")])
    D["eng"] = engineer(False); D["eng_wave"] = engineer(True)
    for c in ("green", "blue", "red", "orange", "grey"):
        D[f"cube_{c}"] = cube(c)
    for k, s in {"b_again": "Run it again!", "b_same": "Same result!", "b_hi": "Hi, I'm Pip!", "b_one": "One row\nper ID!",
                 "b_valid": "valid →", "b_think": "Hmm…", "b_newer": "Newer wins!", "b_hello": "Let's build it!"}.items():
        D[k] = bubble(s)
    D["stamp_wins"] = stamp("WINS", "#2f9e44"); D["stamp_ignored"] = stamp("IGNORED", "#e03131")
    D["stamp_merged"] = stamp("MERGED", "#1971c2"); D["stamp_crash"] = stamp("CRASH!", "#e03131"); D["stamp_ok"] = stamp("OK!", "#2f9e44"); D["stamp_same"] = stamp("SAME PLAN", "#2f9e44")
    return D
