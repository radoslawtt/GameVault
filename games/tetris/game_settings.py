import pygame as pg

VECTOR = pg.math.Vector2

FPS = 60
FIELD_COLOR = (17, 17, 18)

WINDOW_BG = (54, 57, 64)

INFO = ["Rotate - up arrow", "Land tetromino - down arrow", "Move tetromino to left - left arrow", "Move tetromino to right - right arrow",
        "If you leave the game before it finishes, your score will not be saved.",
        "If you beat your best score or the best score in the game", "it will change when you reopen the game."]

ANIMATION_TIME_INTERVAL = 350 #MILISECONDS
FAST_ANIMATION_TIME_INTERVAL = 15

TILE_SIZE = 40
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 10, 20
FIELD_RES = FIELD_WIDTH*TILE_SIZE, FIELD_HEIGHT*TILE_SIZE

NXT_RES = FIELD_RES[0]*0.65, FIELD_RES[1]*0.45


FIELD_SCALE_WIDTH, FIELD_SCALE_HEIGHT = 2, 1.2
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT = FIELD_RES[0]*FIELD_SCALE_WIDTH, FIELD_RES[1]*FIELD_SCALE_HEIGHT

FIELD_MARGIN_X = (WINDOW_WIDTH/FIELD_SCALE_WIDTH)*0.1
FIELD_MARGIN_Y = (WINDOW_HEIGHT/FIELD_SCALE_HEIGHT)*0.1

FIELD_OFFSET_X = int(FIELD_MARGIN_X/TILE_SIZE)
FIELD_OFFSET_Y = int(FIELD_MARGIN_Y/TILE_SIZE)


SPRITE_DIR_PATH = "resources/tetris_assets/images"
FONT_PATH = "resources/tetris_assets/font/xylitol.front-regular.otf"

INIT_POS_OFFSET = VECTOR((FIELD_WIDTH // 2-1)+FIELD_OFFSET_X, FIELD_OFFSET_Y)
NEXT_POS_OFFSET_1 = VECTOR(FIELD_WIDTH*3, FIELD_HEIGHT*0.35)
NEXT_POS_OFFSET_2 = VECTOR(FIELD_WIDTH*3, FIELD_HEIGHT*0.59)
NEXT_POS_OFFSET_3 = VECTOR(FIELD_WIDTH*3, FIELD_HEIGHT*0.84)
MOVE_DIRECTIONS = {"left": VECTOR(-1, 0), "right": VECTOR(1, 0), "down": VECTOR(0, 1)}

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, 1)],
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'J': [(0, 1), (0, 0), (-1, 2), (0, 2)],
    'L': [(0, 1), (0, 0), (0, 2), (1, 2)],
    'I': [(0, 2), (0, 1), (0, 0), (0, 3)],
    'S': [(0, 0), (-1, 0), (0, 1), (1, 1)],
    'Z': [(0, 0), (1, 0), (0, 1), (-1, 1)]
}
