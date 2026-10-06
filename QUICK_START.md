# 🚀 Quick Start Guide - Enhanced VideoCen

## Get Started in 5 Minutes!

### Step 1: Setup (First time only)
```bash
# Run setup to install dependencies and download the female voice
./setup.sh
```

This will:
- ✅ Install Piper TTS with female voice (en_US-amy-medium)
- ✅ Install required Python packages
- ✅ Install ffmpeg for video encoding
- ✅ Set up Excalidraw rendering engine

### Step 2: Create Your First Episode

Create a file `episodes/ep01.py`:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from story import *

# Create episode
E = StoryEp(1, "My First Enhanced Video")

# Intro with agenda
E.intro([
    "Learn about new characters",
    "See vibrant colors",
    "Hear our female narrator"
])

# Add a chapter
E.chapter("Meeting New Friends")

# Add a scene with new characters
E.add("hello_animals", [
    B("Let me introduce you to our animal friends!", [
        T("Animal Friends"),
        text(300, 150, "Cat", 24, "blue"),
        text(640, 150, "Rabbit", 24, "blue")
    ], acts=[
        A("cat", "cat", (0.0, 280, 250, {"pop": 1})),
        A("rabbit", "rabbit", (0.4, 600, 230, {"pop": 1}))
    ], host="happy")
])

# Add vehicles
E.add("colorful_cars", [
    B("Cars come in many beautiful colors!", [
        T("Colorful Vehicles")
    ], acts=[
        A("car1", "car_blue", (0.0, 200, 300, {"pop": 1})),
        A("car2", "car_red", (0.3, 450, 300, {"pop": 1})),
        A("car3", "car_green", (0.6, 700, 300, {"pop": 1}))
    ], host="point")
])

# Add computer components
E.add("tech_components", [
    B("Let's explore computer hardware!", [
        T("Computer Parts")
    ], acts=[
        A("laptop", "laptop_blue", (0.0, 250, 300, {"pop": 1})),
        A("cpu", "cpu_chip", (0.4, 500, 300, {"pop": 1})),
        A("ram", "ram_stick", (0.7, 750, 320, {"pop": 1}))
    ])
])

# Outro
E.outro([
    ("We explored 20+ new characters!", "We explored 20 plus new characters!"),
    ("Everything is more colorful now!", "Everything is more colorful now!")
], None)

E.build()
```

### Step 3: Generate Your Video

```bash
# Generate the episode
python3 episodes/ep01.py

# Render the video
cd render
./run_video.sh 1
```

### Step 4: Preview Your Video

The video will be saved in `OUT/final/`:
- `OUT/final/ep01.mp4` - Your finished video
- `OUT/final/ep01.srt` - Subtitles file

---

## 🎨 Character Reference Cheat Sheet

### Top 10 Most Useful New Characters

#### Animals
```python
A("cat", "cat", (0.0, x, y, {"pop": 1}))           # Cute cat
A("rabbit", "rabbit", (0.0, x, y, {"pop": 1}))     # Fluffy bunny
A("elephant", "elephant", (0.0, x, y, {"pop": 1})) # Big elephant
```

#### Vehicles
```python
A("car", "car_blue", (0.0, x, y, {"pop": 1}))      # Blue car
A("truck", "truck", (0.0, x, y, {"pop": 1}))       # Red truck
A("rocket", "rocket", (0.0, x, y, {"pop": 1}))     # Space rocket
```

#### Computer Components
```python
A("laptop", "laptop", (0.0, x, y, {"pop": 1}))     # Green screen laptop
A("cpu", "cpu_chip", (0.0, x, y, {"pop": 1}))      # CPU chip
A("monitor", "monitor", (0.0, x, y, {"pop": 1}))   # Blue screen monitor
A("keyboard", "keyboard", (0.0, x, y, {"pop": 1})) # Keyboard
```

---

## 🎬 Common Animation Patterns

### Pattern 1: Pop In Sequence
```python
acts=[
    A("char1", "cat", (0.0, 200, 300, {"pop": 1})),
    A("char2", "dog", (0.3, 500, 300, {"pop": 1})),
    A("char3", "rabbit", (0.6, 800, 300, {"pop": 1}))
]
```

### Pattern 2: Walk In From Side
```python
acts=[
    A("char", "asha", (0.0, -120, 520, {"o": 1}), 
                      (0.5, 165, 520, {"walk": 1}))
]
```

### Pattern 3: Appear and Disappear
```python
acts=[
    A("temp", "butterfly", (0.0, 400, 300, {"pop": 1})),
    A("temp", "butterfly", (0.8, 400, 300, {"o": 0}))
]
```

---

## 🎨 Color Options Quick Reference

### Cars
- `car_blue`, `car_red`, `car_green`, `car_orange`

### Laptops
- `laptop` (green screen)
- `laptop_blue` (blue screen)
- `laptop_orange` (orange screen)

### Monitors
- `monitor` (blue screen)
- `monitor_green` (green screen)
- `monitor_purple` (purple screen)

### Card Colors (for text boxes)
```python
"blue"    # Professional, calm
"red"     # Error, warning
"green"   # Success, nature
"orange"  # Attention, energy
"violet"  # Creative, unique
"yellow"  # Important, highlight
"teal"    # Fresh, modern
"grey"    # Neutral, subtle
```

---

## 🎤 Female Voice Features

The new female narrator:
- **Sounds like**: Young adult (21-25 years)
- **Tone**: Friendly, clear, approachable
- **Perfect for**: Education, tutorials, storytelling
- **Model**: Piper TTS `en_US-amy-medium`

No code changes needed - just create content and the female voice is automatically used!

---

## 📁 Project Structure

```
videogen/
├── episodes/          # Your episode scripts (ep01.py, ep02.py, etc.)
├── series.json        # Series configuration
├── sprites.py         # All character definitions (NOW WITH 20+ NEW!)
├── story.py          # Story helper functions
├── course.py         # Episode builder
├── gen.py, gen2.py   # Low-level generators
├── setup.sh          # One-time setup script
├── render/
│   ├── make_video.py # Video renderer (female voice configured here)
│   ├── run_video.sh  # Video generation script
│   └── engine.py     # Rendering engine
└── OUT/
    └── final/        # Generated videos (.mp4 + .srt)
```

---

## 💡 Tips for Great Videos

### Visual Tips
1. **Use Vibrant Colors**: Mix character colors with card colors
2. **Show Progressions**: car → truck → bus → airplane → rocket
3. **Group by Theme**: All tech components together, all animals together
4. **Size Variety**: Mix small (fish), medium (cat), and large (elephant) characters

### Content Tips
1. **Clear Narration**: Female voice is clear - write natural sentences
2. **Pacing**: Use timing (0.0, 0.3, 0.6) to space out animations
3. **Engagement**: Pop effects (`{"pop": 1}`) grab attention
4. **Reinforcement**: Combine visual and spoken information

### Technical Tips
1. **Canvas Size**: 1280×720, keep content in x:50-1100, y:100-660
2. **Character Placement**: Characters at y≈300 for medium height
3. **Host Position**: Pip automatically appears bottom-right
4. **Title**: Use `T("Title")` at the start of each scene

---

## 🐛 Common Issues & Solutions

### Issue: Voice not found
**Solution**: Run `./setup.sh` to download the female voice

### Issue: Character overlaps text
**Solution**: Adjust y-coordinates - characters higher (y=250), text lower (y=400)

### Issue: Animation too fast/slow
**Solution**: Adjust timing values in acts: (0.0, ...), (0.5, ...), (1.0, ...)

### Issue: Video file too large
**Solution**: The encoder automatically keeps videos under 30MB

---

## 📚 Learning Resources

### In This Repository
1. **ENHANCEMENTS.md** - Complete feature documentation
2. **CHARACTER_SHOWCASE.md** - Visual guide for all characters
3. **examples/enhanced_characters_demo.py** - Full working demo
4. **README.md** - Core videogen documentation

### Example Episodes
- `examples/sql_ep01_story_example.py` - Story-based episode
- `examples/spark_ep22_code_example.py` - Code-based episode
- `examples/enhanced_characters_demo.py` - NEW character showcase

---

## 🎯 Next Steps

1. ✅ **Run Setup**: `./setup.sh`
2. ✅ **Try Demo**: `python3 examples/enhanced_characters_demo.py`
3. ✅ **Create Episode**: Copy template above to `episodes/ep01.py`
4. ✅ **Generate Video**: `python3 episodes/ep01.py && cd render && ./run_video.sh 1`
5. ✅ **Watch Result**: Open `OUT/final/ep01.mp4`
6. ✅ **Iterate**: Modify your episode and regenerate!

---

## 🎉 Have Fun!

You now have:
- ✨ 20+ new vibrant characters
- 🎤 Beautiful female voice narration
- 🎨 Eye-catching colors throughout
- 📚 Complete documentation
- 💡 Working examples

**Start creating beautiful educational videos today!** 🎬

---

## 🆘 Need Help?

- **Documentation**: Check `ENHANCEMENTS.md` for detailed guides
- **Examples**: Look in `examples/` folder for working code
- **Character Reference**: See `CHARACTER_SHOWCASE.md` for visual guide
- **API Reference**: Check `README.md` for core API documentation

**Happy video creation!** 🚀✨
