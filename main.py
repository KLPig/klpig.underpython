from underpython import *
import os

player = Player('Chara', 92, 99, 16, 19)
flowery_ani = Animations((640, 240), 4, tpf=5)
flowery_ani.add_animation('idle', [
    'monsters.flowery.idle.1',
    'monsters.flowery.idle.2',
    'monsters.flowery.idle.3',
    'monsters.flowery.idle.4',
    'monsters.flowery.idle.5',
    'monsters.flowery.idle.6',
    'monsters.flowery.idle.7',
    'monsters.flowery.idle.6',
    'monsters.flowery.idle.5',
    'monsters.flowery.idle.4',
    'monsters.flowery.idle.3',
    'monsters.flowery.idle.2',
    'monsters.flowery.idle.1',
                          ])
flowery_ani.add_animation('hurt',
                          [
                              'monsters.flowery.idle.1',
                              'monsters.flowery.idle.1',
                              'monsters.flowery.idle.1',
                              'monsters.flowery.idle.1'
                          ], nxt='idle')
flowery_ani.change_animation('idle')
flowery = Monster(flowery_ani, 'flowery', 500, 90, 5)

monsters = [flowery]


class Bullet(Wave):
    pass


waves = [Bullet]

GAME = Game(player, monsters, waves, os.path.join(os.path.dirname(__file__), 'resources'))
write_game(GAME)


@GAME.set_event
def on_wave_end():
    print('hello')


GAME.build()

GAME.go()
