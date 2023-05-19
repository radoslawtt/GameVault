from .game_window import GameWindow

def start_game(username, window):
    game = GameWindow(username, window)
    game.run()
