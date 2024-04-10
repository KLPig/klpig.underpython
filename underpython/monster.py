from underpython import animations as ani


class Monster:
    def __init__(self, animation: object | None, name: str, hp: int, at: int, df: int):
        self.ani = animation
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df
