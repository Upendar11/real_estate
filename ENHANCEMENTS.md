# VideoCen Enhancements - New Characters, Voice & Colors

## Overview

This enhanced version of videogen includes:
- **20+ new characters** across animals, vehicles, and computer components
- **Vibrant color palette** for all characters
- **Female voice narration** (young adult, age 21-25)
- Enhanced visual appeal with brighter, more saturated colors

---

## 🎭 Complete Character Library

### 🐧 Main Characters
- **Pip** (penguin) - Your friendly host with a teal scarf
  - Poses: `pip_stand`, `pip_point`, `pip_happy`, `pip_stand_talk`, `pip_point_talk`, `pip_happy_talk`, `pip_stand_blink`, `pip_point_blink`, `pip_happy_blink`
  
- **Asha** (student) - Coral tunic, bright blue backpack
  - Poses: `asha`, `asha_think`, `asha_happy`
  
- **Mira** (mentor) - Vibrant purple coat, green pointer
  - Poses: `mira`, `mira_point`, `mira_happy`

### 🐾 Animals

#### Original Animals
- `sheep` - Fluffy white sheep (with optional tag)
- `sheep_noid`, `sheep_mars`, `sheep_17850`, `sheep_12583` - Tagged variations
- `dog` - Friendly sheepdog
- `duck`, `duck_a`, `duck_b` - Ducks with ID tags
- `owl_old`, `owl_new` - Owls holding time signs
- `parrot` - Colorful parrot with vibrant feathers
- `turtle` - Green turtle with shell
- `squirrel` - Brown squirrel with bushy tail
- `ant`, `ant_green`, `ant_blue`, `ant_orange` - Ants carrying colored cubes
- `snail5`, `snail5r`, `snail6`, `snail_f3`, `snail_f4` - Snails carrying data columns

#### **NEW Animals** ✨
- `cat` - Red cat with whiskers (130x100)
- `rabbit` - White fluffy rabbit (100x140)
- `elephant` - Gray elephant with trunk (160x130)
- `giraffe` - Yellow giraffe with spots (110x200)
- `fish` - Blue swimming fish (100x60)
- `butterfly` - Colorful butterfly with wings (90x80)

### 🚗 Vehicles (All NEW) ✨

- `car_blue` - Blue car (140x80)
- `car_red` - Red car (140x80)
- `car_green` - Green car (140x80)
- `car_orange` - Orange car (140x80)
- `truck` - Red delivery truck (180x100)
- `bus` - Yellow school bus (200x110)
- `bicycle` - Two-wheeled bike (140x90)
- `airplane` - Blue airplane (180x100)
- `rocket` - Red rocket ship (100x140)

### 💻 Computer Components (All NEW) ✨

#### Display & Input
- `laptop` - Laptop with green screen (160x100)
- `laptop_blue` - Laptop with blue screen
- `laptop_orange` - Laptop with orange screen
- `monitor` - Desktop monitor with blue screen (140x120)
- `monitor_green` - Monitor with green screen
- `monitor_purple` - Monitor with purple screen
- `keyboard` - Computer keyboard (180x60)
- `mouse` - Computer mouse (60x80)

#### Processing & Storage
- `cpu_chip` - CPU processor chip (100x100)
- `ram_stick` - RAM memory stick (140x60)
- `hard_drive` - HDD storage drive (140x80)
- `usb_drive` - USB flash drive (60x80)

#### Network & Server
- `server_rack` - Server rack with 4 units (120x180)
- `router` - Network router with antennas (160x80)

### 📦 Other Elements
- `cube_green`, `cube_blue`, `cube_red`, `cube_orange`, `cube_grey` - Data cubes
- `stamp_*` - Various stamps (6rows, trusted, error, rejected, null, commit, rollback, wins, ignored, merged, crash, ok, same)
- `eng`, `eng_wave` - Engineer stick figure
- `board` - Whiteboard for text

---

## 🎨 Color Enhancements

### Enhanced Characters
All characters now feature more vibrant, saturated colors:

**Pip (Penguin)**
- Feet/Beak: Bright orange (`#ff8c42`, `#fd7e14`)
- Scarf: Vibrant teal/cyan (`#3bc9db`, `#1098ad`)
- Belly: Pure white (`#ffffff`)

**Asha (Student)**
- Tunic: Vibrant coral/red (`#ff6b6b`, `#e03131`)
- Backpack: Bright blue (`#a5d8ff`, `#339af0`)
- Skin: Warm peach (`#ffc078`)

**Mira (Mentor)**
- Coat: Vivid purple (`#da77f2`, `#862e9c`)
- Pointer: Bright green (`#51cf66`, `#37b24d`)
- Skin: Golden yellow (`#fab005`)

**Animals**
- Sheep: Brighter white wool
- Parrot: More saturated rainbow colors
- Owl: Enhanced brown tones
- And more!

---

## 🎤 Voice Change

### Female Narrator
Changed from `en_US-ryan-high` (male) to `en_US-amy-medium` (female)

**Characteristics:**
- Young adult female voice (sounds age 21-25)
- Clear, friendly, and approachable tone
- Perfect for educational content
- Natural-sounding speech synthesis

**Technical Details:**
- Voice model: Piper TTS `en_US-amy-medium.onnx`
- Updated in: `render/make_video.py` (line 11)
- Setup script: `setup.sh` downloads the new voice automatically

---

## 📝 Usage Examples

### Adding Animals to Your Scene

```python
# Add multiple animals
E.add("animal_parade", [
    B("Look at all these amazing animals!", [
        T("Animal Friends")
    ], acts=[
        A("cat", "cat", (0.0, 200, 300, {"pop": 1})),
        A("rabbit", "rabbit", (0.2, 400, 300, {"pop": 1})),
        A("elephant", "elephant", (0.4, 650, 300, {"pop": 1})),
        A("giraffe", "giraffe", (0.6, 900, 270, {"pop": 1}))
    ])
])
```

### Using Vehicles

```python
# Show different colored cars
E.add("car_showcase", [
    B("Cars come in many colors!", [
        T("Colorful Vehicles")
    ], acts=[
        A("car1", "car_blue", (0.0, 150, 250, {"pop": 1})),
        A("car2", "car_red", (0.25, 350, 250, {"pop": 1})),
        A("car3", "car_green", (0.5, 550, 250, {"pop": 1})),
        A("car4", "car_orange", (0.75, 750, 250, {"pop": 1}))
    ])
])

# Add larger vehicles
E.add("big_vehicles", [
    B("Here's a truck and a bus!", [
        T("Big Vehicles")
    ], acts=[
        A("truck", "truck", (0.0, 200, 300, {"pop": 1})),
        A("bus", "bus", (0.4, 500, 300, {"pop": 1}))
    ])
])

# Air transportation
E.add("flying", [
    B("Taking to the skies!", [
        T("Air Travel")
    ], acts=[
        A("plane", "airplane", (0.0, 200, 280, {"pop": 1})),
        A("rocket", "rocket", (0.4, 500, 260, {"pop": 1}))
    ], sfx=[("whoosh", 0.5)])
])
```

### Computer Components Scene

```python
# Build a computer setup
E.add("computer_parts", [
    B("Let's explore computer hardware!", [
        T("Computer Components"),
        text(300, 150, "Input Devices", 20, "blue"),
        text(750, 150, "Processing", 20, "blue")
    ], acts=[
        # Input/Output
        A("kb", "keyboard", (0.0, 150, 220, {"pop": 1})),
        A("ms", "mouse", (0.2, 360, 220, {"pop": 1})),
        A("mon", "monitor", (0.4, 200, 400, {"pop": 1})),
        # Processing & Storage
        A("cpu", "cpu_chip", (0.6, 700, 250, {"pop": 1})),
        A("ram", "ram_stick", (0.8, 850, 250, {"pop": 1}))
    ])
])

# Show storage and network
E.add("storage_network", [
    B("Storage and networking keep everything connected!", [
        T("Data & Connectivity")
    ], acts=[
        A("hdd", "hard_drive", (0.0, 200, 280, {"pop": 1})),
        A("usb", "usb_drive", (0.25, 400, 280, {"pop": 1})),
        A("router", "router", (0.5, 580, 280, {"pop": 1})),
        A("server", "server_rack", (0.75, 800, 240, {"pop": 1}))
    ])
])
```

### Mixing Characters

```python
# Create a classroom scene with multiple character types
E.add("tech_class", [
    B("Welcome to Computer Science class!", [
        T("Learning About Computers"),
        card(300, 150, 600, "Today we learn about hardware!", "yellow", fs=20)
    ], acts=[
        # Teacher (Mira) with pointer
        A("teacher", "mira_point_L", (0.0, 100, 520)),
        # Student (Asha) taking notes
        A("student", "asha", (0.0, 950, 520)),
        # Computer components on desk
        A("laptop", "laptop_blue", (0.3, 400, 400, {"pop": 1})),
        A("mouse", "mouse", (0.4, 580, 420, {"pop": 1})),
        # Cat mascot
        A("mascot", "cat", (0.5, 800, 450, {"pop": 1}))
    ])
])
```

---

## 🎬 Animation Tips

### Pop Effect
Make characters appear with a pop:
```python
A("id", "sprite_name", (0.0, x, y, {"pop": 1}))
```

### Walk In
Make characters walk into frame:
```python
A("id", "sprite_name", (0.0, -100, y, {"o": 1}), (0.5, x, y, {"walk": 1}))
```

### Flip
Flip a character:
```python
A("id", "sprite_name", (0.0, x, y, {"flip": 1}))
```

### Fade Out
Make character disappear:
```python
A("id", "sprite_name", (0.5, x, y, {"o": 0}))
```

---

## 🔧 Technical Details

### File Changes
1. **sprites.py** - Added 20+ new sprite functions
2. **render/make_video.py** - Changed VOICE variable to `en_US-amy-medium.onnx`
3. **setup.sh** - Updated to download female voice model
4. **README.md** - Documented new features

### Sprite Dimensions
All sprites return `(elements, (width, height))`:

| Category | Sprite | Size (WxH) |
|----------|--------|------------|
| Animals | cat | 130x100 |
| | rabbit | 100x140 |
| | elephant | 160x130 |
| | giraffe | 110x200 |
| | fish | 100x60 |
| | butterfly | 90x80 |
| Vehicles | car | 140x80 |
| | truck | 180x100 |
| | bus | 200x110 |
| | bicycle | 140x90 |
| | airplane | 180x100 |
| | rocket | 100x140 |
| Computer | laptop | 160x100 |
| | monitor | 140x120 |
| | keyboard | 180x60 |
| | mouse | 60x80 |
| | cpu_chip | 100x100 |
| | ram_stick | 140x60 |
| | hard_drive | 140x80 |
| | server_rack | 120x180 |
| | router | 160x80 |
| | usb_drive | 60x80 |

### Color Palette Reference

**Primary Colors:**
- Blue: `#339af0`, `#1864ab`, `#74c0fc`, `#a5d8ff`
- Red: `#ff6b6b`, `#e03131`, `#ff8787`
- Green: `#51cf66`, `#2b8a3e`, `#37b24d`, `#69db7c`
- Orange: `#ff922b`, `#fd7e14`, `#f59f00`, `#ffd43b`
- Purple: `#9775fa`, `#da77f2`, `#7950f2`, `#862e9c`
- Teal: `#20c997`, `#3bc9db`, `#1098ad`
- Yellow: `#ffd43b`, `#ffe066`, `#fab005`

---

## 🚀 Getting Started

### Setup
```bash
# Run setup to install dependencies and download female voice
./setup.sh
```

### Test the New Characters
```bash
# Run the demo episode
python3 examples/enhanced_characters_demo.py

# Preview the output
SC=../OUT/ep99 PV=/some/dir python3 render/preview2.py
```

### Create Your Own Episode
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from story import *

E = StoryEp(1, "My First Episode")

E.intro(["Learn something new", "Meet fun characters", "Have a great time!"])

E.chapter("Getting Started")

E.add("welcome", [
    B("Welcome! Let's learn together!", [
        T("Welcome!")
    ], acts=[
        A("teacher", "mira_happy_L", (0.0, 100, 520)),
        A("student", "asha_happy", (0.0, 950, 520)),
        A("pet", "cat", (0.3, 500, 450, {"pop": 1}))
    ], host="happy")
])

E.outro([("Thanks for watching!", "Thanks for watching!")], None)

E.build()
```

---

## 📚 Additional Resources

- **Original README**: `/workspace/README.md` - Core videogen documentation
- **Example Scripts**: `/workspace/examples/` - Sample episodes
- **Sprites Reference**: `/workspace/sprites.py` - All character definitions
- **Voice Documentation**: Piper TTS voices at https://github.com/rhasspy/piper

---

## 🎉 Summary

This enhanced version of videogen provides:
- ✅ 20+ new characters (animals, vehicles, computer components)
- ✅ Vibrant, eye-catching colors throughout
- ✅ Female voice narration (young adult, 21-25)
- ✅ Backwards compatible with existing episodes
- ✅ Easy to use with the same API
- ✅ Professional, polished visual style

Happy video creating! 🎬
