# basics
def empty_function(): pass
# constant


class Constant:
    def __init__(self, data: int):
        self.data = data


CALCULATE_DAMAGE = Constant(1)


# monster attacks
class Attack:
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
    def on_attack_added(self, added_attack: Attack): pass
    def on_attack_removed(self, removed_attack: Attack): pass
    def on_update(self): pass
    def __init__(self, attacker, targets: list): pass
    def change_targets(self: list): pass
