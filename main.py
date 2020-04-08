import pyglet
from game.mainmenu import MainMenu
from game.gamewindow import GameEnd
from time import sleep


class GameState:
    def __init__(self):
        self.map = None
        self.stage = 1
        self.game_window = None
        self.pc = None
        self.next_stage = False


game = GameState()


if __name__ == "__main__":
    MainMenu(game, resizable=True)
    try:
        pyglet.app.run()
    except GameEnd:
        sleep(1.5)
        pyglet.app.exit()
