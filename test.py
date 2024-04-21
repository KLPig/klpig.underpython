from underpython import font
import pygame as pg

f = font.Font('uidamagetext')

w = pg.Surface((300, 60))
w.fill((0, 0, 0))
f.render(w, (0, 0), '114514')
pg.image.save(w, 'img.png')
