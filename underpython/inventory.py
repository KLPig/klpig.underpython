from underpython import *
from base import Inventory as _Inventory

del Inventory


class Inventory(_Inventory):
    def __init__(self):
        self.inventory = []
        self.items = []

    def set_item(self, name: str, infinity: bool):
        self.items.append()
