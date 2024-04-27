from underpython.overworld import *
import pygame as pg

res = './resources'

ply = Player(res, 'Frisk')
ply.set_pos((240, 680))
mp = Map()
rm = Room(res, 'corridor', [pg.Rect(160, 440, 160, 360), pg.Rect(0, 560, 4800, 240)])
mp.add_room(rm)


@rm.rect_handler
def set_pos_of_160_440_160_40():
    gm.run_game('main')
    ply.set_pos((240, 680))


gm = Game(res, ply, mp)
set_game(gm)

gm.go()
