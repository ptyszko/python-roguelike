import pyglet
from util.levelgen import generate_level
from util import keys, tile
from .creature import Player
from random import randint


class GameEnd(BaseException):
    pass


class Game(pyglet.window.Window):
    def __init__(self, game_state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        game_state.game_window = self

        # ładowanie tile-ów (tymczasowe)
        self.floor = pyglet.image.load('img/dirt-floor.png').get_image_data()
        self.wall = pyglet.image.load('img/dirt-wall.png').get_image_data()
        self.stairs = pyglet.image.load('img/stairs.png').get_image_data()
        self.tile_width = self.floor.width
        self.tile_height = self.floor.height
        self.pc = (
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
        self.draw_stage()

    def draw_stage(self):
        self.game_state.next_stage = False
        self.clear()
        if self.game_state.stage > 5:
            self.win_screen()
            return None
        self.set_caption(f'Stage {self.game_state.stage}')

        # może później funkcja(stage_no)?
        height = self.height // self.tile_height + 2
        width = self.width // self.tile_width + 2
        self.game_state.map = generate_level(width, height)
        for ycoord, row in enumerate(self.game_state.map[1:-1], 1):
            for xcoord, cur_tile in enumerate(row[1:-1], 1):
                try:
                    self.background.blit_into(
                        source=self.tile_types[cur_tile],
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
            if self.game_state.map[ycoord][xcoord] == tile.FLOOR:
                break
        self.pc.xpos = xcoord
        self.pc.ypos = ycoord
        self.pc.update_pos()
        self.pc.draw()

    def key_pressed(self, symbol, modifier):
        if symbol in keys.DIRECTIONAL:
            self.pc.move(*keys.DIRECTIONS_DICT[symbol])
            print(f'moved {keys.DIRECTIONS_DICT[symbol]}')
        if self.game_state.next_stage:
            self.draw_stage()
        else:
            self.clear()
            self.background.blit(0, 0)
            self.pc.draw() # w przyszłości Batch ze wszyskimi stworzeniami (może)
        
    def win_screen(self): #PLACEHOLDER
        from util.fonts import SERIF
        from time import sleep
        
        self.set_caption('END')
        self.pc.delete()
        pyglet.text.Label(
            'You Win!',
            font_name=SERIF, font_size=50,
            x=self.width//2, y=self.height//2,
            anchor_x='center', anchor_y='center'
        ).draw()
        
