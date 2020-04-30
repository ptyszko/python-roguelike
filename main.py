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
        self.enemies = []
        self.creatures = pyglet.graphics.Batch()
        self.stages = 10
        self.width = 45  # w tile-ach, wielokrotność 15
        self.height = 30  # wielokrotność 5
        self.status_bar = None

    def change_size(self, param, change):
        if param == 'width' and self.width + change >= 9:
            self.width += change
        elif self.height + change >= 9:
            self.height += change

    def change_timeout(self, change):
        if self.timeout_limit + change < -0.05:
            pass
        elif abs(self.timeout_limit + change) <= 0.05:
            self.move_timeout = False
            self.timeout_limit = 0
        else:
            self.timeout_limit += change

    def xprint(self, *args: tuple, **kwargs: dict):
        sep = kwargs.get('sep', ' ')
        self.status_bar.text = sep.join(str(a) for a in args)


game = GameState()


if __name__ == "__main__":
    MainMenu(game)
    pyglet.app.run()
