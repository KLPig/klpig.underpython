from underpython import base
import pygame as pg
import math
from underpython import game


class Attack:
    enable_ul = True
    is_attack = True

    def calc_dmg(self, attacker):
        return max(0, attacker.at * 5 - game.GAME.player.df * 3)

    def on_action(self): pass

    def on_init(self): pass

    def on_remove(self): pass

    def __init__(self, position: tuple[int, int], graphic: pg.surface.Surface, rotation=0, **kwargs):
        self.pos = position
        self.remove = False
        self.arr = pg.PixelArray(graphic)
        self.org = pg.transform.scale_by(graphic, 3)
        self.rot = rotation
        self.set_img(graphic)
        self.dis: pg.surface.Surface = self.org
        self.rect = self.org.get_rect()
        self.attr = {}
        self.img = graphic
        self.tick = 0
        for k, v in kwargs.items():
            self.attr[k] = v
        self.set_rotation(rotation)

    def collide_point(self, point: tuple[int, int]) -> bool:
        self.arr = pg.PixelArray(self.dis)
        x, y = point
        px, py = self.rect.topleft
        if self.rect.collidepoint(x, y):
            return self.arr[x - px, y - py] != 6203122
        else:
            return False

    def pos_to(self, steps: float = 1, rotation: float = None) -> tuple[float, float]:
        rot = rotation
        if rot is None:
            rot = self.rot
        ax = math.sin(math.radians(rot)) * steps
        ay = math.cos(math.radians(rot)) * steps
        return ax, -ay

    def move_forward(self, steps: float = 1, rotation: float = None):
        ax, ay = self.pos_to(steps, rotation)
        self.move_pos((ax, ay))

    def move_pos(self, apos: tuple[float, float]):
        ax, ay = apos
        x, y = self.pos
        self.set_pos((x + ax, y + ay))

    def angle_to(self, pos: tuple[float, float]) -> float:
        dx, dy = pos
        x, y = self.pos
        ax, ay = dx - x, dy - y
        if not ay:
            return 270 - 180 * (ax > 0)
        return math.degrees(math.atan(-ax / ay)) + 180 * (dy > y)

    def face_to(self, pos: tuple[float, float]):
        r = self.angle_to(pos)
        self.set_rotation(r)

    def set_pos(self, pos: tuple[float, float]):
        self.pos = pos
        x, y = self.pos
        self.rect.center = int(x), int(y)

    def set_rotation(self, rotation: float):
        self.rot = (rotation % 360 + 360) % 360
        self.dis = pg.transform.rotate(self.org, self.rot)
        self.rect = self.dis.get_rect()
        x, y = self.pos
        self.rect.center = int(x), int(y)

    def set_img(self, img: pg.Surface):
        self.img = img
        self.org = pg.transform.scale_by(img, 3)
        self.set_rotation(self.rot)

    def rotate(self, degree: float):
        self.set_rotation(self.rot + degree)

    def set_attribute(self, **kwargs):
        for k, v in kwargs.items():
            self.attr[k] = v

    def get_attribute(self, name):
        if name in self.attr.keys():
            return self.attr[name]
        else:
            raise base.UnderPythonError('Invalid key while getting attribute',
                                        [self, name, self.get_attribute])

    def remove_atk(self):
        self.remove = True


class Attacks:
    def events(self, func):
        setattr(self, func.__name__, func)

    def on_attack_added(self, added_attack: Attack): pass

    def on_attack_removed(self, removed_attack: Attack): pass

    def on_update(self): pass

    def __init__(self, attacker):
        self.attacker = attacker
        self.attacks: list[Attack] = []

    def add(self, atk: Attack):
        atk.on_init()
        self.on_attack_added(atk)
        self.attacks.append(atk)

    def __getitem__(self, item: int):
        return self.attacks[item]

    def update(self):
        self.on_update()
        for atk in self.attacks:
            if atk.remove:
                atk.on_remove()
                self.attacks.remove(atk)
                self.on_attack_removed(atk)
                continue
            pos = game.GAME.ui.souls.get_now().pos
            if type(game.GAME.ui.souls.get_now()) is CyanSoul:
                pos = game.GAME.ui.souls.get_now().dis_pos
            if atk.collide_point(pos) and not game.GAME.player.wd and atk.is_attack:
                dmg = atk.calc_dmg(self.attacker)
                _d = game.GAME.player.on_attacked(self.attacker, dmg)
                if _d is not None:
                    dmg = _d
                game.GAME.player.hurt(dmg)
                if atk.enable_ul:
                    game.GAME.player.st_wd()
            atk.on_action()
            atk.set_img(atk.img)
            atk.tick += 1
            atk.dis.unlock()
            game.GAME.displayer().blit(atk.dis, atk.rect)


class SoulRect:
    def __init__(self):
        self.rect = pg.rect.Rect((640, 300, 1, 1))
        self.exp_rect = pg.rect.Rect((40, 450, 1200, 300))

    def _update(self):
        if math.fabs(self.exp_rect.left - self.rect.left) < 10:
            self.rect.left = self.exp_rect.left
        else:
            self.rect.left += (self.exp_rect.left - self.rect.left) // 2

        if math.fabs(self.exp_rect.width - self.rect.width) < 20:
            self.rect.width = self.exp_rect.width
        else:
            self.rect.width += (self.exp_rect.width - self.rect.width) // 2

        if math.fabs(self.exp_rect.top - self.rect.top) < 10:
            self.rect.top = self.exp_rect.top
        else:
            self.rect.top += (self.exp_rect.top - self.rect.top) // 2

        if math.fabs(self.exp_rect.height - self.rect.height) < 10:
            self.rect.height = self.exp_rect.height
        else:
            self.rect.height += (self.exp_rect.height - self.rect.height) // 2


class Soul:
    color = (255, 255, 255)
    move_in_rect = True

    def __init__(self):
        self.pos = (0, 0)
        soul = [
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0]
        ]
        arr = pg.PixelArray(pg.Surface((8, 8)))
        for i in range(8):
            for j in range(8):
                if soul[i][j]:
                    arr[j, i] = self.color
                else:
                    arr[j, i] = 0
        self.surface = pg.transform.scale_by(arr.make_surface(), 7)
        arr = pg.PixelArray(pg.Surface((8, 8)))
        for i in range(8):
            for j in range(8):
                if soul[i][j]:
                    arr[j, i] = (255, 255, 255)
                else:
                    arr[j, i] = 0
        self.unabled = pg.transform.scale_by(arr.make_surface(), 7)
        self.rect = self.surface.get_rect()
        x, y = self.pos
        self.rect.center = int(x), int(y)

    def set_pos(self, pos: tuple[float, float]):
        s = game.GAME.ui.soul_rect.rect
        x, y = pos
        if self.move_in_rect:
            x = max(min(s.right - 37, x), s.left + 37)
            y = max(s.top + 37, min(s.bottom - 37, y))
        self.pos = x, y
        self.rect.center = int(x), int(y)

    def move_pos(self, apos: tuple[float, float]):
        ax, ay = apos
        x, y = self.pos
        self.set_pos((x + ax, y + ay))

    def update(self):
        pass


class RedSoul(Soul):
    color = (255, 0, 0)

    def update(self):
        self.set_pos(self.pos)
        if game.GAME.player.wd:
            game.GAME.displayer().blit(self.unabled, self.rect)
        else:
            game.GAME.displayer().blit(self.surface, self.rect)
        keys = pg.key.get_pressed()
        spd = 10
        if keys[pg.K_z]:
            spd = 15
        elif keys[pg.K_x]:
            spd = 5
        if keys[pg.K_UP]:
            self.move_pos((0, -spd))
        elif keys[pg.K_DOWN]:
            self.move_pos((0, spd))
        if keys[pg.K_LEFT]:
            self.move_pos((-spd, 0))
        elif keys[pg.K_RIGHT]:
            self.move_pos((spd, 0))


class CyanSoul(Soul):
    color = (0, 255, 255)
    w = 100
    h = 100

    def __init__(self):
        self.dis_pos = (0, 0)
        super().__init__()

    def update(self):
        s = game.GAME.ui.soul_rect.rect
        d = game.GAME.displayer()
        self.set_pos(self.pos)
        _x, _y = self.pos
        self.pos = (round((_x - s.left - self.w // 2) / self.w) * self.w + s.left + self.w // 2,
                    round((_y - s.top - self.h // 2) / self.h) * self.h + s.top + self.h // 2)
        x, y = self.pos
        dx, dy = self.dis_pos
        if abs(dx - x) < 10:
            dx = x
        else:
            dx -= (dx - x) / 2
        if abs(dy - y) < 10:
            dy = y
        else:
            dy -= (dy - y) / 2
        self.dis_pos = dx, dy
        self.rect.center = dx, dy
        if game.GAME.player.wd:
            game.GAME.displayer().blit(self.unabled, self.rect)
        else:
            game.GAME.displayer().blit(self.surface, self.rect)
        for x in range(s.left + self.w, s.right - self.w + 1, self.w):
            pg.draw.line(d, (0, 255, 255), (x, s.top), (x, s.bottom), width=3)
        for y in range(s.top + self.h, s.bottom - self.h + 1, self.h):
            pg.draw.line(d, (0, 255, 255), (s.left, y), (s.right, y), width=3)
        keys = game.GAME.key_events
        if pg.K_UP in keys:
            self.move_pos((0, -self.h))
        elif pg.K_DOWN in keys:
            self.move_pos((0, self.h))
        if pg.K_LEFT in keys:
            self.move_pos((-self.w, 0))
        elif pg.K_RIGHT in keys:
            self.move_pos((self.w, 0))


class BlueSoul(Soul):
    color = (0, 0, 255)
    direction = 0

    def __init__(self):
        super().__init__()
        self.g = 0

    def collide(self) -> bool:
        s = game.GAME.ui.soul_rect.rect
        if self.direction == 0:
            dist = self.rect.bottom - s.bottom
        elif self.direction == 1:
            dist = self.rect.left - s.left
        elif self.direction == 2:
            dist = s.top - self.rect.top
        else:
            dist = s.right - self.rect.right
        dist = abs(dist)
        return dist < 20

    def set_direction(self, _dir):
        self.direction = _dir
        self.g = 0

    def update(self):
        s = game.GAME.ui.soul_rect.rect
        d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            ax, ay = d[(self.direction + 3) % 4]
            self.move_pos((ax * 12, ay * 12))
        elif key[pg.K_RIGHT]:
            ax, ay = d[(self.direction + 1) % 4]
            self.move_pos((ax * 12, ay * 12))
        if key[pg.K_UP] and (self.collide() or self.g >= 0):
            if self.collide():
                self.g = 40
        else:
            if self.g >= 0 and not self.collide():
                self.g = -5
            elif self.collide():
                self.g = 0
        self.g -= 5
        ax, ay = d[(self.direction + 2) % 4]
        self.move_pos((ax * self.g, ay * self.g))
        if game.GAME.player.wd:
            game.GAME.displayer().blit(self.unabled, self.rect)
        else:
            game.GAME.displayer().blit(self.surface, self.rect)


class Souls:
    def __init__(self):
        self.souls = [RedSoul(), CyanSoul(), BlueSoul()]
        self.now = 0

    def get_now(self) -> RedSoul | CyanSoul | BlueSoul | Soul:
        return self.souls[self.now]

    def set_now(self, now, set_pos=True):
        pos = self.get_now().pos
        self.now = max(0, min(len(self.souls) - 1, now))
        if set_pos:
            self.get_now().pos = pos
