from pyglet.sprite import Sprite
from pyglet.image import load
from pyglet.graphics import Batch
from abc import ABC
from util import tile
from util.levelgen import get_clear_tile
from itertools import repeat, chain, cycle as _cycle
from random import choice


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


class Creature(Sprite, ABC):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None, health=5, name='none'):
        img = load(path)
        self.name = name
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

    def on_damage(self, damage, source):
        self.health -= damage
        print(source.name, 'attacks', self.name, 'for', damage, 'damage.')
        
    def attack(self, target):
        damage = 1 # w przyszłości zależne od statystyk (może)
        target.on_damage(damage, self)


class Player(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=1, ypos=1, group=None):
        super().__init__(path, tile_width, tile_height,
                         game_state, xpos=xpos, ypos=ypos,
                         group=group, name='Player')
        self.game.pc = self

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
            self.ypos =new_y
            self.update_pos()
            if (
                self.game.map
                [self.ypos]
                [self.xpos]
            ) in tile.STAIRS:
                self.game.stage += 1
                self.game.next_stage = True
        # print(f'my pos is ({self.xpos}, {self.ypos})')

    def on_damage(self, damage, source):
        super().on_damage(damage, source)
        if self.health <= 0:
            self.game.game_window.lose()


class Enemy(Creature):
    def __init__(self, path, tile_width, tile_height, game_state,
                 xpos=0, ypos=0, group=None, health=5,
                 move_pattern=still, move_params=(), name='enemy'):
        super().__init__(path, tile_width, tile_height, game_state,
                         xpos=xpos, ypos=ypos, group=group,
                         health=health, name=name)
        self.move_pattern = move_pattern(self, *move_params)
        self.cycle = move_pattern == cycle
        self.game.enemies.append(self)

    def move(self):
        dx, dy = next(self.move_pattern)
        new_x = self.xpos+dx
        new_y = self.ypos+dy
        if (
            self.game.pc.xpos == new_x 
            and self.game.pc.ypos == new_y
        ):
            self.attack(self.game.pc)
        elif (
            self.game.map[new_y][new_x]
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

def add_enemies(game):
    # w przyszłości będzie zależne od poziomu
    xp, yp = get_clear_tile(game)
    nest = Enemy('img/enemy.png', 24, 24, game, xpos=xp, ypos=yp)

    xp, yp = get_clear_tile(game)
    slime = Enemy('img/enemy.png', 24, 24, game, xpos=xp, ypos=yp,
                  move_pattern=cycle,
                  move_params=[(0, 1), (0, 0), (0, -1), (0, 0)])

    xp, yp = get_clear_tile(game)
    bat = Enemy('img/enemy.png', 24, 24, game, xpos=xp, ypos=yp,
                move_pattern=random)
