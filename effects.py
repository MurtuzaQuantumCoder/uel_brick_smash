# Visual effects system: particles, screen shake, glow rendering

import pygame
import random
import math
from settings import *

class Particle:
    """A single particle for explosion effects."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = PARTICLE_LIFETIME
        self.max_lifetime = PARTICLE_LIFETIME
        self.size = random.randint(2, 5)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= dt
        self.vy += 0.1  # gravity

    def draw(self, surface):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(s, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    """Manages multiple particle effects."""
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=PARTICLE_COUNT):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles:
            p.update(dt)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

class ScreenShake:
    """Manages screen shake effect."""
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.time_left = 0

    def start(self, magnitude=SHAKE_MAGNITUDE, duration=SHAKE_DURATION):
        self.time_left = duration

    def update(self, dt):
        if self.time_left > 0:
            self.offset_x = random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE)
            self.offset_y = random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE)
            self.time_left -= dt
        else:
            self.offset_x = 0
            self.offset_y = 0

    def apply(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y

def draw_glow(surface, color, center, radius, glow_radius=None):
    """Draw a glowing effect around a shape."""
    if glow_radius is None:
        glow_radius = radius * 2

    # Draw multiple transparent circles for glow
    for i in range(3):
        alpha = 100 - i * 30
        r = radius + (glow_radius - radius) * (i / 3)
        glow_surf = pygame.Surface((int(r * 2), int(r * 2)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, alpha), (int(r), int(r)), int(r))
        surface.blit(glow_surf, (center[0] - r, center[1] - r))

    # Draw bright center
    pygame.draw.circle(surface, color, center, radius)

def draw_glow_rect(surface, color, rect, glow_radius=10):
    """Draw a glowing rectangle."""
    for i in range(3):
        alpha = 100 - i * 30
        s = pygame.Surface((rect.width + glow_radius * 2, rect.height + glow_radius * 2), pygame.SRCALPHA)
        inflate = glow_radius * (i / 3)
        draw_rect = s.get_rect()
        pygame.draw.rect(s, (*color, alpha), draw_rect, border_radius=8)
        surface.blit(s, (rect.x - glow_radius, rect.y - glow_radius))

    pygame.draw.rect(surface, color, rect, border_radius=5)

def draw_starfield(surface, stars):
    """Draw animated starfield background."""
    for star in stars:
        brightness = random.randint(100, 255)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (int(star[0]), int(star[1])), star[2])

def create_stars(count):
    """Create random stars for the background."""
    stars = []
    for _ in range(count):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 2)
        stars.append([x, y, size])
    return stars

def update_stars(stars):
    """Twinkle stars by slightly adjusting brightness."""
    for star in stars:
        if random.random() < 0.05:
            star[2] = random.randint(1, 2)
