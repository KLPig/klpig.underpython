from underpython import monster, base, chanel, game


class Player:
    hooks = ['on_attack', 'on_act', 'on_item', 'on_mercy', 'on_heal',
             'on_attacked', 'on_save', 'on_saved']

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

    def on_attack(self, damage: int, target: monster.Monster) -> int | None | str:
        return damage * max(self.at * 5 - target.df * 3, 0) // 3

    def on_act(self, name: str, target: monster.Monster): pass

    def on_item(self, name: str): pass

    def on_mercy(self, target: monster.Monster): pass

    def on_heal(self, hp: int) -> int | None: pass

    def on_attacked(self, attacker: monster.Monster, damage: int) -> int | None: pass

    def on_save(self) -> list[str] | None: pass

    def on_saved(self, name: str) -> list[str] | None: pass

    def heal(self, hp: int, gg=None):
        if gg is None:
            ggg = game.GAME
        else:
            ggg = gg
        if hp > 0:
            chanel.Chanel.play(ggg.sounds['healsound'])
        elif hp < 0:
            chanel.Chanel.play(ggg.sounds['hurtsound'])
        self.hp = max(min(self.hp + hp, self.max_hp), 0)

    def hurt(self, hp: int):
        gg = game.GAME
        if hp < 0:
            chanel.Chanel.play(gg.sounds['healsound'])
        elif hp > 0:
            chanel.Chanel.play(gg.sounds['hurtsound'])
        self.hp = max(self.hp - hp, 0)

    def st_wd(self):
        self.wd = self.wdt

    def update(self):
        if self.wd:
            self.wd -= 1

    def write_data(self, p):
        self.name, self.hp, self.max_hp, self.at, self.df, self.lv, self.wdt = \
        p.name, p.hp, p.max_hp, p.at, p.df, p.lv, p.wdt
