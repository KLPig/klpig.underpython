class Monster:
    def __init__(self, animation, name: str, hp: int, at: int, df: int):
        self.ani = animation
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df

    def hurt(self, damage: int):
        self.hp = max(self.hp - damage, 0)

    def heal(self, num: int):
        self.hp = min(self.hp + num, self.max_hp)
