FPS = 60

WINDOW_BG = (54, 57, 64)

TILE_SIZE = 30
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 15, 30
FIELD_RES = FIELD_WIDTH*TILE_SIZE, FIELD_HEIGHT*TILE_SIZE

ROWS_OF_BUTTONS = 2
COLUMNS_OF_BUTTONS = 13
BUTTON_SIZE = TILE_SIZE*1.1
BUTTON_GAP = TILE_SIZE*0.8

FIELD_SCALE_WIDTH, FIELD_SCALE_HEIGHT = 1.7, 1.0
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT = FIELD_RES[0]*FIELD_SCALE_WIDTH, FIELD_RES[1]*FIELD_SCALE_HEIGHT

MAN_DIR_PATH = "resources/hangman_assets/images/hangman"
HEART_DIR_PATH = "resources/hangman_assets/images/hearts"

INFO = ["To make a guess, just click on a letter.", "You get 10 points for every word you solve.", "You have 3 lives.", "You can exit the game at any time,", "by clicking esc or closeing the window."]
