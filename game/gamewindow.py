import pyglet
from util.levelgen import generate_level
from game.creature import Player


class Game(pyglet.window.Window):
    def __init__(self, game_state: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        game_state['game_window'] = self

        # ładowanie tile-ów (tymczasowe)
        self.floor = pyglet.image.load('img/wood_floor.png').get_image_data()
        self.wall = pyglet.image.load('img/obsidian_wall.png').get_image_data()
        self.tile_width = self.floor.width
        self.tile_height = self.floor.height
        game_state['pc'] = self.pc = (
            Player('img/player.png', 
                   self.tile_width, self.tile_height, 
                   xpos=1, ypos=1)
        )

        # korekcja rozmiaru okna
        self.width -= self.width % self.tile_width
        self.height -= self.height % self.tile_height
        self.tile_types = {
            '#': self.wall,
            '.': self.floor
        }
        self.background = pyglet.image.Texture.create(
            height=self.height,
            width=self.width,
            rectangle=True
        )
        self.clear()
        self.draw_level(1)

    def draw_level(self, level_no: int):
        self.set_caption(f'Level {level_no}')
        # może później funkcja(level_no)?
        height = self.height // self.tile_height
        width = self.width // self.tile_width  # j.w
        tiles = generate_level(width, height)
        for ycoord in range(height):
            for xcoord in range(width):
                self.background.blit_into(
                    source=self.tile_types[tiles[ycoord][xcoord]],
                    x=xcoord*self.tile_width,
                    y=ycoord*self.tile_height,
                    z=0
                )
        self.background.blit(0,0)
        self.pc.draw()

    def on_key_press(self, key, modifier):
        super().on_key_press(key, modifier)
        # PROBLEM: gdy naciskam przykiski kierunkowe ekran znika ~Paweł 
        if key == pyglet.window.key.UP:
            self.pc.ypos += 1
        elif key == pyglet.window.key.DOWN:
            self.pc.ypos -= 1
        elif key == pyglet.window.key.LEFT:
            self.pc.xpos -= 1
        elif key == pyglet.window.key.RIGHT:
            self.pc.xpos += 1