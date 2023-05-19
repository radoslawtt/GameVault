import csv
from .game_objects import Snake, Food
from .game_settings import *
from database import load_user_best_score, save_game_data, change_user_best_score, change_user_scores


class GameField:

    def __init__(self, game_window):
        self.game_window = game_window
        self.new_game()
        self.is_over = False

    def new_game(self):
        self.snake = Snake(self)
        self.food = Food(self)

    def change_top_result(self):
        filename = "top_results.csv"
        file = open(filename, "r")
        reader = csv.reader(file)
        rows = list(reader)
        rows[3][1] = self.game_window.username
        rows[3][2] = self.game_window.text.current_score
        file.close()
        file = open(filename, "w", newline='')
        writer = csv.writer(file)
        writer.writerows(rows)
        file.close()

    def chceck_food(self):
        if self.snake.rect.center == self.food.rect.center:
            self.food.rect.center = self.food.get_random_position()
            self.snake.length +=1
            self.game_window.text.current_score += 10

    def check_selfeating(self):
        if len(self.snake.segments) != len(set(segment.center for segment in self.snake.segments)):
            self.is_over = True
            save_game_data(self.game_window.username, "snake", self.game_window.text.current_score)
            change_user_scores(self.game_window.username, "snake", self.game_window.text.current_score)
            if self.game_window.text.current_score > self.game_window.text.user_best_score:
                change_user_best_score(self.game_window.username, "snake", self.game_window.text.current_score)
            if self.game_window.text.current_score > int(self.game_window.text.best_score):
                self.change_top_result()

    def collide_borders(self):
        if self.snake.rect.left < 0 or self.snake.rect.right > FIELD_WIDTH*TILE_SIZE:
            self.is_over = True
            save_game_data(self.game_window.username, "snake", self.game_window.text.current_score)
            change_user_scores(self.game_window.username, "snake", self.game_window.text.current_score)
            if self.game_window.text.current_score > self.game_window.text.user_best_score:
                change_user_best_score(self.game_window.username, "snake", self.game_window.text.current_score)
            if self.game_window.text.current_score > int(self.game_window.text.best_score):
                self.change_top_result()

        if self.snake.rect.top <0 or self.snake.rect.bottom > FIELD_HEIGHT*TILE_SIZE:
            self.is_over = True
            save_game_data(self.game_window.username, "snake", self.game_window.text.current_score)
            change_user_scores(self.game_window.username, "snake", self.game_window.text.current_score)
            if self.game_window.text.current_score > self.game_window.text.user_best_score:
                change_user_best_score(self.game_window.username, "snake", self.game_window.text.current_score)
            if self.game_window.text.current_score > int(self.game_window.text.best_score):
                self.change_top_result()

    def update(self):
        self.check_selfeating()
        self.collide_borders()
        self.chceck_food()
        self.snake.update()
        self.draw()

    def draw_grid(self):
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                pg.draw.rect(self.game_window.screen, "black",
                             (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def draw(self):
        self.draw_grid()
        self.snake.draw()
        self.food.draw()

    def control(self, pressed_key):
        if pressed_key == pg.K_UP and self.snake.directions[pg.K_UP]:
            self.snake.direction = VECTOR(0, -self.snake.size)
            self.snake.directions = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}

        if pressed_key == pg.K_DOWN and self.snake.directions[pg.K_DOWN]:
            self.snake.direction = VECTOR(0, self.snake.size)
            self.snake.directions = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

        if pressed_key == pg.K_RIGHT and self.snake.directions[pg.K_RIGHT]:
            self.snake.direction = VECTOR(self.snake.size, 0)
            self.snake.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

        if pressed_key == pg.K_LEFT and self.snake.directions[pg.K_LEFT]:
            self.snake.direction = VECTOR(-self.snake.size, 0)
            self.snake.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}


class Text:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_score = 0
        self.user_best_score = load_user_best_score(self.main_window.username, "snake")
        self.best_score = self.main_window.data[1]
        self.best_score_username = self.main_window.data[0]

    def draw(self):
        text = pg.font.SysFont("ARIAL", 30).render("BEST SCORE", True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH * 0.8, WINDOW_HEIGHT * 0.08)))

        text = pg.font.SysFont("ARIAL", 30).render(f"{self.best_score}", True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH * 0.9, WINDOW_HEIGHT * 0.15)))

        text = pg.font.SysFont("ARIAL", 30).render("{}".format(self.best_score_username), True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH * 0.70, WINDOW_HEIGHT * 0.15)))

        text = pg.font.SysFont("ARIAL", 30).render("YOUR BEST SCORE", True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH * 0.8, WINDOW_HEIGHT * 0.25)))

        text = pg.font.SysFont("ARIAL", 30).render(f"{self.user_best_score}", True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH * 0.8, WINDOW_HEIGHT * 0.3)))

        text = pg.font.SysFont("ARIAL", 30).render("CURRENT SCORE", True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.35)))

        text = pg.font.SysFont("ARIAL", 30).render(f"{self.current_score}", True, "black")
        self.main_window.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH * 0.8, WINDOW_HEIGHT * 0.4)))

