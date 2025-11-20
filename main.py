# main.py

import pygame
import sys

from game_config import WIDTH, HEIGHT, WINDOW_TITLE, FPS
from caro_game import CaroGame
from menu import Menu


def run_game(screen, mode):
    font = pygame.font.SysFont("Arial", 30, bold=True)
    info_font = pygame.font.SysFont("Arial", 18)
    clock = pygame.time.Clock()

    game = CaroGame(font, mode)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # First check in-game menu buttons
                action = game.handle_menu_click(event.pos)
                if action == "MENU":
                    return "MENU"
                if action == "EXIT":
                    return "EXIT"

                # If not clicking menu buttons, handle board click
                game.handle_click(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset_game()
                if event.key == pygame.K_ESCAPE:
                    return "EXIT"

        game.draw(screen)
        game.draw_info(screen, info_font, WIDTH)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    while True:
        # Main menu
        menu = Menu(screen)
        mode = menu.show()  # "PVP", "PVB", or None

        if mode is None:
            break

        # Run game with selected mode
        result = run_game(screen, mode)

        if result == "EXIT":
            break
        # if result == "MENU": loop continues, show main menu again

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
