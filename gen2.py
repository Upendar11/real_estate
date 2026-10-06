"""Long-form CDC explainer: scenes made of narrated beats.
Each beat = (narration, [step, step, ...]); each step is a list of Excalidraw elements
that fades in while the beat is spoken."""
import json, os
from gen import (text, box, line, cube, database, table, flag, check, cross, legend, base, nid, C)

OUT = os.path.join(os.path.dirname(__file__), "scenes2")
os.makedirs(OUT, exist_ok=True)

def T(s, size=40):          # scene title
    return text(40, 24, s, size)

def cap(s, color="ink", y=640):
    return box(290, y, 700, 58, s, color, fs=26, fill="solid")

def code(x, y, w, lines, fs=18, color="grey"):
    """Code panel: monospace lines on a light panel. Returns list of steps (panel, then each line)."""
    h = len(lines) * fs * 1.45 + 30
    panel = box(x, y, w, h, "", color, fill="solid", rounded=True)
    steps = [panel]
    for i, ln in enumerate(lines):
        col = "green" if ln.strip().startswith(("#", "--")) else "ink"
        els = text(x + 20, y + 15 + i * fs * 1.45, ln, fs, col)
        for e in els:
            e["fontFamily"] = 3
            e["width"] = len(ln) * fs * 0.6
        steps.append(els)
    return steps

def codeblock(x, y, w, lines, fs=18):
    """Same as code() but merged into a single step."""
    return [e for st in code(x, y, w, lines, fs) for e in st]

def merge(*steps):
    return [e for s in steps for e in s]

