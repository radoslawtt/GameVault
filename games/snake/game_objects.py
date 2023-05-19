from .game_settings import *
from random import randrange


class Snake:

    def __init__(self, game_field):
        self.game_field = game_field
        self.size = TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, TILE_SIZE-2, TILE_SIZE-2])
        self.rect.center = self.get_random_position()
        self.direction = VECTOR(0, 0)
        self.anim_time_interval = ANIMATION_TIME_INTERVAL
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.anim_time_interval:
            self.time = time_now
            return True
        return False

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.move()

    def get_random_position(self):
        return [randrange(self.size//2, FIELD_WIDTH*self.size - self.size//2, self.size), randrange(self.size//2,
                                                                    FIELD_HEIGHT*self.size - self.size//2, self.size)]

    def draw(self):
            [pg.draw.rect(self.game_field.game_window.screen, "green", segment) for segment in self.segments]


class Food:

    def __init__(self, game_field):
        self.game_field = game_field
        self.size = TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
        self.rect.center = self.get_random_position()

    def draw(self):
        pg.draw.rect(self.game_field.game_window.screen, "red", self.rect)

    def get_random_position(self):
        position = [randrange(self.size // 2, FIELD_WIDTH * self.size - self.size // 2, self.size),
                    randrange(self.size // 2,
                              FIELD_HEIGHT * self.size - self.size // 2, self.size)]
        collision = True
        while collision:
            for segment in self.game_field.snake.segments:
                if segment == position:
                    position = [randrange(self.size // 2, FIELD_WIDTH * self.size - self.size // 2, self.size),
                                randrange(self.size // 2,
                                          FIELD_HEIGHT * self.size - self.size // 2, self.size)]
                    break
            else:
                collision = False

        return position

