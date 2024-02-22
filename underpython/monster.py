from underpython import *
from base import Monster as _Monster
del Monster


class Monster(_Monster):
    def __init__(self, animation: Animations | None, name: str, hp: int, at: int, df: int):
        self.ani = animation
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df
