# Brick class for UEL Brick Smash 2.0
# Each brick has a UEL-themed label and neon glow

import pygame
import random
from settings import *
from effects import draw_glow_rect

class Brick:
    """A single brick with UEL-themed label."""
    def __init__(self, x, y, color, label):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.label = label
        self.active = True
        self.flash_timer = 0
        self.flash_duration = 100  # ms

    def hit(self):
        """Mark brick as destroyed and start flash effect."""
        self.active = False
        self.flash_timer = self.flash_duration
        return True

    def update(self, dt):
        """Update brick state (flash animation)."""
        if self.flash_timer > 0:
            self.flash_timer -= dt

    def draw(self, surface, font):
        """Draw the brick with glow and label."""
        if not self.active:
            return

        # Flash effect when hit
        if self.flash_timer > 0:
            color = WHITE
        else:
            color = self.color

        # Draw glow background
        glow_rect = self.rect.inflate(10, 10)
        draw_glow_rect(surface, color, glow_rect, glow_radius=8)

        # Draw brick body
        pygame.draw.rect(surface, color, self.rect, border_radius=5)

        # Draw inner highlight
        highlight_rect = self.rect.inflate(-8, -8)
        highlight_color = tuple(min(255, c + 60) for c in color)
        pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=3)

        # Draw label text
        label_font = pygame.font.Font(None, FONT_SMALL)
        text = label_font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class BrickField:
    """Manages all bricks in the game."""
    def __init__(self, rows=BRICK_ROWS, cols=BRICK_COLS):
        self.bricks = []
        self.rows = rows
        self.cols = cols
        self.create_bricks()

    def create_bricks(self):
        """Create brick grid with UEL-themed labels."""
        self.bricks = []

        # Calculate total width to center bricks
        total_width = self.cols * (BRICK_WIDTH + BRICK_PADDING) - BRICK_PADDING
        start_x = (SCREEN_WIDTH - total_width) // 2

        for row in range(self.rows):
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            # Cycle through labels
            label = BRICK_LABELS[row % len(BRICK_LABELS)]

            for col in range(self.cols):
                x = start_x + col * (BRICK_WIDTH + BRICK_PADDING)
                y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                brick = Brick(x, y, color, label)
                self.bricks.append(brick)

    def update(self, dt):
        """Update all bricks."""
        for brick in self.bricks:
            brick.update(dt)

    def draw(self, surface, font):
        """Draw all active bricks."""
        for brick in self.bricks:
            brick.draw(surface, font)

    def check_collision(self, ball):
        """Check and handle ball collision with bricks."""
        hit_bricks = []
        for brick in self.bricks:
            if brick.active and brick.rect.colliderect(ball.rect):
                # Determine collision side
                if ball.vy > 0:  # Moving down - hit top of brick
                    ball.vy = -abs(ball.vy)
                elif ball.vy < 0:  # Moving up - hit bottom
                    ball.vy = abs(ball.vy)
                elif ball.vx > 0:  # Moving right - hit left
                    ball.vx = -abs(ball.vx)
                else:  # Moving left - hit right
                    ball.vx = abs(ball.vx)

                brick.hit()
                hit_bricks.append(brick)

        return hit_bricks

    def count_active(self):
        """Count remaining active bricks."""
        return sum(1 for b in self.bricks if b.active)

    def reset(self):
        """Reset all bricks."""
        self.create_bricks()
