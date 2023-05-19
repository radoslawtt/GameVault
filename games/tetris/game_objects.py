from .game_settings import *
import pygame as pg
import random


class Block(pg.sprite.Sprite):

    def __init__(self, tetromino, position):
        super().__init__(tetromino.game_field.sprite_group)
        self.alive = True
        self.tetromino = tetromino
        self.image = tetromino.image
        self.position = VECTOR(position)+INIT_POS_OFFSET
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position*TILE_SIZE
        self.position_1 = VECTOR(position) + NEXT_POS_OFFSET_1
        self.position_2 = VECTOR(position) + NEXT_POS_OFFSET_2
        self.position_3 = VECTOR(position) + NEXT_POS_OFFSET_3

    def set_rect_position(self):
        position = [self.position, self.position_1, self.position_2, self.position_3][self.tetromino.que_pos]
        if self.tetromino.que_pos == 0:
            self.rect.topleft = position*TILE_SIZE
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pg.transform.scale(self.image, (TILE_SIZE/2, TILE_SIZE/2))
            self.rect.topleft = position * TILE_SIZE/2

    def is_alive(self):
        if not self.alive:
            self.kill()

    def update(self):
        self.is_alive()
        self.set_rect_position()

    def is_collide(self, position):
        x, y = int(position.x), int(position.y)
        if FIELD_OFFSET_X<=x<FIELD_WIDTH+FIELD_OFFSET_X and FIELD_OFFSET_Y<=y < FIELD_HEIGHT+FIELD_OFFSET_Y and (y<0 or not self.tetromino.game_field.field_array[y][x]):
            return False
        return True

    def rotate(self, pivot_position):
        translated = self.position - pivot_position
        rotated = translated.rotate(90)
        return rotated + pivot_position


class Tetromino:
    def __init__(self, game_field, que_pos = 0):
        self.game_field = game_field
        self.que_pos = que_pos
        self.image = random.choice(self.game_field.game_window.images)
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.landing = False
        self.blocks = [Block(self, position) for position in TETROMINOES[self.shape]]


    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def rotate(self):
        pivot_position = self.blocks[0].position
        if self.shape != "O":
            new_block_positions = [block.rotate(pivot_position) for block in self.blocks]

            if not self.is_collide(new_block_positions):
                for i, block in enumerate(self.blocks):
                    block.position = new_block_positions[i]

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.position + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)
        if not is_collide:
            for block in self.blocks:
                block.position += move_direction
        elif direction == "down":
            self.landing = True

    def update(self):
        self.move(direction="down")
