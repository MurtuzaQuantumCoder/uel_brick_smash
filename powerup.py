# Power-up system
# Power-ups fall from destroyed bricks and can be caught by paddles

import pygame
import random
from settings import *

class PowerUp:
    """Falling power-up capsule."""
    def __init__(self, x, y, power_type):
        self.rect = pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)
        self.type = power_type
        self.color = POWERUP_TYPES[power_type]["color"]
        self.label = POWERUP_TYPES[power_type]["label"]
        self.speed = POWERUP_SPEED
        self.active = True
        self.float_offset = 0
        self.float_speed = 5

    def update(self, dt):
        """Update power-up position."""
        self.rect.y += self.speed

        # Floating animation
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.005) * 3

        # Check if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.active = False

    def check_collision(self, paddle_rect):
        """Check if power-up is caught by paddle."""
        if self.rect.colliderect(paddle_rect):
            self.active = False
            return True
        return False

    def draw(self, surface, font):
        """Draw glowing capsule with label."""
        draw_glow_rect(surface, self.color, self.rect, glow_radius=8)

        # Draw capsule shape (rounded rectangle)
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)

        # Draw inner glow
        inner_rect = self.rect.inflate(-6, -6)
        inner_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.rect(surface, inner_color, inner_rect, border_radius=6)

        # Draw label
        label_font = pygame.font.Font(None, FONT_SMALL)
        text = label_font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class PowerUpManager:
    """Manages spawning and updating of power-ups."""
    def __init__(self):
        self.powerups = []

    def spawn_from_brick(self, brick_rect):
        """Randomly spawn power-up from destroyed brick."""
        if random.random() < POWERUP_SPAWN_CHANCE:
            power_type = random.choice(list(POWERUP_TYPES.keys()))
            x = brick_rect.centerx - POWERUP_WIDTH // 2
            y = brick_rect.centery
            powerup = PowerUp(x, y, power_type)
            self.powerups.append(powerup)

    def update(self, dt, paddles, ball=None):
        """Update all power-ups and check collisions."""
        caught_powerups = []

        for powerup in self.powerups[:]:
            if not powerup.active:
                self.powerups.remove(powerup)
                continue

            powerup.update(dt)

            # Check collision with any paddle
            for paddle in paddles:
                if powerup.check_collision(paddle.rect):
                    caught_powerups.append((powerup.type, paddle.player_num))
                    self.powerups.remove(powerup)
                    break

        return caught_powerups

    def draw(self, surface, font):
        """Draw all active power-ups."""
        for powerup in self.powerups:
            if powerup.active:
                # Apply float offset
                draw_rect = powerup.rect.copy()
                draw_rect.y += int(powerup.float_offset)
                powerup.draw(surface, font)

    def reset(self):
        """Clear all power-ups."""
        self.powerups = []
