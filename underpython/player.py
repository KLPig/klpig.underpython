from underpython import *
from base import Player as _Player

del Player


class Player(_Player):
    def __init__(self, name: str, hp: int, at: int, df: int):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df

    def heal(self, hp: int):
        self.hp = max(min(self.hp + hp, self.max_hp), 0)

    def hurt(self, hp: int):
        self.hp = max(min(self.hp - hp, self.max_hp), 0)
