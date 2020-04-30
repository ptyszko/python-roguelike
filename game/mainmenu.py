import pyglet
from util import colors, fonts
from util.button import Button
from .gamewindow import Game
from pyglet.window.key import UP, DOWN, LEFT, RIGHT, ENTER


class MainMenu(pyglet.window.Window):
    def __init__(self, game_state, *args, **kwargs):
        kwargs['visible'] = False
        super().__init__(*args, **kwargs)
        self.game_state = game_state

        self.set_minimum_size(width=480, height=320)
        self.background = pyglet.image.load('img/dirt-floor.png')
        self.main_screen = pyglet.graphics.Batch()
        self.settings_screen = pyglet.graphics.Batch()

        # create title and buttons
        def_style = {'x': self.width//2, 'batch': self.main_screen}

        pyglet.text.Label(
            text='SOME ROGUELIKE', font_name=fonts.SERIF,
            font_size=40, y=self.height-30,
            anchor_x='center', anchor_y='center',
            **def_style
        )

        pyglet.text.Label(
            text='SETTINGS', font_name=fonts.SERIF,
            font_size=40, y=self.height-30,
            anchor_x='center', anchor_y='center',
            x=self.width//2, batch=self.settings_screen
        )

        def_style['game_state'] = game_state
        self.start = Button(
            text='Start Game', y=240,
            action=self.new_game,
            **def_style
        )
        self.menu = Button(
            text='Settings', y=120,
            action=self.open_settings,
            **def_style
        )
        self.exit = Button(
            text='Quit', y=60,
            action=self.close,
            **def_style
        )

        def_style['batch'] = self.settings_screen

        self.done = Button(
            text='Done', y=300,
            action=self.main,
            **def_style
        )

        self.win_w = Button(
            text='Map width: {self.game.width}', y=240,
            action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_size('width', 9),
                'left': lambda: self.game_state.change_size('width', -9)
            },
            **def_style
        )

        self.win_h = Button(
            text='Map height: {self.game.height}', y=180,
            action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_size('height', 3),
                'left': lambda: self.game_state.change_size('height', -3)
            },
            **def_style
        )

        self.timeout = Button(
            text='Move timeout: {self.game.timeout_limit:.1f}s'
            + '\n(0 means no timeout)',
            y=120, action={
                'enter': lambda: None,
                'right': lambda: self.game_state.change_timeout(0.1),
                'left': lambda: self.game_state.change_timeout(-0.1)
            },
            multiline=True, width=self.width,
            **def_style
        )

        self.bcg = pyglet.image.TileableTexture.create_for_image(
            self.background)

        self.visible_buttons = []
        self.main()
        self.set_visible()

    def on_draw(self):
        self.clear()
        self.bcg.blit_tiled(0, 0, 0, width=self.width, height=self.height)
        self.active.draw()

    '''def on_resize(self, width, height):
        super().on_resize(width, height)
        for button in self.visible_buttons:
            button.x = width//2
        self.title.x = width//2
        self.title.y = height - 50'''

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
        # TODO: Ustawienia
        print('settings')
        for b in self.visible_buttons:
            b.color = colors.WHITE
        self.done.color = colors.GREEN
        self.visible_buttons = [self.done, self.win_w,
                                self.win_h, self.timeout]
        self.active_button = 0
        self.active = self.settings_screen

    def main(self):
        for b in self.visible_buttons:
            b.color = colors.WHITE
        self.start.color = colors.GREEN
        self.visible_buttons = [self.start, self.menu, self.exit]
        self.active_button = 0
        self.active = self.main_screen
