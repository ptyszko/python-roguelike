import pyglet
from util.levelgen import generate_level
from util import keys, tile
from game.creature import Player
from random import randint


class Game(pyglet.window.Window):
    def __init__(self, game_state: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        game_state['game_window'] = self
        self.game_state['level'] = 1

        # ładowanie tile-ów (tymczasowe)
        self.floor = pyglet.image.load('img/dirt-floor.png').get_image_data()
        self.wall = pyglet.image.load('img/dirt-wall.png').get_image_data()
        self.stairs = pyglet.image.load('img/stairs.png').get_image_data()
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
            tile.FLOOR: self.floor,
            tile.STAIRS: self.stairs,
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
        self.clear()
        self.set_caption(f'Level {level_no}')
        # może później funkcja(level_no)?
        height = self.height // self.tile_height + 2
        width = self.width // self.tile_width + 2
        self.game_state['map'] = tiles = generate_level(width, height)
        for ycoord in range(1, height-1):
            for xcoord in range(1, width-1):
                try:
                    self.background.blit_into(
                        source=self.tile_types[tiles[ycoord][xcoord]],
                        x=(xcoord-1)*self.tile_width,
                        y=(ycoord-1)*self.tile_height,
                        z=0
                    )
                except KeyError:
                    pass
        self.background.blit(0, 0)
        while True:
            xcoord = randint(1, width-1)
            ycoord = randint(1, height-1)
            if tiles[ycoord][xcoord] == tile.FLOOR:
                break
        self.pc.xpos = xcoord
        self.pc.ypos = ycoord
        self.pc.update_pos()
        self.pc.draw()

    def key_pressed(self, symbol, modifier):
        if symbol in keys.DIRECTIONAL:
            self.pc.move(*keys.DIRECTIONS_DICT[symbol])
        self.clear()
        self.background.blit(0, 0)
        self.pc.draw()
