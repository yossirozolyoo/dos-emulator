import collections
import register


class Instruction(object):
    def __init__(self):
        pass

    def execute(self, processor):
        raise NotImplementedError


class Core(object):
    __REGISTERS__ = []

    def __init__(self, mmu):
        self._mmu = mmu

        # Init state
        self._state = collections.OrderedDict((reg, register.Register()) for reg in self.__REGISTERS__)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        for key in self._state:
            if key in value:
                self._state[key] = value[key]

    def fetch_and_decode(self):
        raise NotImplementedError