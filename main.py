import pyglet
from game.mainmenu import MainMenu


game = {}


if __name__ == "__main__":
    MainMenu(game, resizable=True)
    pyglet.app.run()
