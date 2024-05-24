from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import os
import pygame as pg


class Font:
    def __init__(self):
        self.name = ''
        self.chars = {}

    def load(self, path, name):
        self.name = name
        p = os.path.join(path, 'fonts')
        img = pg.image.load(os.path.join(p, name + '.png'))
        arr = pg.PixelArray(img)
        xml = bf.data(fromstring(open(os.path.join(p, name + '.xml')).read()))
        spc = {'questionmark': '?', 'space': ' ', 'slash': '/', 'dot': '.'}
        for d in xml['font']['spritesheet']['sprite']:
            r = d['rect']
            name = str(d['@name'])
            if name.startswith('unnamed'):
                continue
            elif name in spc.keys():
                name = spc[name]
            self.chars[name] = arr[r['@x']: (r['@x'] + r['@w']),
                               (arr.shape[1] - r['@y'] - r['@h']): (arr.shape[1] - r['@y'])].make_surface()

    def render(self, surface: pg.Surface, pos, text: str, scale=5):
        left, y = pos
        width = sum([self.chars[s].get_width() * scale for s in text]) + len(text) * 5 - 5
        left -= width // 2
        for s in text:
            if s in ['q', 'y', 'p', 'g', 'j']:
                y = pos[1] + 12 * (self.name == 'sans')
            else:
                y = pos[1]
            surf = pg.transform.scale_by(self.chars[s], scale)
            surf_r = surf.get_rect()
            surf_r.bottomleft = left, y
            left += surf_r.width + 5
            surface.blit(surf, surf_r)

    def rend_surf(self, text: str, scale=5, color=(255, 255, 255)):
        width = int(sum([self.chars[s].get_width() * scale for s in text])) + len(text) * 5 - 5
        left = 0
        surface = pg.Surface((width, int(self.chars['F'].get_height() * scale)))
        for s in text:
            if s in ['q', 'y', 'p', 'g', 'j']:
                y = 12 * (self.name == 'sans')
            else:
                y = 0
            surf = pg.transform.scale_by(self.chars[s], scale)
            surf_r = surf.get_rect()
            surf_r.topleft = left, y
            left += surf_r.width + 5
            surface.blit(surf, surf_r)
        p_surf = pg.PixelArray(surface)
        for i in range(p_surf.shape[0]):
            for j in range(p_surf.shape[1]):
                if p_surf[i][j] != surface.map_rgb((0, 0, 0)):
                    p_surf[i][j] = color
        surface = p_surf.make_surface()
        del p_surf
        return surface
