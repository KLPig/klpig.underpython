from underpython import monster, base


class Player:
    hooks = ['on_attack', 'on_act', 'on_item', 'on_mercy', 'on_heal',
             'on_attacked']

    def __init__(self, name: str, hp: int, at: int, df: int, lv: int, wd_time: int = 20):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df
        self.lv = lv
        self.wdt = wd_time
        self.wd = 0

    def events(self, func):
        if func.__name__ in self.hooks:
            setattr(self, func.__name__, func)
        else:
            raise base.UnderPythonError(f'Undefined hook "{func.__name__}"',
                                    [self.events, func])

    def on_attack(self, damage: int, target: monster.Monster) -> int | None: pass

    def on_act(self, name: str, target: monster.Monster): pass

    def on_item(self, name: str): pass

    def on_mercy(self, target: monster.Monster): pass

    def on_heal(self, hp: int) -> int | None: pass

    def on_attacked(self, attacker: monster.Monster, damage: int) -> int | None: pass

    def heal(self, hp: int):
        self.hp = max(min(self.hp + hp, self.max_hp), 0)

    def hurt(self, hp: int):
        self.hp = max(min(self.hp - hp, self.max_hp), 0)

    def st_wd(self):
        self.wd = self.wdt

    def update(self):
        if self.wd:
            self.wd -= 1
