from underpython import game, attacks
import pygame as pg
import underpython.resources as res
from underpython import animations as ani
import random


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

    def __init__(self, save_button=False):
        self.selected = 0
        self.buttons: list[ani.Animations] = []
        self._setup_buttons(save_button)
        self.soul_rect = attacks.SoulRect()
        self.buttons[self.selected].change_animation('selected')

    def _update(self):
        self.soul_rect._update()
        if game.GAME.state == 'SELECT':
            if pg.K_LEFT in game.GAME.key_events:
                self.buttons[self.selected].change_animation('idle')
                self.selected = (self.selected + 3) % 4
                self.buttons[self.selected].change_animation('selected')
            elif pg.K_RIGHT in game.GAME.key_events:
                self.buttons[self.selected].change_animation('idle')
                self.selected = (self.selected + 1) % 4
                self.buttons[self.selected].change_animation('selected')
        for b in self.buttons:
            b._update()
        pg.draw.rect(game.GAME.displayer[0], (0, 0, 0), self.soul_rect.rect)
        pg.draw.rect(game.GAME.displayer[0], (255, 255, 255), self.soul_rect.rect, 8)

