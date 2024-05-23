import pygame as pg
import os
from . import game, player


class Room:
    def rect_handler(self, func):
        r = [int(s) for s in func.__name__.split('_of_')[1].split('_')]
        rect = pg.Rect(r[0], r[1], r[2], r[3])
        self.handler.append((rect, func))

    def __init__(self, rp, name, a_rects: list[pg.Rect], exclude_rects: list[pg.Rect], characters: list[player.Chara] = []):
        self.surface = pg.transform.scale_by(pg.image.load(os.path.join(rp, 'maps/%s.png' % name)), 2)
        self.pos: tuple[int, int] | None = (0, 0)
        self.rl = a_rects
        self.el = exclude_rects
        func = self.__init__
        self.handler: list[tuple[pg.Rect, type(func)]] = []
        self.chara = characters

    def set_pos(self, pos):
        self.pos = pos

    def _calc_pos(self) -> tuple[int, int]:
        return 0, 0

    def _update(self):
        rect = self.surface.get_rect()
        dx, dy = game.GAME.dis_camera
        rect.topleft = (dx, dy)
        game.GAME.dis().blit(self.surface, rect)
        self.handle_handler()

    def handle_handler(self):
        dx, dy = game.GAME.dis_camera
        x, y = game.GAME.player.r_pos
        for f, func in self.handler:
            f.top += dy
            f.left += dx
            if f.collidepoint(x + dx + 640, y + dy + 480):
                func()
            f.top -= dy
            f.left -= dx

    def collide_point(self, pos: tuple[int, int]) -> bool:
        dx, dy = game.GAME.dis_camera
        x, y = pos
        for f in self.el:
            f.top += dy
            f.left += dx
            if f.collidepoint(x, y):
                f.top -= dy
                f.left -= dx
                return False
            f.top -= dy
            f.left -= dx
        for f in self.rl:
            f.top += dy
            f.left += dx
            if f.collidepoint(x, y):
                f.top -= dy
                f.left -= dx
                return True
            f.top -= dy
            f.left -= dx
        return False


class Map:
    def __init__(self):
        self.rooms: list[Room] = []
        self.current = 0

    def set_room(self, no: int):
        self.current = no

    def get_now(self) -> Room:
        return self.rooms[self.current]

    def add_room(self, room: Room):
        self.rooms.append(room)
