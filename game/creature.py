from pyglet.sprite import Sprite
from pyglet.image import load
from pyglet.graphics import Batch
from abc import ABC, abstractmethod
from util import tile

creatures = Batch()


class Creature(Sprite, ABC):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None):
        img = load(path)
        self.game = game_state
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.xpos = xpos
        self.ypos = ypos
        super().__init__(img, x=xpos*tile_width, y=ypos*tile_height,
                         batch=creatures, group=group, usage='dynamic', subpixel=False)

        # po całościowej konstrukcji normalizujemy rozmiar
        self.scale_x /= self.width / self.tile_width
        self.scale_y /= self.height / self.tile_height

    def update_pos(self):
        self.update(
            x=(self.xpos-1) * self.tile_width,
            y=(self.ypos-1) * self.tile_height
        )


class Player(Creature):
    def __init__(self, path, tile_width, tile_height, game_state, xpos=0, ypos=0, group=None):
        super().__init__(path, tile_width, tile_height,
                         game_state, xpos=xpos, ypos=ypos, group=group)
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
