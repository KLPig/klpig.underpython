from underpython import game
import pygame as pg


class Animations:
    def __init__(self, pos=(0, 0)):
        self.animation_defines: dict[str, str] = {}
        self.animations: dict[str, list[str]] = {
            'NULL': ['NULL']
        }
        self.instant = ('NULL', 0)
        self.pos = pos

    def __call__(self, *args, **kwargs):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def add_animation(self, name: str, images: list[str]):
        self.animation_defines[name] = name
        self.animations[name] = [m for m in images]

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

    def _update(self):
        _name, frame = self.instant
        name = self.find_ani_name(_name)
        _surface = self.animations[name][frame]
        surface = game.GAME.graphics[_surface]
        rect = surface.get_rect()
        rect.center = self.pos
        game.GAME.displayer[0].blit(surface, rect)
