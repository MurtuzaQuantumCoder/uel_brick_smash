# UEL Brick Smash 2.0: Duo Deadline
# Main game file - orchestrates all game states and components

import pygame
import sys
import math
import random
from settings import *
from paddle import Paddle
from ball import Ball
from brick import BrickField
from powerup import PowerUpManager
from menu import Menu
from sounds import init_sounds
from effects import ParticleSystem, ScreenShake, create_stars, update_stars, draw_starfield

class Game:
    """Main game class managing all states and logic."""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("UEL Brick Smash 2.0: Duo Deadline")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_MEDIUM)
        self.small_font = pygame.font.Font(None, FONT_SMALL)

        # Initialize systems
        self.sounds = init_sounds()
        self.sounds.set_volume(0.6)

        # Game state
        self.state = MAIN_MENU
        self.game_mode = "solo"  # "solo" or "duo"
        self.score = 0
        self.lives = LIVES_SOLO
        self.max_lives = LIVES_SOLO

        # Game objects
        self.menu = Menu()
        self.brick_field = BrickField()
        self.paddles = []
        self.ball = Ball()
        self.powerup_manager = PowerUpManager()

        # Effects
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.stars = create_stars(STAR_COUNT)

        # Timers
        self.countdown_timer = 0
        self.life_lost_timer = 0
        self.victory_timer = 0

        # Sparkle effects for victory
        self.sparkles = []

    def reset_game(self):
        """Reset game for a new session."""
        self.score = 0
        self.lives = LIVES_DUO if self.game_mode == "duo" else LIVES_SOLO
        self.max_lives = self.lives

        # Create paddles
        self.paddles = []
        p1 = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50, 1, PADDLE_COLOR_P1)
        self.paddles.append(p1)

        if self.game_mode == "duo":
            p2 = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50, 2, PADDLE_COLOR_P2)
            self.paddles.append(p2)

        # Reset ball and other objects
        self.ball.reset()
        self.brick_field.reset()
        self.powerup_manager.reset()
        self.particle_system = ParticleSystem()

    def start_countdown(self):
        """Start 3-2-1 countdown before gameplay."""
        self.state = COUNTDOWN
        self.countdown_timer = COUNTDOWN_TIME

    def update_countdown(self, dt):
        """Update countdown timer and launch ball when done."""
        self.countdown_timer -= dt

        if self.countdown_timer <= 0:
            # Launch ball from first paddle
            self.ball.launch(self.paddles[0].rect)
            self.state = PLAYING

    def handle_playing(self, keys):
        """Handle gameplay state."""
        # Update paddles
        for paddle in self.paddles:
            paddle.update(keys, 0, self.game_mode)

            # Check launch
            if not self.ball.attached:
                continue
            if paddle.launch_ball(keys):
                self.ball.launch(paddle.rect)
                self.sounds.play("paddle")
                break

        # Update ball
        result = self.ball.update(0, keys)

        if result == "lost":
            self.lives -= 1
            self.screen_shake.start()
            self.sounds.play("life_lost")
            if self.lives <= 0:
                self.state = GAME_OVER
                self.sounds.play("game_over")
            else:
                self.state = LIFE_LOST
                self.life_lost_timer = LIFE_LOST_PAUSE
            return

        # Ball-paddle collision
        for paddle in self.paddles:
            if self.ball.check_paddle_collision(paddle.rect):
                self.sounds.play("paddle")
                break

        # Ball-brick collision
        hit_bricks = self.brick_field.check_collision(self.ball)
        if hit_bricks:
            self.sounds.play("brick")
            self.score += len(hit_bricks) * POINTS_PER_BRICK

            # Spawn power-up from first hit brick
            if hit_bricks[0]:
                self.powerup_manager.spawn_from_brick(hit_bricks[0].rect)

            # Increase ball speed
            self.ball.increase_speed()

            # Create explosion particles
            for brick in hit_bricks:
                self.particle_system.emit(brick.rect.centerx, brick.rect.centery, brick.color)

        # Check win condition
        if self.brick_field.count_active() == 0:
            self.state = VICTORY
            self.sounds.play("victory")
            self.victory_timer = 5000  # 5 seconds

        # Update power-ups
        caught = self.powerup_manager.update(0, self.paddles, self.ball)
        for power_type, player_num in caught:
            self.sounds.play("powerup")
            # Apply effect to appropriate paddle(s)
            if power_type == "duo_boost":
                for paddle in self.paddles:
                    paddle.apply_powerup("width")
            else:
                for paddle in self.paddles:
                    if paddle.player_num == player_num:
                        if power_type == "coffee":
                            paddle.apply_powerup("speed")
                        elif power_type == "extension":
                            paddle.apply_powerup("width")
                        elif power_type == "library":
                            self.ball.speed = max(3, self.ball.speed * 0.7)
                        break

        # Update effects
        self.particle_system.update(0)
        self.screen_shake.update(0)
        update_stars(self.stars)

    def handle_life_lost(self, dt):
        """Handle life lost pause state."""
        self.life_lost_timer -= dt

        if self.life_lost_timer <= 0:
            # Reset ball and paddles, continue playing
            self.ball.reset()
            for paddle in self.paddles:
                paddle.reset()
            self.start_countdown()

    def handle_game_over(self):
        """Handle game over state."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            self.state = MAIN_MENU

    def handle_victory(self, dt):
        """Handle victory state."""
        self.victory_timer -= dt

        # Create sparkles
        if random.random() < 0.1:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            self.sparkles.append([x, y, random.randint(2, 5), 255])

        # Update sparkles
        for spark in self.sparkles[:]:
            spark[1] -= 1  # float up
            spark[3] -= 5  # fade
            if spark[3] <= 0:
                self.sparkles.remove(spark)

        if self.victory_timer <= 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                self.state = MAIN_MENU

    def draw(self):
        """Main draw function based on state."""
        # Draw background with stars
        self.screen.fill(BACKGROUND)
        draw_starfield(self.screen, self.stars)

        # Draw gradient background
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(BACKGROUND_GRADIENT_TOP[0] * (1 - ratio) + BACKGROUND_GRADIENT_BOTTOM[0] * ratio)
            g = int(BACKGROUND_GRADIENT_TOP[1] * (1 - ratio) + BACKGROUND_GRADIENT_BOTTOM[1] * ratio)
            b = int(BACKGROUND_GRADIENT_TOP[2] * (1 - ratio) + BACKGROUND_GRADIENT_BOTTOM[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        if self.state == MAIN_MENU:
            self.menu.draw(self.screen, self.font)
        elif self.state in [PLAYING, COUNTDOWN, LIFE_LOST]:
            self.draw_game()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        elif self.state == VICTORY:
            self.draw_victory()

        # Apply screen shake
        if self.screen_shake.offset_x != 0 or self.screen_shake.offset_y != 0:
            self.screen.blit(pygame.transform.offset(self.screen, self.screen_shake.offset_x, self.screen_shake.offset_y), (0, 0))
            self.screen_shake.offset_x = 0
            self.screen_shake.offset_y = 0

        pygame.display.flip()

    def draw_game(self):
        """Draw game objects during gameplay."""
        # Draw bricks
        self.brick_field.draw(self.screen, self.font)

        # Draw paddles
        for paddle in self.paddles:
            paddle.draw(self.screen)

        # Draw ball
        self.ball.draw(self.screen)

        # Draw power-ups
        self.powerup_manager.draw(self.screen, self.font)

        # Draw particles
        self.particle_system.draw(self.screen)

        # Draw UI
        self.draw_ui()

        # Draw countdown overlay
        if self.state == COUNTDOWN:
            self.draw_countdown()

        # Draw life lost overlay
        if self.state == LIFE_LOST:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 50))
            self.screen.blit(overlay, (0, 0))

    def draw_ui(self):
        """Draw score, lives, and power-up indicators."""
        # Score
        score_text = self.font.render(f"SCORE: {self.score}", True, NEON_YELLOW)
        self.screen.blit(score_text, (20, 20))

        # Lives as hearts
        heart_size = HEART_SIZE
        start_x = SCREEN_WIDTH - (self.max_lives * heart_size) - 20
        for i in range(self.max_lives):
            x = start_x + i * (heart_size + 5)
            y = 20
            if i < self.lives:
                # Draw heart shape
                points = [
                    (x + heart_size // 2, y + heart_size // 4),
                    (x + heart_size // 4, y + heart_size // 3),
                    (x, y + heart_size // 2),
                    (x + heart_size // 4, y + 3 * heart_size // 4),
                    (x + heart_size // 2, y + 2 * heart_size // 3),
                    (x + 3 * heart_size // 4, y + 3 * heart_size // 4),
                    (x + heart_size, y + heart_size // 2),
                    (x + 3 * heart_size // 4, y + heart_size // 3),
                ]
                pygame.draw.polygon(self.screen, NEON_RED, points)
            else:
                # Draw empty heart outline
                pygame.draw.circle(self.screen, (100, 100, 100), (x + heart_size // 4, y + heart_size // 3), heart_size // 8)
                pygame.draw.circle(self.screen, (100, 100, 100), (x + 3 * heart_size // 4, y + heart_size // 3), heart_size // 8)

        # Power-up indicators
        for i, paddle in enumerate(self.paddles):
            y_offset = 60 if i == 0 else 90
            # Check active power-ups
            active = []
            if paddle.width_boost_timer > 0:
                active.append("EXT")
            if paddle.speed_boost_timer > 0:
                active.append("COFFEE")

            if active:
                text = f"P{i+1}: {', '.join(active)}"
                power_text = self.small_font.render(text, True, NEON_GREEN)
                self.screen.blit(power_text, (20, y_offset))

        # Mode indicator
        mode_text = self.small_font.render(f"MODE: {self.game_mode.upper()}", True, NEON_WHITE)
        self.screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 20))

    def draw_countdown(self):
        """Draw countdown number."""
        numbers = ["3", "2", "1", "GO!"]
        idx = max(0, 3 - int(self.countdown_timer // 750))
        if idx < len(numbers):
            num = numbers[idx]
            font = pygame.font.Font(None, FONT_TITLE)
            text = font.render(num, True, NEON_MAGENTA)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, rect)

    def draw_game_over(self):
        """Draw game over screen."""
        self.draw_game()

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, FONT_TITLE)
        game_over_text = font_large.render("DEADLINE CRUSHED YOU", True, NEON_RED)
        rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, rect)

        score_text = self.font.render(f"Final Score: {self.score}", True, NEON_YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        cont_text = self.font.render("Press ENTER or SPACE to return to menu", True, NEON_WHITE)
        cont_rect = cont_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(cont_text, cont_rect)

    def draw_victory(self):
        """Draw victory screen with sparkles."""
        self.draw_game()

        # Draw sparkles
        for spark in self.sparkles:
            alpha = spark[3]
            size = spark[2]
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*NEON_YELLOW, alpha), (size, size), size)
            self.screen.blit(s, (spark[0] - size, spark[1] - size))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 50, 180))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, FONT_TITLE)
        victory_text = font_large.render("YOU SURVIVED THE SEMESTER!", True, NEON_GREEN)
        rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(victory_text, rect)

        score_text = self.font.render(f"Final Score: {self.score}", True, NEON_YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        cont_text = self.small_font.render("Press ENTER or SPACE to return to menu", True, NEON_WHITE)
        cont_rect = cont_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(cont_text, cont_rect)

    def run(self):
        """Main game loop."""
        running = True

        while running:
            dt = self.clock.tick(FPS)
            keys = pygame.key.get_pressed()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # State machine
            if self.state == MAIN_MENU:
                action = self.menu.handle_input(keys)
                if action == "solo":
                    self.game_mode = "solo"
                    self.reset_game()
                    self.start_countdown()
                elif action == "duo":
                    self.game_mode = "duo"
                    self.reset_game()
                    self.start_countdown()
                elif action == "credits":
                    self.state = CREDITS
                self.menu.update()

            elif self.state == CREDITS:
                if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN]:
                    self.state = MAIN_MENU

            elif self.state == COUNTDOWN:
                self.update_countdown(dt)

            elif self.state == PLAYING:
                self.handle_playing(keys)

            elif self.state == LIFE_LOST:
                self.handle_life_lost(dt)

            elif self.state == GAME_OVER:
                self.handle_game_over()

            elif self.state == VICTORY:
                self.handle_victory(dt)

            # Draw current state
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
