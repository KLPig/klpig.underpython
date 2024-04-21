import pygame as pg


class _Chanel:
    loop = False

    def __init__(self):
        self.sound: pg.mixer.Sound | None = None

    def play(self, _sound: pg.mixer.Sound):
        if self.sound is not None:
            del self.sound
            self.sound = None
        self.sound = _sound
        self.sound.play(-self.loop)

    def stop(self):
        if self.sound is not None:
            self.sound.stop()

    def resume(self):
        if self.sound is not None:
            self.sound.play()


class _MChanel(_Chanel):
    def play(self, _sound: pg.mixer.Sound):
        if self.sound is not None:
            self.sound.stop()
        super().play(_sound)
    loop = True


Chanel = _Chanel()
MChanel = _MChanel()

