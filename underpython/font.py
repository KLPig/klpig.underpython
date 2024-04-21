from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import os
import pygame as pg


class Font:
    def __init__(self):
        self.chars = {}

    def load(self, path, name):
        p = os.path.join(path, 'fonts')
        img = pg.image.load(os.path.join(p, name + '.png'))
        arr = pg.PixelArray(img)
        xml = bf.data(fromstring(open(os.path.join(p, name + '.xml')).read()))
        spc = {'questionmark': '?', 'space': ' ', 'slash': '/'}
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
            surf = pg.transform.scale_by(self.chars[s], scale)
            surf_r = surf.get_rect()
            surf_r.midleft = left, y
            left += surf_r.width + 5
            surface.blit(surf, surf_r)
