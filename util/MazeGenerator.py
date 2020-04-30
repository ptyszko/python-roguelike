import networkx as nx
import matplotlib.pyplot as plt
import random
from .tile import *


def in_maze(width, height, position):
    if (
        position[0] < 0
        or position[0] >= height
        or position[1] < 0
        or position[1] >= width
    ):
        return False
    return True


def maze(width, height, start):
    nodes = dict()
    for a in range(height):
        for b in range(width):
            nodes[(a, b)] = (False, None)
    nodes[start] = (True, float("inf"))
    wynik = nx.Graph()
    wynik.add_nodes_from(nodes)
    maze_recur(width, height, nodes, wynik, start)
    return wynik


def maze_recur(width, height, nodes, maze, current):
    if(current == float("inf")):
        return()
    direction_map = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    random.shuffle(direction_map)
    for direction in range(4):
        neighbor = (current[0] + direction_map[direction][0],
                    current[1] + direction_map[direction][1])
        if in_maze(width, height, neighbor)\
                and nodes[neighbor][0] is False:
            maze.add_edge(current, neighbor)
            nodes[neighbor] = (True, current)
            maze_recur(width, height, nodes, maze, neighbor)


def rooms_layout(corridors, cells, start_staircase, start_direction_up):
    return(maze(corridors * 3, cells,
                (0, 0)))


"""
c - podłoga korytarza
W - ściana
f - podłoga celi
b - krata
d - schody dół
u - schody góra
S - kamień
P - punkt startowy
"""


def left_room(size):
    wynik = [[P_FLOOR for row in range(size)] for col in range(size)]
    for row in range(size):
        wynik[0][row] = WALL
        wynik[size-1][row] = WALL
    for col in range(size):
        wynik[col][0] = WALL
        wynik[col][size-1] = BARS
    return wynik


def right_room(size):
    wynik = [[P_FLOOR for row in range(size)] for col in range(size)]
    for row in range(size):
        wynik[0][row] = WALL
        wynik[size-1][row] = WALL
    for col in range(size):
        wynik[col][0] = BARS
        wynik[col][size-1] = WALL
    return wynik


def add_room(cell_size, map, position, left):
    if left:
        room = left_room(cell_size)
    else:
        room = right_room(cell_size)
    for row in range(cell_size):
        for col in range(cell_size):
            (map[cell_size * position[0] + row]
             [cell_size * position[1] + col]) = room[row][col]


def add_corridor_slice(cell_size, map, position):
    add_room(cell_size, map, (position[0], 3*position[1]), True)
    add_room(cell_size, map, (position[0], 3*position[1]+2), False)


def add_staircase(cell_size, map, position, up):
    if up:
        stairs = U_STAIRS
    else:
        stairs = D_STAIRS
    for row in range(cell_size):
        for col in range(cell_size):
            (map[cell_size * position[0] + row]
             [cell_size * position[1] + col]) = stairs


def add_staircase_slice(cell_size, map, position, up):
    for s in range(3):
        add_staircase(cell_size, map,
                      (position[0], 3*position[1]+s),
                      up)


def default_floor(cell_size, corridors, cells):
    wynik = [[C_FLOOR for row in range(cell_size * corridors * 3)]
             for col
             in range(cell_size * (cells + 2))]
    for corridor in range(corridors):
        add_staircase_slice(cell_size, wynik,
                            (0, corridor), True)
        for slice in range(1, cells+1):
            add_corridor_slice(cell_size, wynik,
                               (slice, corridor))
        add_staircase_slice(cell_size, wynik,
                            (cells+1, corridor), False)
    return wynik


def room_type(position):
    if (position[1] % 3) == 0:
        return 'lef'
    elif (position[1] % 3) == 1:
        return 'cor'
    else:
        return 'rig'


def add_stone(map, cell_size, position, direction):
    if direction == (-1, 0):
        for col in range(cell_size):
            (map[cell_size * position[0]]
             [cell_size * position[1] + col]) = STONE
    elif direction == (1, 0):
        for col in range(cell_size):
            (map[cell_size * position[0] + cell_size - 1]
             [cell_size * position[1] + col]) = STONE
    elif direction == (0, -1):
        for row in range(cell_size):
            (map[cell_size * position[0] + row]
             [cell_size * position[1]]) = STONE
    elif direction == (0, 1):
        for row in range(cell_size):
            (map[cell_size * position[0] + row]
             [cell_size * position[1] + cell_size - 1]) = STONE


def remove_wall(map, cell_size, position, direction):
    if direction == (-1, 0):
        (map[cell_size*position[0]]
         [cell_size*position[1] + cell_size//2]) = P_FLOOR
    if direction == (1, 0):
        (map[cell_size*position[0] + cell_size - 1]
         [cell_size*position[1] + cell_size//2]) = P_FLOOR
    if direction == (0, -1):
        (map[cell_size*position[0] + cell_size//2]
         [cell_size*position[1]]) = P_FLOOR
    if direction == (0, 1):
        (map[cell_size*position[0] + cell_size // 2]
         [cell_size*position[1] + cell_size - 1]) = P_FLOOR


def floor(cell_size, corridors, cells, start_staircase, start_direction_up):
    floor = default_floor(cell_size, corridors, cells)
    layout = rooms_layout(
        corridors, cells, start_staircase, start_direction_up)
    direction_map = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    rows = cells
    cols = corridors * 3
    for row in range(rows):
        for col in range(cols):
            for direction in range(4):
                neighbor = (
                    row + direction_map[direction][0],
                    col + direction_map[direction][1]
                )
                if in_maze(cols, rows, neighbor):
                    if layout.has_edge((row, col), neighbor):
                        remove_wall(floor, cell_size, (row+1, col),
                                    direction_map[direction])
                    else:
                        if room_type((row, col)) == 'cor':
                            add_stone(floor, cell_size, (row+1, col),
                                      direction_map[direction])
    start_row = cells * cell_size + cell_size//2
    start_col = (start_staircase*3+1) * cell_size + cell_size//2
    if not start_direction_up:
        start_row -= (cells-1) * cell_size
    floor[start_row][start_col] = STARTPOINT
    end_staircase = random.randint(0, corridors-1)
    for cor in range(corridors):
        add_stone(floor, cell_size, (0, cor * 3 + 1), (1, 0))
        add_stone(floor, cell_size, (cells+1, cor * 3 + 1), (-1, 0))
    if start_direction_up:
        remove_wall(floor, cell_size, (0, end_staircase * 3 + 1), (1, 0))
    else:
        remove_wall(floor, cell_size,
                    (cells+1, end_staircase * 3 + 1), (-1, 0))
    return floor, layout


'''
def debug_function():
    dungeon, layout = floor(3, 3, 4, True)
    pos = dict((n, n) for n in layout.nodes())
    nx.draw(layout, with_labels=True, pos=pos, font_weight='bold')
    plt.savefig("mygraph.png")
    for i in range(len(dungeon)):
        print(''.join(dungeon[i]))
'''
