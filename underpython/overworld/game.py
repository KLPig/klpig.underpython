import importlib
import os.path
from . import maps, player, ui
from underpython import displayer, base, chanel, game
import pygame as pg
import sys
import os
import random


def load_image(res_path: str, name: str) -> pg.Surface:
    return pg.image.load(os.path.join(os.path.join(res_path, 'images'), name + '.png'))


class Game:
    Ts = 30

    def __init__(self, resource_path: str, _player: player.Player, _map: maps.Map):
        pg.init()
        self.dis = displayer.Displayer()
        self.map = _map
        self.rp = resource_path
        self.player = _player
        self.dis_camera = (0, 0)
        self.tick = 0
        self.key_events = []
        self.hook = base.Hooks()
        self.ui = ui.ui()
        self.sounds = {}
        self.font = pg.font.SysFont('dtm-sans', 75)
        pg.display.set_caption('UNDERTALE')
        pg.display.set_icon(pg.transform.scale_by(pg.image.load(os.path.join(resource_path, 'images/ui.icon.png')), 4))
        self._load_sounds()

    def _load_sounds(self):
        path = os.path.join(self.rp, 'sounds')
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if (os.path.isfile(img) and
                    (img.endswith('.wav') or img.endswith('.mp3') or img.endswith('.ogg'))):
                self.sounds[f.split('.')[0]] = pg.mixer.Sound(img)

    def _update(self):
        self.dis.clear()
        if not self.ui.pause:
            self.player._move()
        self.map.get_now()._update()
        for c in self.map.get_now().chara:
            c._update()
        self.player._update()
        self.ui.update()
        self.dis._update()

    def go(self):
        self._loop()

    def _loop(self):
        tick = 0
        while True:
            if not self.tick:
                self.st = pg.time.get_ticks()
            self.key_events = []
            self.tick = tick
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.hook.on_game_quit()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    self.key_events.append(event.key)
            self._update()
            d = pg.time.get_ticks() - self.st
            if d <= self.Ts * (self.tick + 1):
                pg.time.delay(self.Ts * (self.tick + 1) - d)
            else:
                """
                raise base.UnderPythonWarning(
                    'fps was lower than the set one, losing speeds.'
                )"""
            tick += 1

    def quit(self):
        pg.quit()
        sys.exit()

    def run_game(self, name):
        p = pg.mixer.Sound(os.path.join(self.rp, 'sounds/BeginBattle%d.wav' % random.randint(1, 3))).play()
        w = self.dis.window
        w.fill((0, 0, 0))
        splash = pg.transform.scale_by(pg.image.load('splash.png'), 5)
        rect = splash.get_rect()
        rect.center = w.get_rect().center
        w.blit(splash, rect)
        pg.display.update()
        while p.get_busy():
            pass
        _game = importlib.import_module(name)
        importlib.reload(_game)
        gg = game.GAME
        gg.player.write_data(self.player.data)
        gg.inventory.write_data(self.player.inv)
        gg.go(True, _game.__name__)
        while not gg.game_success:
            importlib.reload(_game)
            gg.player.write_data(self.player.data)
            gg.inventory.write_data(self.player.inv)
            gg.go(True)
        self.player.data.write_data(gg.player)
        self.player.inv.write_data(gg.inventory)
        chanel.MChanel.stop()
        self.st = pg.time.get_ticks() - self.Ts * (self.tick + 1)
        return gg.route




def set_game(_game: Game):
    global GAME
    GAME = _game


GAME: Game
