from underpython import *


class Wave:
    hooks = ['on_wave_start', 'on_wave_update', 'on_wave_end']
    def __init__(self, *args): pass

    def events(self, function: type(empty_function)):
        if function.__name__ in self.hooks:
            self.__setattr__(function.__name__, function)
        else:
            raise UnderPythonError(f'Undefined hook "{function.__name__}"',
                                    [self.events, function])

    def on_wave_start(self): pass

    def on_wave_update(self): pass

    def on_wave_end(self): pass
