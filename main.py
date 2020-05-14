#!/usr/bin/python3
import pyglet
from game.mainmenu import MainMenu
from time import sleep


class GameState:
    def __init__(self):
        self.map = None
        self.stage = 1
        self.game_window = None
        self.pc = None
        self.next_stage = False
        self.move_timeout = True
        self.timeout_limit = 3  # sekundy
        self.enemies = set()
        self.consumables = set()
        self.equippables = set()
        self.sprites = pyglet.graphics.Batch()
        self.items = pyglet.graphics.Batch()
        self.stages = 10
        self.cell_size = 5
        self.width = 45  # w tile-ach, wielokrotność 3*sell_size
        self.height = 30  # wielokrotność cell_size
        self.status_bar = None
        self.difficulty = 0
        self.groups = [pyglet.graphics.OrderedGroup(0),
                       pyglet.graphics.OrderedGroup(1)]

    def change_size(self, param, change):
        if param == 'width' and self.width > self.cell_size*3:
            self.width += change * self.cell_size * 3
        elif self.height > self.cell_size*3:
            self.height += change * self.cell_size

    def change_timeout(self, change):
        if self.timeout_limit + change < -0.05:
            pass
        elif abs(self.timeout_limit + change) <= 0.05:
            self.move_timeout = False
            self.timeout_limit = 0
        else:
            self.timeout_limit += change
            
    def change_diff(self, change):
        self.difficulty = max(self.difficulty+change, 0)

    def xprint(self, *args, sep=' '):
        self.status_bar.text = sep.join(str(a) for a in args)
        
    def new_stage(self):
        for a in self.enemies | self.consumables | self.equippables:
            a.delete()
        self.enemies=set()
        self.consumables = set()
        self.equippables = set()
        self.next_stage = False
        


game = GameState()


if __name__ == "__main__":
    MainMenu(game)
    pyglet.app.run()
