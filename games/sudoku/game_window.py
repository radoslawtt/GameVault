from .game_settings import *
from .game_fields import SudokuPuzzle, Text
from .info_windows import GameOverWindow, StartWindow, AboutGame, GameWonWindow
from database import load_user_best_score, change_user_scores, change_user_best_score
import csv


class MainWindow:

    def __init__(self, username, window):
        pg.init()
        pg.display.set_caption("Sudoku")
        self.tkinter_window = window
        self.username = username
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(WINDOW_RES)
        self.data = self.load_data()
        self.window = "menu"
        self.start_window = StartWindow(self)
        self.sudoku_puzzle = SudokuPuzzle(self)
        self.current_box = ""
        self.text = Text(self)
        self.about_game = AboutGame(self)
        self.game_over_window = GameOverWindow(self)
        self.game_won_window = GameWonWindow(self)
        self.user_best_score = load_user_best_score(self.username, "sudoku")

    def load_data(self):
        file = open("top_results.csv", "r")
        reader = csv.reader(file)
        header = next(reader)
        first_row = next(reader)
        second_row = next(reader)
        file.close()
        return second_row[1:3]

    def draw(self):

        self.screen.fill(color=WINDOW_BG)
        if self.window == "game":
            self.screen.fill(color=FIELD_COLOR, rect=(MARGIN_X, MARGIN_Y, *FIELD_RES))
            self.sudoku_puzzle.draw()
            self.text.draw()
        if self.window == "menu":
            self.start_window.draw()
        if self.window == "info":
            self.about_game.draw()
        if self.sudoku_puzzle.is_game_over:
            self.game_over_window.draw()
        if self.sudoku_puzzle.is_solved:
            self.game_won_window.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.tkinter_window.deiconify()
                pg.quit()
                self.tkinter_window.mainloop()
            if self.window == "game":

                if not self.sudoku_puzzle.is_game_over:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        clicked_pos = event.pos
                        if self.text.box.collidepoint(clicked_pos):
                            self.sudoku_puzzle.__init__(self)
                            self.text.__init__(self)
                            self.text.start_time()
                        for box, digit in self.sudoku_puzzle.filled_boxes:
                            if box.collidepoint(clicked_pos) and digit == "":
                                self.current_box = box
                                self.sudoku_puzzle.insert_digit(self.current_box, digit)

                    elif event.type == pg.KEYDOWN:
                        if event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                            digit = chr(event.key)
                            self.sudoku_puzzle.insert_digit(self.current_box, digit)
                        if event.key == pg.K_c:
                            self.sudoku_puzzle.delete_digit(self.current_box, "")

            if event.type == pg.MOUSEBUTTONDOWN and self.sudoku_puzzle.is_game_over:
                clicked_pos = event.pos
                if self.game_over_window.play_again.collidepoint(clicked_pos):
                    self.sudoku_puzzle.__init__(self)
                    self.text.__init__(self)
                    self.text.start_time()

            if self.sudoku_puzzle.is_solved:
                change_user_scores(self.username, "sudoku", 25)
                if self.data[1] > "{:02d}:{:02d}".format(self.text.minutes, self.text.seconds):
                    self.sudoku_puzzle.change_top_result()
                if self.user_best_score > "{:02d}:{:02d}".format(self.text.minutes, self.text.seconds) or self.user_best_score == "00:00":
                    change_user_best_score(self.username, "sudoku", "{:02d}:{:02d}".format(self.text.minutes, self.text.seconds))
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.game_won_window.next_sudoku.collidepoint(clicked_pos):
                        self.sudoku_puzzle.__init__(self)
                        self.text.__init__(self)
                        self.text.start_time()

            if self.window == "menu":
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.start_window.play_again.collidepoint(clicked_pos):
                        self.window = "game"
                        self.text.start_time()
                    if self.start_window.about_game.collidepoint(clicked_pos):
                        self.window = "info"

            if self.window == "info":
                if event.type == pg.MOUSEBUTTONDOWN:
                    clicked_pos = event.pos
                    if self.about_game.back_button.collidepoint(clicked_pos):
                        self.window = "menu"

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        if not self.sudoku_puzzle.is_game_over and self.window == "game" and not self.sudoku_puzzle.is_solved:
            self.text.update()
            self.sudoku_puzzle.update()

    def run(self):
        while True:
            self.update()
            self.draw()
            self.check_event()

