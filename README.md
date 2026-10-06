# videogen — sketch-animated, narrated teaching videos

Hand-drawn (Excalidraw-style) scenes with vibrant colors, a penguin host (Pip), student/mentor characters (Asha, Mira),
offline TTS narration (Piper, en_US-amy-medium - young female voice), burned-in subtitles + .srt, sound effects, a ducked music bed,
chapter progress bar, camera zoom on code, and a two-pass encode that keeps each video under 30 MB.

## 🎨 Enhanced Features

### 🎭 Expanded Character Library
- **Animals**: penguin (Pip), sheep, dog, duck, owl, parrot, snail, ant, turtle, squirrel, cat, rabbit, elephant, giraffe, fish, butterfly
- **Vehicles**: car (4 colors), truck, bus, bicycle, airplane, rocket
- **Computer Components**: laptop (3 colors), monitor (3 colors), keyboard, mouse, CPU chip, RAM stick, hard drive, server rack, router, USB drive
- **Human Characters**: Asha (student), Mira (mentor), engineer, stick figures

### 🎨 Vibrant Color Palette
All characters now feature enhanced, vibrant colors for better visual appeal:
- Pip: Bright teal scarf, vivid orange feet and beak
- Asha: Coral tunic, bright blue backpack, warm skin tones
- Mira: Vibrant purple coat, enhanced skin tones, bright green pointer
- Animals: Enhanced with more saturated, eye-catching colors

### 🎤 Female Voice Narration
- Changed from male voice (ryan-high) to female voice (amy-medium)
- Natural-sounding young adult female (age 21-25)
- Perfect for educational content with a friendly, approachable tone

## Layout
```
videogen/
  setup.sh            one-time install (piper, voice, playwright, ffmpeg, excalidraw bundle, sprites)
  series.json         series name, output folder, video groups
  gen.py gen2.py      primitives: text, box(t=rectangle|ellipse|diamond), line, T(title), merge
  course.py           Episode builder (intro, chapter, bullets, code, compare, flow, table_els, quiz, outro, add, build)
  story.py            StoryEp(Episode): story(), tables(), practice(), hook(), warn()  + reads series.json
  sprites.py          characters & stamps (pip_*, asha[_think|_happy], mira[_point|_happy][_L], stamp_*, cube_*, 
                       animals: cat, rabbit, elephant, giraffe, fish, butterfly, sheep, dog, duck, owl, parrot, turtle, squirrel, ant, snail
                       vehicles: car_[blue|red|green|orange], truck, bus, bicycle, airplane, rocket
                       tech: laptop[_blue|_orange], monitor[_green|_purple], keyboard, mouse, cpu_chip, ram_stick, 
                             hard_drive, server_rack, router, usb_drive)
  combine.py          merges episodes into long videos per series.json groups
  episodes/epNN.py    one script per episode (you write these)
  render/engine.py    tts | steps | audio | frames | final | all | scene i,j
  render/run_video.sh N   build group N's episodes → combine → render → <30 MB mp4 + srt in OUT/final/
  render/preview2.py  SC=../OUT/epNN PV=/some/dir python3 preview2.py  → last-frame PNGs + contact sheets
  render/make_video.py  SPOKEN / ACR pronunciation tables (add acronyms here)
```

## Episode script template
```python
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from story import *          # B, A, card, text, box, line, T, merge, sb, StoryEp

E = StoryEp(3, "Episode Title")
E.intro(["agenda 1", "agenda 2", "agenda 3", "agenda 4"])      # ≤4 items (say_hello= to override greeting)
E.chapter("Part title")                                          # up to 8 per episode
E.story("Scene title", [("N", "on-screen narration", "spoken"),
                        ("A", "Asha's line", "spoken", "think"),   # poses: think | happy
                        ("M", "Mira's line", "spoken", "point")])  # poses: point | happy
E.bullets("Title", [("card text", "spoken", "blue"), ...])        # colours: teal blue orange violet green yellow red grey
E.compare("Title", [("Head", "body", "orange", "spoken"), ...])   # 2-4 columns
E.flow("Title", [("Step\nlabel", "spoken", "green"), ...], note=("yellow note", "spoken"))
E.code("Title", '''SQL or Python…''', [(lines_shown_cumulative, "spoken", "optional output card"), ...])
E.tables("Title", [("label", header, rows, "spoken", {row_index: "green"})])   # auto-fit/wrap; (…, hl, x, y) to place
E.practice(n, "Question?", '''answer code''', [(lines, "spoken", "output")], total=5, atitle=None)
E.warn("Teacher corrections", [("text", "spoken"), ...])          # red cards
E.add("custom", [B("spoken", [T("Title"), box(...), text(...)], acts=[A("id", "sprite", (t0, x, y, {"pop":1}), (t1, x2, y2, {"walk":1}))],
                   sfx=[("ding", 0.5)], host="happy", focus=[x, y, w, h])])
E.hook("memory hook", "pause question?", "spoken answer", "short answer card")
E.outro([("recap card", "spoken"), ...], "Next episode title")   # None on the final episode → END_LINE
E.build()
```
Rules of thumb: canvas 1280×720; keep content in x 50–1100, y 100–660 (Pip lives bottom-right, subtitles at the bottom).
Acts keyframe t is a fraction of the beat (0..1); actor ids persist across beats in a scene. sfx: pop whoosh ding buzz chime tick.
Speech bubbles: `A("b", sb("Short text!"), (0.2, 1000, 520, {"pop": 1}))` — new bubbles need `render/sprites_render.py` (run_video.sh does it).
Code panels auto-size; long SQL lines wrap at commas/keywords; small fonts trigger an automatic zoom.

## Make a series
1. `./setup.sh`
2. Edit `series.json`: `{"name", "out", "file_prefix", "end_line", "welcome", "groups": [["Video name", [1,2,3,4]], …]}`
3. Write `episodes/ep01.py …`, run each (`python3 episodes/ep01.py`) and preview with `render/preview2.py`; fix overlaps.
4. `nohup render/run_video.sh 1 > render/v1.log 2>&1 &` (≈ 25–35 min per 25-min video on 2 CPUs). Queue the rest sequentially.
5. Deliver `OUT/final/*.mp4` and zip the `.srt` files with the episode `script.md` files.
