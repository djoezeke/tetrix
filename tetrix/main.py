"""MAin Game"""

import sys
import random
import pygame

from tetrix.game import config
from tetrix.game.colors import Colors
from tetrix.game.grid import Grid

from tetrix.game.blocks import LBlock
from tetrix.game.blocks import JBlock
from tetrix.game.blocks import IBlock
from tetrix.game.blocks import OBlock
from tetrix.game.blocks import SBlock
from tetrix.game.blocks import TBlock
from tetrix.game.blocks import ZBlock

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)


class Game:
    """Game"""

    def __init__(self):
        self.grid = Grid()
        self.blocks = [
            LBlock(),
            JBlock(),
            IBlock(),
            OBlock(),
            ZBlock(),
            SBlock(),
            TBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0

    def update_score(self, lines_cleared, moved_down_points):
        """update_score"""
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += moved_down_points

    def reset(self):
        """reset"""
        self.grid.reset()
        self.blocks = [
            LBlock(),
            JBlock(),
            IBlock(),
            OBlock(),
            ZBlock(),
            SBlock(),
            TBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def draw(self, screen: pygame.Surface):
        """draw"""
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        self.next_block.draw(screen, 270, 270)

    def block_inside(self):
        """Block inside window"""
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.col) is False:
                return False
        return True

    def block_fits(self):
        """block_fits"""

        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.col) is False:
                return False
        return True

    def lock_block(self):
        """lock_block"""

        tiles = self.current_block.get_cell_positions()

        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_row()

        if rows_cleared > 0:
            self.update_score(rows_cleared, 0)

        if self.block_fits() is False:
            self.game_over = True

    def move_left(self):
        """move_left"""
        self.current_block.move(0, -1)
        if self.block_inside() is False or self.block_fits() is False:
            self.current_block.move(0, 1)

    def move_right(self):
        """move_right"""
        self.current_block.move(0, 1)
        if self.block_inside() is False or self.block_fits() is False:
            self.current_block.move(0, -1)

    def move_down(self):
        """move_down"""

        self.current_block.move(1, 0)
        if self.block_inside() is False or self.block_fits() is False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def rotate(self):
        """rotate"""
        self.current_block.rotate()
        if self.block_inside() is False or self.block_fits() is False:
            self.current_block.undo_rotate()
        else:
            # self.rotate_sound.play()
            pass

    def get_random_block(self):
        """get_random_block"""

        if len(self.blocks) == 0:
            self.blocks = [
                LBlock(),
                JBlock(),
                IBlock(),
                OBlock(),
                ZBlock(),
                SBlock(),
                TBlock(),
            ]

        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block


game = Game()
score_suface = config.font.render("Score", True, Colors.white)
score_rect = pygame.Rect(320, 55, 170, 60)

next_suface = config.font.render("Next", True, Colors.white)
next_rect = pygame.Rect(320, 215, 170, 180)

over_suface = config.font.render("GAME OVER", True, Colors.white)


def tetrix(args: list):
    """tetrix"""

    pygame.display.set_caption("Tetrix")

    config.music.set_volume(config.volume)
    config.music.play(loops=-1)

    if "--nosound" in args:
        config.music.set_volume(0)
        config.music.stop()

    run: bool = True

    config.clock = pygame.time.Clock()

    # main game loop
    while run:
        config.clock.tick(config.FPS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if game.game_over is True:
                    game.game_over = False
                    game.reset()

                if event.key == pygame.K_LEFT and game.game_over is False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over is False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over is False:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and game.game_over is False:
                    game.rotate()
            if event.type == GAME_UPDATE and game.game_over is False:
                game.move_down()

        score_value_surface = config.font.render(str(game.score), True, Colors.white)

        config.WINDOW.fill(Colors.dark_blue)
        config.WINDOW.blit(score_suface, (365, 20, 50, 50))
        config.WINDOW.blit(next_suface, (375, 150, 50, 50))

        if game.game_over is True:
            config.WINDOW.blit(over_suface, (320, 450, 50, 50))

        pygame.draw.rect(config.WINDOW, Colors.light_blue, score_rect, 0, 10)

        config.WINDOW.blit(
            score_value_surface,
            score_value_surface.get_rect(
                centerx=score_rect.centerx, centery=score_rect.centery
            ),
        )

        pygame.draw.rect(config.WINDOW, Colors.light_blue, next_rect, 0, 10)
        game.draw(config.WINDOW)

    pygame.quit()
    sys.exit()


def main(args):
    """Main"""
    try:
        tetrix(args)
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
        print("Exiting")


if __name__ == "__main__":
    main(sys.argv)
