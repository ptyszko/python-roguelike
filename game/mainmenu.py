import pyglet
from util import colors, fonts
from util.button import Button
from game.gamewindow import Game


class MainMenu(pyglet.window.Window):
    def __init__(self, game_state: set, *args, **kwargs):
        kwargs['visible'] = False
        super().__init__(*args, **kwargs)
        self.game_state = game_state

        self.set_minimum_size(width=480, height=320)
        self.background = pyglet.image.load('img/wood_floor.png')
        self.batch = pyglet.graphics.Batch()

        # create title and buttons
        def_style = {'x': self.width//2, 'batch': self.batch}
        self.title = pyglet.text.Label(
            'SOME ROGUELIKE',
            font_name=fonts.SERIF,
            font_size=40, y=self.height-30,
            anchor_x='center', anchor_y='center',
            **def_style
        )

        '''self.start = pyglet.text.Label(
            'Start game',
            font_name=fonts.SANS, font_size=30,
            y=220, color=colors.GREEN,
            **def_style
        )

        self.menu = pyglet.text.Label(
            'Settings',
            font_name=fonts.SANS, font_size=30,
            y=100, **def_style
        )

        self.exit = pyglet.text.Label(
            'Quit',
            font_name=fonts.SANS, font_size=30,
            y=40, **def_style
        )'''
        self.start = Button(
            text='Start Game',
            y=220, color=colors.GREEN,
            action=self.new_game,
            **def_style
        )
        self.menu = Button(
            text='Settings', y=100,
            action=self.open_settings,
            **def_style
        )
        self.exit = Button(
            text='Quit', y=40,
            action=self.close,
            **def_style
        )

        self.buttons = [self.start, self.menu, self.exit]
        self.active_button = 0
        self.set_visible()

    def on_draw(self):
        self.clear()
        bcg = pyglet.image.TileableTexture.create_for_image(self.background)
        bcg.blit_tiled(0, 0, 0, width=self.width, height=self.height)
        self.batch.draw()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        for button in self.buttons:
            button.x = width//2
        self.title.x = width//2
        self.title.y = height - 50

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == pyglet.window.key.UP:
            self.buttons[self.active_button].color = colors.WHITE
            self.active_button = ((self.active_button-1)
                                  % len(self.buttons))
            self.buttons[self.active_button].color = colors.GREEN
        elif symbol == pyglet.window.key.DOWN:
            self.buttons[self.active_button].color = colors.WHITE
            self.active_button = ((self.active_button+1)
                                  % len(self.buttons))
            self.buttons[self.active_button].color = colors.GREEN
        elif symbol == pyglet.window.key.ENTER:
            self.buttons[self.active_button]()
        elif symbol == pyglet.window.key.F1:
            print(self)

    def open_settings(self):
        # TODO: Ustawienia
        print('settings')

    def new_game(self):
        Game(
            width=self.width,
            height=self.height,
            game_state=self.game_state,
            caption='Level -1'  # placeholder
        )
        self.close()