import csv
from .game_settings import *
from .game_field import GameField, Text
from .info_windows import StartWindow, GameOverWindow, AboutGame


class MainWindow:

    def __init__(self, username, window):
        pg.init()
        pg.display.set_caption("Snake")
        self.tkinter_window = window
        self.username = username
        self.screen = pg.display.set_mode(WINDOW_RES)
        self.clock = pg.time.Clock()
        self.game_field = GameField(self)
        self.data = self.load_data()
        self.window = "menu"
        self.text = Text(self)
        self.start_window = StartWindow(self)
        self.about_game = AboutGame(self)
        self.game_over_window = GameOverWindow(self)

    def load_data(self):
        file = open("top_results.csv", "r")
        reader = csv.reader(file)
        header = next(reader)
        first_row = next(reader)
        second_row = next(reader)
        third_row = next(reader)
        file.close()
        return third_row[1:3]

    def update(self):
        pg.display.flip()
        if not self.game_field.is_over:
            self.game_field.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=WINDOW_BG)
        if self.window == "game":
            self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
            self.game_field.draw()
            self.text.draw()
        if self.window == "about game":
            self.about_game.draw()
        if self.window == "menu":
            self.start_window.draw()
        if self.game_field.is_over:
            self.game_over_window.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.tkinter_window.deiconify()
                pg.quit()
                self.tkinter_window.mainloop()
            if event.type == pg.KEYDOWN:
                self.game_field.control(pressed_key=event.key)

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

            if self.game_field.is_over:
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.game_over_window.play_again.collidepoint(clicked_pos):
                        self.game_field.__init__(self)
                        self.text.__init__(self)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()

