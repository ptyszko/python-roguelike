from pyglet.sprite import Sprite
from pyglet.image import load
from pyglet.graphics import Batch
from pyglet.text import Label

from util import tile
from util.levelgen import get_clear_tile
from util.fonts import SANS
from itertools import repeat, chain, cycle as _cycle
from random import choice, normalvariate
from json import loads
<<<<<<< HEAD
import numpy
=======
>>>>>>> small_changes

'''
RANDOMIZED_STATS = {
    'health', 'damage', 'exp'
}

LEVELED_STATS = {
    'health', 'damage', 'gold'
}
'''
RANDOMIZED_STATS = LEVELED_STATS = set()
LEVELING_FACTOR = 1/20
VAR = 1/10


def still(self):
    return repeat((0, 0))


def cycle(self, *movements):
    return _cycle(movements)


def random(self, neighborhood=4, freq=1):
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # sąsiedztwo von Neumanna
    if neighborhood == 8:  # sąsiedztwo Conwaya
        moves += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    move = 0
    while True:
        yield choice(moves) if move == 0 else (0, 0)
        move = (move+1) % freq

<<<<<<< HEAD
def aggresive(self, game, neighbourhood=8):
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # sąsiedztwo von Neumanna
    if neighbourhood == 8:  # sąsiedztwo Conwaya
        moves += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    while True:
        if numpy.abs(self.xpos - game.pc.xpos) < 3 and numpy.abs(self.ypos - game.pc.ypos) < 3:
            dx = -numpy.sign(self.xpos - game.pc.xpos)
            dy = -numpy.sign(self.ypos - game.pc.ypos)
            yield (dx,dy)
        else:
            yield (0,0)

def steady(self, game, neighbourhood=4):
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # sąsiedztwo von Neumanna
    if neighbourhood == 8:  # sąsiedztwo Conwaya
        moves += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    while True:
        if numpy.abs(self.ypos - game.pc.ypos) == 1 and numpy.abs(self.xpos - game.pc.xpos) == 0:
            dx = 0
            dy = -numpy.sign(self.ypos - game.pc.ypos)
        elif numpy.abs(self.xpos - game.pc.xpos) < 3 and numpy.abs(self.ypos - game.pc.ypos) < 3:
            dx = -numpy.sign(self.xpos - game.pc.xpos)
            dy = 0
        else:
            dx = 0
            dy = 0
        yield (dx,dy)

patterns = {
    'still': still, 'cycle': cycle,
    'random': random, 'aggresive': aggresive,
    'steady': steady
}

=======

patterns = {
    'still': still, 'cycle': cycle,
    'random': random
}


>>>>>>> small_changes
class Creature(Sprite):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None, health=5, defence=0, name='none'):
        img = load(path)
        self.name = name
        self.health = self.maxhealth = health
        self.game = game_state
        self.tile_width = tile_width
        self.tile_height = tile_height
        if xpos == ypos == 0:
<<<<<<< HEAD
            self.xpos, self.ypos = get_clear_tile(game)
=======
            self.xpos, self.ypos = get_clear_tile(game_state)
>>>>>>> small_changes
        else:
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

    def on_damage(self, damage, source):
        self.health -= damage
        self.game.xprint(source.name, 'attacks', self.name,
                         'for', damage, 'damage.')

    def attack(self, target):
<<<<<<< HEAD
        damage = 1  # w przyszłości zależne od statystyk (może)
=======
        damage = 1  # w przyszłości zależne od statystyk
>>>>>>> small_changes
        target.on_damage(damage, self)


class Player(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None):
        super().__init__(path, tile_width, tile_height,
                         game_state, xpos=xpos, ypos=ypos,
                         group=group, name='Player')
        self.game.pc = self
        self.exp = 0
        self.status_indicator = Label(
            x=self.game.game_window.width,
            y=self.game.game_window.height-40,
            width=100, multiline=True, font_name=SANS,
            font_size=20, anchor_x='right', anchor_y='top',
            batch=self.game.game_window.main_batch
        )

    def move(self, dx, dy):
        new_x = self.xpos+dx
        new_y = self.ypos+dy
        enemy = next((m for m in self.game.enemies
                      if m.xpos == new_x
                      and m.ypos == new_y), None)

        if enemy is not None:
            self.attack(enemy)
        elif (
            self.game.map
            [new_y]
            [new_x]
        ) in tile.TRAVERSABLE:
            self.xpos = new_x
            self.ypos = new_y
            self.update_pos()
            if (
                self.game.map
                [self.ypos]
                [self.xpos]
            ) in tile.STAIRS:
                self.game.stage += 1
                self.game.next_stage = True
        self.update_status()

    def on_damage(self, damage, source):
        super().on_damage(damage, source)
        self.update_status()
        if self.health <= 0:
            self.game.game_window.lose()

    def update_status(self):
        self.status_indicator.text = f'''HP: {self.health}/{self.maxhealth}
x: {self.xpos}
y: {self.ypos}'''


class Enemy(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None, health=5,
                 move_pattern=still, move_params=(), name='enemy'):
        super().__init__(path, tile_width, tile_height, game_state,
                         xpos=xpos, ypos=ypos, group=group,
                         health=health, name=name)
        if type(move_pattern) == str:
<<<<<<< HEAD
            self.move_pattern = patterns[move_pattern](self, self.game, *move_params)
        else:
            self.move_pattern = move_pattern(self, self.game, *move_params)
        self.cycle = move_pattern == cycle
        self.game.enemies.append(self)
=======
            self.move_pattern = patterns[move_pattern](self, *move_params)
        else:
            self.move_pattern = move_pattern(self, *move_params)
        self.cycle = move_pattern in {cycle, 'cycle'}
        self.game.enemies.add(self)
>>>>>>> small_changes

    def move(self):
        dx, dy = next(self.move_pattern)
        new_x = self.xpos+dx
        new_y = self.ypos+dy
        if (
            self.game.pc.xpos == new_x
            and self.game.pc.ypos == new_y
        ):
            self.attack(self.game.pc)
<<<<<<< HEAD
=======
            if self.cycle:
                self.move_pattern = chain([(dx,dy)], self.move_pattern)
>>>>>>> small_changes
        elif (
            0 < new_x < self.game.width-1
            and 0 < new_y < self.game.height-1

            and self.game.map[new_y][new_x]
            in tile.TRAVERSABLE
            and not any(new_x == e.xpos
                        and new_y == e.ypos
                        for e in self.game.enemies)
        ):
            self.xpos += dx
            self.ypos += dy
            self.update_pos()
        elif self.cycle:
            self.move_pattern = chain([(dx, dy)], self.move_pattern)

    def on_damage(self, damage, source):
        super().on_damage(damage, source)
        if self.health <= 0:
            self.game.enemies.remove(self)
            self.delete()

    @staticmethod
    def from_json(path, game):
        with open(path, 'r') as json:
            base_stats = loads(''.join(json.readlines()))
        for stat in LEVELED_STATS:
            base_stats[stat] *= 1 + LEVELING_FACTOR*game.stage
        for stat in RANDOMIZED_STATS:
            base_stats[stat] *= normalvariate(1, VAR)
        for stat in LEVELED_STATS | RANDOMIZED_STATS:
            base_stats[stat] = int(base_stats[stat])

        xp, yp = get_clear_tile(game)
<<<<<<< HEAD
        if path == 'enemies/guard.json':
            return Enemy(tile_height=24, tile_width=24, game_state=game, xpos = 37, ypos = 24, **base_stats)
        if path == 'enemies/guard1.json':
            return Enemy(tile_height=24, tile_width=24, game_state=game, xpos = 22, ypos = 24, **base_stats)
        if path == 'enemies/guard2.json':
            return Enemy(tile_height=24, tile_width=24, game_state=game, xpos = 7, ypos = 24, **base_stats)
=======
>>>>>>> small_changes
        return Enemy(tile_height=24, tile_width=24, game_state=game, xpos=xp, ypos=yp, **base_stats)


def add_enemies(game):
    # w przyszłości będzie zależne od poziomu
<<<<<<< HEAD
    """
=======
>>>>>>> small_changes
    xp, yp = get_clear_tile(game)
    nest = Enemy('img/enemy.png', 24, 24, game, xpos=xp, ypos=yp)

    xp, yp = get_clear_tile(game)
    slime = Enemy('img/enemy.png', 24, 24, game, xpos=xp, ypos=yp,
                  move_pattern=cycle,
                  move_params=[(0, 1), (0, 0), (0, -1), (0, 0)])
<<<<<<< HEAD
    """

    #bat = Enemy.from_json('enemies/bat.json', game)


    bandit1 = Enemy.from_json('enemies/bandit.json', game)
    bandit2 = Enemy.from_json('enemies/bandit.json', game)
    bandit3 = Enemy.from_json('enemies/bandit.json', game)
    bandit4 = Enemy.from_json('enemies/bandit.json', game)
    bandit5 = Enemy.from_json('enemies/bandit.json', game)
    bandit6 = Enemy.from_json('enemies/bandit.json', game)
    bandit7 = Enemy.from_json('enemies/bandit.json', game)
    bandit8 = Enemy.from_json('enemies/bandit.json', game)
    bandit9 = Enemy.from_json('enemies/bandit.json', game)

    guard = Enemy.from_json('enemies/guard.json', game)
    guard1 = Enemy.from_json('enemies/guard1.json', game)
    guard2 = Enemy.from_json('enemies/guard2.json', game)
=======

    xp, yp = get_clear_tile(game)
    bat = Enemy.from_json('enemies/bat.json', game)
>>>>>>> small_changes
