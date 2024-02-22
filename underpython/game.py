from underpython import *
from base import Game as _Game

del Game


class Game(_Game):
    def __init__(self, player: Player, monsters: list[Monster], waves: list[Wave]):
        self.hook = Hooks()
        self.inventory = Inventory()
        self.player = player
        self.monsters = monsters
        self.waves = waves
        self.wave_no = 0

    def build(self):
        pass

    def go(self):
        pass



