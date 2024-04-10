from underpython import game
import pygame as pg
import underpython.resources as res


class Displayer:
    def __init__(self):
        self.camera = (0, 0, 0)
        self.window = pg.display.set_mode((1280, 960), pg.SCALED)
        pg.display.set_caption('UNDERTALE')
        pg.display.set_icon(res.icon)
        self.surfaces = [pg.surface.Surface((1280, 960)) for i in range(3)]

    def clear(self):
        for surface in self.surfaces:
            surface.fill((0, 0, 0))

    def _update(self):
        self.window.fill((0, 0, 0))
        x, y, r = self.camera
        for surface in self.surfaces:
            r_surf = pg.transform.rotate(surface, r)
            r_surf_rect = r_surf.get_rect()
            r_surf_rect.topleft = (x, y)
            self.window.blit(r_surf, r_surf_rect)

    def __index__(self, idx) -> pg.surface.Surface:
        return self.surfaces[idx]

    def __call__(self) -> pg.surface.Surface:
        return self.surfaces[1]


class UI:
    def __init__(self):
        pass

    def _update(self):
        d = game.GAME.displayer[1]
        d.clear()
