# UEL Brick Smash 2.0: Duo Deadline

A retro-style brick breaker game with a University of East London theme, built for the UEL Computing Society AI Build-a-Thon 2026.

![Python](https://img.shields.io/badge/python-3.11+-blue?logo=python)
![Pygame](https://img.shields.io/badge/pygame-2.5+-green?logo=pygame)

## 🎮 Overview

UEL Brick Smash 2.0 is a neon cyberpunk-styled brick breaker featuring UEL campus landmarks as brick labels. Smash bricks labeled with locations like Docklands, Library, Comp Lab, and more! The game supports both solo and cooperative two-player modes.

## ✨ Features

- **Neon cyberpunk visuals** – Glowing neon bricks, starfield background, and smooth animations
- **UEL-themed content** – Bricks labeled with iconic UEL locations
- **Two game modes**:
  - Solo Deadline – Single-player classic brick breaker
  - Partner Study – Two-player cooperative mode on the same keyboard
- **Power-ups** – Coffee (speed), Extension (width), Library (slow ball), Duo Boost (both paddles, duo only)
- **Dynamic difficulty** – Ball speeds up as you break more bricks
- **Chiptune sound effects** – Programmatically generated retro sounds
- **Visual effects** – Particle explosions, screen shake, neon glows

## 🎯 Controls

### Solo Mode (Player 1)
| Action | Key |
|--------|-----|
| Move Left | ← (Left Arrow) |
| Move Right | → (Right Arrow) |
| Launch Ball | SPACE |

### Duo Mode (Both Players)
**Player 1**:
- Move: ← → (Arrow keys)
- Launch: SPACE

**Player 2**:
- Move: A / D
- Launch: W

**Shared**:
- Both paddles use the same ball
- Lives are shared (5 total in duo mode)
- Both can catch power-ups

## 🔧 Installation

1. **Prerequisites**: Python 3.11+ installed

2. **Clone and setup**:
   ```bash
   git clone https://github.com/MurtuzaQuantumCoder/uel_brick_smash.git
   cd uel_brick_smash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
uel_brick_smash/
├── main.py          # Main game loop and state management
├── settings.py      # Global configuration and constants
├── paddle.py        # Paddle class for both players
├── ball.py          # Ball physics and movement
├── brick.py         # Brick class with UEL labels
├── powerup.py       # Power-up system
├── menu.py          # Main menu and credits screen
├── effects.py       # Visual effects (particles, shake, glow)
├── sounds.py        # Chiptune sound generation
├── requirements.txt # Dependencies
└── README.md        # This file
```

## 🎨 Technical Details

- Built with **Python 3.11** and **Pygame 2.5+**
- 800×600 resolution
- 60 FPS gameplay
- No external assets – all graphics are drawn procedurally with Pygame shapes
- Sounds generated in real-time using `pygame.sndarray` and sine waves

## 🏆 UEL Computing Society AI Build-a-Thon

This project was created for the **UEL Computing Society AI Build-a-Thon 2026**.

```
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣰⣿⡿⠛⠛⠛⠿⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢰⣿⡏⠀⠀⠀⠀⠀⠈⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⢿⣷⡀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠻⢿⣶⣶⣶⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    UEL COMP SOC AI BUILD-A-THON 2026
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```

## 📝 License

This project is provided as-is for educational and hackathon purposes.

## 🙏 Credits

Game concept and development: UEL Computing Society
Powered by: Python & Pygame

---

*"Survive the semester, smash the bricks!"*
