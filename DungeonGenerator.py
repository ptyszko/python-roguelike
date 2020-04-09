import pyglet
import pymunk
import numpy
from pymunk.pyglet_util import DrawOptions
from pyglet.window import key
from pyglet.gl import *
from scipy.spatial import Delaunay
import networkx as nx

def round(number, grid_size):
    return numpy.floor(((number + grid_size - 1) / grid_size)) * grid_size

def get_random_point(radius, x_offset, y_offset, grid_size):
    fi = 2*numpy.pi*numpy.random.uniform()
    r = radius*numpy.random.uniform()
    x_position = round((x_offset+r*numpy.cos(fi))*grid_size,grid_size)
    y_position = round((y_offset+r*numpy.sin(fi))*grid_size,grid_size)
    return x_position, y_position

def get_random_polygon(radius, x_offset, y_offset, grid_size, x_size, y_size):
    x_offset *= grid_size
    y_offset *= grid_size
    x_position, y_position = get_random_point(radius, x_offset, y_offset, grid_size)
    body = pymunk.Body(1,float("infinity"),body_type=pymunk.Body.DYNAMIC)
    body.position = (x_position, y_position)
    poly = pymunk.Poly.create_box(body, size=(x_size*grid_size,y_size*grid_size))
    return x_position, y_position, body, poly

window = pyglet.window.Window(700, 700, "Pymunk Tester", resizable = True)
options = DrawOptions()
space = pymunk.Space()

grid = 4

room_number = 80
room_size_mean = 10
room_size_sd = 4

room_list = [] # lista par [body, poly]
room_volume_list = []
position_list = []
room_volume_threshold = 1.75

for i in range(room_number):
    x_size = numpy.random.normal(loc=room_size_mean, scale=room_size_sd)
    y_size = numpy.random.normal(loc=room_size_mean, scale=room_size_sd)
    x_position, y_position, body, poly = get_random_polygon(15,20,20,grid,x_size,y_size)
    room_list.append([body,poly])
    position_list.append((x_position,y_position))
    room_volume_list.append(x_size*y_size)
    space.add(body,poly)

room_volume_mean = numpy.mean(room_volume_list)
final_room_list = []
final_position_list = []

for i in range(room_number):
    if room_volume_list[i] > room_volume_threshold * room_volume_mean:
        room_list[i][1].color = (255,0,0)
        final_room_list.append(room_list[i])
        final_position_list.append(position_list[i])

dungeon_tree = Delaunay(final_position_list)

G = nx.Graph()
G.add_nodes_from(range(len(final_room_list[0])))

def triangulation_neighbors(dungeon_tree, G):
    for i in range(len(dungeon_tree.simplices)):
        triangle = dungeon_tree.simplices[i]
        G.add_edges_from([(triangle[0],triangle[1]),(triangle[0],triangle[2]),(triangle[1],triangle[2])])

triangulation_neighbors(dungeon_tree,G)

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    if val > 0: return 1
    else: return -1

def dist(a,b):
    return numpy.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def dist_line_point(x,y,p):
    return numpy.absolute(((y[1]-x[1])*p[0]-(y[0]-x[0])*p[1]+y[0]*x[1]-y[1]*x[0])/dist(x,y))

def two_lines_intersect(line1, line2):
    o = line1[0]
    x = line2[0]
    y = line2[1]
    z = line1[1]
    if not(orientation(o, x, y) == orientation(o, x, z) and orientation(o, x, y) == orientation(o, z, y)): return False
    if dist(o,z) < dist_line_point(x,y,o): return False
    return True

def line_room_collision(line,room,position):
    lines_room = []
    for i in range(3):
        lines_room.append(((room[1].get_vertices()[i].x,room[1].get_vertices()[i].y),(room[1].get_vertices()[i+1].x,room[1].get_vertices()[i+1].y)))
    lines_room.append(((room[1].get_vertices()[0].x,room[1].get_vertices()[0].y),(room[1].get_vertices()[3].x,room[1].get_vertices()[3].y)))
    for i in range(4):
        lines_room[i] += position
        if not two_lines_intersect(line,lines_room[i]): return False
    return True

def optimal_rooms(room_list,position_list,G):
    result = []
    for i in range(len(room_list)):
        if line_room_collision(((0,0),(900,900)),room_list[i],position_list[i]): result.append(room_list[i])
    return result

optimal_room_list = optimal_rooms(room_list,position_list,G)

#for i in range(len(room_list)):
 #   space.remove(room_list[i][0],room_list[i][1])

for i in range(len(optimal_room_list)):
    space.add(optimal_room_list[i][0],optimal_room_list[i][1])


"""
boss_number = 3
boss_size = 10

encounter_number = 15
encounter_size = 6

corridor_size = 2
corridor_number = 600

for i in range(boss_number):
    x_size = round(numpy.random.uniform((boss_size-3),(boss_size+3)),1)
    y_size = round(numpy.random.uniform((boss_size-3),(boss_size+3)),1)
    body, poly = get_random_polygon(20,0,0,grid,x_size,y_size)
    poly.color = (255,0,0)
    space.add(body,poly)

x_size = round(numpy.random.uniform((boss_size-3),(boss_size+3)),1)
y_size = round(numpy.random.uniform((boss_size-3),(boss_size+3)),1)
body, poly = get_random_polygon(0,0,0,grid,2,2)
poly.color = (255,255,255)
space.add(body,poly)

for i in range(encounter_number):
    x_size = round(numpy.random.uniform((encounter_size-2),(encounter_size+2)),1)
    y_size = round(numpy.random.uniform((encounter_size-2),(encounter_size+2)),1)
    body, poly = get_random_polygon(20,0,0,grid,x_size,y_size)
    poly.color = (255,69,0)
    space.add(body,poly)

for i in range(corridor_number):
    x_size = round(numpy.random.uniform((corridor_size-1),(corridor_size+1)),1)
    y_size = round(numpy.random.uniform((corridor_size-1),(corridor_size+1)),1)
    body, poly = get_random_polygon(20,0,0,grid,x_size,y_size)
    poly.color = (0,0,255)
    space.add(body,poly)
"""

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    window.clear()
    space.debug_draw(options)
#    glBegin(GL_LINES)
 #   glVertex2f(0,0)
  #  glVertex2f(900,900)
   # glEnd()

@window.event
def on_key_press(keys, modifiers):
    if keys==key.DOWN:
        glTranslatef(0,50,0)
    if keys==key.UP:
        glTranslatef(0,-50,0)
    if keys==key.RIGHT:
        glTranslatef(-50,0,0)
    if keys==key.LEFT:
        glTranslatef(50,0,0)

def update(dt):
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
