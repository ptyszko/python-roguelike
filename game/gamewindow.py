import pyglet
from util.levelgen import generate_level
from util import keys, tile, fonts, colors
from . import creature
from random import randint


class Game(pyglet.window.Window):
    def __init__(self, game_state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(0, 0)
        self.game_state = game_state
        game_state.game_window = self

        # ładowanie tile-ów (tymczasowe)
        self.floor = game_state.tile_textures['floor']
        self.wall = game_state.tile_textures['wall']
        self.stairs = game_state.tile_textures['stairs']
        self.bars = game_state.tile_textures['bars']
        self.rubble = game_state.tile_textures['rubble']

        # do wyciemnienia przy fow
        """self.dark_floor = game_state.tile_textures['floor']
        self.dark_wall = game_state.tile_textures['wall']
        self.dark_stairs = game_state.tile_textures['stairs']
        self.dark_bars = game_state.tile_textures['bars']
        self.dark_rubble = game_state.tile_textures['rubble']"""

        self.tile_width = self.floor.width
        self.tile_height = self.floor.height
        self.main_batch = pyglet.graphics.Batch()

        self.time_elapsed = 0
        self.time_to_move = game_state.timeout_limit

        # korekcja rozmiaru okna
        self.width = (game_state.width-2) * self.tile_width + 100
        self.height = (game_state.height-2) * self.tile_height + 40
        game_state.status_bar = pyglet.text.Label(
            x=0, y=self.height, anchor_y='top', batch=self.main_batch,
            font_name=fonts.SANS, font_size=20
        )

        self.pc = (creature.Player(
            self.tile_width, self.tile_height,
            xpos=1, ypos=1,
            game_state=self.game_state
        ))

        self.tile_types = {
            tile.WALL: self.wall,
            tile.C_FLOOR: self.floor,
            tile.P_FLOOR: self.floor,
            tile.STARTPOINT: self.floor,
            tile.U_STAIRS: self.stairs,
            tile.D_STAIRS: self.stairs,
            tile.BARS: self.bars,
            tile.STONE: self.rubble,
        }
        self.background = pyglet.image.Texture.create(
            height=self.height,
            width=self.width,
            rectangle=True
        )

        self.push_handlers(on_key_press=self.key_pressed)
        self.clear()
        if game_state.move_timeout:
            self.timer = pyglet.text.Label(
                '{0:>.1f}'.format(self.time_to_move),
                font_name=fonts.MONO, font_size=20,
                anchor_x='right', anchor_y='top',
                y=self.height, x=self.width,
                batch=self.main_batch
            )
        pyglet.clock.schedule_interval(self.time_step, 1/30)
        self.speedrun_counter = pyglet.text.Label(
            '0:00.00', font_name=fonts.MONO, font_size=20,
            color=colors.SEMI_WHITE, batch=self.main_batch
        )
        self.draw_stage(0, False)

    def draw_stage(self, start_staircase, start_direction_up):
        if self.game_state.move_timeout:
            pyglet.clock.unschedule(self.time_step)
            self.time_to_move = self.game_state.timeout_limit
        self.game_state.new_stage()
        self.clear()

        if self.game_state.stage > self.game_state.stages:
            self.win_screen()
            return None
        self.set_caption(f'Stage {self.game_state.stage}')

        height = self.game_state.height
        width = self.game_state.width
        self.game_state.map, self.game_state.layout, self.game_state.end_staircase = generate_level(
            self.game_state, start_staircase, start_direction_up)
        for ycoord, row in enumerate(self.game_state.map[1:-1], 1):
            for xcoord, cur_tile in enumerate(row[1:-1], 1):
                try:
                    if cur_tile == tile.STARTPOINT:
                        self.pc.xpos = xcoord
                        self.pc.ypos = ycoord
                    self.background.blit_into(
                        source=self.tile_types[cur_tile],
                        x=(xcoord-1)*self.tile_width,
                        y=(ycoord-1)*self.tile_height,
                        z=0
                    )
                except KeyError:
                    # błędne i puste tile nie są rysowane w ogóle
                    pass
        self.background.blit(0, 0)
        self.pc.update_pos()
        self.pc.update_status()
        creature.add_enemies(self.game_state)
        self.game_state.sprites.draw()
        if self.game_state.move_timeout:
            pyglet.clock.schedule_interval(self.time_step, 1/30)

    def key_pressed(self, symbol, modifier):
        self.game_state.xprint()
        self.redraw()
        if symbol in keys.DIRECTIONAL:
            self.pc.move(*keys.DIRECTIONS_DICT[symbol])
        elif symbol == keys.SPACE:
            self.pc.heal()
        self.update()
        if self.game_state.next_stage:
            start_staircase = (self.pc.xpos - 5) // 15
            start_direction_up = True
            if self.pc.ypos > 15:
                start_direction_up = False
            self.draw_stage(start_staircase, start_direction_up)

    def win_screen(self):  # PLACEHOLDER
        pyglet.clock.unschedule(self.time_step)
        self.set_caption('END')
        self.pc.delete()
        pyglet.text.Label(
            'You win!\n'
            + 'Your time was:\n'
            + '{:2d}:{:02d}:{:02d}.{:02d}'.format(
                int(self.time_elapsed) // 360000 % 60,
                (int(self.time_elapsed) // 6000) % 60,
                (int(self.time_elapsed) // 100) % 60,
                int(self.time_elapsed) % 100
            ),
            font_name=fonts.SERIF, font_size=50,
            x=self.width//2, y=self.height//2,
            anchor_x='center', anchor_y='center',
            multiline=True, align='center',
            width=self.width
        ).draw()

        self.pop_handlers()
        self.push_handlers(on_key_press=lambda *_: pyglet.app.exit())

    def lose(self):
        self.clear()
        pyglet.clock.unschedule(self.time_step)
        self.set_caption('FAIL')
        pyglet.text.Label(
            'You lose! :(', font_name=fonts.SERIF,
            font_size=50, x=self.width//2, y=self.height//2,
            anchor_x='center', anchor_y='center',
        ).draw()

        self.pop_handlers()
        self.push_handlers(on_key_press=lambda *_: pyglet.app.exit())

    def update(self):
        [en.move() for en in self.game_state.enemies]
        self.time_to_move = self.game_state.timeout_limit

    def time_step(self, dt):
        if self.game_state.move_timeout:
            self.time_to_move -= dt
            self.timer.text = '{0:>.1f}'.format(self.time_to_move)
            if self.time_to_move < 0:
                self.update()

        self.time_elapsed += dt * 100
        self.speedrun_counter.text = '{:2d}:{:02d}:{:02d}.{:02d}'.format(
            int(self.time_elapsed) // 360000,
            (int(self.time_elapsed) // 6000) % 60,
            (int(self.time_elapsed) // 100) % 60,
            int(self.time_elapsed) % 100
        )
        self.redraw()

    def redraw(self):
        self.clear()
        self.background.blit(0, 0)
        self.game_state.sprites.draw()
        self.main_batch.draw()
