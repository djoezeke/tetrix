"""Block"""

import pygame
from tetrix.game.colors import Colors
from tetrix.game.position import Position


class Block:
    """Block Size"""

    def __init__(self, id: int):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.col_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_color()

    def undo_rotate(self):
        """move_down"""
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def rotate(self):
        """move_down"""
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def move(self, row, col):
        """move"""

        self.col_offset += col
        self.row_offset += row

    def get_cell_positions(self):
        """get_cell_positions"""
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(
                position.row + self.row_offset, position.col + self.col_offset
            )
            moved_tiles.append(position)
        return moved_tiles

    def draw(self, screen, offset_x, offset_y):
        """Draw"""
        tiles = self.get_cell_positions()

        for tile in tiles:
            tile_rect = pygame.Rect(
                offset_x + tile.col * self.cell_size,
                offset_y + tile.row * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1,
            )
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
