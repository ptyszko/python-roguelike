import pyglet
from util.levelgen import generate_level
from util import keys, tile
from game.creature import Player


class Game(pyglet.window.Window):
    def __init__(self, game_state: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        game_state['game_window'] = self

        # ładowanie tile-ów (tymczasowe)
        self.floor = pyglet.image.load('img/dirt.png').get_image_data()
        self.wall = pyglet.image.load('img/obsidian_wall.png').get_image_data()
        self.tile_width = self.floor.width
        self.tile_height = self.floor.height
        game_state['pc'] = self.pc = (
            Player('img/player.png',
                   self.tile_width, self.tile_height,
                   xpos=1, ypos=1,
                   game_state=self.game_state)
        )

        # korekcja rozmiaru okna
        self.width -= self.width % self.tile_width
        self.height -= self.height % self.tile_height
        self.tile_types = {
            tile.WALL: self.wall,
            tile.FLOOR: self.floor
        }
        self.background = pyglet.image.Texture.create(
            height=self.height,
            width=self.width,
            rectangle=True
        )

        self.push_handlers(on_key_press=self.key_pressed)

        self.clear()
        self.draw_level(1)

    def draw_level(self, level_no: int):
        self.set_caption(f'Level {level_no}')
        # może później funkcja(level_no)?
        height = self.height // self.tile_height
        width = self.width // self.tile_width  # j.w
        self.game_state['map'] = tiles = generate_level(width, height)
        for ycoord in range(height):
            for xcoord in range(width):
                self.background.blit_into(
                    source=self.tile_types[tiles[ycoord][xcoord]],
                    x=xcoord*self.tile_width,
                    y=ycoord*self.tile_height,
                    z=0
                )
        self.background.blit(0, 0)
        self.pc.draw()

    def key_pressed(self, symbol, modifier):
        if symbol in keys.DIRECTIONAL:
            self.pc.move(*keys.DIRECTIONS_DICT[symbol])
        self.clear()
        self.background.blit(0, 0)
        self.pc.draw()
