from underpython import base


class Inventory:
    hooks = ['on_item_used', 'on_update']

    def on_item_used(self, item_name: str) -> list[str] | None:
        pass

    def on_update(self):
        pass

    def events(self, function: type(base.empty_function)):
        if function.__name__ in self.hooks:
            self.__setattr__(function.__name__, function)
        else:
            raise base.UnderPythonError(f'Undefined hook "{function.__name__}"',
                                    [self.events, function])

    def __init__(self):
        self.inventory = []
        self.items = {'NULL': True}

    def set_item(self, name: str, infinity: bool):
        self.items[name] = infinity

    def set_inventory(self, invent:list[str]):
        for t in invent:
            if t not in self.items.keys():
                raise base.UnderPythonError(f'Unknown item: {t}',
                                       [self.set_inventory, invent])
        self.inventory = invent

    def __index__(self, index: int):
        while len(self.inventory) > index + 1:
            self.inventory.append('NULL')
        return self.inventory[index]

    def append_inventory(self, name: str):
        for i in range(len(self.inventory)):
            if self.inventory[i] == 'NULL':
                self.inventory[i] = name
                return
        self.inventory.append(name)

    def write_data(self, invent):
        self.inventory = invent.inventory
        for k, v in invent.items.items():
            self.items[k] = v
