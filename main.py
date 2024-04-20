from underpython import *
import os
import random

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
flowery = Monster(flowery_ani, 'flowery', 500, 12, 5,
                  ['heal'])


@flowery.events
def on_act(name: str) -> str | None:
    if name == 'check':
        return 'Flowery, 5 df 12 at.[endl]Last enemy.'
    elif name == 'heal':
        GAME.player.heal(50)
        return 'Recovered 50 HP!'


monsters = [flowery]


class Fb(Attack):
    def u_ani(self):
        self.set_img(GAME.graphics['pj.attack.fb.idle.%d' % (self.tick // 2 % 2 + 1)])


class FbRise(Fb):
    def on_action(self):
        self.u_ani()
        if self.tick > 40:
            self.move_forward(40)
        elif self.tick == 40:
            self.face_to(GAME.ui.souls.get_now().pos)
        else:
            self.move_pos((0, -20))


class Bullet(Wave):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(440, 300, 400, 400)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 10 == 1:
            self.attacks[0].add(FbRise((random.randint(0, 200), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
        elif self.tick % 10 == 6:
            self.attacks[0].add(FbRise((random.randint(1080, 1280), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


waves = [Bullet]

GAME = Game(player, monsters, waves, os.path.join(os.path.dirname(__file__), 'resources'))
write_game(GAME)


@GAME.set_event
def on_wave_end():
    print('hello')


GAME.build()

GAME.go()
