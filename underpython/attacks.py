import copy

from underpython import base
import pygame as pg
import math


class Attack:
    def events(self, func):
        setattr(self, func.__name__, func)

    def on_action(self, tick: int) -> bool: pass

    def on_init(self): pass

    def on_remove(self): pass

    def __init__(self, position: tuple[int, int], damage: int | base.Constant = base.CALCULATE_DAMAGE, rotation=0): pass

    def update_shapes(self): pass

    def collide_point(self, point: tuple[int, int]): pass

    def update(self): pass

    def move_forward(self, steps: int = 1): pass

    def face_to(self, position: tuple[int, int]): pass

    def set_rotation(self, rotation: int): pass

    def set_attribute(self, name: str, data): pass

    def get_attribute(self, name: str): pass

    def __index__(self, name: str): pass


class Attacks:
    def events(self, func):
        setattr(self, func.__name__, func)

    def on_attack_added(self, added_attack: Attack): pass

    def on_attack_removed(self, removed_attack: Attack): pass

    def on_update(self): pass

    def __init__(self, attacker, targets: list): pass

    def change_targets(self: list): pass

    def __add__(self, atk: Attack): pass

    def __index__(self, idx: int): pass


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

