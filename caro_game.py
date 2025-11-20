# caro_game.py

import pygame
from game_config import *
from bot import CaroBot


class CaroGame:
    def __init__(self, font, mode="PVP"):
        self.font = font
        self.mode = mode
        self.bot = CaroBot() if mode == "PVB" else None

        button_width = 110
        button_height = 35

        center_x = WIDTH // 2

        self.btn_menu = pygame.Rect(center_x - button_width - 10, 5, button_width, button_height)
        self.btn_exit = pygame.Rect(center_x + 10, 5, button_width, button_height)

        self.reset_game()

    def reset_game(self):
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = "X"
        self.game_over = False
        self.win_line = []

    def handle_click(self, pos):
        if self.game_over:
            return

        mx, my = pos

        if not (
            MARGIN < mx < MARGIN + GRID_SIZE * CELL_SIZE
            and 80 < my < 80 + GRID_SIZE * CELL_SIZE
        ):
            return

        x = (mx - MARGIN) // CELL_SIZE
        y = (my - 80) // CELL_SIZE

        if self.board[y][x] is None:
            self.board[y][x] = self.current_player

            if self.check_win(x, y):
                self.game_over = True
                return

            if self.mode == "PVP":
                self.current_player = "O" if self.current_player == "X" else "X"
                return

            if self.mode == "PVB":
                self.current_player = "O"
                move = self.bot.get_move(self.board)
                if move:
                    bx, by = move
                    self.board[by][bx] = "O"

                    if self.check_win(bx, by):
                        self.game_over = True
                    else:
                        self.current_player = "X"

    def handle_menu_click(self, pos):
        if self.btn_menu.collidepoint(pos):
            return "MENU"
        if self.btn_exit.collidepoint(pos):
            return "EXIT"
        return None

    def check_win(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            line = [(x, y)]

            tx, ty = x + dx, y + dy
            while (
                0 <= tx < GRID_SIZE
                and 0 <= ty < GRID_SIZE
                and self.board[ty][tx] == self.board[y][x]
            ):
                line.append((tx, ty))
                tx += dx
                ty += dy

            tx, ty = x - dx, y - dy
            while (
                0 <= tx < GRID_SIZE
                and 0 <= ty < GRID_SIZE
                and self.board[ty][tx] == self.board[y][x]
            ):
                line.append((tx, ty))
                tx -= dx
                ty -= dy

            if len(line) >= 5:
                self.win_line = line
                return True
        return False

    def draw_top_menu(self, screen):
        button_font = pygame.font.SysFont("Arial", 20, bold=True)

        pygame.draw.rect(screen, (240, 240, 240), self.btn_menu, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), self.btn_menu, 2, border_radius=8)
        screen.blit(
            button_font.render("Menu", True, (0, 0, 0)),
            (self.btn_menu.x + 25, self.btn_menu.y + 7),
        )

        pygame.draw.rect(screen, (240, 240, 240), self.btn_exit, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), self.btn_exit, 2, border_radius=8)
        screen.blit(
            button_font.render("Exit", True, (0, 0, 0)),
            (self.btn_exit.x + 35, self.btn_exit.y + 7),
        )

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)

        for i in range(GRID_SIZE + 1):
            pygame.draw.line(
                screen,
                GRID_COLOR,
                (MARGIN, 80 + i * CELL_SIZE),
                (MARGIN + GRID_SIZE * CELL_SIZE, 80 + i * CELL_SIZE),
            )
            pygame.draw.line(
                screen,
                GRID_COLOR,
                (MARGIN + i * CELL_SIZE, 80),
                (MARGIN + i * CELL_SIZE, 80 + GRID_SIZE * CELL_SIZE),
            )

        for (x, y) in self.win_line:
            pygame.draw.rect(
                screen,
                WIN_HIGHLIGHT_COLOR,
                (MARGIN + x * CELL_SIZE, 80 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                4,
            )

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.board[y][x]:
                    text = self.font.render(
                        self.board[y][x],
                        True,
                        X_COLOR if self.board[y][x] == "X" else O_COLOR,
                    )
                    cx = MARGIN + x * CELL_SIZE + CELL_SIZE // 2
                    cy = 80 + y * CELL_SIZE + CELL_SIZE // 2
                    screen.blit(text, text.get_rect(center=(cx, cy)))

        self.draw_top_menu(screen)

    def draw_info(self, screen, info_font, width):
        mode_text = "Mode: Two Players" if self.mode == "PVP" else "Mode: Player vs Bot"

        if self.game_over:
            msg = f"{self.current_player} wins! Press R to restart."
        else:
            msg = f"{mode_text}  |  Turn: {self.current_player}  |  R = Restart, ESC = Quit"

        label = info_font.render(msg, True, TEXT_COLOR)
        screen.blit(label, (width // 2 - label.get_width() // 2, 50))
