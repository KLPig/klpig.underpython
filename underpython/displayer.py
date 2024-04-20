from underpython import game, attacks, wave
import pygame as pg
from underpython import animations as ani
import math


class Displayer:
    def __init__(self):
        self.camera = (0, 0, 0)
        self.window = pg.display.set_mode((640, 480), pg.SCALED | pg.RESIZABLE)
        self.surfaces = [pg.surface.Surface((1280, 960))]

    def set_window(self):
        pg.display.set_caption('UNDERTALE')
        pg.display.set_icon(game.GAME.graphics['ui.icon'])

    def clear(self):
        for i in range(len(self.surfaces)):
            self.surfaces[i] = pg.surface.Surface((1280, 960))

    def _update(self):
        self.window.fill((0, 0, 0))
        x, y, r = self.camera
        for surface in self.surfaces:
            scale = min(self.window.get_width() / surface.get_width(),
                        self.window.get_height() / surface.get_height())
            r_surf = pg.transform.scale_by(surface, scale)
            r_surf = pg.transform.rotate(r_surf, r)
            r_surf_rect = r_surf.get_rect()
            r_surf_rect.center = (self.window.get_width() / 2 + x,
                                  self.window.get_height() / 2 + y)
            self.window.blit(r_surf, r_surf_rect)
            break
        pg.display.update()

    def __getitem__(self, idx) -> pg.surface.Surface:
        return self.surfaces[idx]

    def __call__(self) -> pg.surface.Surface:
        return self.surfaces[0]


class UI:
    class dialoger:
        args = ['no-skip', 'tpc', 'color']

        def __init__(self, string: str, kwargs):
            game.GAME.ui.soul_rect.exp_rect = pg.rect.Rect(40, 450, 1200, 300)
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
            self.idx = 0
            self._timer = 0
            self.texts = ['* ']
            self.line = 0
            self.end = False
            self.res = False
            for c in string:
                print(c)
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

        def process(self):
            if self.idx >= len(self.tasks):
                return True
            s = self.tasks[self.idx]
            while s.startswith('[['):
                cmd = s.removeprefix('[[')
                if cmd == 'endl':
                    self.texts.append('* ')
                    self.line += 1
                self.idx += 1
                if self.idx >= len(self.tasks):
                    return True
                s = self.tasks[self.idx]
            self.texts[self.line] += s
            self.idx += 1
            return self.idx >= len(self.tasks)

        def update(self):
            if self.end:
                return
            if self._timer > 0:
                self._timer -= 1
                return
            if pg.K_x in game.GAME.key_events and not self.arg['no_skip']:
                while not self.process():
                    pass
            if self.process():
                if pg.K_z in game.GAME.key_events:
                    self.res = True
                    self.end = True
                    return
            else:
                self._timer = self.arg['tpc']
            r = game.GAME.ui.soul_rect.rect
            top = r.top + 50
            for text in self.texts:
                txt = game.GAME.font.render(text, True, self.arg['color'])
                txt_rect = txt.get_rect()
                txt_rect.topleft = (r.left + self.left, top)
                game.GAME.displayer().blit(txt, txt_rect)
                top += 120

    class selector(dialoger):
        args = ['color']

        def __init__(self, options: list[str], kwargs):
            self.arg = {'color': (255, 255, 255)}
            for k, v in kwargs.items():
                if k in self.args:
                    self.arg[k] = v
            self.options = options
            self.res = 0
            self.end = False
            self._pos = 0
            self._dir = 0
            self.sr = []
            self.first = True
            r = game.GAME.ui.soul_rect.exp_rect
            r.width = 400
            r.centerx = 640
            b = r.bottom
            r.height = 500
            r.bottom = b
            for opt in options:
                txt = game.GAME.font.render(opt, True, self.arg['color'])
                txt_rect = txt.get_rect()
                txt_rect.centerx = 640
                self.sr.append((txt, txt_rect))

        def update(self):
            if self.first:
                self.first = False
                return
            if self.end:
                return
            if self._pos % 10 == 0:
                self.idx = self._pos // 10
                if (pg.K_DOWN in game.GAME.key_events and
                        self.idx < len(self.sr) - 1):
                    self._dir = 1
                elif pg.K_UP in game.GAME.key_events and self.idx:
                    self._dir = -1
                elif pg.K_z in game.GAME.key_events:
                    self.end = True
                    self.res = self.idx
                    return
                else:
                    self._dir = 0
            self._pos += self._dir * 2
            i = 0
            for t, r in self.sr:
                if self.idx - 3 < i < self.idx + 3:
                    r.centery = (game.GAME.ui.soul_rect.rect.centery +
                                 (i - self._pos / 10) * 80)
                    t.set_alpha(255 - min(abs(r.centery - game.GAME.ui.soul_rect.rect.centery) // 2, 255))
                    game.GAME.displayer[0].blit(t, r)
                i += 1

    def attack_bars(self, func):
        setattr(self, '_atk_bars', func)

    def _atk_bars(self) -> list[tuple[int, int]]:
        tmp = [(40, 30)]
        return tmp

    def _setup_buttons(self, save):
        self.names = ['fight', 'act', 'item', 'mercy']
        for i in range(len(self.names)):
            anim = ani.Animations((160 + 320 * i, 900), 2, 10)
            anim.add_animation('idle',
                               ['ui.button.%s.idle.1' % self.names[i]])
            anim.add_animation('selected',
                               ['ui.button.%s.selected.%d' % (self.names[i], n) for n in [1, 1, 2, 3, 3, 2]])
            anim.change_animation('idle')
            self.buttons.append(anim)
        if save:
            anim = ani.Animations((480, 900), 2, 10)
            anim.add_animation('idle', ['ui.button.save.idle.1'])
            anim.add_animation('selected', ['ui.button.save.selected.%d' % i for i in range(1, 8)])
            anim.change_animation('idle')
            self.buttons[1] = anim

    def _setup_states(self):
        p = game.GAME.player
        texts = [(p.name, 80), ('LV', 10), (str(p.lv), 50), ('HP', 10),
                 (str(p.hp), 10), ('/', 10), (str(p.max_hp), 20)]
        left = 50
        for text, space in texts:
            txt = game.GAME.font.render(text, True, (255, 255, 255))
            txt_rect = txt.get_rect()
            txt_rect.midleft = (left, self.state_y)
            left += txt_rect.width + space
            self.texts.append((txt, txt_rect, space))
        self.hp_bar_left = left
        self.hp_bar_width = min(p.max_hp * 5, 1200 - self.hp_bar_left)

    def _update_states(self):
        p = game.GAME.player
        change_list = [(2, p.lv), (4, p.hp), (6, p.max_hp)]
        for idx, val in change_list:
            txt = game.GAME.font.render(str(val), True, (255, 255, 255))
            self.texts[idx] = (txt, txt.get_rect(), self.texts[idx][2])
        left = 50
        for text, text_rect, space in self.texts:
            text_rect.left = left
            text_rect.centery = self.state_y
            left += text_rect.width + space
        self.hp_bar_left = left
        self.hp_bar_width = min(p.max_hp * 5, 1200 - self.hp_bar_left)

    def _draw_states(self):
        gg = game.GAME
        d = gg.displayer[0]
        p = gg.player
        for txt, txt_rect, _ in self.texts:
            d.blit(txt, txt_rect)
        hp_bar = pg.rect.Rect(self.hp_bar_left, self.state_y - 25, self.hp_bar_width, 50)
        pg.draw.rect(d, (255, 0, 0), hp_bar)
        hp_bar.width = math.ceil(hp_bar.width / p.max_hp * p.hp)
        pg.draw.rect(d, (255, 255, 0), hp_bar)

    def __init__(self, save_button=False):
        self.state_y = 790
        self.selected = 0
        self.buttons: list[ani.Animations] = []
        self._setup_buttons(save_button)
        self.soul_rect = attacks.SoulRect()
        self.buttons[self.selected].change_animation('selected')
        self.texts: list[tuple[pg.surface.Surface, pg.rect.Rect, int]] = []
        self.text_setup = False
        self.hp_bar_left = 0
        self.hp_bar_width = 0
        self._attack_display_timer = 0
        self._attack_bars = []
        self._state = 'select'
        self._attack_score = 0
        self._damage_timer = 0
        self._dialog: UI.dialoger = None
        self._dialog_states = ('', '')
        self.target = 0
        self.dialog_res = ''
        self.wave: wave.Wave | None = None
        self.souls = attacks.Souls()

    def _attack_bar_shower(self, process: int, swap: bool = False):
        r = self.soul_rect.rect
        if len(self._attack_bars) > 1:
            s = len(self._attack_bars)
            if not self._attack_bars[s - 2][1]:
                self._attack_bars.pop(s - 2)
        for i in range(process):
            h = math.sqrt(process) - math.sqrt(process - i)
            h *= 10
            for x in [i * 4, -i * 4]:
                rect = pg.rect.Rect(r.centerx + x - 2, r.top + h,  4, r.height - 2 * h)
                pg.draw.rect(game.GAME.displayer[0], (255, 255 - i // 8 * 8, 255 - i // 8 * 8), rect)
            f: bool = game.GAME.tick // 2 % 2
            for x, _ in self._attack_bars:
                if _:
                    pg.draw.rect(game.GAME.displayer[0], (255, f * 255, f * 255), (x - 20, r.top, 40, r.height))
                    pg.draw.rect(game.GAME.displayer[0], (0, 0, 0), (x - 20, r.top, 40, r.height), width=10)
                else:
                    bar = pg.surface.Surface((40, r.height))
                    bar.fill((255, f * 255, f * 255))
                    pg.draw.rect(bar, (0, 0, 0), bar.get_rect(), width=10)
                    bar.set_alpha(50)
                    bar_rect = bar.get_rect()
                    bar_rect.center = x, r.centery
                    game.GAME.displayer[0].blit(bar, bar_rect)

                f = not f

    def dialog(self, string: str, end_state='self', **kwargs):
        self._dialog = self.dialoger(string, kwargs)
        self._dialog_states = self._state, game.GAME.state
        if end_state != 'self':
            self._dialog_states = end_state, game.GAME.state
        self._state = 'dialog'
        game.GAME.set_state('DIALOG')

    def choose(self, options: list[str], end_state='self', **kwargs):
        self._dialog = self.selector(options, kwargs)
        self._dialog_states = self._state, game.GAME.state
        if end_state != 'self':
            self._dialog_states = end_state, game.GAME.state
        self._state = 'dialog'
        game.GAME.set_state('DIALOG')

    def _update(self):
        if not self.text_setup:
            self._setup_states()
            self.text_setup = True
        self.soul_rect._update()

        gg = game.GAME
        if gg.state == 'SELECT':
            self.soul_rect.exp_rect = pg.rect.Rect(40, 450, 1200, 300)
            if self.buttons[self.selected].instant[0] == 'idle':
                self.buttons[self.selected].change_animation('selected')
            self._state = 'select'
            if pg.K_LEFT in gg.key_events:
                self.buttons[self.selected].change_animation('idle')
                self.selected = (self.selected + 3) % 4
                self.buttons[self.selected].change_animation('selected')
            elif pg.K_RIGHT in gg.key_events:
                self.buttons[self.selected].change_animation('idle')
                self.selected = (self.selected + 1) % 4
                self.buttons[self.selected].change_animation('selected')
            elif pg.K_z in gg.key_events:
                if self.selected == 0:
                    gg.set_state('ATTACK')
                    self._state = 'atk_choosing'
                    names = []
                    for m in gg.monsters:
                        names.append(m.name)
                    self.choose(names, 'show_bg')
                    self._attack_display_timer = 0
                    self._attack_bars = []
                elif self.selected == 1:
                    gg.set_state('ACT')
                    self._state = 'act_mc'
                    names = []
                    for m in gg.monsters:
                        names.append(m.name)
                    self.choose(names, 'act_pac')
                elif self.selected == 2:
                    if len(gg.inventory.inventory):
                        gg.set_state('ACT')
                        self._state = 'item_ic'
                        self.choose(gg.inventory.inventory, 'item_e')

        else:
            for button in self.buttons:
                button.change_animation('idle')

        for b in self.buttons:
            b._update()

        self._update_states()
        self._draw_states()

        if self._state.endswith('_ee'):
            self._state = 'soul'
            gg.set_state('SOUL')
            self.wave = gg.waves[gg.ins_wave]()
            gg.hook.on_wave_start(self.wave)
            self.wave.on_wave_start()

        if gg.state == 'ACT':
            if self._state == 'act_pac':
                self._state = 'act_ac'
                self.target = self.dialog_res
                self.choose(gg.monsters[self.target].acts, 'act_e')
            elif self._state == 'act_e':
                m = gg.monsters[self.target]
                txt = m.on_act(m.acts[self.dialog_res])
                if txt is not None:
                    self.dialog(txt, 'act_ee')
                else:
                    self._state = 'act_ee'
        elif gg.state == 'ITEM':
            if self._state == 'item_e':
                inv = gg.inventory
                txt = inv.on_item_used(inv[self.dialog_res])
                if txt is not None:
                    self._state = 'item_ee'
                else:
                    self.dialog(txt, 'item_ee')
        if gg.state == 'ATTACK':
            if math.pow(self._attack_display_timer, 2) > min(self.soul_rect.rect.width // 8, 255):
                self._attack_bar_shower(min(self.soul_rect.rect.width // 8, 255))
                if self._state == 'show_bg':
                    self.soul_rect.exp_rect = pg.rect.Rect(40, 450, 1200, 300)
                    self.target = self.dialog_res
                    self._state = 'show_bars'
                    self._attack_bars = self._atk_bars()
                    self._attack_score = 0
                elif self._state == 'show_bars':
                    for i in range(len(self._attack_bars)):
                        self._attack_bars[i] = \
                            (self._attack_bars[i][0] + self._attack_bars[i][1], self._attack_bars[i][1])
                    if self._attack_bars[0][1]:
                        if abs(self._attack_bars[0][0] - 640) > 650 or pg.K_z in gg.key_events:
                            self._attack_score += int(math.sqrt(500 - min(abs(self._attack_bars[0][0] - 640), 500)))
                            self._attack_bars.append((self._attack_bars[0][0], 0))
                            self._attack_bars.pop(0)
                    else:
                        self.soul_rect.exp_rect.left += 200
                        self.soul_rect.exp_rect.width -= 400
                        dmg = gg.player.on_attack(self._attack_score, gg.monsters[self.target])
                        if dmg is not None:
                            self._attack_score = dmg
                        self._attack_score = self._attack_score
                        self._state = 'show_damage'
                        self._damage_timer = 0
                elif self._state == 'show_damage':
                    m = gg.monsters[self.target]
                    d = gg.displayer[0]
                    if self._damage_timer == 5:
                        m.ani.change_animation('hurt')
                    if 5 <= self._damage_timer <= 25:
                        m.hurt(self._attack_score // 10)
                    if self._damage_timer >= 30:
                        self._state = 'attack_ee'
                    else:
                        self._damage_timer += 1
                        rect = pg.rect.Rect((0, 0, 400, 50))
                        rect.center = m.ani.pos
                        pg.draw.rect(d, (255, 0, 0), rect)
                        rect.width = int(400 / m.max_hp * m.hp)
                        pg.draw.rect(d, (0, 255, 0), rect)
            else:
                self._attack_bar_shower(int(math.pow(self._attack_display_timer, 2)))
                self._attack_display_timer += 1
        else:
            pg.draw.rect(gg.displayer[0], (0, 0, 0), self.soul_rect.rect)
            pg.draw.rect(gg.displayer[0], (255, 255, 255), self.soul_rect.rect, 8)

        if gg.state == 'SOUL':
            self.souls.get_now().update()
            w = self.wave
            w._update()
            if w.end:
                gg.set_state('SELECT')
                self._state = 'select'

        game.GAME.player.update()

        if self._dialog is not None:
            if self._dialog.end:
                self._state, gg.state = self._dialog_states
                self.dialog_res = self._dialog.res
                del self._dialog
                self._dialog = None
            else:
                self._dialog.update()

