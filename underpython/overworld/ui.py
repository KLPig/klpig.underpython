from underpython.attacks import SoulRect
from underpython.displayer import UI
from underpython import chanel
from . import game
import pygame as pg


def _ui__nothing(**args):
    pass


class ui(SoulRect):
    class dialoger(UI.dialoger):
        def _get_key_events(self):
            return game.GAME.key_events

        def __init__(self, string: str, left, kwargs):
            self.arg = {'no_skip': False, 'tpc': 0, 'color': (255, 255, 255)}
            self.left = 50
            for k, v in kwargs.items():
                if k in self.args:
                    self.arg[k] = v
                elif k == 'left':
                    self.left = v
            cmd = ''
            writing_cmd = False
            self.tasks = []
            self.l_left = left
            self.idx = 0
            self._timer = 0
            self.texts = [self.st]
            self.line = 0
            self.end = False
            self.res = False
            for c in string:
                if c == ']':
                    writing_cmd = False
                    self.tasks.append('[[' + cmd)
                    cmd = ''
                    continue
                elif c == '[':
                    writing_cmd = True
                    continue
                if writing_cmd:
                    cmd += c
                else:
                    self.tasks.append(c)

        def _display(self):
            r = game.GAME.ui.exp_rect
            top = r.top + 10
            for text in self.texts:
                txt = game.GAME.font.render(text, True, self.arg['color'])
                txt_rect = txt.get_rect()
                txt_rect.topleft = (r.left + self.left, top)
                game.GAME.dis().blit(txt, txt_rect)
                top += 100

    class selector(UI.selector):
        def _get_key_events(self):
            return game.GAME.key_events

        def _setup_rect(self):
            game.GAME.ui.exp_rect.width = 400
            game.GAME.ui.exp_rect.height = 500

        def _render_fonts(self, options):
            for opt in options:
                txt = game.GAME.font.render(opt, True, self.arg['color'])
                txt_rect = txt.get_rect()
                txt_rect.centerx = 640
                self.sr.append((txt, txt_rect))
        def _display(self):
            i = 0
            for t, r in self.sr:
                if self.idx - 3 < i < self.idx + 3:
                    r.centerx = game.GAME.ui.rect.centerx
                    r.centery = (game.GAME.ui.rect.centery +
                                 (i - self._pos / 10) * 80)
                    t.set_alpha(255 - min(abs(r.centery - game.GAME.ui.rect.centery) // 2, 255))
                    game.GAME.dis[0].blit(t, r)
                i += 1

    def close(self, nothing = 6, **args):
        self.exp_rect = pg.Rect(0, 0, 1, 1)

    def __init__(self):
        self.end_func = None
        d = self.dialoger
        self._dialog: d | None = None
        super().__init__()
        self.pause: bool = False
        self.close()

    def update(self):
        gg = game.GAME
        pg.draw.rect(gg.dis[0], (0, 0, 0), self.rect)
        pg.draw.rect(gg.dis[0], (255, 255, 255), self.rect, 8)
        super()._update()
        if self._dialog is not None:
            self.pause = True
            if self._dialog.end:
                if type(self._dialog) is self.selector:
                    chanel.Chanel.play(gg.sounds['menuconfirm'])
                if len(self._dialog.l_left) > 1:
                    self._dialog = self.dialoger(self._dialog.l_left[0],
                                                 self._dialog.l_left[1:],
                                                 self._dialog.arg)
                    return
                elif len(self._dialog.l_left):
                    self._dialog = self.dialoger(self._dialog.l_left[0], [],
                                                 self._dialog.arg)
                    return
                res = self._dialog.res
                del self._dialog
                self._dialog = None
                self.end_func(res)
            else:
                if type(self._dialog) is self.selector:
                    if pg.K_x in gg.key_events:
                        chanel.Chanel.play(gg.sounds['menuconfirm'])
                        res = self._dialog.res
                        del self._dialog
                        self._dialog = None
                        self.end_func(res)
                        return

                self._dialog.update()
        else:
            self.pause = False
            if pg.K_c in game.GAME.key_events:
                self.choose(['STAT', 'ITEM', 'CELL'], end_func=self.handle_stats)
                self.exp_rect.width = 250
                self.exp_rect.height = 400
                self.exp_rect.midleft = (0, 480)

    def dialog(self, strings: list[str], end_func=__nothing, **kwargs):
        self._dialog = self.dialoger(strings[0], strings[1: ], kwargs)
        self.end_func = end_func

    def choose(self, options: list[str], end_func=__nothing, **kwargs):
        self._dialog = self.selector(options, kwargs)
        self.end_func = end_func

    def handle_item(self, res):
        if res == 0:
            self.choose(game.GAME.player.inv.inventory, end_func=game.GAME.player._handle_check)
        elif res == 1:
            self.choose(game.GAME.player.inv.inventory, end_func=game.GAME.player._handle_inv)
        else:
            self.close()

    def handle_stats(self, res):
        if res == 0:
            p = game.GAME.player
            self.exp_rect = pg.Rect(40, 650, 1200, 300)
            self.dialog([f'\'{p.data.name}\',[endl]{p.data.at} AT, {p.data.df} DF.',
                         f'{p.data.hp}/{p.data.max_hp}HP({int(p.data.hp / p.data.max_hp * 100)}%).[endl]'
                         f'{p.g} GOLD, LV{p.data.lv}({p.exp} EXP).', p.desc], end_func=self.close)
        elif res == 1:
            self.choose(['CHECK', 'USE'], end_func=self.handle_item)
        else:
            self.close()
