from underpython import *
import os
import random

player = Player('Frisk', 20, 5, 20, 1)
flowery_ani = Animations((640, 240), 4, tpf=5)
flowery_ani.add_animation('idle',
                          ['monsters.flowery.idle.%d' % i for i in [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]])
flowery_ani.add_animation('hurt',
                          ['monsters.flowery.idle.1' for i in range(4)], nxt='idle')
flowery_ani.change_animation('idle')
flowery = Monster(flowery_ani, 'flowery', 400, 14, 8,
                  ['hopes', 'dreams'])


@flowery.events
def on_act(name: str) -> list[str] | None:
    if name == 'check':
        return ['Flowery, 15 at 15 df.[endl]The loast princess.']
    elif name == 'hopes':
        player.df += 2
        return ['You thought about why you\'re [nxtl]here, ', 'Defense greatly increased!!']
    elif name == 'dreams':
        player.heal(20)
        return ['You closed your eyes, ', 'Thinking about what you [nxtl]are looking for', 'HP fully recovered!']


monsters = [flowery]


class Fb(Attack):
    def u_ani(self):
        self.set_img(GAME.graphics['pj.attack.fb.idle.%d' % (self.tick // 2 % 2 + 1)])


class FbRise(Fb):
    def on_action(self):
        if self.tick > 40:
            self.move_forward(20 + self.tick // 2)
        elif self.tick == 40:
            self.face_to(GAME.ui.souls.get_now().pos)
        else:
            self.move_pos((0, -40 + self.tick))
        self.u_ani()


class FbRhb(FbRise):
    def on_action(self):
        r = GAME.ui.soul_rect.rect
        if self.tick > 65:
            self.move_forward(20 + self.tick // 2)
            if self.pos[1] > r.bottom:
                chanel.Chanel.play(GAME.sounds['hitsound'])
                self.remove_atk()
        elif self.tick == 65:
            chanel.Chanel.play(GAME.sounds['toss'])
            self.face_to((random.randint(r.left, r.right), r.bottom))
        else:
            self.move_pos((0, -45 + self.tick))
        self.u_ani()


class FbD(Fb):
    def on_action(self):
        self.move_forward(10 + self.tick // 2)
        self.u_ani()


class FbS(Fb):
    def set_r(self, r):
        self.set_attribute(r=r)

    def on_action(self):
        rot = (self.get_attribute('r') + self.tick * 10) % 360
        # print(rot, self.tick)
        self.set_pos(GAME.ui.soul_rect.rect.center)
        self.set_rotation(rot)
        self.move_forward(400 - self.tick * 10)
        if self.tick >= 40:
            self.remove_atk()
        self.u_ani()
        self.set_rotation(0)


class BulletRiser(Wave):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(540, 500, 200, 200)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 20 == 1:
            self.attacks[0].add(FbRise((random.randint(0, 200), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
        elif self.tick % 20 == 11:
            self.attacks[0].add(FbRise((random.randint(1080, 1280), random.randint(1000, 1500)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


class BulletSpin(Wave):

    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(490, 350, 300, 300)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 30 == 1:
            r = random.randint(0, 359)
            for i in range(r, r + 359, 45):
                atk = FbS((0, 0), GAME.graphics['pj.attack.fb.idle.1'])
                atk.set_r(i % 360)
                self.attacks[0].add(atk)
        if self.tick >= 200:
            self.end_wave()


class BulletRiserOver(Wave):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(440, 300, 400, 400)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 15 == 1:
            for i in range(2):
                self.attacks[0].add(FbRise((random.randint(200, 1080), random.randint(900, 1000)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


class BulletShoot(Wave):
    def __init__(self):
        super().__init__()
        self.tgt = 0

    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(440, 560, 400, 200)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 20 == 1:
            self.tgt = random.randint(240, 1040)
            if self.tick == 181:
                self.tgt = 640
        elif self.tick % 20 < 12:
            flowery_ani.set_pos(((flowery_ani.pos[0] + self.tgt) // 2, flowery_ani.pos[1]))
        else:
            a_s = []
            if self.tick % 5 == 1:
                a_s = [-30, 0, 30]
            elif self.tick % 5 == 3:
                a_s = [-15, 15]
            for a in a_s:
                atk = FbD(flowery_ani.pos, GAME.graphics['pj.attack.fb.idle.1'])
                atk.face_to(GAME.ui.souls.get_now().pos)
                atk.rotate(a)
                self.attacks[0].add(atk)
        if self.tick >= 200:
            self.end_wave()

    def on_wave_end(self):
        flowery_ani.pos = (640, flowery_ani.pos[1])


class BulletMixed(Wave):
    def __init__(self):
        super().__init__()
        self.tgt = 0

    def on_wave_start(self):
        GAME.ui.soul_rect.exp_rect.__init__(390, 300, 500, 400)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 30 == 21:
            for i in range(2):
                self.attacks[0].add(FbRise((random.randint(100, 1180), random.randint(900, 1000)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()
        for atk in self.attacks:
            atk.update()
        if self.tick % 30 == 1:
            self.tgt = random.randint(240, 1040)
            if self.tick == 271:
                self.tgt = 640
        elif self.tick % 30 < 12:
            flowery_ani.set_pos(((flowery_ani.pos[0] + self.tgt) // 2, flowery_ani.pos[1]))
        elif self.tick % 30 < 16:
            pass
        else:
            a_s = []
            if self.tick % 10 == 2:
                a_s = [-60, -30, 0, 30, 60]
            elif self.tick % 10 == 6:
                a_s = [-45, -15, 15, 45]
            for a in a_s:
                atk = FbD(flowery_ani.pos, GAME.graphics['pj.attack.fb.idle.1'])
                atk.face_to(GAME.ui.souls.get_now().pos)
                atk.rotate(a)
                self.attacks[0].add(atk)
        if self.tick >= 300:
            self.end_wave()

    def on_wave_end(self):
        flowery_ani.pos = (640, 240)


class BulletShootFast(BulletShoot):
    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 10 == 1:
            self.tgt = random.randint(240, 1040)
            if self.tick == 181:
                self.tgt = 640
        elif self.tick % 10 < 9:
            flowery_ani.set_pos(((flowery_ani.pos[0] + self.tgt) // 2, flowery_ani.pos[1]))
        else:
            for a in [-30, 0, 30]:
                atk = FbD(flowery_ani.pos, GAME.graphics['pj.attack.fb.idle.1'])
                atk.face_to(GAME.ui.souls.get_now().pos)
                atk.rotate(a)
                self.attacks[0].add(atk)
        if self.tick >= 200:
            self.end_wave()


class BottomShooter(Wave):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(540, 530, 200, 100)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 20 == 1:
            self.attacks[0].add(FbRhb((random.randint(0, 640), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
        elif self.tick % 20 == 11:
            self.attacks[0].add(FbRhb((random.randint(640, 1280), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


class MixShooter(BottomShooter):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(490, 500, 300, 200)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 10 == 1:
            self.attacks[0].add(FbRise((random.randint(400, 880), random.randint(1500, 1700)), game.GAME.graphics['pj.attack.fb.idle.1']))
            if random.randint(0, 1):
                self.attacks[0].add(FbRhb((random.randint(0, 400), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
            else:
                self.attacks[0].add(FbRhb((random.randint(880, 1280), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 200:
            self.end_wave()


class Hurricane(BottomShooter):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(390, 500, 500, 200)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 5 == 1:
            if random.randint(0, 1):
                self.attacks[0].add(FbRhb((random.randint(0, 400), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
            else:
                self.attacks[0].add(FbRhb((random.randint(880, 1280), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
        if self.tick >= 300:
            self.end_wave()


class BulletFinal(BulletShoot):
    def on_wave_start(self):
        game.GAME.ui.soul_rect.exp_rect.__init__(440, 400, 400, 400)
        self.attacks.append(attacks.Attacks(GAME.monsters[0]))
        GAME.ui.souls.get_now().set_pos(GAME.ui.soul_rect.rect.center)

    def on_wave_update(self):
        for atk in self.attacks:
            atk.update()
        if self.tick % 15 == 1:
            if self.tick % 45 == 1:
                r = random.randint(0, 359)
                for i in range(r, r + 340, 60):
                    atk = FbS((0, 0), GAME.graphics['pj.attack.fb.idle.1'])
                    atk.set_r(i % 360)
                    self.attacks[0].add(atk)
            self.tgt = random.randint(240, 1040)
            if self.tick == 181:
                self.tgt = 640
        elif self.tick % 15 < 9:
            GAME.ui.soul_rect.exp_rect.centerx -= (flowery_ani.pos[0] + self.tgt) // 2 - flowery_ani.pos[0]
            GAME.ui.souls.get_now().move_pos((-(flowery_ani.pos[0] + self.tgt) // 2 + flowery_ani.pos[0], 0))
            flowery_ani.set_pos(((flowery_ani.pos[0] + self.tgt) // 2, flowery_ani.pos[1]))
            if self.tick % 15 == 4:
                self.attacks[0].add(FbRhb((random.randint(0, 1280), random.randint(1000, 1200)), game.GAME.graphics['pj.attack.fb.idle.1']))
        elif self.tick % 4 == 1:
            for a in [-30, 0, 30]:
                atk = FbD(flowery_ani.pos, GAME.graphics['pj.attack.fb.idle.1'])
                atk.face_to(GAME.ui.souls.get_now().pos)
                atk.rotate(a)
                self.attacks[0].add(atk)
        if self.tick >= 200:
            self.end_wave()


waves = [BulletRiser, BulletShoot, BulletRiserOver, BulletSpin, BulletMixed, BulletShootFast,
         BottomShooter, MixShooter, Hurricane, BulletFinal]

GAME = Game(player, monsters, waves, os.path.join('../undertale.determination/', 'resources'))
write_game(GAME)


GAME.build()
idx = 0
say = [
    ['You are just[nxtl]so stupid', 'You know I\'ll[nxtl]become a flower[nxtl]again, don\'t you?'],
    ['Are you just[nxtl]trying to get[nxtl]your[nxtl]\'Perfect Endding\'?', 'So silly,', 'You are just[nxtl]noob trying to[nxtl]save everything'],
    ['See this?[nxtl]Your determination,[nxtl]it helps you[nxtl]to achieve[nxtl]everything,'],
    ['How much I[nxtl]love it?', 'But got STUCK[nxtl]with it!', 'All you do[nxtl]was not in[nxtl]mind, right?'],
    ['Let\'s just[nxtl]don\'t say this', 'Focus on your[nxtl]fight'],
    ['Hey,[endl]watch out!'],
    ['You\'ve seen[nxtl]rain?'],
    ['Hey,[endl]watch up!', 'No![endl]watch down!'],
    ['shooting quickly,[nxtl]looks like rain,[nxtl]', 'I\'d like to[nxtl]call it[nxtl]\'The Hurricane\''],
    ['let\'s see[nxtl]how many times[nxtl]will you try[nxtl]for this attack?'],
    ['']
]


@GAME.set_event
def on_wave_start(wave):
    global say, idx
    GAME.ui.monster_speech(flowery_ani().midleft, say[idx])
    idx = min(idx + 1, len(say) - 1)
    GAME.theme_color = (127, 0, 0)


@GAME.set_event
def on_wave_end(wave):
    GAME.player.df = 20
    GAME.ins_wave = (GAME.ins_wave + 1) % len(waves)
    if not GAME.ins_wave and flowery.hp == flowery.max_hp:
        flowery.defeat = PACIFIST_ROUTE
    GAME.theme_color = (255, 255, 255)


GAME.inventory.set_item('last dream', False)
GAME.inventory.set_item('determin.', False)
GAME.inventory.set_inventory(['last dream' for i in range(8)])


@GAME.inventory.events
def on_item_used(item_name: str) -> list[str] | None:
    if item_name == 'last dream':
        GAME.player.heal(10)
        GAME.player.hp += 30
        return ['Your last hopes, [endl]Your last dreams,', 'Your determination..', 'Your recover 10 HP!', 'You got extra 30 hp!']
    if item_name == 'determin.':
        GAME.player.heal(100)
        return ['Determination.']


@GAME.ui.attack_bars
def atk():
    tmp = []
    for i in range(4):
        tmp.append((-i * 200, 50))
    return tmp


@player.events
def on_attack(damage: int, target: monster.Monster) -> int | None:
    global idx
    GAME.inventory.set_inventory(['determin.' for i in range(8)])
    flowery.acts = ['useless']
    player.lv = 20
    player.max_hp = 100
    MChanel.stop()
    idx = len(say) - 1
    return damage * max(player.at * 5 - target.df * 3, 0) // 3


MChanel.play(GAME.sounds['mus_flowery'])


GAME.theme_color = (127, 0, 0)


if __name__ == '__main__':
    GAME.go()
