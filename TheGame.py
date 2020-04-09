from __future__ import division
from pyglet.window import key
import pyglet

pyglet.resource.path = ["img"]
pyglet.resource.reindex()

player_img = pyglet.resource.image("pc_sprite.png")

game_window = pyglet.window.Window(
    width=800,
    height=650,
    caption="A game like Rogue"
)

game_window.set_mouse_visible(False)
pyglet.gl.glClearColor(0.4, 0.4, 1, 1)

player = pyglet.sprite.Sprite(player_img, x=400, y=0)
player_x = 0
player_y = 0
player_speed = 50
player_direction = key.UP
can_move_flag = True
movement_flag = False

@game_window.event
def on_draw():
    game_window.clear()
    player.draw()

@game_window.event
def on_key_press(symbol, modifiers):
    global player_x, player_y, player_direction, can_move_flag, movement_flag
    movement_flag = True
    if symbol != player_direction:
        player_direction = symbol
        print("kierunek: ",player_direction)
        can_move_flag = False
    else:
        if player_direction == key.LEFT:
            player_x = -player_speed
            player_y = 0
        elif player_direction == key.RIGHT:
            player_x = player_speed
            player_y = 0
        elif player_direction == key.UP:
            player_x = 0
            player_y = player_speed
        elif player_direction == key.DOWN:
            player_x = 0
            player_y = -player_speed
        elif player_direction == key.SPACE:
            player_x = 0
            player_y = 0

def move(dt):
    global can_move_flag, movement_flag, player_x, player_y
    if can_move_flag and movement_flag:
        player.x += player_x
        player.y += player_y
        player_x = 0
        player_y = 0
        can_move_flag = False

def update(dt):
    global can_move_flag
    can_move_flag = True

if __name__ == '__main__':
    pyglet.clock.schedule_interval(move, 0.01)
    pyglet.clock.schedule_interval(update, 1)
    pyglet.app.run()
