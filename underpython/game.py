from underpython import player, monster, wave, base, inventory, displayer
import pygame as pg
import os


class Game:
    def __init__(self, _player: player.Player, monsters: list[monster.Monster], waves: list[type(wave.Wave)], resource_path: str = None):
        self.hook = base.Hooks()
        self.inventory = inventory.Inventory()
        self.player = _player
        self.monsters = monsters
        self.waves = waves
        self.wave_no = 0
        self.graphics: dict[str, pg.surface.Surface] = {}
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.rp = resource_path
        self.state = 'START'
        self.displayer = displayer.Displayer()

    def _load_graphics(self):
        path = os.path.join(self.rp, 'images')
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if os.path.isfile(img) and img.endswith('.png'):
                self.graphics[f.removesuffix('.png')] = pg.image.load(img)

    def _load_sounds(self):
        return
        path = os.path.join(self.rp, 'sounds')
        for f in os.listdir(path):
            self.sounds[f.split('.')[0]] = pg.mixer.Sound(os.path.join(path, f))

    def build(self):
        self._load_graphics()
        self._load_sounds()

    def go(self):
        pass


GAME: Game
