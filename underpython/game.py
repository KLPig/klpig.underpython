import copy
from underpython import player, monster, wave, base, inventory, displayer, chanel
import pygame as pg
import os
import time
import sys


class Game:
    Ts = 50
    states = ['SELECT', 'FIGHT', 'ACT', 'ITEM', 'MERCY', 'SAVE', 'ATTACK', 'DIALOG', 'SOUL', 'END', 'SAVE']

    def set_event(self, func):
        if func.__name__ in self.hook.__dir__():
            self.hook.__setattr__(func.__name__, func)

    def __init__(self, _player: player.Player, monsters: list[monster.Monster], waves: list[type(wave.Wave)], resource_path: str = None, save_enabled: bool = False):
        pg.init()
        f = sys.modules['__main__'].__file__
        print('UnderPython Game Init: ', f.removeprefix(os.path.dirname(f)))
        print('Init basics...', end='\r')
        self.theme_color: tuple[int, int, int] = (255, 255, 255)
        self.confirm_color: tuple[int, int, int] = (255, 255, 0)
        self.color_changed = False
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
        print('Initing displayer', end='\r')
        self.displayer = displayer.Displayer()
        self.st_time: type(time.time())
        self.ui = displayer.UI(save_enabled)
        print('\rLoading fonts: uidamagetext', end='')
        self.ui.dmg_font.load(self.rp, 'uidamagetext')
        print('\rLoading fonts: uibattlesmall', end='')
        self.ui.state_font.load(self.rp, 'uibattlesmall')
        for name in self.ui.names:
            print('\rLoading fonts:', name, end='')
            self.ui.speech_fonts[name].load(self.rp, name)
        self.key_events = []
        self.state = 'SELECT'
        self.tick = 0
        print('\rLoading fonts:', 'dtm sans', end='')
        self.font = pg.font.SysFont('dtm-sans', 75)
        self.route: base.GameMethod | None = None
        self.subrun = False
        self.game_success = False
        self.before_player_dialog: str | None = None
        self.blank_col = pg.PixelArray(copy.copy(pg.image.load(os.path.join(os.path.join(resource_path, 'images'), 'ui.system.blank.png'))))[0, 0]
        print()
        print('Init done.')

    def _load_graphics(self):
        path = os.path.join(self.rp, 'images')
        m = len(os.listdir(path))
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if os.path.isfile(img) and img.endswith('.png'):
                print('\rLoading', f, end='')
                self.graphics[f.removesuffix('.png')] = pg.image.load(img)

    def _load_sounds(self):
        path = os.path.join(self.rp, 'sounds')
        for f in os.listdir(path):
            img = os.path.join(path, f)
            if (os.path.isfile(img) and
                    (img.endswith('.wav') or img.endswith('.mp3') or img.endswith('.ogg'))):
                print('\rLoading', f, end='')
                self.sounds[f.split('.')[0]] = pg.mixer.Sound(img)

    def build(self):
        print('Source Building...')
        print('Loading graphics:')
        self._load_graphics()
        print()
        print('Loading sounds:')
        self._load_sounds()
        print()
        print('Setting up windows...')
        self.displayer.set_window()
        print('Source building done.')

    def go(self, subrun=False, name=''):
        print('Process: ', end='')
        if subrun:
            print('subprocess', name)
        else:
            f = sys.modules['__main__'].__file__
            print('root process', f.removeprefix(os.path.dirname(f)))
        self.subrun = subrun
        self._loop()

    def _update(self, tick: int):
        if tick == 1:
            self.hook.on_game_go()
        if self.ui._state == 'end_game':
            if not self.subrun:
                pg.quit()
                sys.exit()
        self.tick = tick
        self.displayer.clear()
        if self.player.hp == 0 and self.state != 'END':
            chanel.Chanel.play(self.sounds['heartbeatbreaker'])
            chanel.MChanel.play(self.sounds['mus_gameover'])
            self.player.hp = self.player.max_hp
            self.ui.dialogs(['GAME OVER[endl]Do not loose hope![endl]%s, [endl]stay determined!' % self.player.name], 'end_game', no_skip=True, tpc=10)
            self.hook.on_game_lost()
            self.ui.soul_rect.exp_rect = pg.rect.Rect(0, 0, 1280, 960)
            self.set_state('END')
        for enemy in self.monsters:
            if enemy.defeat is not None:
                if self.route is None:
                    self.route = enemy.defeat
                elif self.route != enemy.defeat:
                    self.route = base.NEUTRAL_ROUTE
                self.monsters.remove(enemy)
                if not len(self.monsters):
                    self.hook.on_game_won(self.route)
                    self.game_success = True
                    if self.route is base.GENOCIDE_ROUTE:
                        chanel.Chanel.play(self.sounds['levelup'])
                        self.ui.dialog('You won. =)', 'end_game', color=(255, 0, 0))
                    else:
                        self.ui.dialog('You won.', 'end_game')
                    self.set_state('END')
                continue
            enemy.ani._update()
        self.ui._update()
        self.displayer._update()

    def change_color(self, main_col: None | tuple[int, int, int] = None, conf_col: None | tuple[int, int, int] = None):
        if main_col is not None:
            self.theme_color = main_col
        if conf_col is not None:
            self.confirm_color = conf_col
        self.color_changed = True

    def _loop(self):
        tick = 0
        while True:
            if not self.tick:
                self.st = pg.time.get_ticks()
            self.key_events = []
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.hook.on_game_quit()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    self.key_events.append(event.key)
            self._update(tick)
            if self.ui._state == 'end_game':
                break
            self.color_changed = False
            d = pg.time.get_ticks() - self.st
            if d <= self.Ts * (self.tick + 1):
                pg.time.delay(self.Ts * (self.tick + 1) - d)
            else:
                """
                raise base.UnderPythonWarning(
                    'fps was lower than the set one, losing speeds.'
                )"""
            print('\rTime', d, ', Tick', self.tick, end=' ')
            num = 0
            if wave.Wave.ins_attack is not None:
                for a in wave.Wave.ins_attack:
                    num += len(a.attacks)
            print('No of atks', num, end='')
            tick += 1

    def set_state(self, state: str):
        if state in self.states:
            self.state = state


    def blank(self, size: tuple[int, int]) -> pg.Surface:
        return pg.transform.scale_by(GAME.graphics['ui.system.blank'], size)



GAME: Game


def write_game(game: Game):
    global GAME
    GAME = game

def blank(size: tuple[int, int]) -> pg.Surface:
    return pg.transform.scale_by(copy.copy(pg.image.load(os.path.join('./resources/images', 'ui.system.blank.png'))), size)
