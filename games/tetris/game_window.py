from .game_settings import *
from .game_field import GameField, Text
from .info_window import StartWindow, GameOverWindow, AboutGame
from database import load_user_best_score
import csv
import pathlib


class GameWindow:

    def __init__(self, username, window):
        pg.init()
        pg.display.set_caption("Tetris")
        self.tkinter_window = window
        self.username = username
        self.screen = pg.display.set_mode(WINDOW_RES)
        self.clock = pg.time.Clock()
        self.window = "menu"
        self.start_window = StartWindow(self)
        self.about_game = AboutGame(self)
        self.game_over_window = GameOverWindow(self)
        self.set_timer()
        self.images = self.load_images()
        self.game_field = GameField(self)
        self.text = Text(self)
        self.data = self.load_data()
        self.user_best_score = load_user_best_score(self.username, "tetris")

    def load_data(self):
        file = open("top_results.csv", "r")
        reader = csv.reader(file)
        header = next(reader)
        first_row = next(reader)
        file.close()
        return first_row[1:3]

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob("*.png") if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.animation_trigger = False
        self.fast_animation_trigger = False
        pg.time.set_timer(self.user_event, ANIMATION_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIMATION_TIME_INTERVAL)

    def update(self):
        if self.window == "game":
            self.game_field.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=WINDOW_BG)
        if self.window == "game":
            self.screen.fill(color=FIELD_COLOR, rect=(FIELD_MARGIN_X, FIELD_MARGIN_Y, *FIELD_RES))
            self.screen.fill(color=FIELD_COLOR, rect=(FIELD_MARGIN_X + FIELD_MARGIN_X + FIELD_RES[0], FIELD_MARGIN_Y , *NXT_RES))
            self.game_field.draw()
            self.text.draw()

        if self.window == "menu":
            self.start_window.draw()
        if self.window == "about game":
            self.about_game.draw()
        if self.game_field.is_over:
            self.game_over_window.draw()

        pg.display.flip()

    def check_events(self):
        self.animation_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event. key == pg.K_ESCAPE):
                    self.tkinter_window.deiconify()
                    pg.quit()
                    self.tkinter_window.mainloop()

            if self.window == "game":
                if not self.game_field.is_over:
                    if event.type == pg.KEYDOWN:
                        self.game_field.control(pressed_key=event.key)
                    elif event.type == self.user_event:
                        self.animation_trigger = True
                    elif event.type == self.fast_user_event:
                        self.fast_animation_trigger = True

                elif event.type == pg.MOUSEBUTTONDOWN and self.game_field.is_over:
                    clicked_pos = event.pos
                    if self.game_over_window.play_again.collidepoint(clicked_pos):
                        self.game_field.__init__(self)

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

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
