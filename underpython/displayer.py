import random
from underpython import game, attacks
import pygame as pg
import underpython.resources as res
from underpython import animations as ani
import math


class Displayer:
    def __init__(self):
        self.camera = (0, 0, 0)
        self.window = pg.display.set_mode((640, 480), pg.SCALED | pg.RESIZABLE)
        pg.display.set_caption('UNDERTALE')
        pg.display.set_icon(res.icon)
        self.surfaces = [pg.surface.Surface((1280, 960))]

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
    def attack_bars(self, func):
        setattr(self, '_atk_bars', func)

    def _atk_bars(self) -> list[tuple[int, int]]:
        tmp = []
        for i in range(5):
            d = random.choice([-1, 1])
            tmp.append((-d * (600 + i * 200) + 640, d * 30))
        return tmp

    def _setup_buttons(self, save):
        self.names = ['fight', 'act', 'fight', 'act']
        for i in range(len(self.names)):
            anim = ani.Animations((160 + 320 * i, 900), 2, 10)
            anim.add_animation('idle',
                               ['ui.button.%s.idle.1' % self.names[i]])
            anim.add_animation('selected',
                               ['ui.button.%s.selected.%d' % (self.names[i], n) for n in [1, 1, 2, 3, 3, 2]])
            anim.change_animation('idle')
            self.buttons.append(anim)

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
        d = game.GAME.displayer[0]
        p = game.GAME.player
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

    def _attack_bar_shower(self, process: int):
        r = self.soul_rect.rect
        for i in range(process):
            h = math.sqrt(process) - math.sqrt(process - i)
            h *= 10
            for x in [i * 4, -i * 4]:
                rect = pg.rect.Rect(r.centerx + x - 2, r.top + h,  4, r.height - 2 * h)
                pg.draw.rect(game.GAME.displayer[0], (255, 255 - i // 8 * 8, 255 - i // 8 * 8), rect)
            f: bool = game.GAME.tick // 5 % 2
            for x, _ in self._attack_bars:
                pg.draw.rect(game.GAME.displayer[0], (255, f * 255, f * 255), (x - 20, r.top, 40, r.height))
                pg.draw.rect(game.GAME.displayer[0], (0, 0, 0), (x - 20, r.top, 40, r.height), width=10)
                f = not f

    def _update(self):
        if not self.text_setup:
            self._setup_states()
            self.text_setup = True
        self.soul_rect._update()

        if game.GAME.state == 'SELECT':
            self.soul_rect.exp_rect = pg.rect.Rect(40, 450, 1200, 300)
            if self.buttons[self.selected].instant[0] == 'idle':
                self.buttons[self.selected].change_animation('selected')
            self._state = 'select'
            if pg.K_LEFT in game.GAME.key_events:
                self.buttons[self.selected].change_animation('idle')
                self.selected = (self.selected + 3) % 4
                self.buttons[self.selected].change_animation('selected')
            elif pg.K_RIGHT in game.GAME.key_events:
                self.buttons[self.selected].change_animation('idle')
                self.selected = (self.selected + 1) % 4
                self.buttons[self.selected].change_animation('selected')
            elif pg.K_z in game.GAME.key_events:
                if self.selected == 0:
                    game.GAME.set_state('ATTACK')
                    self._state = 'show_bg'
                    self._attack_display_timer = 0

        else:
            for button in self.buttons:
                button.change_animation('idle')

        for b in self.buttons:
            b._update()

        self._update_states()
        self._draw_states()

        if game.GAME.state == 'ATTACK':
            if math.pow(self._attack_display_timer, 2) > min(self.soul_rect.rect.width // 8, 255):
                self._attack_bar_shower(min(self.soul_rect.rect.width // 8, 255))
                if self._state == 'show_bg':
                    self._state = 'show_bars'
                    self._attack_bars = self._atk_bars()
                    self._attack_score = 0
                elif self._state == 'show_bars':
                    for i in range(len(self._attack_bars)):
                        self._attack_bars[i] = \
                            (self._attack_bars[i][0] + self._attack_bars[i][1], self._attack_bars[i][1])
                    if len(self._attack_bars):
                        if abs(self._attack_bars[0][0] - 640) > 700 or pg.K_z in game.GAME.key_events:
                            self._attack_score += int(math.sqrt(500 - min(abs(self._attack_bars[0][0] - 640), 500)))
                            self._attack_bars.pop(0)
                    else:
                        self.soul_rect.exp_rect.left += 200
                        self.soul_rect.exp_rect.width -= 400
                        self._attack_score = self._attack_score // 10
                        self._state = 'show_damage'
                        self._damage_timer = 0
                elif self._state == 'show_damage':
                    m = game.GAME.monsters[0]
                    d = game.GAME.displayer[0]
                    if self._damage_timer == 5:
                        m.ani.change_animation('hurt')
                    if 5 <= self._damage_timer <= 25:
                        m.hurt(self._attack_score // 5)
                    if self._damage_timer >= 30:
                        self._state = 'select'
                        game.GAME.set_state('SELECT')
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
            pg.draw.rect(game.GAME.displayer[0], (0, 0, 0), self.soul_rect.rect)
            pg.draw.rect(game.GAME.displayer[0], (255, 255, 255), self.soul_rect.rect, 8)

