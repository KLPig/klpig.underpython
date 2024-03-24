from game import *
from base import Animations as _Animations
import pygame as pg

del Animations


class Animations(_Animations):
    def __init__(self):
        self.animation_defines: dict[str, str] = {}
        self.animations: dict[str, list[tuple[str, pg.rect.Rect]]] = {
            'NULL': [('NULL', pg.rect.Rect(0, 0, 0, 0))]
        }
        self.instant = ('NULL', 0)

    def add_animation(self, name: str, images: list[str]):
        self.animation_defines[name] = name
        self.animations[name] = [(m, GAME.graphics[m].get_rect()) for m in images]

    def change_animation(self, name: str):
        self.instant = (name, 0)

    # Disjoint union sets
    def define_animation(self, old_ani: str, new_ani: str):
        self.animation_defines[old_ani] = new_ani

    def find_ani_name(self, name: str) -> str:
        if self.animation_defines[name] == name:
            return name
        else:
            self.animation_defines[name] = \
                self.find_ani_name(self.animation_defines[name])
            return self.animation_defines[name]
        
