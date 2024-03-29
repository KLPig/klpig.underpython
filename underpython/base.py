import underpython.class_base as cb


# basics
def empty_function(): pass


# Errors

class UnderPythonError(Exception):
    def __init__(self, message, objects: list = None):
        self.message = message
        self.obj = objects

    def __str__(self):
        s = f'\nUnderPythonError: {self.message}.'
        if type(self.obj[0]) is list:
            s += '\nWhile raising the error, we received '\
                 'some objects or methods with some descriptions '\
                 'that should be wrong:\n'
            for o in self.obj:
                s += f'A {str(type(o[0]))} object: {str(o[0])}, {str(o[1])}\n'
        elif type(self.obj) is list:
            s += '\nWhile raising the error, we received '\
                 'some objects or methods that should be wrong:\n'
            for o in self.obj:
                s += f'A {str(type(o))} object: {str(o)}\n'
        else:
            s += '\nNo more description received\n'
        return s


# constant


class Constant:
    def __init__(self, data: int):
        self.data = data


CALCULATE_DAMAGE = Constant(1)


class GameMethod(Constant):
    pass


MERCY_ROUTE = GameMethod(2)
GENOCIDE_ROUTE = GameMethod(3)
NORMAL_ROUTE = GameMethod(4)


# monster attacks
class Attack:
    def events(self, func):
        setattr(self, func.__name__, func)

    def on_action(self, tick: int) -> bool: pass

    def on_init(self): pass

    def on_remove(self): pass

    def __init__(self, position: tuple[int, int], damage: int | Constant = CALCULATE_DAMAGE, rotation=0): pass

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


# general
class Animations:
    def events(self, func):
        setattr(self, func.__name__, func)

    def on_animation_changed(self, prev_animation_name: str): pass

    def on_update(self): pass

    def __init__(self, name: str): pass

    def add_animation(self, name: str, numbers: list[int]): pass

    def change_animation(self, name: str): pass

    def define_animation(self, old_ani: str, new_ani: str): pass

    def find_ani_name(self, name: str) -> str: pass


class Player(cb.Player):
    def __init__(self, *args): pass

    def events(self, func):
        setattr(self, func.__name__, func)

    def on_attack(self, damage: int, target: cb.Monster) -> int | None: pass

    def on_act(self, name: str, target: cb.Monster): pass

    def on_item(self, name: str): pass

    def on_mercy(self, target: cb.Monster): pass

    def on_heal(self, hp: int) -> int | None: pass

    def on_attacked(self, attacker: cb.Monster, damage: int) -> int | None: pass

    def heal(self, hp: int): pass

    def hurt(self, hp: int): pass


class Monster(cb.Monster):
    def __init__(self, *args): pass

    def events(self, func):
        setattr(self, func.__name__, func)

    def on_act(self, name: str): pass

    def on_spared(self): pass

    def on_hurt(self, damage: int) -> int | None: pass

    def on_heal(self, hp: int) -> int | None: pass

    def on_attacked(self, damage: int) -> int | None: pass

    def on_attack(self, damage: int) -> int | None: pass


class Wave:
    def __init__(self, *args): pass

    def events(self, func):
        setattr(self, func.__name__, func)

    def on_wave_start(self): pass

    def on_wave_update(self): pass

    def on_wave_end(self): pass


class Inventory:
    def __init__(self):pass

    def events(self, func):
        setattr(self, func.__name__, func)

    def on_item_used(self, name: str): pass

    def set_item(self, name: str, infinity: bool): pass

    def set_inventory(self, name: list[str]): pass

    def __add__(self, other: str): pass


class Hooks:
    def __init__(self):pass

    def events(self, func):
        setattr(self, func.__name__, func)

    def on_wave_end(self, wave: Wave): pass

    def on_wave_start(self, wave: Wave): pass

    def on_init(self): pass

    def on_game_end(self): pass

    def on_game_won(self, method: GameMethod): pass

    def on_game_lost(self): pass

    def on_game_escaped(self): pass

    def on_game_quit(self): pass


# game
class Game:
    def __init__(self, *args): pass
    def build(self): pass
    def go(self): pass


# constants


SystemPlayerAttacker = Monster(None, 'Attacker', 0, 0, 0)
SystemMonsterAttacker = Player('Attacker', 0, 0, 0)
