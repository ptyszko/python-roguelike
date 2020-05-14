from pyglet.sprite import Sprite
from pyglet.image import load, create, SolidColorImagePattern
from pyglet.graphics import Batch
from pyglet.text import Label

from util import tile
from util.levelgen import get_clear_tile
from util.fonts import SANS
from util.colors import RED
from itertools import repeat, chain, cycle as _cycle
from random import choice, normalvariate
from json import loads


def sign(x):
    return x and int(x/abs(x))


HP = 'health'
DMG = 'damage'
DEF = 'defence'
EXP = 'exp'
HPMAX = 'maxhealth'
G = 'gold'


RANDOMIZED_STATS = {
    HP, DMG, EXP
}

LEVELED_STATS = {
    HP, DMG, G
}

# RANDOMIZED_STATS = LEVELED_STATS = set()
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


def aggresive(self, neighbourhood=8):
    game = self.game
    while True:
        if abs(self.xpos - game.pc.xpos) < 3 and abs(self.ypos - game.pc.ypos) < 3:
            dx = -sign(self.xpos - game.pc.xpos)
            dy = -sign(self.ypos - game.pc.ypos)
            yield (dx, dy)
        else:
            yield (0, 0)


def steady(self, neighbourhood=4):
    game = self.game
    while True:
        dx = dy = 0
        if (abs(self.ypos-game.pc.ypos) == 1
                and self.xpos-game.pc.xpos == 0):
            dy = game.pc.ypos - self.ypos
        elif (abs(self.xpos - game.pc.xpos) < 3
              and abs(self.ypos - game.pc.ypos) < 3):
            dx = -sign(self.xpos - game.pc.xpos)
        yield (dx, dy)


patterns = {
    'still': still, 'cycle': cycle,
    'random': random, 'aggresive': aggresive,
    'steady': steady
}


class Creature(Sprite):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, health=5, defence=0, group=None,
                 name='none', damage=1):
        img = load(path)
        self.stats = {DMG: damage, DEF: defence, HP: health, HPMAX: health}
        self.name = name
        self.game = game_state
        self.tile_width = tile_width
        self.tile_height = tile_height
        if xpos == ypos == 0:
            self.xpos, self.ypos = get_clear_tile(game_state)
        else:
            self.xpos = xpos
            self.ypos = ypos
        if group is None: 
            group = self.game.groups[0]
        super().__init__(
            img, x=(xpos-1)*tile_width, y=(ypos-1)*tile_height,
            batch=game_state.sprites, group=group,
            usage='dynamic', subpixel=False
        )

        # po całościowej konstrukcji normalizujemy rozmiar
        self.scale_x /= self.width / self.tile_width
        self.scale_y /= self.height / self.tile_height

    def update_pos(self):
        self.update(
            x=(self.xpos-1) * self.tile_width,
            y=(self.ypos-1) * self.tile_height
        )

    def on_damage(self, damage, source):
        self.stats[HP] -= damage
        self.game.xprint(source.name, 'attacks', self.name,
                         'for', damage, 'damage.')

    def attack(self, target):
        target.on_damage(max(self.stats[DMG] - target.stats[DEF], 1), self)


class Player(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None):
        super().__init__(path, tile_width, tile_height,
                         game_state, xpos=xpos, ypos=ypos,
                         group=group, name='Player')
        self.game.pc = self
        self.stats[EXP] = self.stats[G] = 0
        self.inv = {}
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
        elif self.game.map[new_y][new_x] in tile.TRAVERSABLE:
            self.xpos = new_x
            self.ypos = new_y
            self.update_pos()

            if self.game.map[self.ypos][self.xpos] in tile.STAIRS:
                self.game.stage += 1
                self.game.next_stage = True

        found_items = (c for c in self.game.consumables
                       if c.xpos == self.xpos and c.ypos == self.ypos)
        for item in found_items:
            item.consume()
        found_gear = (e for e in self.game.equippables
                      if e.xpos == self.xpos and e.ypos == self.ypos)
        for gear in found_gear:
            gear.equip()
        self.update_status()

    def on_damage(self, damage, source):
        super().on_damage(damage, source)
        self.update_status()
        if self.stats[HP] <= 0:
            self.game.game_window.lose()

    def update_status(self):
        self.status_indicator.text = f'''HP: {self.stats[HP]}/{self.stats[HPMAX]}
x: {self.xpos}
y: {self.ypos}
gold: {self.stats[G]}'''

    def normalize(self):
        self.stats[HPMAX] = max(1, self.stats[HPMAX])
        self.stats[HP] = max(min(self.stats[HP], self.stats[HPMAX]), 1)
        self.update_status()


class Enemy(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None, health=5,
                 move_pattern=still, move_params=(), name='enemy',
                 gold=0, exp=0):
        super().__init__(path, tile_width, tile_height, game_state,
                         xpos=xpos, ypos=ypos, group=group,
                         health=health, name=name)
        if type(move_pattern) == str:
            self.move_pattern = patterns[move_pattern](
                self, *move_params)
        else:
            self.move_pattern = move_pattern(self, *move_params)
        self.cycle = move_pattern == cycle
        self.game.enemies.add(self)
        self.stats[G] = gold
        self.stats[EXP] = exp
        self.healthbar = Sprite(create(24, 4, SolidColorImagePattern(RED)),
                                x=self.x, y=self.y, batch=self.batch,
                                group=self.game.groups[1])

    def move(self):
        dx, dy = next(self.move_pattern)
        new_x = self.xpos+dx
        new_y = self.ypos+dy
        if (
            self.game.pc.xpos == new_x
            and self.game.pc.ypos == new_y
        ):
            self.attack(self.game.pc)
            if self.cycle:
                self.move_pattern = chain([(dx, dy)], self.move_pattern)
        elif (
            0 < new_x < self.game.width-1
            and 0 < new_y < self.game.height-1
            and self.game.map[new_y][new_x]
            in tile.TRAVERSABLE
            and not any(new_x == e.xpos
                        and new_y == e.ypos
                        for e in self.game.enemies - {self})
        ):
            self.xpos += dx
            self.ypos += dy
            self.update_pos()
        elif self.cycle:
            self.move_pattern = chain([(dx, dy)], self.move_pattern)

    def on_damage(self, damage, source):
        super().on_damage(damage, source)
        if self.stats[HP] <= 0:
            self.game.enemies.remove(self)
            self.game.pc.stats[G] += self.stats[G]
            self.game.pc.stats[EXP] += self.stats[EXP]
            self.healthbar.delete()
            self.delete()
            return None
        self.healthbar.image = create(
            round(24*self.stats[HP]/self.stats[HPMAX]), 
            4, SolidColorImagePattern(RED)
        )
        self.healthbar.draw()
        
    def update_pos(self):
        super().update_pos()
        self.healthbar.x = self.x
        self.healthbar.y = self.y

    @staticmethod
    def from_json(path, game, xp=0, yp=0):
        with open(path, 'r') as json:
            base_stats = loads(''.join(json.readlines()))

        if xp == yp == 0:
            xp, yp = get_clear_tile(game)
        ret = Enemy(tile_height=24, tile_width=24, game_state=game,
                    xpos=xp, ypos=yp, **base_stats)
        for stat in LEVELED_STATS:
            ret.stats[stat] *= 1 + LEVELING_FACTOR*game.stage*(2*game.difficulty+1)
        for stat in RANDOMIZED_STATS:
            ret.stats[stat] *= normalvariate(1, VAR)
        for stat in LEVELED_STATS | RANDOMIZED_STATS:
            ret.stats[stat] = int(ret.stats[stat])


def add_enemies(game):
    # w przyszłości będzie zależne od poziomu
    for i in range(10):
        Enemy.from_json('enemies/bandit.json', game)

    for x in range(7, game.width, 15):
        Enemy.from_json('enemies/guard.json', game, xp=x, yp=game.height-6)
