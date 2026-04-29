# Main menu and credits screen

import pygame
from settings import *

class Menu:
    """Main menu with options and credits."""
    def __init__(self):
        self.selected_option = 0
        self.options = ["SOLO DEADLINE", "PARTNER STUDY", "HEAD CONTROL", "CREDITS"]
        self.option_rects = []
        self.title_color = NEON_MAGENTA
        self.selected_color = NEON_CYAN
        self.normal_color = NEON_WHITE

    def handle_input(self, keys):
        """Handle menu navigation."""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            return "select"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            return "select"
        elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            return self.select_option()
        return None

    def select_option(self):
        """Return the selected option action."""
        if self.selected_option == 0:
            return "solo"
        elif self.selected_option == 1:
            return "duo"
        elif self.selected_option == 2:
            return "head_control"
        elif self.selected_option == 3:
            return "credits"
        return None

    def draw(self, surface, font):
        """Draw the main menu."""
        surface.fill(BACKGROUND)

        # Draw animated stars
        from effects import draw_starfield, update_stars, create_stars
        if not hasattr(self, 'stars'):
            self.stars = create_stars(STAR_COUNT)
        update_stars(self.stars)
        draw_starfield(surface, self.stars)

        # Title
        title_font = pygame.font.Font(None, FONT_TITLE)
        title_text = "UEL BRICK SMASH"
        title_surface = title_font.render(title_text, True, NEON_CYAN)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        surface.blit(title_surface, title_rect)

        subtitle_font = pygame.font.Font(None, FONT_LARGE)
        subtitle_text = "2.0: DUO DEADLINE"
        subtitle_surface = subtitle_font.render(subtitle_text, True, NEON_MAGENTA)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        surface.blit(subtitle_surface, subtitle_rect)

        # Menu options
        option_font = pygame.font.Font(None, FONT_MEDIUM + 10)
        self.option_rects = []
        start_y = 280
        spacing = 60

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.normal_color

            # Glow effect for selected
            if i == self.selected_option:
                text_surface = option_font.render(option, True, color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
                # Draw glow
                glow_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (*color, 80), glow_surf.get_rect())
                surface.blit(glow_surf, (text_rect.x - 10, text_rect.y - 5))

            text_surface = option_font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
            surface.blit(text_surface, text_rect)
            self.option_rects.append(text_rect)

        # Instructions
        inst_font = pygame.font.Font(None, FONT_SMALL + 5)
        inst_text = "UP/DOWN or W/S to select, ENTER or SPACE to confirm"
        inst_surface = inst_font.render(inst_text, True, (150, 150, 150))
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        surface.blit(inst_surface, inst_rect)

    def draw_credits(self, surface, font):
        """Draw credits screen."""
        surface.fill(BACKGROUND)

        # Draw animated stars
        from effects import draw_starfield, update_stars
        update_stars(self.stars)
        draw_starfield(surface, self.stars)

        # Credits title
        title_font = pygame.font.Font(None, FONT_LARGE)
        title_text = "CREDITS"
        title_surface = title_font.render(title_text, True, NEON_MAGENTA)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_surface, title_rect)

        # Credits content
        content_font = pygame.font.Font(None, FONT_MEDIUM)
        lines = [
            "",
            "UEL Brick Smash 2.0: Duo Deadline",
            "",
            "Developed for UEL Computing Society",
            "AI Build-a-Thon 2026",
            "",
            "",
            "Game Design & Programming:",
            "Your Name Here",
            "",
            "",
            "Powered by Python & Pygame",
            "",
            "",
            "Press ESC or ENTER to return"
        ]

        y = 180
        for line in lines:
            text_surface = content_font.render(line, True, NEON_CYAN if line else WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
            surface.blit(text_surface, text_rect)
            y += 40

    def update(self):
        """Update menu state."""
        pass
