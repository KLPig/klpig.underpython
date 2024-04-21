from underpython import *
import os
import random

player = Player('Frisk', 20, 8, 24, 1)
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
flowery = Monster(flowery_ani, 'flowery', 500, 15, 10,
                  ['say'])


@flowery.events
def on_act(name: str) -> list[str] | None:
    if name == 'check':
        return ['Flowery, 15 at 15 df.[endl]Your best friend.']
    elif name == 'say':
        flowery.spare_able = True
        return ['You said hi to flowery.', 'Flowery is now spare-able!']


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


class BulletTwice(Wave):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(440, 300, 400, 400)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 7 == 1:
            self.attacks[0].add(FbRise((random.randint(0, 200), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
            self.attacks[0].add(FbRise((random.randint(1080, 1280), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


class BulletOnce(Wave):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(590, 200, 100, 600)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 3 == 1:
            self.attacks[0].add(FbRise((random.randint(0, 200), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


waves = [BulletOnce, BulletTwice]

GAME = Game(player, monsters, waves, os.path.join(os.path.dirname(__file__), 'resources'))
write_game(GAME)


GAME.build()


@GAME.set_event
def on_wave_end(wave):
    GAME.ins_wave = random.randint(0, 1)


GAME.inventory.set_item('coffee', True)
GAME.inventory.set_item('candy', False)
GAME.inventory.set_inventory(['candy', 'candy', 'candy', 'candy', 'candy', 'coffee'])


@GAME.inventory.events
def on_item_used(item_name: str) -> list[str] | None:
    if item_name == 'candy':
        GAME.player.heal(20)
        return ['You had a nice time on the candy.', 'HP fully restored!']
    elif item_name == 'coffee':
        hp = random.randint(-2, 5)
        GAME.player.heal(hp)
        if hp <= 0:
            return ['You had some bad coffee.', 'Disgusting!', 'You loss you hp!']
        else:
            return ['You had some coffee.', 'Not so bad!', 'You got %d hp!' % hp]


MChanel.play(GAME.sounds['mus_flowery'])


GAME.go()
