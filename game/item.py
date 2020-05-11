import pyglet
from random import randint
from json import loads


class Item(pyglet.sprite.Sprite):
    def __init__(self, path, game, name, stat, effect, xpos=0, ypos=0):
        img = pyglet.image.load(path)
        while xpos == 0 or xpos == game.pc.xpos:
            xpos = randint(1, game.width - 2)
        while ypos == 0 or ypos == game.pc.ypos:
            ypos = randint(game.cell_size, game.height - 1 - game.cell_size)
            
        self.xpos = xpos
        self.ypos = ypos
        super().__init__(img=img, x=self.xpos*24, y=self.ypos*24, batch=game.sprites)
        self.stat = stat
        self.effect = effect
        self._name = name
        self.game = game
    
    @property
    def name(self):
        return f'{self._name} ({self.stat}{self.effect:+d})'

    @staticmethod
    def from_JSON(path, xpos=0, ypos=0):
        """
        Wygląd pliku <item>.json - obiekt z polami:
        
        type = "consumable"|"equippable"
        
        stat = stat gracza który zmienia

        effect = wpływ na powyższy stat
        
        name (opcjonalne) = nazwa przedmiotu / slot w którym jest założony
        
        path = ścieżka do tekstury"""
        with open(path, 'r') as fin:
            specs = loads(''.join(fin.readlines()))

        type = specs.pop('type', '')
        if type == 'consumable':
            return Consumable(xpos=xpos, ypos=ypos, **specs)
        elif type == 'equippable':
            return Equippable(xpos=xpos, ypos=ypos, **specs)


class Consumable(Item):
    def __init__(self, path, game, stat, effect, name='consumable', xpos=0, ypos=0):
        super().__init__(path, game, name, stat, effect, xpos=xpos, ypos=ypos)
        self.game.consumables.add(self)
    
    def consume(self):
        self.game.pc.stats[self.stat] += self.effect
        self.game.xprint(f'consumed {self.name}')
        self.game.consumables.remove(self)
        self.delete()
        
        
class Equippable(Item):
    def __init__(self, path, game, stat, effect, name='equippable', xpos=0, ypos=0):
        super().__init__(path, game, name, stat, effect, xpos=xpos, ypos=ypos)
        self.game.equippables.add(self)
    
    def equip(self):
        equipped_item = self.game.pc.inv.get(self._name, None)
        if equipped_item is not None and equipped_item.effect >= self.effect:
            return None
        elif equipped_item is not None:
            equipped_item.unequip()
        self.game.pc.inv[self._name] = self
        self.game.pc.stats[self.stat] += self.effect
        self.game.pc.normalize()
        self.game.equippables.remove(self)
        self.image(pyglet.image.Texture.create(1,1))
        
    def unequip(self):
        self.game.pc.inv.pop(self._name)
        self.game.pc.stats[self.stat] -= self.effect
        self.game.pc.normalize()
        self.delete()
            