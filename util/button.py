from pyglet.text import Label
from .fonts import SANS
from .colors import WHITE


class Button(Label):
    def __init__(self, text='', bold=False, italic=False, color=WHITE,
                 x=0, y=0, align='center', batch=None, multiline=False,
                 action=lambda: None, game_state=None, width=None):
        super().__init__(text='', font_name=SANS, font_size=30,
                         bold=bold, italic=italic, color=color, x=x,
                         y=y, anchor_x='center', anchor_y='top',
                         align=align, batch=batch, multiline=multiline,
                         width=width)
        self.action = action
        self.game = game_state
        self.base_text = text
        self.calculate()

    def __call__(self, action=None):
        ret = (self.action() if type(self.action) != dict
               else self.action[action]())
        self.calculate()
        return ret

    def calculate(self):
        self.text = self.base_text.format(**locals())
