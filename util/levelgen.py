from typing import List
from .tile import *
from random import randint
from .MazeGenerator import floor
<<<<<<< HEAD
# do zamienienia przez generację poziomów
def generate_level(width, height, start_staircase, start_direction_up) -> List[List[str]]:
=======

# do zamienienia przez generację poziomów


def generate_level(width, height) -> List[List[str]]:
>>>>>>> small_changes
    ret = []
    for i in range(height):
        ret.append([])
        '''for j in range(width):
            if i*j == 0 or i == height-1 or j == width-1:
                ret[i].append(WALL)
            else:
                ret[i].append(C_FLOOR)'''
<<<<<<< HEAD
    return add_game_elems(ret, width, height, start_staircase, start_direction_up)
def add_game_elems(map_tiles, width, height, start_staircase, start_direction_up):
    cell_size = 5
    corridors = width//15
    cells = height//5 - 2
    map_tiles, layout = floor(cell_size, corridors,
                              cells, start_staircase, start_direction_up)
    #print(f'height: {len(map_tiles)}, width: {len(map_tiles[0])}')
    return map_tiles
# koniec części do zamienienia
def get_clear_tile(game):
    """zwraca tile po którym gracz może chodzić,
=======
    return add_game_elems(ret, width, height)


def add_game_elems(map_tiles, width, height):
    start_staircase = 0
    start_direction_up = True
    cell_size = 3
    corridors = width//9
    cells = height//3 - 2
    map_tiles, layout = floor(cell_size, corridors,
                              cells, start_staircase, start_direction_up)
    # print(f'height: {len(map_tiles)}, width: {len(map_tiles[0])}')
    return map_tiles
# koniec części do zamienienia


def get_clear_tile(game):
    """zwraca tile po którym gracz może chodzić, 
>>>>>>> small_changes
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
<<<<<<< HEAD
=======


>>>>>>> small_changes
"""
c - podłoga korytarza
W - ściana
f - podłoga celi
b - krata
d - schody dół
u - schody góra
S - kamień
"""
