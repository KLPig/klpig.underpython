from underpython import base, attacks


class Wave:
    hooks = ['on_wave_start', 'on_wave_update', 'on_wave_end']

    def __init__(self, *args):
        self.end = False
        self.tick = 0
        self.attacks: list[attacks.Attacks] = []
        self.on_wave_start()

    def _update(self):
        self.tick += 1
        self.on_wave_update()

    def end_wave(self):
        self.end = True
        self.on_wave_end()

    def events(self, function: type(base.empty_function)):
        if function.__name__ in self.hooks:
            self.__setattr__(function.__name__, function)
        else:
            raise base.UnderPythonError(f'Undefined hook "{function.__name__}"',
                                    [self.events, function])

    def on_wave_start(self): pass

    def on_wave_update(self): pass

    def on_wave_end(self): pass
