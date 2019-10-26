class Register(object):
    __MASK__ = 0xFFFFFFFF

    def __init__(self, value=0):
        self._value = long(value) & self.__MASK__

    def __int__(self):
        return int(self._value)

    def __long__(self):
        return long(self._value)

    def __add__(self, other):
        return Register(self._value + long(other))

    def __radd__(self, other):
        return Register.__add__(self, other)

    def __iadd__(self, other):
        self._value = (self._value + long(other)) & self.__MASK__
        return self

    def __sub__(self, other):
        return Register(self._value - long(other))

    def __rsub__(self, other):
        return Register(long(other) - self._value)

    def __isub__(self, other):
        self._value = (self._value - long(other)) & self.__MASK__
        return self

    def __mul__(self, other):
        return Register(self._value * long(other))

    def __rmul__(self, other):
        return Register.__mul__(self, other)

    def __imul__(self, other):
        self._value = (self._value * long(other)) & self.__MASK__
        return self

    def __div__(self, other):
        return Register(self._value / long(other))

    def __rdiv__(self, other):
        return Register(long(other) / self._value)

    def __idiv__(self, other):
        self._value = (self._value / long(other)) & self.__MASK__
        return self

    def __lshift__(self, other):
        return Register(self._value << long(other))

    def __rlshift__(self, other):
        return Register(long(other) << self._value)

    def __ilshift__(self, other):
        self._value = (self._value << long(other)) & self.__MASK__
        return self

    def __rshift__(self, other):
        return Register(self._value >> long(other))

    def __rrshift__(self, other):
        return Register(long(other) >> self._value)

    def __irshift__(self, other):
        self._value >>= long(other)
        return self

    def __and__(self, other):
        return Register(self._value & long(other))

    def __rand__(self, other):
        return Register.__and__(self, other)

    def __iand__(self, other):
        self._value &= long(other)
        return self

    def __or__(self, other):
        return Register(self._value | long(other))

    def __ror__(self, other):
        return Register.__or__(self, other)

    def __ior__(self, other):
        self._value = (self._value | long(other)) & self.__MASK__
        return self

    def __xor__(self, other):
        return Register(self._value ^ long(other))

    def __rxor__(self, other):
        return Register.__xor__(self, other)

    def __ixor__(self, other):
        self._value = (self._value ^ long(other)) & self.__MASK__
        return self

    def __repr__(self):
        return '0x{:08x}'.format(self._value)
