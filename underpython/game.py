from underpython import *
import pygame as pg
import os


class Game:
    def __init__(self, player: Player, monsters: list[Monster], waves: list[Wave], resource_path: str = None):
        self.hook = Hooks()
        self.inventory = Inventory()
        self.player = player
        self.monsters = monsters
        self.waves = waves
        self.wave_no = 0
        self.graphics: dict[str, pg.surface.Surface] = {}
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.rp = resource_path
        self.state = 'START'

    def _load_graphics(self):
        path = os.path.join(self.rp, 'images')
        for f in os.listdir(path):
            self.graphics[f.split('.')[0]] = pg.image.load(os.path.join(path, f))

    def _load_sounds(self):
        path = os.path.join(self.rp, 'sounds')
        for f in os.listdir(path):
            self.sounds[f.split('.')[0]] = pg.mixer.Sound(os.path.join(path, f))

    def build(self):
        self._load_graphics()
        self._load_sounds()

    def go(self):
        pass


GAME: Game
