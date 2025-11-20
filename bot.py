# bot.py

import random
from game_config import GRID_SIZE


class CaroBot:
    def __init__(self):
        pass

    # Try to block the human if they have 4 in a row
    def find_block_move(self, board, human_symbol):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if board[y][x] == human_symbol:

                    for dx, dy in directions:
                        line = [(x, y)]

                        # forward
                        tx, ty = x + dx, y + dy
                        while (
                            0 <= tx < GRID_SIZE
                            and 0 <= ty < GRID_SIZE
                            and board[ty][tx] == human_symbol
                        ):
                            line.append((tx, ty))
                            tx += dx
                            ty += dy

                        # backward
                        tx, ty = x - dx, y - dy
                        while (
                            0 <= tx < GRID_SIZE
                            and 0 <= ty < GRID_SIZE
                            and board[ty][tx] == human_symbol
                        ):
                            line.append((tx, ty))
                            tx -= dx
                            ty -= dy

                        if len(line) == 4:
                            # candidate cells on both sides
                            px1 = line[0][0] - dx
                            py1 = line[0][1] - dy
                            px2 = line[-1][0] + dx
                            py2 = line[-1][1] + dy

                            if (
                                0 <= px1 < GRID_SIZE
                                and 0 <= py1 < GRID_SIZE
                                and board[py1][px1] is None
                            ):
                                return (px1, py1)

                            if (
                                0 <= px2 < GRID_SIZE
                                and 0 <= py2 < GRID_SIZE
                                and board[py2][px2] is None
                            ):
                                return (px2, py2)

        return None

    # Prefer cells near existing stones
    def find_good_area(self, board):
        candidates = []

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if board[y][x] is None:
                    score = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                                if board[ny][nx] is not None:
                                    score += 1
                    if score > 0:
                        candidates.append((score, (x, y)))

        if not candidates:
            return None

        candidates.sort(reverse=True)
        return candidates[0][1]

    # Fallback random move
    def random_move(self, board):
        empty = [
            (x, y)
            for y in range(GRID_SIZE)
            for x in range(GRID_SIZE)
            if board[y][x] is None
        ]
        return random.choice(empty) if empty else None

    # Main bot move
    def get_move(self, board, human_symbol="X", bot_symbol="O"):
        # 1) Block
        move = self.find_block_move(board, human_symbol)
        if move:
            return move

        # 2) Good area
        move = self.find_good_area(board)
        if move:
            return move

        # 3) Random
        return self.random_move(board)
