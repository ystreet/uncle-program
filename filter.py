
class ProgramFilter ():
    program = None

    def __init__ (self, program):
        self.program = program

    def filter (self):
        raise NotImplementedError


