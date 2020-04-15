import networkx as nx
import matplotlib.pyplot as plt
import random

def in_maze(width, height, position):
    if position[0]<0 or position[0]>=width or position[1]<0 or position[1]>=height: return False
    return True

def maze(width, height, start):
    nodes = dict()
    for a in range(width):
        for b in range(height):
            nodes[(a,b)] = (False, None)
    nodes[start] = (True, float("inf"))
    wynik = nx.Graph()
    wynik.add_nodes_from(nodes)
    maze_recur(width, height, nodes, wynik, start)
    return wynik

def maze_recur(width, height, nodes, maze, current):
    if(current == float("inf")): return()
    direction_map = [(1,0),(0,-1),(-1,0),(0,1)]
    random.shuffle(direction_map)
    for direction in range(4):
        neighbor = (current[0] + direction_map[direction][0], current[1] + direction_map[direction][1])
        if(in_maze(width, height, neighbor) and nodes[neighbor][0]==False):
            maze.add_edge(current,neighbor)
            nodes[neighbor] = (True,current)
            maze_recur(width, height, nodes, maze, neighbor)

def rooms_layout(corridors, cells, start_staircase):
    return(maze(corridors * 3, cells + 2, (1 + 3 * start_staircase, cells + 1)))

"""
c - podłoga korytarza
W - ściana
f - podłoga celi
b - krata
d - schody dół
u - schody góra
S - kamień
"""

def left_room(size):
    wynik = [['f' for row in range(size)] for col in range(size)]
    for row in range(size):
        wynik[0][row] = 'W'
        wynik[size-1][row] = 'W'
    for col in range(size):
        wynik[col][0] = 'W'
        wynik[col][size-1] = 'b'
    return wynik

def right_room(size):
    wynik = [['f' for row in range(size)] for col in range(size)]
    for row in range(size):
        wynik[0][row] = 'W'
        wynik[size-1][row] = 'W'
    for col in range(size):
        wynik[col][0] = 'b'
        wynik[col][size-1] = 'W'
    return wynik

def add_room(cell_size, map, position, left):
    if left:
        room = left_room(cell_size)
    else:
        room = right_room(cell_size)
    for row in range(cell_size):
        for col in range(cell_size):
            map[cell_size * position[0] + row][cell_size * position[1] + col] = room[row][col]

def add_corridor_slice(cell_size, map, position):
    add_room(cell_size, map, (position[0], 3*position[1]), True)
    add_room(cell_size, map, (position[0], 3*position[1]+2), False)

def add_staircase(cell_size, map, position, up):
    if up:
        stairs = 'u'
    else:
        stairs = 'd'
    for row in range(cell_size):
        for col in range(cell_size):
            map[cell_size * position[0] + row][cell_size * position[1] + col] = stairs

def add_staircase_slice(cell_size, map, position, up):
    for s in range(3):
        add_staircase(cell_size, map, (position[0], 3*position[1]+s), up)

def default_floor(cell_size, corridors, cells):
    wynik = [['c' for row in range(cell_size * corridors * 3)] for col in range(cell_size * (cells + 2))]
    for corridor in range(corridors):
        add_staircase_slice(cell_size, wynik, (0, corridor), True)
        for slice in range(1, cells+1):
            add_corridor_slice(cell_size, wynik, (slice, corridor))
        add_staircase_slice(cell_size, wynik, (cells+1, corridor), False)
    return wynik

def room_type(position):
    if (position[0] % 3) == 0: return 'lef'
    elif (position[0] % 3) == 1: return 'cor'
    else: return 'rig'

def add_stone(map, cell_size, position, direction):
    if direction == (1,0):
        for col in range(cell_size):
            map[cell_size * position[0]][cell_size * position[1] + col] = 'S'
    elif direction == (-1,0):
        for col in range(cell_size):
            map[cell_size * position[0] + cell_size - 1][cell_size * position[1] + col] = 'S'
    elif direction == (0,-1):
        for row in range(cell_size):
            map[cell_size * position[0] + row][cell_size * position[1]] = 'S'
    elif direction == (0,1):
        for row in range(cell_size):
            map[cell_size * position[0] + row][cell_size * position[1] + cell_size - 1] = 'S'

def remove_wall(map, cell_size, position, direction):
    if direction == (1,0):
        map[cell_size*position[0]][cell_size*position[1] + cell_size//2] = 'f'
    if direction == (-1,0):
        map[cell_size*position[0] + cell_size - 1][cell_size*position[1] + cell_size//2] = 'f'
    if direction == (0,-1):
        map[cell_size*position[0] + cell_size//2][cell_size*position[1]] = 'f'
    if direction == (0,1):
        map[cell_size*position[0] + cell_size//2][cell_size*position[1] + cell_size - 1] = 'f'

def floor(cell_size, corridors, cells, test_randomization):
    floor = default_floor(cell_size, corridors, cells)
    layout = rooms_layout(corridors, cells, 0)
    if not test_randomization: return floor, layout
    direction_map = [(1,0),(0,-1),(-1,0),(0,1)]
    rows = cells + 2
    cols = corridors * 3
    for row in range(1, rows-1):
        for col in range(cols):
            for direction in range(4):
                neighbor = (row+direction_map[direction][0], col + direction_map[direction][1])
                if in_maze(rows, cols, neighbor):
                    if layout.has_edge((row,col),neighbor):
                        remove_wall(floor, cell_size, (row,col), direction_map[direction])
                    else:
                        if room_type((row,col)) == 'cor':
                            add_stone(floor, cell_size, (row,col), direction_map[direction])
    return floor, layout

def main():
    dungeon, layout = floor(3, 3, 4, True)
    pos = dict( (n, n) for n in layout.nodes() )
    nx.draw(layout, with_labels=True, pos = pos, font_weight='bold')
    plt.savefig("mygraph.png")
    for i in range(len(dungeon)):
        print(''.join(dungeon[i]))

main()