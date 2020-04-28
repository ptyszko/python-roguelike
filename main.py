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
        self.timeout_limit = 3 # sekundy
        self.enemies = []
        self.creatures = pyglet.graphics.Batch()
        self.stages = 3
        self.width = 36 # w tile-ach
        self.height = 24 # j.w


game = GameState()


if __name__ == "__main__":
    win = MainMenu(game)
    pyglet.app.run()
