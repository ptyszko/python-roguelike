import pyglet
class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = pyglet.image.load('img/wood_floor.png')
        self.title = pyglet.text.Label(
            'some roguelike',
            font_name='Helvetica', font_size=30,
            anchor_x='center', anchor_y='center',
            x=self.width//2, y=self.height//2
        )
        print(type(self.background))
        print(f'({self.background.height},{self.background.width})')
    
    def on_draw(self):
        self.clear()
        bcg = pyglet.image.TileableTexture.create_for_image(self.background)
        bcg.blit_tiled(0, 0, 0, width=self.width, height=self.height)
        self.title.draw()
        
    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        if symbol == pyglet.window.key.UP:
            background.x+=10;
        
win = Game()

pyglet.app.run()