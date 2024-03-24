from underpython import *
from base import Player as _Player

del Player


class Player(_Player):
    hooks = ['on_attack', 'on_act', 'on_item', 'on_mercy', 'on_heal',
             'on_attacked']

    def __init__(self, name: str, hp: int, at: int, df: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df

    def events(self, func):
        if func.__name__ in self.hooks:
            setattr(self, func.__name__, func)
        else:
            raise UnderPythonError(f'Undefined hook "{func.__name__}"',
                                    [self.events, func])

    def on_attack(self, damage: int, target: cb.Monster) -> int | None: pass

    def on_act(self, name: str, target: cb.Monster): pass

    def on_item(self, name: str): pass

    def on_mercy(self, target: cb.Monster): pass

    def on_heal(self, hp: int) -> int | None: pass

    def on_attacked(self, attacker: cb.Monster, damage: int) -> int | None: pass

    def heal(self, hp: int):
        self.hp = max(min(self.hp + hp, self.max_hp), 0)

    def hurt(self, hp: int):
        self.hp = max(min(self.hp - hp, self.max_hp), 0)
