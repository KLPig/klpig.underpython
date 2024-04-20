from underpython import player, monster, wave, base, inventory, displayer
import pygame as pg
import os
import time
import sys


class Game:
    Ts = 30
    states = ['SELECT', 'FIGHT', 'ACT', 'ITEM', 'MERCY', 'SAVE', 'ATTACK', 'DIALOG', 'SOUL']

    def set_event(self, func):
        if func.__name__ in self.hook.__dir__():
            self.hook.__setattr__(func.__name__, func)

    def __init__(self, _player: player.Player, monsters: list[monster.Monster], waves: list[type(wave.Wave)], resource_path: str = None, save_enabled: bool = False):
        pg.init()
        self.ins_wave = 0
        self.hook = base.Hooks()
        self.inventory = inventory.Inventory()
        self.player = _player
        self.monsters = monsters
        self.waves = waves
        self.wave_no = 0
        self.graphics: dict[str, pg.surface.Surface] = {'NULL': pg.surface.Surface((1, 1))}
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.rp = resource_path
        self.state = 'START'
        self.displayer = displayer.Displayer()
        self.st_time: type(time.time())
        self.ui = displayer.UI(save_enabled)
        self.key_events = []
        self.state = 'SELECT'
        self.tick = 0
        self.font = pg.font.SysFont('dtm-sans', 75)

    def _load_graphics(self):
        path = os.path.join(self.rp, 'images')
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if os.path.isfile(img) and img.endswith('.png'):
                self.graphics[f.removesuffix('.png')] = pg.image.load(img)

    def _load_sounds(self):
        path = os.path.join(self.rp, 'sounds')
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if (os.path.isfile(img) and
                    (img.endswith('.wav') or img.endswith('.mp3') or img.endswith('.ogg'))):
                self.sounds[f.split('.')[0]] = pg.mixer.Sound(img)

    def build(self):
        self._load_graphics()
        self._load_sounds()
        self.displayer.set_window()

    def go(self):
        self.st_time = time.time()
        self.st = time.time()
        self._loop()

    def _update(self, tick: int):
        self.tick = tick
        self.displayer.clear()
        self.key_events = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.key_events.append(event.key)
        for enemy in self.monsters:
            enemy.ani._update()
        self.ui._update()
        self.displayer._update()

    def _loop(self):
        tick = 0
        while True:
            self._update(tick)
            d = time.time() - self.st

            if d < self.Ts:
                time.sleep((self.Ts - d) / 1000)
            else:
                raise base.UnderPythonWarning(
                    'fps was lower than the set one, losing speeds.'
                )
            self.st = time.time()
            tick += 1

    def set_state(self, state: str):
        if state in self.states:
            self.state = state


GAME: Game


def write_game(game: Game):
    global GAME
    GAME = game
