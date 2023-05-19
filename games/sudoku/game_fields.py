from .game_settings import *
import time
import csv
from database import save_game_data, load_sudoku
import random


class Text:
    def __init__(self, main_window):
        self.main_window = main_window
        self.box = 0
        self.time = 0
        self.mistakes = 0
        self.minutes = 0
        self.seconds = 0
        self.best_time = self.main_window.data[1]
        self.best_time_username = self.main_window.data[0]

    def start_time(self):
        if self.main_window.window == "game":
            self.time = time.time()

    def timer(self):

        current_time = time.time()-self.time
        self.seconds = int(current_time % 60)
        self.minutes = int(current_time // 60)

    def draw(self):
        text = pg.font.SysFont("ARIAL", 30).render("Best time", True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.08))

        text = pg.font.SysFont("ARIAL", 30).render(self.best_time, True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH * 0.83, WINDOW_HEIGHT * 0.2))

        text = pg.font.SysFont("ARIAL", 30).render("{}".format(self.best_time_username), True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH * 0.62, WINDOW_HEIGHT * 0.2))

        text = pg.font.SysFont("ARIAL", 30).render("Your best time", True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH * 0.65, WINDOW_HEIGHT * 0.3))

        text = pg.font.SysFont("ARIAL", 30).render(self.main_window.user_best_score, True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH * 0.73, WINDOW_HEIGHT * 0.4))

        text = pg.font.SysFont("ARIAL", 30).render("Current time {:02d}:{:02d}".format(self.minutes, self.seconds), True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH*0.6, WINDOW_HEIGHT*0.65))

        text = pg.font.SysFont("ARIAL", 30).render(f"Mistakes: {self.mistakes}/3", True, "black")
        self.main_window.screen.blit(text, (WINDOW_WIDTH * 0.65, WINDOW_HEIGHT * 0.5))

        text = pg.font.SysFont("ARIAL", 30).render("New sudoku", True, "black")
        self.box = pg.Rect((WINDOW_WIDTH * 0.64, WINDOW_HEIGHT * 0.79, TILE_SIZE*5, TILE_SIZE*1.5))
        text_rect = text.get_rect(center=(self.box.x + TILE_SIZE*2.5, self.box.y+TILE_SIZE*0.75))
        pg.draw.rect(self.main_window.screen, (227, 239, 255), self.box)
        pg.draw.rect(self.main_window.screen, "black", self.box, 2)
        self.main_window.screen.blit(text, text_rect)

    def update(self):
        self.timer()


class SudokuPuzzle:

    def __init__(self, game_window):
        self.game_window = game_window
        self.solution_length = 0
        self.is_solved = False
        self.is_game_over = False
        self.solution = []
        self.boxes = []
        self.digits = []
        self.filled_boxes = []
        self.list_to_fill = []
        self.solution = []
        self.prepare_boxes()
        self.prepare_sudoku()
        self.fill_boxes()

    def change_top_result(self):
        filename = "top_results.csv"
        file = open(filename, "r")
        reader = csv.reader(file)
        rows = list(reader)
        rows[2][1] = self.game_window.username
        rows[2][2] = "{:02d}:{:02d}".format(self.game_window.answer.minutes, self.game_window.answer.seconds)
        file.close()
        file = open(filename, "w", newline='')
        writer = csv.writer(file)
        writer.writerows(rows)
        file.close()

    def draw_grid(self):

        for row in range(0, ROWS, 3):
            for column in range(0, COLUMNS, 3):
                pg.draw.rect(self.game_window.screen, "black",
                             (row * TILE_SIZE + MARGIN_X, column * TILE_SIZE + MARGIN_Y, TILE_SIZE*3, TILE_SIZE*3), 3)

        pg.draw.rect(self.game_window.screen, "black",
                     (MARGIN_X,MARGIN_Y, TILE_SIZE * ROWS, TILE_SIZE * COLUMNS), 5)

    def prepare_boxes(self):

        for row in range(ROWS):
            for column in range(COLUMNS):
                x = (row * TILE_SIZE + MARGIN_X)
                y = (column * TILE_SIZE + MARGIN_Y)
                box = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.boxes.append(box)

    def fill_boxes(self):

        for index, box in enumerate(self.boxes):
            digit = self.digits[index]
            self.filled_boxes.append([box, digit])

    def draw_filled_boxes(self):

        for box, digit in self.filled_boxes:
            digit_render = pg.font.SysFont("ARIAL", 30).render(digit, True, "black")
            digit_rect = digit_render.get_rect(center=(box.x + TILE_SIZE * 0.5, box.y + TILE_SIZE * 0.5))
            self.game_window.screen.blit(digit_render, digit_rect)
            pg.draw.rect(self.game_window.screen, "light grey", box, 1)

    def prepare_sudoku(self):

        random_number = random.randint(1, 1000)

        puzzle, solution = load_sudoku(random_number)
        self.digits = [char if char != "0" else "" for char in puzzle]

        solution1 = [char for char in solution]

        self.solution_length = puzzle.count("0")

        self.solution = [solution1[i:i + 9] for i in range(0, 81, 9)]

    def insert_digit(self, box, digit):

        if digit != "" and self.solution[int(box.x/TILE_SIZE - 1)][int(box.y/TILE_SIZE - 1)] != digit:
            self.game_window.text.mistakes += 1

        if self.list_to_fill:
            for item in self.list_to_fill:
                if item[0] == box:
                    if digit == "":
                        return
                    item[1] = digit
                    return
            self.list_to_fill.append([box, digit])
        else:
            self.list_to_fill.append([box, digit])

    def delete_digit(self, box, digit):

        if self.list_to_fill:
            for item in self.list_to_fill:
                if item[0] == box:
                    item[1] = digit
                    return

    def check_is_solved(self):
        if len(self.list_to_fill) == self.solution_length:
            solved = True
            for box, digit in self.list_to_fill:
                if digit != self.solution[int(box.x/TILE_SIZE - 1)][int(box.y/TILE_SIZE - 1)]:
                    solved = False
            self.is_solved = solved
            if solved:
                save_game_data(self.game_window.username, "sudoku", 25)

    def drawing(self):

        for box, digit in self.list_to_fill:
            pg.draw.rect(self.game_window.screen, "white", box)
            digit_render = pg.font.SysFont("ARIAL", 30).render(digit, True, "blue")
            digit_rect = digit_render.get_rect(center=(box.x + TILE_SIZE * 0.5, box.y + TILE_SIZE * 0.5))
            self.game_window.screen.blit(digit_render, digit_rect)
            pg.draw.rect(self.game_window.screen, "light grey", box, 1)

            if box == self.game_window.current_box:
                pg.draw.rect(self.game_window.screen, "light blue", box)
                digit_render = pg.font.SysFont("ARIAL", 30).render(digit, True, "blue")
                digit_rect = digit_render.get_rect(center=(box.x + TILE_SIZE * 0.5, box.y + TILE_SIZE * 0.5))
                self.game_window.screen.blit(digit_render, digit_rect)
                pg.draw.rect(self.game_window.screen, "light grey", box, 1)

            if digit != "" and self.solution[int(box.x/TILE_SIZE - 1)][int(box.y/TILE_SIZE - 1)] != digit:
                if box == self.game_window.current_box:
                    pg.draw.rect(self.game_window.screen, "light blue", box)
                else:
                    pg.draw.rect(self.game_window.screen, "white", box)
                digit_render = pg.font.SysFont("ARIAL", 30).render(digit, True, "red")
                digit_rect = digit_render.get_rect(center=(box.x + TILE_SIZE * 0.5, box.y + TILE_SIZE * 0.5))
                self.game_window.screen.blit(digit_render, digit_rect)
                pg.draw.rect(self.game_window.screen, "light grey", box, 1)

    def draw(self):
        self.draw_filled_boxes()
        self.drawing()
        self.draw_grid()

    def check_is_game_over(self):
        if self.game_window.text.mistakes == 3:
            self.is_game_over = True
            save_game_data(self.game_window.username, "sudoku", 0)

    def update(self):
        self.check_is_game_over()
        self.check_is_solved()

