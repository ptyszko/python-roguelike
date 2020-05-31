#!/usr/bin/python3
import pyglet
from pyglet.image import load as load_image, ImageGrid, TextureGrid
from pyglet.media import load as load_media, StaticSource
from pyglet.graphics import Batch, OrderedGroup
from game.mainmenu import MainMenu
from time import sleep


class GameState:
    def __init__(self):
        self.map = None
        self.layout = None
        self.end_staircase = None
        self.stage = 1
        self.game_window = None
        self.pc = None
        self.next_stage = False
        self.move_timeout = True
        self.timeout_limit = 1  # sekundy
        self.enemies = set()
        self.consumables = set()
        self.equippables = set()
        self.sprites = Batch()
        self.items = Batch()
        self.stages = 5
        self.cell_size = 5
        self.width = 45  # w tile-ach, wielokrotność 3*sell_size
        self.height = 30  # wielokrotność cell_size
        self.status_bar = None
        self.difficulty = 0
        self.groups = [OrderedGroup(0), OrderedGroup(1)]

        self.tileset = TextureGrid(
            ImageGrid(load_image('img/tiles.png'), 5, 5)
        )

        self.tile_textures = {
            'floor': self.tileset.get(4, 0).get_image_data(),
            'wall': self.tileset.get(4, 1).get_image_data(),
            'bars': self.tileset.get(4, 2).get_image_data(),
            'rubble': self.tileset.get(4, 3).get_image_data(),
            'stairs': self.tileset.get(4, 4).get_image_data(),
        }

        self.sprite_textures = {
            'bandit_dig': self.tileset.get(0, 0),
            'bandit_disg': self.tileset.get(0, 1),
            'bandit_fierce': self.tileset.get(0, 2),
            'bandit_wander': self.tileset.get(0, 3),
            'bandit_wary': self.tileset.get(0, 4),
            'bandit_aggr': self.tileset.get(1, 2),
            'bandit_coward': self.tileset.get(1, 3),
            'bandit_def': self.tileset.get(1, 4),

            'guard_glass': self.tileset.get(1, 0),
            'guard_unlk': self.tileset.get(1, 1),
            'guard': self.tileset.get(2, 0),
            'guard_angry': self.tileset.get(2, 1),
            'guard_blnk': self.tileset.get(2, 2),
            'guard_chase': self.tileset.get(2, 3),
            'guard_def': self.tileset.get(2, 4),

            'player': self.tileset.get(3, 0),
            'player_h': self.tileset.get(3, 1),
            'player_d': self.tileset.get(3, 2),
            'player_dh': self.tileset.get(3, 3),

            'item': self.tileset.get(3, 4),
        }

        self.sounds = {
            'player_hit': StaticSource(load_media('sound/player_hit.wav')),
            'bandit_hit': StaticSource(load_media('sound/bandit_hit.wav')),
            'guard_hit': StaticSource(load_media('sound/guard_hit.wav')),
        }

    def change_size(self, param, change):
        if param == 'width' and self.width > self.cell_size*3:
            self.width += change * self.cell_size * 3
        elif self.height > self.cell_size*3:
            self.height += change * self.cell_size

    def change_timeout(self, change):
        if self.timeout_limit + change < -0.05:
            pass
        elif abs(self.timeout_limit + change) <= 0.05:
            self.move_timeout = False
            self.timeout_limit = 0
        else:
            self.timeout_limit += change

    def change_diff(self, change):
        self.difficulty = max(self.difficulty+change, 0)

    def xprint(self, *args, sep=' '):
        self.status_bar.text = sep.join(str(a) for a in args)

    def new_stage(self):
        for a in self.enemies | self.consumables | self.equippables:
            a.delete()
        self.enemies = set()
        self.consumables = set()
        self.equippables = set()
        self.next_stage = False


if __name__ == "__main__":
    game = GameState()
    MainMenu(game)
    pyglet.app.run()
