import pygame as pg
from .game_objects import Buttons, Hangman, Word, Hearts, Text
from .info_window import GameOverWindow, StartWindow, AboutGame
from .game_settings import *
import pathlib
from database import save_game_data, load_user_best_score, change_user_best_score, change_user_scores
import csv


class GameWindow:

    def __init__(self, username, window):
        pg.init()
        pg.display.set_caption("Hangman")
        self.tkinter_window = window
        self.username = username
        self.screen = pg.display.set_mode(WINDOW_RES)
        self.clock = pg.time.Clock()
        self.hangman_images = self.load_hangman_images()
        self.heart_images = self.load_heart_images()
        self.buttons = Buttons(self)
        self.word = Word(self)
        self.hangman = Hangman(self)
        self.hearts = Hearts(self)
        self.start_window = StartWindow(self)
        self.about_game = AboutGame(self)
        self.game_over_window = GameOverWindow(self)
        self.window = "menu"
        self.is_game_over = False
        self.data = self.load_data()
        self.user_best_score = load_user_best_score(self.username, "hangman")
        self.text = Text(self)
        self.current_score = 0

    def load_data(self):
        file = open("top_results.csv", "r")
        reader = csv.reader(file)
        header = next(reader)
        first_row = next(reader)
        second_row = next(reader)
        third_row = next(reader)
        fourth_row = next(reader)
        file.close()
        return fourth_row[1:3]

    def change_top_result(self):
        filename = "top_results.csv"
        file = open(filename, "r")
        reader = csv.reader(file)
        rows = list(reader)
        rows[4][1] = self.username
        rows[4][2] = self.current_score
        file.close()
        file = open(filename, "w", newline='')
        writer = csv.writer(file)
        writer.writerows(rows)
        file.close()

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=WINDOW_BG)
        if self.window == "about game":
            self.about_game.draw()
        if self.window == "menu":
            self.start_window.draw()
        if self.window == "game":
            self.hangman.draw()
            self.buttons.draw()
            self.word.draw()
            self.hearts.draw()
            self.text.draw()
        if self.is_game_over:
            self.game_over_window.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.tkinter_window.deiconify()
                pg.quit()
                self.tkinter_window.mainloop()

            if self.window == "game" and not self.is_game_over:
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    for button, letter in self.buttons.buttons:
                        if button.collidepoint(clicked_pos):

                            self.word.guessed.append(letter)
                            self.word.check_letter()
                            self.buttons.buttons.remove([button, letter])

                            if letter not in self.word.word:
                                self.hangman.status += 1

                            if self.hangman.status == 6:
                                self.hearts.status -= 1
                                self.hangman.__init__(self)
                                self.word.__init__(self)
                                self.buttons.__init__(self)
                            if self.hearts.status == -1:
                                self.is_game_over = True
                                change_user_scores(self.username, "hangman", self.current_score)
                                save_game_data(self.username, "hangman", self.current_score)
                                if self.current_score > int(self.data[1]):
                                    self.change_top_result()
                                if self.current_score > self.user_best_score:
                                    change_user_best_score(self.username, "hangman", self.current_score)
                            if self.word.is_solved():
                                self.current_score += 10
                                self.hangman.__init__(self)
                                self.word.__init__(self)
                                self.buttons.__init__(self)

            if self.window == "menu":
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.start_window.play_again.collidepoint(clicked_pos):
                        self.window = "game"
                    if self.start_window.about_game.collidepoint(clicked_pos):
                        self.window = "about game"

            if self.window == "about game":
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.about_game.back_button.collidepoint(clicked_pos):
                        self.window = "menu"

            if self.is_game_over:
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.game_over_window.play_again.collidepoint(clicked_pos):
                        self.hangman.__init__(self)
                        self.word.__init__(self)
                        self.buttons.__init__(self)
                        self.hearts.__init__(self)
                        self.current_score = 0
                        self.is_game_over = False

    def load_hangman_images(self):
        files = [item for item in pathlib.Path(MAN_DIR_PATH).rglob("*.png") if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        return images

    def load_heart_images(self):
        files = [item for item in pathlib.Path(HEART_DIR_PATH).rglob("*.png") if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        return images

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()
