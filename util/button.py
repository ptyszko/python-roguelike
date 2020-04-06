from pyglet.text import Label
from util.fonts import SANS
from util.colors import WHITE


class Button(Label):
    def __init__(self, text='', bold=False, italic=False, color=WHITE,
                 x=0, y=0, width=None, height=None, align='left',
                 multiline=False, dpi=None, batch=None, group=None,
                 action=lambda: None):
        super().__init__(text=text, font_name=SANS, font_size=30,
                         bold=bold, italic=italic, color=color, x=x,
                         y=y, width=width, height=height,
                         anchor_x='center', anchor_y='center',
                         align=align, multiline=multiline, dpi=dpi,
                         batch=batch, group=group)
        self.action = action

    def __call__(self):
        return self.action()
