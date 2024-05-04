from underpython.overworld import *
import underpython as up
import pygame as pg

res = './resources'

ply = Player(res, 'Frisk', up.Player('Frisk', 20, 5, 20, 1),
             up.Inventory(), 'the SAVIOUR.')
ply.inv.set_item('last dream', False)
ply.inv.set_inventory(['last dream' for i in range(5)])
ply.set_pos((240, 680))
mp = Map()
rm = Room(res, 'corridor', [pg.Rect(160, 440, 160, 360), pg.Rect(0, 560, 4800, 240)], [])
mp.add_room(rm)


def run(res):
    gm.run_game('main')
    gm.ui.close()


@rm.rect_handler
def set_pos_of_160_440_160_40():
    gm.ui.exp_rect = pg.Rect(40, 650, 1200, 300)
    gm.ui.dialog(['Hey, [endl]How are you, Frisk!', 'You are just so annoying.', 'Why will you come, trying to [nxtl]SAVE a little flower?', 'Heh heh..', 'Then, I\' satisfy you.'], end_func=run)
    ply.set_pos((240, 481))


@ply.on_item_checked
def check(no):
    gm.ui.exp_rect = pg.Rect(40, 650, 1200, 300)
    name = ply.inv.inventory[no]
    if name == 'last dream':
        gm.ui.dialog(['last dream.', 'recover 10 hp and extra 30 hp[nxtl]when used.', 'The power of determination.'], end_func=gm.ui.close)
    elif name == 'determin.':
        gm.ui.dialog(['Determination', 'I have it.'], end_func=gm.ui.close, tpc=5)
    else:
        gm.ui.close()


@ply.on_item_used
def check(no):
    gm.ui.exp_rect = pg.Rect(40, 650, 1200, 300)
    name = ply.inv.inventory[no]
    if name == 'last dream':
        ply.data.heal(10, game.GAME)
        ply.data.hp += 30
        gm.ui.dialog(['Your last dream..', 'You recovered 10 hp and[nxtl]30 extra!'], end_func=gm.ui.close)
    elif name == 'determin.':
        ply.data.heal(100, game.GAME)
        gm.ui.dialog(['Determination.'], end_func=gm.ui.close)
    else:
        gm.ui.close()


gm = Game(res, ply, mp)
set_game(gm)

gm.go()
