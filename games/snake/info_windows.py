from .game_settings import *


class StartWindow:

    def __init__(self, game_window):
        self.game_window = game_window
        self.play_again = pg.Rect(WINDOW_WIDTH*0.4, WINDOW_HEIGHT*0.3, TILE_SIZE*6, TILE_SIZE*2)
        self.about_game = pg.Rect(WINDOW_WIDTH*0.4, WINDOW_HEIGHT*0.5, TILE_SIZE*6, TILE_SIZE*2)

    def draw(self):
        text = pg.font.SysFont("Arial", 30).render("Play game", True, "black")
        text_rect = text.get_rect(center=(self.play_again.x + TILE_SIZE*3, self.play_again.y + TILE_SIZE))
        pg.draw.rect(self.game_window.screen, (204, 215, 200), self.play_again)
        pg.draw.rect(self.game_window.screen, "black", self.play_again, 1)
        self.game_window.screen.blit(text, text_rect)

        text_1 = pg.font.SysFont("Arial", 30).render("About game", True, "black")
        text_1_rect = text_1.get_rect(center=(self.about_game.x + TILE_SIZE * 3, self.about_game.y + TILE_SIZE))
        pg.draw.rect(self.game_window.screen,  (204, 215, 200), self.about_game)
        pg.draw.rect(self.game_window.screen, "black", self.about_game, 1)
        self.game_window.screen.blit(text_1, text_1_rect)


class GameOverWindow:

    def __init__(self, game_window):
        self.game_window = game_window
        self.play_again = pg.Rect(WINDOW_WIDTH*0.4, WINDOW_HEIGHT*0.45, TILE_SIZE*5, TILE_SIZE*2)

    def draw(self):
        text = pg.font.SysFont("Arial", 30).render("Play again", True, "black")
        text_rect = text.get_rect(center=(self.play_again.x + TILE_SIZE*2.5, self.play_again.y + TILE_SIZE))
        pg.draw.rect(self.game_window.screen, (204, 215, 200), self.play_again)
        pg.draw.rect(self.game_window.screen, "black", self.play_again, 1)
        self.game_window.screen.blit(text, text_rect)


class AboutGame:

    def __init__(self, main_window):
        self.main_window = main_window
        self.info = INFO
        self.back_button = pg.Rect(WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.3, TILE_SIZE * 5, TILE_SIZE * 2)

    def draw(self):

        for line in INFO:
            text = pg.font.SysFont("Arial", 15).render(line, True, "black")
            text_rect = text.get_rect(
                center=(WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.1 + TILE_SIZE * INFO.index(line)))
            self.main_window.screen.blit(text, text_rect)

        text_1 = pg.font.SysFont("Arial", 30).render("Back", True, "black")
        text_1_rect = text_1.get_rect(center=(self.back_button.x + TILE_SIZE * 2.5, self.back_button.y + TILE_SIZE))
        pg.draw.rect(self.main_window.screen, (204, 215, 200), self.back_button)
        pg.draw.rect(self.main_window.screen, "black", self.back_button, 1)
        self.main_window.screen.blit(text_1, text_1_rect)

