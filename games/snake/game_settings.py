import pygame as pg

VECTOR = pg.math.Vector2

FPS = 60
FIELD_COLOR = (17, 17, 18)

WINDOW_BG = (146, 161, 150)

ANIMATION_TIME_INTERVAL = 150 #miliseconds

TILE_SIZE = 30
FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 15, 30
FIELD_RES = FIELD_WIDTH*TILE_SIZE, FIELD_HEIGHT*TILE_SIZE

FIELD_SCALE_WIDTH, FIELD_SCALE_HEIGHT = 1.7, 1.0
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT = FIELD_RES[0]*FIELD_SCALE_WIDTH, FIELD_RES[1]*FIELD_SCALE_HEIGHT

SPRITE_DIR_PATH = "resources/tetris_assets/images"
FONT_PATH = "resources/tetris_assets/font/xylitol.front-regular.otf"

INFO = ["You use arrows to control the snake.", "You receive 10 points for each apple consumed.", "When you reopen the game, the best player is reset.", "You can exit the game at any time by pressing the escape button or by closing the window."]




