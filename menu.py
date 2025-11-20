# menu.py

import pygame
from game_config import WIDTH, HEIGHT, TEXT_COLOR


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 45, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 28, bold=True)

        self.btn_pvp = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 60)
        self.btn_pvb = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 40, 300, 60)

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (230, 230, 230), rect, border_radius=12)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3, border_radius=12)

        label = self.font_btn.render(text, True, TEXT_COLOR)
        self.screen.blit(
            label,
            (
                rect.x + rect.width // 2 - label.get_width() // 2,
                rect.y + rect.height // 2 - label.get_height() // 2,
            ),
        )

    def show(self):
        while True:
            self.screen.fill((240, 220, 180))

            title = self.font_title.render("CARO GAME", True, TEXT_COLOR)
            self.screen.blit(
                title, (WIDTH // 2 - title.get_width() // 2, 120)
            )

            self.draw_button(self.btn_pvp, "Two Players")
            self.draw_button(self.btn_pvb, "Play vs Bot")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if self.btn_pvp.collidepoint(mx, my):
                        return "PVP"
                    if self.btn_pvb.collidepoint(mx, my):
                        return "PVB"
