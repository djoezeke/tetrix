"""Grid Class"""

import pygame
from tetrix.game.colors import Colors


class Grid:
    """Grid"""

    def __init__(self):
        self.num_row = 20
        self.num_col = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_col)] for i in range(self.num_row)]
        self.colors = Colors.get_cell_color()

    def reset(self):
        """reset"""
        for row in range(self.num_row):
            for col in range(self.num_col):
                self.grid[row][col] = 0

    def draw(self, window: pygame.Surface):
        """draw"""

        for row in range(self.num_row):
            for col in range(self.num_col):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(
                    col * self.cell_size + 11,
                    row * self.cell_size + 11,
                    self.cell_size - 1,
                    self.cell_size - 1,
                )
                pygame.draw.rect(window, self.colors[cell_value], cell_rect)

    def print_grid(self):
        """Print grid"""
        for row in range(self.num_row):
            for col in range(self.num_col):
                print(self.grid[row][col], end=" ")
            print()

    def is_inside(self, row, col):
        """Check if block is inside game window"""

        if row >= 0 and row < self.num_row and col >= 0 and col < self.num_col:
            return True
        return False

    def is_empty(self, row, col):
        """grid"""
        if self.grid[row][col] == 0:
            return True
        return False

    def is_row_full(self, row):
        """is_row_full"""
        for col in range(self.num_col):
            if self.grid[row][col] == 0:
                return False
        return True

    def clear_row(self, row):
        """clear_row"""
        for col in range(self.num_col):
            self.grid[row][col] = 0

    def move_row_down(self, row, num_rows):
        """move_row_down"""
        for col in range(self.num_col):
            self.grid[row + num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    def clear_full_row(self):
        """clear_full_row"""

        completed = 0
        for row in range(self.num_row - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)

        return completed
