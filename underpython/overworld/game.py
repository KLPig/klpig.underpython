import importlib
import os.path
from . import maps, player
from underpython import displayer, base, chanel
import pygame as pg
import sys
import os
import random


class Game:
    Ts = 30

    def __init__(self, resource_path: str, _player: player.Player, _map: maps.Map):
        pg.init()
        self.dis = displayer.Displayer()
        self.map = _map
        self.rp = resource_path
        self.chara = []
        self.player = _player
        self.dis_camera = (0, 0)
        self.tick = 0
        self.key_events = []
        self.hook = base.Hooks()
        pg.display.set_caption('UNDERTALE')
        pg.display.set_icon(pg.transform.scale_by(pg.image.load(os.path.join(resource_path, 'images/ui.icon.png')), 4))

    def _update(self):
        self.dis.clear()
        self.map.get_now()._update()
        self.player._update()
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
        game = importlib.import_module(name)
        importlib.reload(game)
        game.GAME.go(True)
        chanel.MChanel.stop()
        del game.GAME
        self.st = pg.time.get_ticks() - self.Ts * (self.tick + 1)


def set_game(_game: Game):
    global GAME
    GAME = _game


GAME: Game
