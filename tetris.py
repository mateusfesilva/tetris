from settings import *
import math
from tetramino import Tetramino
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.62, WIN_H * 0.03),
                            text='TETRIS', fgcolor=(185, 243, 228),
                            size=TILE_SIZE * 0.9)
        self.font.render_to(self.app.screen, (WIN_W * 0.7, WIN_H * 0.28),
                            text='next: ', fgcolor='white',
                            size=TILE_SIZE * 0.7)
        self.font.render_to(self.app.screen, (WIN_W * 0.7, WIN_H * 0.72),
                            text='score: ', fgcolor='white',
                            size=TILE_SIZE * 0.7)
        self.font.render_to(self.app.screen, (WIN_W * 0.74, WIN_H * 0.82),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 0.7)

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetramino = Tetramino(self)
        self.next_tetramino = Tetramino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H -1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    def put_tetramino_blocks_in_array(self):
        for block in self.tetramino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetramino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_tetramino_landing(self):
        if self.tetramino.landing:
            self.speed_up = False
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.put_tetramino_blocks_in_array()
                self.next_tetramino.current = True
                self.tetramino = self.next_tetramino
                self.next_tetramino = Tetramino(self ,current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetramino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetramino.move(direction='right')
        elif pressed_key == pg.K_UP and self.tetramino.shape != 'O':
            self.tetramino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, (151, 222, 206),
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetramino.update()
            self.check_tetramino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
