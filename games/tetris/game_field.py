from .game_settings import *
import pygame as pg
from .game_objects import Tetromino
import pygame.freetype as ft
from database import change_user_scores, change_user_best_score, save_game_data
import csv


class Text:
    def __init__(self, main_window):
        self.main_window = main_window
        self.font = ft.Font(FONT_PATH)
        self.font_1 = pg.font.Font(FONT_PATH, 35)
        self.rect = pg.rect.Rect(FIELD_MARGIN_X + FIELD_MARGIN_X + FIELD_RES[0] + int(NXT_RES[0]/2), FIELD_MARGIN_Y, TILE_SIZE, TILE_SIZE)

    def draw(self):
        self.font.render_to(self.main_window.screen, (WINDOW_WIDTH*0.65, FIELD_MARGIN_Y*1.2),
                            text="NEXT", fgcolor="white",
                            size=TILE_SIZE*1.65)

        high_score = self.font_1.render("High-score", True, "white")
        high_score_rect = high_score.get_rect(center=(self.rect.x, self.rect.y+TILE_SIZE*10))
        self.main_window.screen.blit(high_score, high_score_rect)

        best_player = self.font_1.render(f"{self.main_window.data[0]}", True, "white")
        best_player_rect = best_player.get_rect(center=(self.rect.x, self.rect.y + TILE_SIZE * 11.5))
        self.main_window.screen.blit(best_player, best_player_rect)

        best_score = self.font_1.render(f"{self.main_window.data[1]}", True, "white")
        best_score_rect = best_score.get_rect(center=(self.rect.x, self.rect.y + TILE_SIZE * 13))
        self.main_window.screen.blit(best_score, best_score_rect)

        text_user_best_score = self.font_1.render("YOUR BEST SCORE", True, "white")
        text_user_best_score_rect = text_user_best_score.get_rect(center=(self.rect.x, self.rect.y + TILE_SIZE * 15))
        self.main_window.screen.blit(text_user_best_score, text_user_best_score_rect)

        user_best_score = self.font_1.render(f"{self.main_window.user_best_score}", True, "white")
        user_best_score_rect = user_best_score.get_rect(center=(self.rect.x, self.rect.y + TILE_SIZE * 16.5))
        self.main_window.screen.blit(user_best_score, user_best_score_rect)

        text_score = self.font_1.render("SCORE", True, "white")
        text_score_rect = text_score.get_rect(center=(self.rect.x, self.rect.y + TILE_SIZE * 18))
        self.main_window.screen.blit(text_score, text_score_rect)

        actual_score = self.font_1.render(f"{self.main_window.game_field.score}", True, "white")
        actual_score_rect = actual_score.get_rect(center=(self.rect.x, self.rect.y + TILE_SIZE * 19.5))
        self.main_window.screen.blit(actual_score, actual_score_rect)

        pg.draw.rect(self.main_window.screen, "blue", (FIELD_MARGIN_X + FIELD_MARGIN_X + FIELD_RES[0], FIELD_MARGIN_Y , *NXT_RES), 3)


class GameField:

    def __init__(self, game_window):
        self.game_window = game_window
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino_1 = Tetromino(self, que_pos=1)
        self.next_tetromino_2 = Tetromino(self, que_pos=2)
        self.next_tetromino_3 = Tetromino(self, que_pos=3)
        self.speed_up = False
        self.is_over = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 200, 3: 700, 4: 1500}

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.position.x), int(block.position.y)
            self.field_array[y][x] = block

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_HEIGHT+int(FIELD_OFFSET_Y)-1

        for y in range(FIELD_HEIGHT + int(FIELD_OFFSET_Y) -1, int(FIELD_OFFSET_Y), -1):
            for x in range(FIELD_WIDTH+FIELD_OFFSET_X):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[row][x]:
                    self.field_array[row][x].position = VECTOR(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_WIDTH:
                row -= 1
            else:
                for x in range(int(FIELD_OFFSET_X), int(FIELD_WIDTH+FIELD_OFFSET_X)):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                    #zrobic sprawdzanie w góre 
                    if sum(map(bool, self.field_array[y+1])) == FIELD_WIDTH:
                        self.field_array[row+1][x].alive = False
                        self.field_array[row+1][x] = 0

                self.full_lines += 1

    def get_field_array(self):
        return [[0 for x in range(int(FIELD_WIDTH+FIELD_MARGIN_X))] for y in range(int(FIELD_HEIGHT+FIELD_MARGIN_Y))]

    def is_game_over(self):
        if self.tetromino.blocks[3].position.y == INIT_POS_OFFSET[1]+1:
            if self.score > self.game_window.user_best_score:
                change_user_best_score(self.game_window.username, "tetris", self.score)
            if self.score > int(self.game_window.data[1]):
                filename = "top_results.csv"
                file = open(filename, "r")
                reader = csv.reader(file)
                rows = list(reader)
                rows[1][1] = self.game_window.username
                rows[1][2] = self.score
                file.close()
                file = open(filename, "w", newline='')
                writer = csv.writer(file)
                writer.writerows(rows)
                file.close()
            change_user_scores(self.game_window.username, "tetris", self.score)
            save_game_data(self.game_window.username, "tetris", self.score)
            self.is_over = True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
                self.is_game_over()
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino_1.que_pos = 0
                self.next_tetromino_2.que_pos = 1
                self.next_tetromino_3.que_pos = 2
                self.tetromino = self.next_tetromino_1
                self.next_tetromino_1 = self.next_tetromino_2
                self.next_tetromino_2 = self.next_tetromino_3
                self.next_tetromino_3 = Tetromino(self, que_pos=3)

    def draw_grid(self):
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                pg.draw.rect(self.game_window.screen, "black",
                             (x*TILE_SIZE+FIELD_MARGIN_X, y*TILE_SIZE+FIELD_MARGIN_Y, TILE_SIZE, TILE_SIZE), 1)

        pg.draw.rect(self.game_window.screen, "blue",
                             (FIELD_MARGIN_X, FIELD_MARGIN_Y, FIELD_RES[0], FIELD_RES[1]), 5)

    def update(self):
        trigger = [self.game_window.animation_trigger, self.game_window.fast_animation_trigger][self.speed_up]
        if trigger:
            self.tetromino.update()
            self.check_full_lines()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.game_window.screen)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()

