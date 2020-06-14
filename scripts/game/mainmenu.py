import pyglet
from ..util import colors, fonts
from ..util.button import Button
from .gamewindow import Game
from pyglet.window.key import UP, DOWN, LEFT, RIGHT, ENTER


class MainMenu(pyglet.window.Window):
    def __init__(self, game_state, *args, **kwargs):
        kwargs['visible'] = False
        super().__init__(*args, **kwargs)
        self.game_state = game_state

        self.set_minimum_size(width=480, height=320)
        self.background = game_state.tile_textures['floor']
        self.main_screen = pyglet.graphics.Batch()
        self.settings_screen = pyglet.graphics.Batch()

        # create title and buttons
        def_style = {'x': self.width//2, 'batch': self.main_screen}
        title_style = {'font_name': fonts.SERIF, 'font_size': 40,
                       'y': self.height-30, 'anchor_x': 'center',
                       'anchor_y': 'center'}

        pyglet.text.Label(text='SOME ROGUELIKE', **def_style, **title_style)

        pyglet.text.Label(text='SETTINGS', x=self.width//2,
                          batch=self.settings_screen, **title_style)

        def_style['game_state'] = game_state
        start = Button(
            text='Start Game', y=240,
            action=self.new_game,
            **def_style
        )
        menu = Button(
            text='Settings', y=120,
            action=self.open_settings,
            **def_style
        )
        exit = Button(
            text='Quit', y=60,
            action=self.close,
            **def_style
        )
        self.main_buttons = [start, menu, exit]

        def_style['batch'] = self.settings_screen
        def_style['font_size'] = 20

        done = Button(
            text='Done', y=300,
            action=self.main,
            **def_style
        )
        difficulty = Button(
            text='Difficulty: {self.game.difficulty}', y=200,
            action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_diff(1),
                'left': lambda: self.game_state.change_diff(-1)
            },
            **def_style
        )
        win_w = Button(
            text='Map width: {self.game.width}', y=160,
            action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_size('width', 1),
                'left': lambda: self.game_state.change_size('width', -1)
            },
            **def_style
        )
        win_h = Button(
            text='Map height: {self.game.height}', y=120,
            action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_size('height', 1),
                'left': lambda: self.game_state.change_size('height', -1)
            },
            **def_style
        )
        timeout = Button(
            text='Move timeout: {self.game.timeout_limit:.1f}s'
            + '\n(0 means no timeout)',
            y=80, action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_timeout(0.1),
                'left': lambda: self.game_state.change_timeout(-0.1)
            },
            multiline=True, width=self.width,
            **def_style
        )
        self.settings_buttons = [done, difficulty, win_w,
                                 win_h, timeout]

        self.bcg = pyglet.image.TileableTexture.create_for_image(
            self.background)

        self.visible_buttons = self.main_buttons
        self.main()
        self.set_visible()

    def on_draw(self):
        self.clear()
        self.bcg.blit_tiled(0, 0, 0, width=self.width, height=self.height)
        self.active.draw()

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == UP:
            self.visible_buttons[self.active_button].color = colors.WHITE
            self.active_button = ((self.active_button-1)
                                  % len(self.visible_buttons))
            self.visible_buttons[self.active_button].color = colors.GREEN
        elif symbol == DOWN:
            self.visible_buttons[self.active_button].color = colors.WHITE
            self.active_button = ((self.active_button+1)
                                  % len(self.visible_buttons))
            self.visible_buttons[self.active_button].color = colors.GREEN
        elif symbol == ENTER:
            self.visible_buttons[self.active_button]('enter')
        elif symbol == RIGHT:
            self.visible_buttons[self.active_button]('right')
        elif symbol == LEFT:
            self.visible_buttons[self.active_button]('left')
        elif symbol == pyglet.window.key.F1:
            print(self)

    def new_game(self):
        Game(
            game_state=self.game_state,
            caption='Level -1'  # placeholder
        )
        self.close()

    def open_settings(self):
        for b in self.visible_buttons:
            b.color = colors.WHITE
        self.visible_buttons = self.settings_buttons
        self.active_button = 0
        self.visible_buttons[0].color = colors.GREEN
        self.active = self.settings_screen

    def main(self):
        for b in self.visible_buttons:
            b.color = colors.WHITE
        self.visible_buttons = self.main_buttons
        self.active_button = 0
        self.visible_buttons[0].color = colors.GREEN
        self.active = self.main_screen
