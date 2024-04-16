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


class UnderPythonWarning(Warning):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'UnderPythonWarning: %s' % self.message

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


class Hooks:
    def __init__(self): pass

    def on_wave_end(self, wave): pass

    def on_wave_start(self, wave): pass

    def on_init(self): pass

    def on_game_end(self): pass

    def on_game_won(self, method: GameMethod): pass

    def on_game_lost(self): pass

    def on_game_escaped(self): pass

    def on_game_quit(self): pass
