# Ball class with physics and speed scaling

import pygame
import random
import math
from settings import *
from effects import draw_glow

class Ball:
    """The game ball with physics-based movement."""
    def __init__(self):
        self.radius = BALL_RADIUS
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.reset()

    def reset(self):
        """Reset ball to initial state (attached to paddle)."""
        self.speed = BALL_SPEED_INITIAL
        self.vx = 0
        self.vy = 0
        self.attached = True
        self.attached_offset = 0
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.update_rect()

    def update_rect(self):
        """Update rect position from center."""
        self.rect.center = (int(self.x), int(self.y))

    def launch(self, paddle_rect):
        """Launch ball from paddle with random angle."""
        self.x = paddle_rect.centerx
        self.y = paddle_rect.top - self.radius

        # Random angle between -60 and 60 degrees (pointing upward)
        angle = random.uniform(-60, 60) * (math.pi / 180)
        self.vx = math.sin(angle) * self.speed
        self.vy = -math.cos(angle) * self.speed
        self.attached = False
        self.update_rect()

    def increase_speed(self):
        """Increase ball speed after hitting a brick."""
        if self.speed < BALL_MAX_SPEED:
            self.speed += BALL_SPEED_INCREMENT
            # Normalize velocity to new speed
            mag = math.sqrt(self.vx**2 + self.vy**2)
            if mag > 0:
                self.vx = (self.vx / mag) * self.speed
                self.vy = (self.vy / mag) * self.speed

    def update(self, dt, keys=None, paddle_rect=None):
        """Update ball position and handle collisions."""
        if self.attached and paddle_rect:
            # Follow paddle
            self.x = paddle_rect.centerx
            self.y = paddle_rect.top - self.radius
            self.vx = 0
            self.vy = 0
            self.update_rect()
            return

        # Move ball
        self.x += self.vx
        self.y += self.vy
        self.update_rect()

        # Wall collisions
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vx = -abs(self.vx)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)

        # Bottom - ball lost (handled in main)
        if self.rect.bottom >= SCREEN_HEIGHT:
            return "lost"

        return "active"

    def check_paddle_collision(self, paddle_rect):
        """Handle collision with paddle."""
        if self.rect.colliderect(paddle_rect):
            # Determine hit position relative to paddle center
            hit_pos = (self.rect.centerx - paddle_rect.centerx) / (paddle_rect.width / 2)

            # Reflect Y and add horizontal direction based on hit position
            self.vy = -abs(self.vy)

            # Add English (spin effect)
            english_strength = 3
            self.vx = hit_pos * english_strength

            # Ensure minimum horizontal speed
            if abs(self.vx) < 1:
                self.vx = 1 if hit_pos >= 0 else -1

            # Prevent ball from getting stuck inside paddle
            self.rect.bottom = paddle_rect.top
            self.y = self.rect.centery

            return True
        return False

    def draw(self, surface):
        """Draw ball with glow effect."""
        # Glow
        draw_glow(surface, BALL_COLOR, self.rect.center, self.radius, glow_radius=BALL_GLOW_RADIUS * 2)

        # Main ball
        pygame.draw.circle(surface, BALL_COLOR, self.rect.center, self.radius)

        # Highlight
        highlight_pos = (self.rect.centerx - self.radius // 3, self.rect.centery - self.radius // 3)
        highlight_radius = self.radius // 3
        pygame.draw.circle(surface, WHITE, highlight_pos, highlight_radius)
