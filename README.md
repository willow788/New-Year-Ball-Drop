<div align="center">

# 🎊 New Year Ball Drop 🎉

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Turtle_Graphics-FF6B6B?style=for-the-badge&logo=turtle&logoColor=white" alt="Turtle">
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">

### ✨ A stunning, animated New Year's Eve ball drop celebration built with Python!  ✨

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Customization](#-customization)

---

</div>

## 🌟 Features

<table>
<tr>
<td>

🎨 **Beautiful Graphics**
- Gorgeous gradient ball with glossy highlights
- Twinkling starfield background
- Dynamic LED lights

</td>
<td>

⚡ **Smooth Animation**
- Physics-based ball drop
- Particle effects & sparkles
- Falling snow simulation

</td>
</tr>
<tr>
<td>

🎆 **Festive Effects**
- Firework bursts on landing
- Color interpolation & blending
- Holiday color palette

</td>
<td>

🎯 **Easy to Use**
- Simple one-file execution
- No complex dependencies
- Fully customizable parameters

</td>
</tr>
</table>

---

## 🎥 Demo

> **Watch the magic happen as the illuminated ball descends from the sky, surrounded by twinkling stars and festive lights, culminating in a spectacular celebration!**

The animation features:
- 🌌 A starry night sky with 220+ twinkling stars
- 🔴 A beautifully rendered red ball with realistic shading
- 💡 Colorful LED lights dancing around the ball
- ❄️ Gentle snowfall throughout the scene
- 🎆 Explosive fireworks when the ball reaches the ground

---

## 🚀 Installation

### Prerequisites

- **Python 3.7+** installed on your system
- The `turtle` module (comes built-in with Python)

### Clone the Repository

```bash
git clone https://github.com/willow788/New-Year-Ball-Drop.git
cd New-Year-Ball-Drop
```

---

## 🎮 Usage

Run the animation with a single command:

```bash
python "Python Main Code/NewYearBall.py"
```

**That's it!** Sit back and enjoy the show!  🍿

---

## 🎨 Customization

Want to make it your own? Here are some parameters you can tweak in `NewYearBall.py`:

### Ball Settings
```python
BALL_RADIUS = 105           # Size of the ball
BALL_START_Y = 260          # Starting height
BALL_GROUND_Y = -40         # Landing position
```

### Color Palette
```python
BASE_OUTER = (55, 8, 18)    # Deep holiday red
BASE_INNER = (245, 55, 75)  # Bright red core
HIGHLIGHT = (255, 210, 220) # Glossy highlight
```

### LED Colors
```python
LED_PALETTE = [
    (255, 70, 70),    # Red
    (80, 255, 150),   # Green
    (90, 160, 255),   # Blue
    (255, 230, 120),  # Yellow
    (210, 140, 255),  # Purple
    (255, 160, 70),   # Orange
]
```

### Star Count
```python
build_stars(count=220, seed=7)  # Adjust star density
```

---

## 🛠️ Technical Details

### Core Features

- **Color Interpolation**: Smooth gradient transitions using `lerp_color()`
- **Clamping & Brightening**: Mathematical color manipulation for realistic effects
- **Layer System**: Separate turtle layers for background, ball, lights, effects, snow, and text
- **Random Seeding**: Reproducible star patterns with customizable seeds

### Screen Configuration
- **Resolution**: 980 × 720 pixels
- **Color Mode**: RGB (255)
- **Background**: Deep night blue `(8, 10, 18)`

---

## 📁 Project Structure

```
New-Year-Ball-Drop/
├── Python Main Code/
│   └── NewYearBall.py      # Main animation script
├── Demonstration/          # Demo files & screenshots
├── . gitignore
└── README.md
```

---

## 💡 How It Works

1. **Initialization**: Sets up the turtle screen with layers for different visual elements
2. **Star Generation**: Creates a starfield with random positions and sizes
3. **Ball Rendering**: Draws a gradient sphere with highlights and LED lights
4. **Animation Loop**: Smoothly drops the ball using physics-based motion
5. **Effects**: Triggers snow, sparkles, and fireworks at key moments
6. **Celebration**: Displays festive text and effects when the ball lands

---

## 🎯 Future Enhancements

- [ ] Add countdown timer display
- [ ] Sound effects and music
- [ ] Multiple ball designs to choose from
- [ ] Interactive controls (pause, restart, speed)
- [ ] Export animation as video/GIF

---

## 🤝 Contributing

Contributions are welcome! Feel free to: 

1. 🍴 Fork the repository
2. 🌿 Create a new branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

---

## 📜 License

This project is open source and available for anyone to use and modify.

---

## ⭐ Show Your Support

If you enjoyed this project, please consider giving it a ⭐ star on GitHub! It helps others discover the magic too! ✨

---

<div align="center">

### 🎊 Happy New Year! 🎊

**Made with ❤️ and Python**

🎆 May your year be filled with joy, code, and celebration! 🎆

---

*Ring in the new year with style! * 🥂

</div>
