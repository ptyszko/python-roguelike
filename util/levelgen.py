from typing import List
from .tile import *
from random import randint
from .MazeGenerator import floor

"""
# do zamienienia przez generację poziomów
def generate_level(width, height) -> List[List[str]]:
    ret = []
    for i in range(height):
        ret.append([])
        for j in range(width):
            if i*j == 0 or i == height-1 or j == width-1:
                ret[i].append(WALL)
            else:
                ret[i].append(FLOOR)
    add_game_elems(ret, width, height)
    return ret


def add_game_elems(map_tiles, width, height):
    while True:
        x = randint(1, width-1)
        y = randint(1, height-1)
        if map_tiles[y][x] == FLOOR:
            map_tiles[y][x] = STAIRS
            break
# koniec części do zamienienia
"""

"""
c - podłoga korytarza
W - ściana
f - podłoga celi
b - krata
d - schody dół
u - schody góra
S - kamień
"""

cell_size = 3
corridors = 3
cells = 4
test_randomisation = False
dungeon, layout = floor(cell_size, corridors, cells, test_randomisation)

def get_clear_tile(game):
    """zwraca tile po którym gracz może chodzić, 
    który nie zawiera już innego stworzenia
    """
    x = y = 0
    while (
        game.map[y][x] == WALL 
        or (game.pc.xpos == x and game.pc.ypos == y)
        or any(x == e.xpos and y == e.ypos for e in game.enemies)
    ):
        y = randint(0, len(game.map)-1)
        x = randint(0, len(game.map[0])-1)
    return x,y


if __name__ == "__main__":
    print(generate_level(10, 15))
