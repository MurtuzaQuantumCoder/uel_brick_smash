# Paddle class for both solo and duo modes
# Player 1: Arrow keys (left/right), Space to launch
# Player 2: A/D keys, W to launch

import pygame
from settings import *
from effects import draw_glow_rect

class Paddle:
    """A player-controlled paddle."""
    def __init__(self, x, y, player_num=1, color=PADDLE_COLOR_P1):
        self.base_width = PADDLE_WIDTH
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color
        self.player_num = player_num
        self.speed = PADDLE_SPEED
        self.base_speed = PADDLE_SPEED
        self.launched = False
        self.can_launch = True

        # Power-up timers
        self.width_boost_timer = 0
        self.speed_boost_timer = 0

    def update(self, keys, dt, game_mode, head_pos=None):
        """Update paddle position based on key input or head tracking."""
        # Check power-up timers
        if self.width_boost_timer > 0:
            self.width_boost_timer -= dt
            if self.width_boost_timer <= 0:
                self.width = self.base_width

        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed = self.base_speed

        # Movement - use head position if provided (head control mode)
        move_left = False
        move_right = False

        if head_pos is not None:
            # Head control: map head position to movement with deadzone
            deadzone = 0.1
            center = 0.5
            threshold = deadzone
            
            if head_pos < center - threshold:
                move_left = True
            elif head_pos > center + threshold:
                move_right = True
        elif self.player_num == 1:
            move_left = keys[pygame.K_LEFT]
            move_right = keys[pygame.K_RIGHT]
        elif self.player_num == 2 and game_mode == "duo":
            move_left = keys[pygame.K_a]
            move_right = keys[pygame.K_d]

        if move_left and self.rect.left > 0:
            self.rect.x -= self.speed
        if move_right and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        # Clamp to screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def launch_ball(self, keys):
        """Check if player wants to launch ball."""
        if self.launched:
            return False

        can_launch = False
        if self.player_num == 1:
            can_launch = keys[pygame.K_SPACE]
        elif self.player_num == 2:
            can_launch = keys[pygame.K_w]

        if can_launch and self.can_launch:
            self.launched = True
            self.can_launch = False
            return True
        return False

    def apply_powerup(self, powerup_type):
        """Apply power-up effect to paddle."""
        if powerup_type == "width":
            self.width = int(self.base_width * 1.5)
            self.width_boost_timer = POWERUP_DURATION
        elif powerup_type == "speed":
            self.speed = int(self.base_speed * 1.5)
            self.speed_boost_timer = POWERUP_DURATION

        # Update rect size
        self.rect.width = self.width

    def reset(self, x=None):
        """Reset paddle to starting state."""
        if x is None:
            x = SCREEN_WIDTH // 2 - self.width // 2
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - 50
        self.width = self.base_width
        self.speed = self.base_speed
        self.launched = False
        self.can_launch = True
        self.width_boost_timer = 0
        self.speed_boost_timer = 0

    def draw(self, surface):
        """Draw paddle with glow effect."""
        draw_glow_rect(surface, self.color, self.rect, glow_radius=PADDLE_GLOW_RADIUS)

        # Draw inner gradient effect
        inner_rect = self.rect.inflate(-4, -4)
        inner_color = tuple(min(255, c + 40) for c in self.color)
        pygame.draw.rect(surface, inner_color, inner_rect, border_radius=4)

        # Draw player indicator
        font = pygame.font.Font(None, 18)
        label = f"P{self.player_num}"
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
