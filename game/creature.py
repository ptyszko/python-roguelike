import networkx as nx
from itertools import repeat, chain, cycle as _cycle
from random import choice, normalvariate, randint
from json import loads
from pyglet.sprite import Sprite
from pyglet.image import create, SolidColorImagePattern
from pyglet.graphics import Batch
from pyglet.text import Label
import pyglet

from util import tile
from util.levelgen import get_clear_tile
from util.fonts import SANS
from util.colors import RED
from . import item


def sign(x):
    return x and int(x / abs(x))


HP = 'health'
DMG = 'damage'
DEF = 'defence'
EXP = 'exp'
HPMAX = 'maxhealth'
G = 'gold'
LV = 'level'
NLV = 'exp to next level'

RANDOMIZED_STATS = {
    DMG, EXP  # , HP
}
LEVELED_STATS = {
    HP, DMG, G
}

# RANDOMIZED_STATS = LEVELED_STATS = set()
LEVELING_FACTOR = 1 / 20
VAR = 1 / 10


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
        move = (move + 1) % freq


def random_step(self):
    rand = (randint(1, 10)-5, randint(1, 10)-5)
    if (abs(rand[0]) > abs(rand[1])):
        return(sign(rand[0]), 0)
    elif (abs(rand[0]) < abs(rand[1])):
        return(0, sign(rand[1]))
    else:
        return(0, 0)


def standard(self):
    game = self.game
    player_hit = False
    player_seen = False
    while True:
        if game.pc.stats[HP] < game.pc.stats[HPMAX]:
            player_hit = True
        if (abs(self.ypos - game.pc.ypos) + abs(self.xpos - game.pc.xpos)) == 1:
            player_hit = True
        if player_hit:
            if room(self) == room(game.pc):
                player_seen = True
            if player_seen:
                yield (chasing_step(self))
            else:
                yield(random_step(self))
        else:
            yield(random_step(self))


def door(self):
    game = self.game
    player_hit = False
    player_seen = False
    while True:
        if game.pc.stats[HP] < game.pc.stats[HPMAX]:
            player_hit = True
        if (abs(self.ypos - game.pc.ypos) + abs(self.xpos - game.pc.xpos)) == 1:
            player_hit = True
        if player_hit:
            if room(self) == room(game.pc):
                player_seen = True
            if player_seen:
                yield (chasing_step(self))
            else:
                yield (0, 0)
        elif room(self) == room(game.pc):
            yield(-1, 0)
        else:
            yield(0, 0)


def aggresive(self, neighbourhood=8):
    game = self.game
    while True:
        if (room(self) == room(game.pc)):
            dist_x = abs(self.xpos - game.pc.xpos)
            dist_y = abs(self.ypos - game.pc.ypos)
            dx = sign(self.xpos - game.pc.xpos)
            dy = sign(self.ypos - game.pc.ypos)
            if dist_x < dist_y:
                yield (0, -dy)
            elif dist_x > dist_y:
                yield (-dx, 0)
            else:
                rand = randint(0, 1)
                if rand == 0:
                    yield (0, -dy)
                else:
                    yield (-dx, 0)
        else:
            yield (0, 0)


"""
    while True:
        if abs(self.xpos - game.pc.xpos) < 3 and abs(self.ypos - game.pc.ypos) < 3:
            dx = -sign(self.xpos - game.pc.xpos)
            dy = -sign(self.ypos - game.pc.ypos)
            yield (dx, dy)
        else:
            yield (0, 0)
"""


def coward(self):
    game = self.game
    while True:
        if (abs(self.ypos - game.pc.ypos)) == 1 and (abs(self.xpos - game.pc.xpos)) == 0:
            rand = randint(0, 1)
            yield (-2*rand+1, 0)
        elif (abs(self.ypos - game.pc.ypos)) == 0 and (abs(self.xpos - game.pc.xpos)) == 1:
            rand = randint(0, 1)
            yield (0, -2*rand+1)
        else:
            yield (0, 0)


def room(self):
    game = self.game
    row = (self.ypos) // 5 - 1
    col = (self.xpos) // 5
    return (row, col)


def change_room(self, variant):
    change_map = [[(-1, 0), self.ypos, (0, 1)], [(0, 1), self.xpos, (1, 0)], [(1, 0), self.ypos, (0, 1)],
                  [(0, -1), self.xpos, (1, 0)]]
    if change_map[variant][1] % 5 == 2 or ((variant == 1 or variant == 3) and (room(self)[1]) % 3 == 1):
        return (change_map[variant][0])
    elif change_map[variant][1] % 5 < 2:
        return change_map[variant][2]
    else:
        return (-change_map[variant][2][0], -change_map[variant][2][1])


def chasing_step(self, neighbourhood=8):
    game = self.game
    if (room(game.pc)[0] >= 4):
        return (0, 0)
    if (room(self) == room(game.pc)):
        dist_x = abs(self.xpos - game.pc.xpos)
        dist_y = abs(self.ypos - game.pc.ypos)
        dx = sign(self.xpos - game.pc.xpos)
        dy = sign(self.ypos - game.pc.ypos)
        if dist_x < dist_y:
            return (0, -dy)
        elif dist_x > dist_y:
            return (-dx, 0)
        else:
            rand = randint(0, 1)
            if rand == 0:
                return (0, -dy)
            else:
                return (-dx, 0)
    else:
        layout = self.game.layout
        path = nx.shortest_path(layout, (room(self)), (room(game.pc)))
        direction = tuple(map(lambda i, j: i - j, path[0], path[1]))
        variant = 0
        if direction == (0, 1):
            variant = 0
        elif direction == (-1, 0):
            variant = 1
        elif direction == (0, -1):
            variant = 2
        else:
            variant = 3
        return change_room(self, variant)


def chasing(self):
    counter = 0
    while True:
        if counter == 2 or counter == 3 or counter == 4:
            yield (chasing_step(self))
        else:
            yield (0, 0)
        counter += 1
        counter = counter % 5


def fierce(self):
    counter = 0
    while room(self) != room(self.game.pc):
        yield (0, 0)
    while True:
        if counter != 4:
            yield (chasing_step(self))
        else:
            yield (0, 0)
        counter += 1
        counter = counter % 5


def glasses(self, neighbourhood=4):
    game = self.game
    while True:
        dx = dy = 0
        if (abs(self.ypos - game.pc.ypos) == 1
                and self.xpos - game.pc.xpos == 0):
            dy = game.pc.ypos - self.ypos
        elif (abs(self.ypos - game.pc.ypos) == 0
                and self.xpos - game.pc.xpos == 1):
            dx = game.pc.xpos - self.xpos
        elif (abs(self.xpos - game.pc.xpos) < 3
              and abs(self.ypos - game.pc.ypos) < 3):
            dx = -sign(self.xpos - game.pc.xpos)
        yield (dx, dy)


def angry(self):
    game = self.game
    player_seen = False
    while True:
        if player_seen:
            rand = randint(1, 4)
            if rand == 1:
                yield (0, 0)
            else:
                yield chasing_step(self)
        else:
            if (room(self) == room(game.pc)):
                player_seen = True
                self.image = self.game.sprite_textures['guard_angry']
            yield (0, 0)


"""def unlucky(self):
    game = self.game
    while True:
        yield (0, 0)"""


def unlucky(self):
    counter = 0
    game = self.game
    while room(self) != room(game.pc):
        yield(0, 0)
    while True:
        counter += 1
        if counter == 1:
            yield(0, -1)
        elif counter == 10:
            self.image = game.tile_textures['rubble']
            counter -= 1
            if room(self) == room(game.pc):
                self.game.pc.image = self.game.sprite_textures['player_d']
            yield(0, 0)
        elif (abs(self.ypos - game.pc.ypos)) == 1 and (abs(self.xpos - game.pc.xpos)) == 0:
            yield (0, game.pc.ypos - self.ypos)
        elif (abs(self.ypos - game.pc.ypos)) == 0 and (abs(self.xpos - game.pc.xpos)) == 1:
            yield (game.pc.xpos - self.xpos, 0)
        yield(0, 0)


def wary(self):
    game = self.game
    while True:
        if (abs(self.ypos - game.pc.ypos)) == 1 and (abs(self.xpos - game.pc.xpos)) == 0:
            yield (0, game.pc.ypos - self.ypos)
        elif (abs(self.ypos - game.pc.ypos)) == 0 and (abs(self.xpos - game.pc.xpos)) == 1:
            yield (game.pc.xpos - self.xpos, 0)
        else:
            yield (0, 0)


def goldenrule(self):
    game = self.game
    balance = 0
    maxhp = self.stats[HP]
    while True:
        if self.stats[HP] + balance < maxhp:
            yield (chasing_step(self))
            balance += 1
        else:
            yield (0, 0)


patterns = {
    'still': still, 'cycle': cycle,
    'random': random, 'aggresive': aggresive,
    'glasses': glasses, 'coward': coward,
    'chasing': chasing, 'wary': wary,
    'goldenrule': goldenrule, 'angry': angry,
    'unlucky': unlucky, 'fierce': fierce,
    'standard': standard, 'door': door
}


class Creature(Sprite):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, health=3, defence=0, group=None,
                 name='none', damage=1, hitsound='player_hit'):
        img = game_state.sprite_textures[path]
        self.stats = {DMG: damage, DEF: defence, HP: health, HPMAX: health}
        self.name = name
        self.game = game_state
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.hit = game_state.sounds[hitsound]
        if xpos == ypos == 0:
            self.xpos, self.ypos = get_clear_tile(game_state)
        else:
            self.xpos = xpos
            self.ypos = ypos
        if group is None:
            group = self.game.groups[0]
        super().__init__(
            img, x=(xpos - 1) * tile_width, y=(ypos - 1) * tile_height,
            batch=game_state.sprites, group=group,
            usage='dynamic', subpixel=False
        )

        # po całościowej konstrukcji normalizujemy rozmiar
        self.scale_x /= self.width / self.tile_width
        self.scale_y /= self.height / self.tile_height

    def update_pos(self):
        self.update(
            x=(self.xpos - 1) * self.tile_width,
            y=(self.ypos - 1) * self.tile_height
        )

    def on_damage(self, damage, source):
        self.stats[HP] -= damage
        self.game.xprint(source.name, 'attacks', self.name,
                         'for', damage, 'damage.')

    def attack(self, target):
        target.on_damage(max(self.stats[DMG] - target.stats[DEF], 1), self)


class Player(Creature):
    def __init__(self, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None):
        super().__init__('player', tile_width, tile_height,
                         game_state, xpos=xpos, ypos=ypos,
                         group=group, name='Player')
        self.game.pc = self
        self.stats[EXP] = self.stats[G] = 0
        self.stats[LV] = 1
        self.stats[NLV] = 50
        self.inv = {}
        self.status_indicator = Label(
            x=self.game.game_window.width,
            y=self.game.game_window.height - 40,
            width=100, multiline=True, font_name=SANS,
            font_size=20, anchor_x='right', anchor_y='top',
            batch=self.game.game_window.main_batch
        )

    def move(self, dx, dy):
        new_x = self.xpos + dx
        new_y = self.ypos + dy
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
        # source.hit.play()
        if self.stats[HP] <= 0:
            self.game.game_window.lose()
        if self.stats[HP] < 3:
            self.game.pc.image = self.game.sprite_textures['player_h']

    def update_status(self):
        self.status_indicator.text = f'''HP: {self.stats[HP]}/{self.stats[HPMAX]}
level {self.stats[LV]}
EXP: {self.stats[EXP]}/{self.stats[NLV]}
ATK: {self.stats[DMG]}
DEF: {self.stats[DEF]}
{self.stats[G]} G'''

    def normalize(self):
        self.stats[HPMAX] = max(1, self.stats[HPMAX])
        self.stats[HP] = max(min(self.stats[HP], self.stats[HPMAX]), 1)
        self.update_status()

    def heal(self, points=1):
        self.stats[HP] += points
        if self.stats[HP] >= 3:
            self.image = self.game.sprite_textures['player']
        self.normalize()

    def attack(self, target):
        super().attack(target)
        if self.stats[EXP] >= self.stats[NLV]:
            self.levelup()

    def levelup(self):
        self.stats[LV] += 1
        self.stats[EXP] -= self.stats[NLV]
        self.stats[NLV] = self.stats[LV] * 50
        if self.stats[LV] % 2 == 1:
            self.stats[DMG] += 1
        else:
            self.stats[HPMAX] += 1
            self.heal()


class Enemy(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None, health=3,
                 move_pattern=still, move_params=(), name='enemy',
                 gold=1, exp=1, hitsound='bandit_hit'):
        super().__init__(path, tile_width, tile_height, game_state,
                         xpos=xpos, ypos=ypos, group=group,
                         health=health, name=name, hitsound=hitsound)
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
        """
        # niedziałający kod leczenia się przeciwników
        if dx == 0 and dy == 0:
            if self.stats[HP] < self.stats[HPMAX]:
                self.stats[HP] += 1
        """
        new_x = self.xpos + dx
        new_y = self.ypos + dy
        if (
                self.game.pc.xpos == new_x
                and self.game.pc.ypos == new_y
        ):
            self.attack(self.game.pc)
            if self.cycle:
                self.move_pattern = chain([(dx, dy)], self.move_pattern)
        elif (
                0 < new_x < self.game.width - 1
                and 0 < new_y < self.game.height - 1
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

    def on_damage(self, damage, source: Creature):
        super().on_damage(damage, source)
        if self.stats[HP] <= 0:
            self.game.enemies.remove(self)
            if source == self.game.pc:
                source.stats[G] += self.stats[G]
                source.stats[EXP] += self.stats[EXP]
            # item.Item.from_JSON('items/nugget.json', self.game,
            #                    xpos=self.xpos, ypos=self.ypos)
            self.delete()
            return None
        self.healthbar.scale_x = self.stats[HP]/self.stats[HPMAX]
        self.healthbar.draw()

    def update_pos(self):
        super().update_pos()
        self.healthbar.x = self.x
        self.healthbar.y = self.y

    def delete(self):
        self.healthbar.delete()
        return super().delete()

    @staticmethod
    def from_json(path, game, xp=0, yp=0):
        with open(path, 'r') as json:
            base_stats = loads(''.join(json.readlines()))

        if xp == yp == 0:
            xp, yp = get_clear_tile(game)
        ret = Enemy(tile_height=24, tile_width=24, game_state=game,
                    xpos=xp, ypos=yp, **base_stats)
        for stat in LEVELED_STATS:
            ret.stats[stat] *= 1 + LEVELING_FACTOR * \
                game.stage * (2 * game.difficulty + 1)
        for stat in RANDOMIZED_STATS:
            ret.stats[stat] *= normalvariate(1, VAR)
        for stat in LEVELED_STATS | RANDOMIZED_STATS:
            ret.stats[stat] = int(ret.stats[stat])


def add_enemies(game):
    primary_bandit_type = ['enemies/bandit_coward.json', 'enemies/bandit_goldenrule.json',
                           'enemies/bandit_wary.json', 'enemies/bandit_fierce.json']
    secondary_bandit_type = ['enemies/bandit_goldenrule.json', 'enemies/bandit_wary.json',
                             'enemies/bandit_fierce.json', 'enemies/bandit_fierce.json']
    guard_type = ['enemies/guardian_glasses.json', 'enemies/guardian_angry.json', 'enemies/guardian_unlucky.json',
                  'enemies/guardian_door.json']

    corridors = game.width // 3 // game.cell_size
    cells = game.height // game.cell_size - 2

    if game.stage == 5:
        for cor in range(corridors):
            for cell in range(cells):
                if (cor == room(game.pc)[1]-1 and cell == 0):
                    pass
                elif (cor == game.end_staircase and cell == cells-1):
                    pass
                else:
                    Enemy.from_json('enemies/guardian_standard.json', game, xp=cor * 15 + 7,
                                    yp=(cell + 1) * 5 + 2)
        Enemy.from_json('enemies/guardian_door.json', game,
                        xp=7 + 15 * game.end_staircase, yp=game.height - 6)

    else:
        for cor in range(corridors):
            for side in range(2):
                for cell in range(cells):
                    rand = randint(0, 4)
                    if rand == 0:
                        Enemy.from_json(secondary_bandit_type[game.stage - 1], game, xp=cor * 15 + side * 10 + 2,
                                        yp=(cell + 1) * 5 + 2)
                    else:
                        Enemy.from_json(primary_bandit_type[game.stage - 1], game, xp=cor * 15 + side * 10 + 2,
                                        yp=(cell + 1) * 5 + 2)
        Enemy.from_json(guard_type[game.stage - 1], game,
                        xp=7 + 15 * game.end_staircase, yp=game.height - 6)
        if game.stage == 3:
            Enemy.from_json('enemies/guardian_chasing.json', game,
                            xp=game.pc.xpos, yp=game.pc.ypos - 1)
