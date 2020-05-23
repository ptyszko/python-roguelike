#!/usr/bin/python3
import pyglet
from pyglet.image import load as load_image
from pyglet.media import load as load_media, StaticSource
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
        self.sprites = pyglet.graphics.Batch()
        self.items = pyglet.graphics.Batch()
        self.stages = 3
        self.cell_size = 5
        self.width = 45  # w tile-ach, wielokrotność 3*sell_size
        self.height = 30  # wielokrotność cell_size
        self.status_bar = None
        self.difficulty = 0
        self.groups = [pyglet.graphics.OrderedGroup(0),
                       pyglet.graphics.OrderedGroup(1)]
        
        self.tile_textures = {
            'bars': load_image('img/bars.png').get_image_data(),
            'floor': load_image('img/dirt-floor.png').get_image_data(),
            'wall': load_image('img/dirt-wall.png').get_image_data(),
            'rubble': load_image('img/rubble.png').get_image_data(),
            'stairs': load_image('img/stairs.png').get_image_data(),
        }
        
        self.sprite_textures = {
            'bandit_aggr': load_image('img/bandit_aggresive.png'),
            'bandit_coward': load_image('img/bandit_coward.png'),
            'bandit_def': load_image('img/bandit_default.png'),
            'bandit_dig': load_image('img/bandit_digger.png'),
            'bandit_disg': load_image('img/bandit_disguised.png'),
            'bandit_wander': load_image('img/bandit_wandering.png'),
            'bandit_wary': load_image('img/bandit_wary.png'),
            
            'guard': load_image('img/guard.png'),
            'guard_angry': load_image('img/guard_angry.png'),
            'guard_chase': load_image('img/guard_chasing.png'),
            'guard_def': load_image('img/guard_default.png'),
            'guard_glass': load_image('img/guard_glasses.png'),
            'guard_unlk': load_image('img/guard_unlucky.png'),
            'guard': load_image('img/guard.png'),
            
            'player': load_image('img/player.png'),
            'player_h': load_image('img/player_hurt.png'),
            'player_d': load_image('img/player_disguised.png'),
            'player_dh': load_image('img/player_disguised_hurt.png'),
            
            'item': load_image('img/item.png'),
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
        self.enemies=set()
        self.consumables = set()
        self.equippables = set()
        self.next_stage = False
        


game = GameState()


if __name__ == "__main__":
    MainMenu(game)
    pyglet.app.run()
