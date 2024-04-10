from underpython import *
import os

player = Player('Chara', 92, 99, 16)
flowery_ani = Animations((600, 50))
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
flowery_ani.change_animation('idle')
flowery = Monster(flowery_ani, 'flowery', 5, 90, 5)

monsters = [flowery]


class Bullet(Wave):
    pass


waves = [Bullet]

GAME = Game(player, monsters, waves, os.path.join(os.path.dirname(__file__), 'resources'))

GAME.build()
