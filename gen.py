"""Generate hand-drawn Excalidraw scenes for the CDC explainer video."""
import json, random, os

random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "scenes")
os.makedirs(OUT, exist_ok=True)

# Excalidraw palette (stroke, background)
C = {
    "teal":   ("#0c8599", "#c3fae8"),
    "orange": ("#e8590c", "#ffd8a8"),
    "green":  ("#2f9e44", "#b2f2bb"),
    "blue":   ("#1971c2", "#a5d8ff"),
    "red":    ("#e03131", "#ffc9c9"),
    "yellow": ("#f08c00", "#ffec99"),
    "grey":   ("#868e96", "#e9ecef"),
    "violet": ("#6741d9", "#d0bfff"),
    "ink":    ("#1e1e1e", "transparent"),
    "bronze": ("#a0522d", "#f4d6b8"),
    "silver": ("#495057", "#dee2e6"),
    "gold":   ("#e67700", "#ffe066"),
}

_id = 0
def nid(p="e"):
    global _id
    _id += 1
    return f"{p}{_id}"

def base(t, x, y, w, h, color="ink", fill="hachure", sw=2, style="solid", rough=1, rounded=False, opacity=100):
    s, b = C[color]
    return {
        "id": nid(), "type": t, "x": x, "y": y, "width": w, "height": h, "angle": 0,
        "strokeColor": s, "backgroundColor": b if fill else "transparent",
        "fillStyle": fill or "hachure", "strokeWidth": sw, "strokeStyle": style,
        "roughness": rough, "opacity": opacity, "groupIds": [], "frameId": None,
        "roundness": {"type": 3} if rounded else None,
        "seed": random.randint(1, 2**31), "version": 1, "versionNonce": random.randint(1, 2**31),
        "isDeleted": False, "boundElements": None, "updated": 1, "link": None, "locked": False,
    }

def tsize(text, fs):
    lines = text.split("\n")
    return max(len(l) for l in lines) * fs * 0.56, len(lines) * fs * 1.25

def text(x, y, s, fs=20, color="ink", align="left"):
    out = []
    for k, ln in enumerate(s.split("\n")):
        w, h = len(ln) * fs * 0.56, fs * 1.25
        lx = x - w / 2 if align == "center" else x
        e = base("text", lx, y + k * fs * 1.3, w, h, color, fill=None)
        e.update({"text": ln, "originalText": ln, "fontSize": fs, "fontFamily": 1,
                  "textAlign": align, "verticalAlign": "top", "containerId": None,
                  "lineHeight": 1.25, "autoResize": True, "backgroundColor": "transparent"})
        out.append(e)
    return out

def box(x, y, w, h, label="", color="ink", fs=20, fill="hachure", t="rectangle", style="solid", sw=2, rounded=True):
    e = base(t, x, y, w, h, color, fill=fill, style=style, sw=sw, rounded=rounded and t == "rectangle")
    out = [e]
    if label:
        n = len(label.split("\n"))
        th = n * fs * 1.3
        out += text(x + w / 2, y + (h - th) / 2, label, fs, "ink", align="center")
        g = nid("g")
        for el in out:
            el["groupIds"] = [g]
    return out

def line(pts, color="ink", arrow=True, style="solid", sw=2, both=False):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs = [p[0] for p in rel]; ys = [p[1] for p in rel]
    e = base("arrow" if arrow else "line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), color, fill=None, style=style, sw=sw)
    e.update({"points": rel, "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
              "startArrowhead": "arrow" if both else None, "endArrowhead": "arrow" if arrow else None,
              "elbowed": False, "backgroundColor": "transparent"})
    if arrow:
        e["roundness"] = {"type": 2}
    return [e]

def cube(x, y, color, s=26, label=""):
    return box(x, y, s, s, label, color, fs=14, fill="solid", rounded=False)

def database(x, y, w=140, h=200, label="Source DB", color="teal"):
    out = box(x, y + 18, w, h - 18, "", color, rounded=False)
    out += box(x, y, w, 36, "", color, t="ellipse", fill="solid")
    out += box(x, y + h - 18, w, 36, "", color, t="ellipse", fill="solid")
    out += text(x + w / 2, y + h / 2, label, 22, align="center")
    return out

def table(x, y, w, rows, label="", color="orange", rh=34, highlights=None, fs=16):
    """rows: list of strings; highlights: {row_index: color}"""
    highlights = highlights or {}
    out = []
    if label:
        out += text(x + w / 2, y - 34, label, 22, color, align="center")
    for i, r in enumerate(rows):
        c = highlights.get(i, color)
        f = "solid" if i in highlights else "hachure"
        out += box(x, y + i * rh, w, rh, r, c, fs=fs, fill=f, rounded=False)
    return out

def flag(x, y, h=160, label="last watermark", color="yellow"):
    out = line([(x, y + h), (x, y)], color, arrow=False, sw=4)
    out += box(x, y, 60, 34, "", color, fill="solid", rounded=False)
    out += text(x, y + h + 8, label, 18, color, align="center")
    return out

def title(n, s):
    return text(40, 24, f"{n}. {s}", 36)

def caption(s, color="ink"):
    return box(340, 640, 600, 56, s, color, fs=26, fill="solid")

def check(x, y, color="green"):
    return line([(x, y + 10), (x + 10, y + 22), (x + 30, y - 4)], color, arrow=False, sw=4)

def cross(x, y, color="red", s=24):
    return line([(x, y), (x + s, y + s)], color, arrow=False, sw=4) + line([(x + s, y), (x, y + s)], color, arrow=False, sw=4)

def legend(x, y):
    out = []
    for i, (c, n) in enumerate([("green", "insert"), ("blue", "update"), ("red", "delete")]):
        out += cube(x + i * 120, y, c, 22)
        out += text(x + i * 120 + 30, y, n, 18)
    return out

# ---------------------------------------------------------------- scenes
S = []

def scene(fn):
    S.append(fn)
    return fn

@scene
def s01():
    e = title(1, "The problem: full reloads")
    e += database(60, 200, 160, 240)
    e += box(240, 300, 600, 44, "", "grey", fill="hachure", rounded=False)
    for i in range(5):
        for j in range(3):
            e += cube(250 + i * 30, 230 + j * 30 if j < 2 else 310, "grey", 24)
    for i in range(7):
        e += cube(420 + i * 55, 309, "grey", 24)
    e += box(880, 240, 260, 160, "Target", "orange", fs=28)
    e += box(980, 100, 70, 70, "", "ink", t="ellipse", fill=None)
    e += line([(1015, 135), (1015, 108)], arrow=False, sw=3) + line([(1015, 135), (1038, 148)], arrow=False, sw=3)
    e += text(1070, 120, "hours...", 24, "red")
    e += box(1080, 440, 40, 140, "", "red", fill="solid", rounded=False)
    e += text(1100, 590, "cost", 18, "red", align="center")
    e += text(540, 380, "every row, every run", 22, "grey", align="center")
    e += caption("Full reload = hours", "red")
    return e

@scene
def s02():
    e = title(2, "The fix: move only what changed")
    e += database(60, 200, 160, 240)
    e += box(240, 300, 600, 44, "", "grey", fill=None, rounded=False)
    for x, c in [(330, "green"), (520, "blue"), (710, "red")]:
        e += cube(x, 309, c, 26)
    e += line([(300, 270), (800, 270)], "ink")
    e += box(880, 240, 260, 160, "Target", "orange", fs=28)
    e += box(980, 100, 70, 70, "", "ink", t="ellipse", fill=None)
    e += line([(1015, 135), (1015, 108)], arrow=False, sw=3) + line([(1015, 135), (1028, 128)], arrow=False, sw=3)
    e += text(1070, 120, "minutes", 24, "green")
    e += box(1080, 540, 40, 40, "", "green", fill="solid", rounded=False)
    e += text(1100, 590, "cost", 18, "green", align="center")
    e += legend(380, 470)
    e += caption("Only what changed", "green")
    return e

@scene
def s03():
    e = title(3, "Snapshot once, then only changes")
    e += database(60, 200, 160, 240)
    e += box(880, 220, 260, 200, "Target", "orange", fs=28)
    e += box(300, 140, 460, 80, "1. Initial snapshot (full copy, once)", "teal", fs=22, fill="solid")
    e += line([(770, 180), (870, 260)])
    for i, c in enumerate(["green", "blue", "red", "green", "blue"]):
        e += cube(330 + i * 80, 330, c, 26)
    e += line([(300, 380), (860, 380)], "ink")
    e += text(530, 400, "2. Then every run: only changes", 22, align="center")
    e += box(300, 490, 560, 60, "Full load again only for backfill / recovery", "grey", fs=20, fill="hachure", style="dashed")
    e += caption("Snapshot once, then increments")
    return e

@scene
def s04():
    e = title(4, "Simple capture: timestamp & ID")
    rows = ["09:10", "09:40", "10:05", "10:20", "10:45"]
    e += table(80, 170, 260, rows, "Timestamp watermark", "teal", rh=50, highlights={2: "green", 3: "blue", 4: "green"}, fs=20)
    e += line([(50, 268), (380, 268)], "yellow", arrow=False, sw=4, style="dashed")
    e += text(390, 255, "last watermark = 10:00", 20, "yellow")
    e += text(80, 440, "WHERE updated_at > last_watermark", 18, "teal")
    ids = ["id 101", "id 102  (edited)", "id 103", "id 104", "id 105", "id 106"]
    e += table(760, 170, 280, ids, "Incremental ID", "violet", rh=44, highlights={4: "green", 5: "green"}, fs=18)
    e += line([(730, 346), (1070, 346)], "yellow", arrow=False, sw=4, style="dashed")
    e += text(1080, 334, "max id = 104", 18, "yellow")
    e += cross(1060, 220)
    e += text(1095, 220, "update missed", 16, "red")
    e += box(150, 520, 980, 56, "Cheap and simple  —  but can't see deletes", "grey", fs=22, fill="hachure")
    e += caption("Timestamp watermark  ·  Incremental ID")
    return e

@scene
def s05():
    e = title(5, "Other capture methods")
    # Log-based
    e += database(60, 150, 120, 170, "DB")
    e += box(200, 260, 230, 40, "", "teal", fill=None, rounded=False, style="dashed")
    for i, c in enumerate(["green", "blue", "red"]):
        e += cube(220 + i * 70, 267, c, 26)
    e += text(250, 220, "transaction log", 18, "teal", align="center")
    e += text(250, 360, "Log-based CDC\nall changes + deletes\nvery low load", 22, "green", align="center")
    # Triggers
    e += database(500, 150, 120, 170, "DB")
    for dx, dy in [(-10, -10), (125, -5), (130, 40)]:
        e += text(500 + dx, 150 + dy, "*", 30, "orange")
    e += line([(630, 240), (700, 240)])
    e += table(710, 200, 120, ["audit", "row", "row"], "", "orange", rh=30)
    e += text(670, 360, "Triggers\nhigh load on writes", 22, "orange", align="center")
    # Snapshot diff
    for gx in (920, 1080):
        for i in range(3):
            for j in range(3):
                c = "red" if (gx == 1080 and i == 1 and j == 2) else ("blue" if (gx == 1080 and i == 0 and j == 0) else "grey")
                e += cube(gx + i * 34, 190 + j * 34, c, 26, )
    e += text(1035, 220, "vs", 26, align="center")
    e += text(1060, 360, "Snapshot diff\ncompare row hashes\nhigh load", 22, "red", align="center")
    e += caption("Log-based CDC  ·  Triggers  ·  Snapshot diff")
    return e

@scene
def s06():
    e = title(6, "The watermark window")
    e += line([(60, 360), (1180, 360)], "ink", sw=3)
    e += box(380, 230, 420, 130, "", "yellow", fill="hachure", rounded=False, style="dashed")
    e += flag(380, 200, 160, "last watermark", "yellow")
    e += flag(800, 200, 160, "upper bound", "blue")
    for x in (130, 250):
        e += cube(x, 333, "grey", 26)
    for x, c in [(440, "green"), (560, "blue"), (690, "green")]:
        e += cube(x, 260, c, 26)
        e += line([(x + 13, 330), (x + 13, 292)], c, sw=1)
    e += cube(900, 333, "violet", 26)
    e += text(913, 400, "arrived mid-run:\npicked up next run", 18, "violet", align="center")
    e += text(590, 440, "WHERE updated_at > :last_watermark\n  AND updated_at <= :run_upper_bound", 20, "teal", align="center")
    e += caption("Read only this window")
    return e

@scene
def s07():
    e = title(7, "Every run: 4 steps")
    steps = [("1. Read last\nwatermark", "yellow"), ("2. Pull changes\ninto staging", "teal"),
             ("3. MERGE into\ntarget", "orange"), ("4. Advance\nwatermark", "green")]
    for i, (s, c) in enumerate(steps):
        x = 60 + i * 290
        e += box(x, 230, 230, 130, s, c, fs=24)
        if i < 3:
            e += line([(x + 236, 295), (x + 284, 295)], sw=3)
    e += line([(1055, 370), (1055, 470), (175, 470), (175, 370)], "grey", style="dashed")
    e += text(615, 480, "next run", 20, "grey", align="center")
    e += box(350, 540, 580, 56, "Watermark moves ONLY after the merge commits", "red", fs=20, fill="hachure")
    e += caption("Read → Stage → Merge → Advance")
    return e

@scene
def s08():
    e = title(8, "Failed run? Rerun safely")
    for row, (lbl, ok) in enumerate([("Run 1", False), ("Run 2 (retry)", True)]):
        y = 170 + row * 220
        e += text(60, y + 40, lbl, 26)
        e += box(260, y, 220, 110, "Staging", "teal", fs=24)
        e += line([(490, y + 55), (690, y + 55)], "green" if ok else "red", sw=3, style="solid" if ok else "dashed")
        e += box(700, y, 220, 110, "Target", "orange", fs=24)
        if ok:
            e += check(580, y + 15)
        else:
            e += cross(578, y + 18, s=30)
            e += text(590, y + 70, "MERGE fails", 18, "red", align="center")
        e += flag(1010, y - 10, 100, "10:00" if not ok or row == 0 else "10:00 → 11:00", "yellow")
    e += text(1010, 300, "stays put", 18, "red", align="center")
    e += caption("No lost rows, no duplicates", "green")
    return e

@scene
def s09():
    e = title(9, "Deletes & duplicates")
    e += text(330, 110, "Soft delete", 28, "red", align="center")
    rows = ["order 41   paid", "order 42   shipped", "order 43   paid"]
    e += table(160, 170, 340, rows, "", "orange", rh=50, highlights={1: "grey"}, fs=20)
    e += line([(170, 245), (490, 245)], "red", arrow=False, sw=2)
    e += cube(40, 207, "red", 30, "D")
    e += line([(76, 222), (152, 222)], "red")
    e += text(330, 340, "is_deleted = TRUE\n(row kept, history safe)", 20, "red", align="center")
    e += text(930, 110, "MERGE on primary key", 28, "blue", align="center")
    e += cube(720, 200, "blue", 34, "42")
    e += cube(720, 270, "blue", 34, "42")
    e += line([(765, 217), (850, 250)], "blue") + line([(765, 287), (850, 258)], "blue")
    e += box(860, 225, 220, 56, "order 42", "blue", fs=22, fill="solid", rounded=False)
    e += text(970, 300, "one row, never two", 20, "blue", align="center")
    e += box(220, 450, 840, 60, "Rerun the same batch → same result (idempotent)", "green", fs=22, fill="hachure")
    e += caption("Soft delete  ·  MERGE on key")
    return e

@scene
def s10():
    e = title(10, "Ordering, late rows, schema changes")
    # latest wins
    e += text(210, 120, "Latest wins", 26, "blue", align="center")
    for i, v in enumerate(["v2", "v1", "v3"]):
        e += cube(110 + i * 70, 180, "blue", 40, v)
    e += line([(210, 235), (210, 300)])
    e += cube(190, 310, "blue", 40, "v3")
    e += text(210, 370, "keep newest per key", 18, align="center")
    # overlap
    e += text(630, 120, "Overlap window", 26, "yellow", align="center")
    e += line([(450, 290), (820, 290)], sw=3)
    e += box(560, 220, 90, 70, "", "yellow", fill="hachure", rounded=False, style="dashed")
    e += flag(650, 180, 110, "", "yellow")
    e += cube(590, 240, "violet", 26)
    e += text(630, 330, "re-read last 15 min\ncatches late rows", 18, align="center")
    # schema
    e += text(1030, 120, "Schema changes", 26, "green", align="center")
    e += table(900, 180, 180, ["id | status", "1 | paid", "2 | new"], "", "orange", rh=40, fs=18)
    e += box(1090, 180, 90, 120, "+ col", "green", fs=18, fill="solid", rounded=False)
    e += text(1030, 320, "new column → added\ndropped column → ⚠ alert", 18, align="center")
    e += caption("Latest wins · Overlap · Schema alerts")
    return e

@scene
def s11():
    e = title(11, "History & backfills")
    e += text(200, 110, "SCD Type 1", 26, "orange", align="center")
    e += box(100, 170, 200, 50, "status: shipped", "orange", fs=18, fill="solid", rounded=False)
    e += text(200, 235, "overwrite → current state", 18, align="center")
    e += text(560, 110, "SCD Type 2", 26, "violet", align="center")
    for i, (s, d) in enumerate([("new", "Jan–Feb"), ("paid", "Feb–Mar"), ("shipped", "Mar–now")]):
        e += box(430, 170 + i * 52, 260, 46, f"{s}   {d}", "violet", fs=18, fill="solid" if i == 2 else "hachure", rounded=False)
    e += text(560, 335, "keep every version", 18, align="center")
    e += text(990, 110, "Backfill", 26, "teal", align="center")
    e += line([(820, 320), (1170, 320)], sw=3)
    e += box(880, 250, 160, 70, "reload range", "teal", fill="hachure", rounded=False, style="dashed")
    e += flag(880, 200, 120, "reset", "yellow")
    e += line([(1120, 190), (900, 190)], "yellow", sw=2, style="dashed")
    e += text(990, 380, "reset watermark,\nbounded full load", 18, align="center")
    e += caption("SCD 1 / SCD 2 · Backfill")
    return e

@scene
def s12():
    e = title(12, "Databricks Pattern A: watermark job + MERGE")
    e += database(40, 220, 140, 200, "External DB")
    e += line([(190, 320), (330, 320)], sw=3)
    e += text(260, 290, "JDBC", 20, align="center")
    e += box(320, 150, 860, 380, "", "grey", fill=None, style="dashed")
    e += text(750, 160, "Databricks job  (hourly)", 22, "grey", align="center")
    e += box(350, 270, 200, 100, "Staging", "teal", fs=24)
    e += line([(560, 320), (640, 320)])
    e += box(650, 270, 160, 100, "MERGE", "blue", fs=24)
    e += line([(820, 320), (900, 320)])
    e += box(910, 255, 240, 130, "Delta table\n(silver)", "orange", fs=24)
    e += table(560, 450, 260, ["orders | 10:00"], "control table", "yellow", rh=40, fs=18)
    e += line([(690, 440), (450, 380)], "yellow", style="dashed")
    e += caption("External DB → Delta, tracked by watermark")
    return e

@scene
def s13():
    e = title(13, "Databricks Pattern B: Delta Change Data Feed")
    for i, (n, c) in enumerate([("Bronze", "bronze"), ("Silver", "silver"), ("Gold", "gold")]):
        e += box(140 + i * 360, 260, 260, 120, n, c, fs=30)
        if i < 2:
            e += line([(410 + i * 360, 320), (490 + i * 360, 320)], sw=3)
    e += text(450, 210, "change feed", 18, "teal", align="center")
    for i, c in enumerate(["green", "blue", "red"]):
        e += cube(380 + i * 30, 240 - 0, c, 20)
    e += box(300, 400, 120, 50, "checkpoint", "yellow", fs=16, fill="solid", rounded=False)
    e += line([(360, 400), (330, 385)], "yellow", arrow=False)
    e += text(640, 480, "_change_type: insert / update / delete", 22, "teal", align="center")
    e += caption("No watermark table needed")
    return e

@scene
def s14():
    e = title(14, "Databricks Pattern C: AUTO CDC pipeline")
    for i in range(3):
        e += box(60 + i * 18, 230 + i * 18, 110, 130, "JSON", "grey", fs=18, fill="solid", rounded=False)
    e += text(140, 410, "CDC events\n(e.g. Debezium)", 18, align="center")
    e += line([(210, 310), (290, 310)])
    e += box(300, 250, 170, 110, "Auto Loader\n→ bronze", "bronze", fs=20)
    e += line([(480, 310), (560, 310)])
    e += box(570, 220, 320, 180, "AUTO CDC\nkeys: order_id\nsequence by updated_at\ndelete when op = 'D'", "violet", fs=20)
    e += line([(900, 310), (980, 310)])
    e += box(990, 250, 200, 110, "Silver\nSCD 1 or 2", "silver", fs=22)
    for i, c in enumerate(["blue", "green", "red"]):
        e += cube(600 + i * 34, 430, c, 24)
    e += text(830, 430, "out-of-order → sorted", 18, align="center")
    e += caption("Upserts, deletes, ordering: handled")
    return e

@scene
def s15():
    e = title(15, "Monitoring every run")
    tiles = [("Row counts\nsource = target", "green"), ("Freshness lag", "blue"), ("Run log", "grey"),
             ("No duplicate\nkeys", "green"), ("CDC log\nhealth", "teal"), ("Schema drift\nalert", "yellow")]
    for i, (s, c) in enumerate(tiles):
        x = 90 + (i % 3) * 380; y = 140 + (i // 3) * 230
        e += box(x, y, 320, 190, "", c, fill="hachure")
        e += text(x + 160, y + 20, s, 24, align="center")
    e += check(240, 280); e += check(240, 510)
    e += box(570, 240, 120, 60, "", "blue", t="ellipse", fill=None)
    e += line([(630, 270), (655, 248)], "blue", arrow=False, sw=3)
    for j in range(3):
        e += line([(900, 250 + j * 22), (1120, 250 + j * 22)], "grey", arrow=False)
    e += line([(520, 500), (750, 500)], "teal", arrow=False, sw=3)
    e += text(630, 515, "log size steady", 18, "teal", align="center")
    e += text(1010, 470, "⚠", 44, "yellow", align="center")
    e += caption("Reconcile · Lag · Run log · Drift")
    return e

@scene
def s16():
    e = title(16, "Risks & next steps")
    e += text(60, 110, "Watch out for", 26, "red")
    for i, r in enumerate(["updated_at not always set", "hard deletes are invisible", "clock skew / long transactions", "replication slot filling disk"]):
        e += text(60, 170 + i * 50, "⚠  " + r, 20, "red")
    e += text(640, 110, "Next steps", 26, "green")
    steps = ["List source tables", "Pick method per table", "Create watermark + run log",
             "Pilot one table", "Snapshot, then incremental", "Add lag alerts", "Roll out"]
    for i, s in enumerate(steps):
        y = 170 + i * 52
        e += box(640, y, 30, 30, "", "green", fill=None, rounded=False)
        e += check(642, y + 2)
        e += text(690, y, s, 20)
    e += caption("Pilot one table → roll out", "green")
    return e


def build():
    combined, frames = [], []
    for i, fn in enumerate(S, 1):
        els = fn()
        doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
               "elements": els,
               "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
               "files": {}}
        with open(os.path.join(OUT, f"clip{i:02d}.excalidraw"), "w") as f:
            json.dump(doc, f)
        # combined board: 2 columns of 1280x720 frames
        ox = (i - 1) % 4 * 1400; oy = (i - 1) // 4 * 820
        fr = base("frame", ox, oy, 1280, 720, "ink", fill=None)
        fr.update({"name": f"Clip {i}", "backgroundColor": "transparent"})
        frames.append(fr)
        for el in json.loads(json.dumps(els)):
            el["id"] = el["id"] + f"_c{i}"
            if el.get("containerId"):
                el["containerId"] += f"_c{i}"
            if el.get("boundElements"):
                for b in el["boundElements"]:
                    b["id"] += f"_c{i}"
            el["x"] += ox; el["y"] += oy
            el["frameId"] = fr["id"]
            combined.append(el)
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": combined + frames,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}
    with open(os.path.join(OUT, "all_clips_board.excalidraw"), "w") as f:
        json.dump(doc, f)
    print(len(S), "scenes written")

if __name__ == "__main__":
    build()
