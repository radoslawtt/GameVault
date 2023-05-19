import pygame as pg


VECTOR = pg.math.Vector2

FPS = 60
FIELD_COLOR = (255,255,255)

WINDOW_BG = (171, 183, 201)

ANIMATION_TIME_INTERVAL = 150 #miliseconds
FAST_ANIMATION_TIME_INTERVAL = 15

TILE_SIZE = 40
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 9, 9
FIELD_RES = FIELD_WIDTH*TILE_SIZE, FIELD_HEIGHT*TILE_SIZE

MARGIN_X = TILE_SIZE
MARGIN_Y = TILE_SIZE

ROWS = 9
COLUMNS = 9

FIELD_SCALE_WIDTH, FIELD_SCALE_HEIGHT = 2, 1.2
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT = FIELD_RES[0]*FIELD_SCALE_WIDTH, FIELD_RES[1]*FIELD_SCALE_HEIGHT

INFO = ["To insert a digit, click in the rectangle and then press the digit key on the keyboard.",
        "You can remove a typed digit by pressing the c key on your keyboard.",
        "Each sudoku puzzle solved earns you 50 points.", "If you want a new puzzle click play gain button", "If you beat your best time or best time in game changes will",
        "change will be seen after you reopen game"]




