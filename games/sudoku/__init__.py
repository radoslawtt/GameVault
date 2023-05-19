from .game_window import MainWindow

def start_game(username, window):
    game = MainWindow(username, window)
    game.run()