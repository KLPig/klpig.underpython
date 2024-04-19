from underpython import base


class Monster:
    hooks = ['on_act']

    def __init__(self, animation, name: str, hp: int, at: int, df: int, act_options: list[str] = []):
        self.ani = animation
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df
        self.acts = ['check']
        self.acts.extend(act_options)

    def hurt(self, damage: int):
        self.hp = max(self.hp - damage, 0)

    def heal(self, num: int):
        self.hp = min(self.hp + num, self.max_hp)

    def events(self, func):
        if func.__name__ in self.hooks:
            setattr(self, func.__name__, func)
        else:
            raise base.UnderPythonError(f'Undefined hook "{func.__name__}"',
                                    [self.events, func])

    def on_act(self, name: str) -> str | None:
        pass
