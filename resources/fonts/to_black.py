import pygame as pg

name = 'monster'

img = pg.image.load('%s.png' % name)

arr = pg.PixelArray(img)

for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        if arr[i, j] == 4294967295:
            arr[i, j] = (0, 0, 0)

o = arr.make_surface()

pg.image.save(o, '%s.png' % name)
