from typing import List
from .tile import *
from random import randint
from .mazegenerator import floor
# do zamienienia przez generację poziomów


def generate_level(game_state, start_staircase, start_direction_up):
    cell_size = game_state.cell_size
    corridors = game_state.width // 3 // cell_size
    cells = game_state.height // cell_size - 2
    map_tiles, layout, end_staircase = floor(cell_size, corridors,
                                             cells, start_staircase, start_direction_up)
    print(f'height: {len(map_tiles)}, width: {len(map_tiles[0])}')
    return map_tiles, layout, end_staircase
# koniec części do zamienienia


def get_clear_tile(game):
    """zwraca tile po którym gracz może chodzić,
    który nie zawiera już innego stworzenia
    """
    x = y = 0
    while (
        game.map[y][x] not in FLOOR
        or (game.pc.xpos == x and game.pc.ypos == y)
        or any(x == e.xpos and y == e.ypos for e in game.enemies)
    ):
        y = randint(3, len(game.map)-4)
        x = randint(0, len(game.map[0])-1)
    return x, y


"""
c - podłoga korytarza
W - ściana
f - podłoga celi
b - krata
d - schody dół
u - schody góra
S - kamień
"""
