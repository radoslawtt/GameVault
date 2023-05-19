import pygame as pg
import pygame.font
from database import load_word
from .game_settings import *


class Buttons:

    def __init__(self, main_window):
        self.main_window = main_window
        self.size = BUTTON_SIZE
        self.boxes = []
        self.buttons = []
        self.create_boxes()
        self.fill_boxes()

    def create_boxes(self):
        for row in range(ROWS_OF_BUTTONS):
            for col in range(COLUMNS_OF_BUTTONS):
                x = ((col*BUTTON_GAP) + BUTTON_GAP) + (self.size*col)
                y = ((row * BUTTON_GAP) + BUTTON_GAP) + (self.size * row) + WINDOW_HEIGHT*0.5
                box = pg.Rect(x, y, self.size, self.size)
                self.boxes.append(box)

    def fill_boxes(self):
        for index, box in enumerate(self.boxes):
            letter = chr(65+index)
            button = [box, letter]
            self.buttons.append(button)

    def draw(self):
        for box, letter in self.buttons:
            pg.draw.rect(self.main_window.screen, (101, 104, 112), box)
            btn_text = pygame.font.SysFont("ARIAL", 20).render(letter, True, "black")
            btn_rect = btn_text.get_rect(center=(box.x + 16, box.y +15))
            self.main_window.screen.blit(btn_text, btn_rect)
            pg.draw.rect(self.main_window.screen, "black", box, 2)


class Hangman:

    def __init__(self, game_window):
        self.game_window = game_window
        self.status = 0
        self.images = self.game_window.hangman_images

    def draw(self):
        self.game_window.screen.blit(self.images[self.status], (WINDOW_WIDTH*0.45, 0))


class Word:

    def __init__(self, game_window):
        self.game_window = game_window
        self.answer = ""
        self.guessed = []
        self.word = load_word()
        self.check_letter()

    def check_letter(self):
        self.answer = ""
        for letter in self.word:
            if letter in self.guessed:
                self.answer += f"{letter}"
            else:
                self.answer += "_ "

    def is_solved(self):
        if self.answer == self.word:
            return True

    def draw(self):
        textt = pygame.font.SysFont("ARIAL", 30).render(self.answer, True, "black")
        textt_rect = textt.get_rect(center=(WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.35))
        self.game_window.screen.blit(textt, textt_rect)


class Hearts:

    def __init__(self, game_window):
        self.game_window = game_window
        self.status = 2
        self.images = self.game_window.heart_images

    def draw(self):
        self.game_window.screen.blit(self.images[self.status], (WINDOW_WIDTH * 0.85, 0))


class Text:
    def __init__(self, main_window):
        self.main_window = main_window
        self.frame_1 = pg.Rect(WINDOW_WIDTH*0.15, WINDOW_HEIGHT*0.7, 1, 1)
        self.frame_2 = pg.Rect(WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.7, 1, 1)
        self.best_result = self.main_window.data[1]
        self.best_result_username = self.main_window.data[0]

    def draw(self):
        text_best_result = pg.font.SysFont("ARIAL", 30).render("Best result", True, "black")
        text_best_result_rect = text_best_result.get_rect(center=(self.frame_1.x+TILE_SIZE, self.frame_1.y))
        self.main_window.screen.blit(text_best_result, text_best_result_rect)

        value_best_result = pg.font.SysFont("ARIAL", 30).render(self.best_result, True, "black")
        value_best_result_rect = text_best_result.get_rect(center=(self.frame_1.x+TILE_SIZE*5, self.frame_1.y+TILE_SIZE*2))
        self.main_window.screen.blit(value_best_result, value_best_result_rect)

        text_best_result_username = pg.font.SysFont("ARIAL", 30).render(self.best_result_username, True, "black")
        text_best_result_username_rect = text_best_result_username.get_rect(center=(self.frame_1.x-TILE_SIZE, self.frame_1.y+TILE_SIZE*2))
        self.main_window.screen.blit(text_best_result_username, text_best_result_username_rect)

        text_your_best_result = pg.font.SysFont("ARIAL", 30).render("Your best result", True, "black")
        text_your_best_result_rect = text_your_best_result.get_rect(center=(self.frame_1.x + TILE_SIZE, self.frame_1.y + TILE_SIZE * 4))
        self.main_window.screen.blit(text_your_best_result, text_your_best_result_rect)

        value_your_best_result = pg.font.SysFont("ARIAL", 30).render(f"{self.main_window.user_best_score}", True, "black")
        value_your_best_result_rect = value_your_best_result.get_rect(center=(self.frame_1.x + TILE_SIZE, self.frame_1.y + TILE_SIZE * 6))
        self.main_window.screen.blit(value_your_best_result, value_your_best_result_rect)

        current_result = pg.font.SysFont("ARIAL", 30).render("Current score", True,"black")
        current_result_rect = current_result.get_rect(center=(self.frame_2.x + TILE_SIZE, self.frame_2.y))
        self.main_window.screen.blit(current_result, current_result_rect)

        value_current_result = pg.font.SysFont("ARIAL", 30).render(f"{self.main_window.current_score}", True, "black")
        value_current_result_rect = value_current_result.get_rect(center=(self.frame_2.x + TILE_SIZE, self.frame_2.y+TILE_SIZE*2))
        self.main_window.screen.blit(value_current_result, value_current_result_rect)

