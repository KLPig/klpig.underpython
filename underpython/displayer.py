from underpython import *
import pygame as pg
import resources as res


class Displayer:
    def __init__(self):
        self.camera = (0, 0, 0)
        self.window = pg.display.set_mode((1280, 960), pg.SCALED)
        pg.display.set_caption('UNDERTALE')
        pg.display.set_icon(res.icon)
        self.pre_surface = pg.surface.Surface((1280, 960))
        self.blits = []

    def blit(self, surface, rect):
        self.blits.append((surface, rect))

    def _update(self):
        self.window.fill((0, 0, 0))
        self.pre_surface.fill((0, 0, 0))
        for surface, rect in self.blits:
            self.pre_surface.blit(surface, rect)
        x, y, r = self.camera
        self.pre_surface = pg.transform.rotate(self.pre_surface, r)
        pSurfaceRect = self.pre_surface.get_rect()
        pSurfaceRect.center = (640 + x, 480 + y)
        self.window.blit(self.pre_surface, pSurfaceRect)
        self.blits.clear()



