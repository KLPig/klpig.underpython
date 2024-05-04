import pygame as pg
import os
from . import game
from underpython import player, inventory


class Chara:
    is_player = False

    def __init__(self, rp, name):
        self.surfaces = [pg.image.load(os.path.join(rp, 'sprites/%s/%d.png' % (name, i))) for i in range(16)]
        self.r_pos = (0, 0)
        self.instant = 1
        self.ed = -1
        self.dirs = [pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_UP]
        self.timer = 0

    def _move(self):
        if self.is_player:
            spd = 0
            _dir = self.instant // 4
            keys = pg.key.get_pressed()
            x, y = self.r_pos
            if keys[pg.K_LEFT]:
                spd = 8
                _dir = 1
                x -= spd
            elif keys[pg.K_RIGHT]:
                spd = 8
                _dir = 2
                x += spd
            if keys[pg.K_UP]:
                spd = 8
                _dir = 3
                y -= spd
            elif keys[pg.K_DOWN]:
                spd = 8
                _dir = 0
                y += spd
            if self.ed and keys[self.dirs[self.ed]]:
                _dir = self.ed
            elif pg.K_UP in game.GAME.key_events:
                _dir = 3
                self.ed = _dir
            elif pg.K_DOWN in game.GAME.key_events:
                _dir = 0
                self.ed = _dir
            elif pg.K_LEFT in game.GAME.key_events:
                _dir = 1
                self.ed = _dir
            elif pg.K_RIGHT in game.GAME.key_events:
                _dir = 2
                self.ed = _dir
            dis_x = min(max(-x, 1280 - game.GAME.map.get_now().surface.get_width()), 0)
            dis_y = min(max(-y, 960 - game.GAME.map.get_now().surface.get_height()), 0)
            game.GAME.dis_camera = dis_x, dis_y
            if game.GAME.map.get_now().collide_point((x + dis_x + 640, self.r_pos[1] + dis_y + 480)):
                self.r_pos = x, self.r_pos[1]
            if game.GAME.map.get_now().collide_point((self.r_pos[0] + dis_x + 640, y + dis_y + 480)):
                self.r_pos = self.r_pos[0], y
            dis_x = min(max(-self.r_pos[0], 1280 - game.GAME.map.get_now().surface.get_width()), 0)
            dis_y = min(max(-self.r_pos[1], 960 - game.GAME.map.get_now().surface.get_height()), 0)
            game.GAME.dis_camera = dis_x, dis_y
            if self.timer % 10 == 0:
                if self.instant // 4 != _dir:
                    self.instant = _dir * 4 + 2
                elif spd:
                    self.instant -= _dir * 4
                    self.instant = (self.instant + 1) % 4
                    self.instant += _dir * 4
            if not spd:
                self.instant = _dir * 4 + 1
                self.timer = 0
            self.timer += bool(spd)

    def _update(self):
        x, y = self.r_pos
        ax, ay = game.GAME.dis_camera
        surf = pg.transform.scale_by(self.surfaces[self.instant], 2.5)
        rect = surf.get_rect()
        rect.midbottom = x + ax + 640, y + ay + 480
        game.GAME.dis().blit(surf, rect)

    def set_pos(self, pos, c_view=False):
        x, y = pos
        self.r_pos = x - 640, y - 480
        if c_view:
            self._move()
            self._update()


class Player(Chara):
    is_player = True

    def _handle_inv(self, item_no: int):
        game.GAME.ui.close()

    def _handle_check(self, item_no: int):
        game.GAME.ui.close()

    def on_item_used(self, func):
        self.__setattr__('_handle_inv', func)


    def on_item_checked(self, func):
        self.__setattr__('_handle_check', func)

    def __init__(self, rp, name, data: player.Player, invent: inventory.Inventory, desc: str, g=0, exp=0):
        super().__init__(rp, name)
        self.data = data
        self.inv = invent
        self.g = g
        self.exp = exp
        self.desc = desc
