from lib import pyglet


class MainMenu(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        kwargs['visible'] = False
        super().__init__(*args, **kwargs)
        self.set_minimum_size(width=480, height=320)
        self.background = pyglet.image.load('img/wood_floor.png')
        self.batch = pyglet.graphics.Batch()
        def_fonts = ['Helvetica', 'Arial', 'sans-serif']
        def_style = {'anchor_x': 'center', 'anchor_y': 'center',
                     'x': self.width//2, 'batch': self.batch}

        self.title = pyglet.text.Label(
            'SOME ROGUELIKE',
            font_name=['Liberation Serif', 'Times New Roman', 'serif'],
            font_size=40, y=self.height-30,
            **def_style
        )

        self.start = pyglet.text.Label(
            'Start game',
            font_name=def_fonts, font_size=30,
            y=220, color=(0, 255, 0, 255),
            **def_style
        )

        self.menu = pyglet.text.Label(
            'Settings',
            font_name=def_fonts, font_size=30,
            y=100, **def_style
        )

        self.exit = pyglet.text.Label(
            'Quit',
            font_name=def_fonts, font_size=30,
            y=40, **def_style
        )

        self.buttons = [self.start, self.menu, self.exit]
        self.active_button = 0
        self.set_visible()

    def on_draw(self):
        self.clear()
        bcg = pyglet.image.TileableTexture.create_for_image(self.background)
        bcg.blit_tiled(0, 0, 0, width=self.width, height=self.height)
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == pyglet.window.key.UP:
            self.buttons[self.active_button].color = (255, 255, 255, 255)
            self.active_button = (self.active_button-1) % len(self.buttons)
            self.buttons[self.active_button].color = (0, 255, 0, 255)
        elif symbol == pyglet.window.key.DOWN:
            self.buttons[self.active_button].color = (255, 255, 255, 255)
            self.active_button = (self.active_button+1) % len(self.buttons)
            self.buttons[self.active_button].color = (0, 255, 0, 255)
        elif symbol == pyglet.window.key.ENTER:
            button = self.buttons[self.active_button]
            if button == self.start:
                # TODO: Nowa gra
                pyglet.window.Window(
                    caption='tu bedzie okno nowej gry',
                    width=self.width,
                    height=self.height
                )
                self.close()

            elif button == self.menu:
                #TODO: Ustawienia
                print('settings')
            else:
                pyglet.app.exit()
        elif symbol == pyglet.window.key.F1:
            print(self)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        for button in self.buttons:
            button.x = width//2
        self.title.x = width//2
        self.title.y = height - 50


if __name__ == "__main__":
    win = MainMenu(resizable=True)
    pyglet.app.run()
