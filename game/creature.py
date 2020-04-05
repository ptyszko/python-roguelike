from pyglet.sprite import Sprite
from pyglet.image import load
from abc import ABC


class Creature(Sprite, ABC):
    def __init__(self, path, tile_width, tile_height,
                 xpos=0, ypos=0,  batch=None, group=None):
        img = load(path)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self._xpos = xpos
        self._ypos = ypos
        super().__init__(img, x=xpos*tile_width, y=ypos*tile_height,
                         batch=batch, group=group, usage='dynamic', subpixel=False)
        
    def update_position(self):
        self.x = self._xpos * self.tile_width
        self.y = self._ypos * self.tile_height
        
    def set_xpos(self, val):
        self._xpos = val
        self.update_position()
        
    def set_ypos(self, val):
        self._ypos = val
        self.update_position()
    
    def get_xpos(self):
        return self._xpos
    
    def get_ypos(self):
        return self._ypos
    
    xpos = property(get_xpos, set_xpos)
    ypos = property(get_ypos, set_ypos)


class Player(Creature):
    pass
