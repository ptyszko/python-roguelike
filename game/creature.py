from pyglet.sprite import Sprite
from pyglet.image import load
from pyglet.graphics import Batch
from abc import ABC, abstractmethod
from util import tile


def still(self):
    while True:
        yield (0, 0)


def cycle(self, *movements):
    while True:
        for m in movements:
            yield m


class Creature(Sprite, ABC):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None, health=5):
        img = load(path)
        self.health = self.maxhealth = health
        self.game = game_state
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.xpos = xpos
        self.ypos = ypos
        super().__init__(img, x=(xpos-1)*tile_width, y=(ypos-1)*tile_height,
                         batch=game_state.creatures, group=group,
                         usage='dynamic', subpixel=False)

        # po całościowej konstrukcji normalizujemy rozmiar
        self.scale_x /= self.width / self.tile_width
        self.scale_y /= self.height / self.tile_height

    def update_pos(self):
        # print(self.xpos, self.ypos)
        self.update(
            x=(self.xpos-1) * self.tile_width,
            y=(self.ypos-1) * self.tile_height
        )


class Player(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None):
        super().__init__(path, tile_width, tile_height,
                         game_state, xpos=xpos, ypos=ypos,
                         group=group)
        self.game.pc = self

    def move(self, dx, dy):
        if (
            self.game.map
            [self.ypos+dy]
            [self.xpos+dx]
        ) != tile.WALL:
            self.xpos += dx
            self.ypos += dy
            self.update_pos()
            if (
                self.game.map
                [self.ypos]
                [self.xpos]
            ) == tile.STAIRS:
                self.game.stage += 1
                self.game.next_stage = True
        # print(f'my pos is ({self.xpos}, {self.ypos})')


class Enemy(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None, health=5,
                 move_pattern=still, move_params=()):
        super().__init__(path, tile_width, tile_height, game_state,
                         xpos=xpos, ypos=ypos, group=group,
                         health=health)
        self.move_pattern = move_pattern(self, *move_params)
        self.game.enemies.append(self)

    def move(self):
        dx, dy = next(self.move_pattern)
        if (
            self.game.map
            [self.ypos+dy]
            [self.xpos+dx]
        ) != tile.WALL:
            self.xpos += dx
            self.ypos += dy
            self.update_pos()
