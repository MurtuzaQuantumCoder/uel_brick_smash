# UEL Brick Smash 2.0: Duo Deadline
# Game Settings and Configuration

import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (Cyberpunk Neon Palette)
BACKGROUND = (10, 5, 30)  # Deep purple/blue
BACKGROUND_GRADIENT_TOP = (20, 10, 60)
BACKGROUND_GRADIENT_BOTTOM = (5, 2, 15)

# Neon Colors
NEON_MAGENTA = (255, 0, 255)
NEON_CYAN = (0, 255, 255)
NEON_LIME = (50, 255, 50)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 0)
NEON_RED = (255, 50, 50)
NEON_BLUE = (100, 200, 255)
NEON_PURPLE = (200, 100, 255)
WHITE = (255, 255, 255)

# Brick colors by row (top to bottom)
BRICK_COLORS = [
    NEON_MAGENTA,
    NEON_CYAN,
    NEON_LIME,
    NEON_ORANGE,
    NEON_YELLOW
]

# UEL-themed brick labels
BRICK_LABELS = [
    "DOCKLANDS",
    "LIBRARY",
    "COMP LAB",
    "UNI SQ",
    "DOME",
    "LECTURE",
    "EXAM"
]

BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 80
BRICK_OFFSET_LEFT = 35

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
PADDLE_COLOR_P1 = NEON_CYAN
PADDLE_COLOR_P2 = NEON_ORANGE
PADDLE_GLOW_RADIUS = 15

# Ball
BALL_RADIUS = 10
BALL_SPEED_INITIAL = 5
BALL_SPEED_INCREMENT = 0.5
BALL_MAX_SPEED = 12
BALL_COLOR = NEON_WHITE = WHITE
BALL_GLOW_RADIUS = 8

# Power-ups
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
POWERUP_SPEED = 3
POWERUP_SPAWN_CHANCE = 0.20  # 20%

# Additional neon colors for power-ups
NEON_BROWN = (139, 69, 19)
NEON_GREEN = (0, 200, 0)

POWERUP_TYPES = {
    "coffee": {
        "color": NEON_BROWN,
        "label": "COFFEE",
        "duration": 10000,  # 10 seconds in ms
        "effect": "speed"
    },
    "extension": {
        "color": NEON_GREEN,
        "label": "EXT",
        "duration": 15000,  # 15 seconds
        "effect": "width"
    },
    "library": {
        "color": NEON_BLUE,
        "label": "LIB",
        "duration": 12000,  # 12 seconds
        "effect": "slow"
    },
    "duo_boost": {
        "color": NEON_PURPLE,
        "label": "DUO",
        "duration": 8000,  # 8 seconds
        "effect": "both_width"
    }
}

# Lives
LIVES_SOLO = 3
LIVES_DUO = 5
HEART_SIZE = 20

# Game states
MAIN_MENU = 0
PLAYING = 1
COUNTDOWN = 2
LIFE_LOST = 3
GAME_OVER = 4
VICTORY = 5
CREDITS = 6

# Timing
COUNTDOWN_TIME = 3000  # 3 seconds in ms
LIFE_LOST_PAUSE = 1500  # 1.5 seconds
POWERUP_DURATION = 15000  # 15 seconds max

# Scoring
POINTS_PER_BRICK = 10

# Font sizes
FONT_SMALL = 20
FONT_MEDIUM = 32
FONT_LARGE = 48
FONT_TITLE = 72

# Starfield
STAR_COUNT = 150

# Screen shake
SHAKE_MAGNITUDE = 8
SHAKE_DURATION = 500  # ms

# Particles
PARTICLE_COUNT = 30
PARTICLE_LIFETIME = 1000  # ms
