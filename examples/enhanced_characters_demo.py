"""
Enhanced Characters Demo - Showcasing new animals, vehicles, and computer components
This example demonstrates how to use the newly added vibrant characters in your videos.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from story import *

E = StoryEp(99, "Character Showcase - Animals, Vehicles & Tech")

# Intro with enhanced colorful Asha and Mira
E.intro([
    "Meet our new animal friends!", 
    "Explore vehicles in action",
    "Discover computer components",
    "See vibrant colors everywhere!"
], say_hello="Welcome to our enhanced character showcase!")

# Chapter 1: New Animals
E.chapter("Amazing Animals")

E.story("Animal Friends", [
    ("N", "Let's meet our new animal friends!", "Let's meet our new animal friends!"),
    ("A", "Look at all these cute animals!", "Look at all these cute animals!", "happy"),
    ("M", "Each one has its own personality!", "Each one has its own personality!", "point")
])

# Show animals with description
E.add("animals_showcase", [
    B("Here's a playful cat, a hopping rabbit, and a majestic elephant!", [
        T("New Animals"),
        text(200, 150, "Cat", 24, "blue"),
        text(450, 150, "Rabbit", 24, "blue"),
        text(750, 150, "Elephant", 24, "blue")
    ], acts=[
        A("cat", "cat", (0.0, 180, 220, {"pop": 1})),
        A("rabbit", "rabbit", (0.3, 420, 220, {"pop": 1})),
        A("elephant", "elephant", (0.6, 700, 220, {"pop": 1}))
    ], host="happy")
])

E.add("more_animals", [
    B("We also have a tall giraffe, a swimming fish, and a colorful butterfly!", [
        T("More Animals"),
        text(200, 150, "Giraffe", 24, "blue"),
        text(500, 150, "Fish", 24, "blue"),
        text(800, 150, "Butterfly", 24, "blue")
    ], acts=[
        A("giraffe", "giraffe", (0.0, 150, 200, {"pop": 1})),
        A("fish", "fish", (0.3, 460, 280, {"pop": 1})),
        A("butterfly", "butterfly", (0.6, 770, 270, {"pop": 1}))
    ], host="happy")
])

# Chapter 2: Vehicles
E.chapter("Transportation")

E.story("Getting Around", [
    ("N", "Now let's explore different ways to travel!", "Now let's explore different ways to travel!"),
    ("A", "I love the colorful cars!", "I love the colorful cars!", "happy"),
    ("M", "Transportation makes our world connected!", "Transportation makes our world connected!", "point")
])

E.add("vehicles_showcase", [
    B("Cars come in many colors: blue, red, green, and orange!", [
        T("Colorful Cars"),
        text(150, 150, "Blue", 20, "blue"),
        text(350, 150, "Red", 20, "red"),
        text(550, 150, "Green", 20, "green"),
        text(750, 150, "Orange", 20, "orange")
    ], acts=[
        A("car1", "car_blue", (0.0, 120, 200, {"pop": 1})),
        A("car2", "car_red", (0.25, 300, 200, {"pop": 1})),
        A("car3", "car_green", (0.5, 480, 200, {"pop": 1})),
        A("car4", "car_orange", (0.75, 660, 200, {"pop": 1}))
    ], host="stand")
])

E.add("big_vehicles", [
    B("Larger vehicles like trucks and buses carry more passengers and cargo!", [
        T("Big Vehicles"),
        text(250, 150, "Truck", 24, "blue"),
        text(650, 150, "Bus", 24, "blue")
    ], acts=[
        A("truck", "truck", (0.0, 150, 220, {"pop": 1})),
        A("bus", "bus", (0.4, 500, 220, {"pop": 1}))
    ])
])

E.add("air_transport", [
    B("For faster travel, we have airplanes and rockets!", [
        T("Air Travel"),
        text(250, 150, "Airplane", 24, "blue"),
        text(650, 150, "Rocket", 24, "blue")
    ], acts=[
        A("plane", "airplane", (0.0, 150, 200, {"pop": 1})),
        A("rocket", "rocket", (0.4, 600, 230, {"pop": 1}))
    ], sfx=[("whoosh", 0.5)], host="happy")
])

# Chapter 3: Computer Components
E.chapter("Computer Hardware")

E.story("Inside Your Computer", [
    ("N", "Let's explore the components that make computers work!", "Let's explore the components that make computers work!"),
    ("M", "Understanding hardware helps us appreciate technology!", "Understanding hardware helps us appreciate technology!", "point"),
    ("A", "This is so interesting!", "This is so interesting!", "think")
])

E.add("input_output", [
    B("We interact with computers through input and output devices.", [
        T("Input & Display"),
        text(200, 150, "Laptop", 20, "blue"),
        text(450, 150, "Monitor", 20, "blue"),
        text(700, 150, "Keyboard", 20, "blue"),
        text(950, 150, "Mouse", 20, "blue")
    ], acts=[
        A("laptop", "laptop", (0.0, 140, 220, {"pop": 1})),
        A("monitor", "monitor", (0.25, 370, 220, {"pop": 1})),
        A("keyboard", "keyboard", (0.5, 600, 260, {"pop": 1})),
        A("mouse", "mouse", (0.75, 920, 250, {"pop": 1}))
    ], host="point")
])

E.add("processing", [
    B("The CPU and RAM are the brain and memory of your computer!", [
        T("Processing Power"),
        text(300, 150, "CPU Chip", 24, "blue"),
        text(700, 150, "RAM Stick", 24, "blue")
    ], acts=[
        A("cpu", "cpu_chip", (0.0, 240, 220, {"pop": 1})),
        A("ram", "ram_stick", (0.4, 600, 260, {"pop": 1}))
    ], sfx=[("ding", 0.1), ("ding", 0.5)], host="happy")
])

E.add("storage_network", [
    B("Hard drives store your data, while routers and servers connect you to the internet!", [
        T("Storage & Network"),
        text(200, 150, "Hard Drive", 20, "blue"),
        text(450, 150, "Server", 20, "blue"),
        text(700, 150, "Router", 20, "blue"),
        text(950, 150, "USB Drive", 20, "blue")
    ], acts=[
        A("hdd", "hard_drive", (0.0, 140, 240, {"pop": 1})),
        A("server", "server_rack", (0.25, 390, 240, {"pop": 1})),
        A("router", "router", (0.5, 620, 260, {"pop": 1})),
        A("usb", "usb_drive", (0.75, 920, 260, {"pop": 1}))
    ])
])

# Chapter 4: Colors & Customization
E.chapter("Vibrant Colors")

E.bullets("Enhanced Visual Design", [
    ("All characters now feature vibrant, eye-catching colors", 
     "All characters now feature vibrant, eye-catching colors", "blue"),
    ("Asha has a coral tunic and bright blue backpack", 
     "Asha has a coral tunic and bright blue backpack", "orange"),
    ("Mira wears a vibrant purple coat", 
     "Mira wears a vibrant purple coat", "violet"),
    ("Pip the penguin sports a teal scarf", 
     "Pip the penguin sports a teal scarf", "teal"),
    ("Vehicles come in multiple color options", 
     "Vehicles come in multiple color options", "green"),
    ("Laptops and monitors available in different screen colors", 
     "Laptops and monitors available in different screen colors", "blue")
])

# Practice exercise
E.practice(1, 
    "How would you add a red car and a laptop to your scene?",
    """# Example code for adding characters
acts=[
    A("mycar", "car_red", (0.0, 200, 300, {"pop": 1})),
    A("mylaptop", "laptop_blue", (0.4, 600, 350, {"pop": 1}))
]""",
    [
        (4, "This creates animated characters that pop into the scene!", 
         "This creates animated characters that pop into the scene!")
    ],
    total=1
)

# Memory hook
E.hook("Vibrant visuals engage learners", 
       "Why are colorful characters important in educational videos?",
       "They capture attention, make content memorable, and create an enjoyable learning experience!",
       "Colorful = Memorable")

# Outro
E.outro([
    ("We've added 20+ new characters across animals, vehicles, and tech!", 
     "We've added 20 plus new characters across animals, vehicles, and tech!"),
    ("All characters feature enhanced, vibrant colors", 
     "All characters feature enhanced, vibrant colors"),
    ("Female voice narration makes content more approachable", 
     "Female voice narration makes content more approachable"),
    ("Mix and match characters to create engaging stories!", 
     "Mix and match characters to create engaging stories!")
], None)

E.build()
