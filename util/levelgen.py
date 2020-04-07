from typing import List
from .tile import *
from random import randint

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
    
if __name__ == "__main__":
    print(generate_level(10, 15))