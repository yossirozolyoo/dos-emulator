import struct


def _deserialize_long(buff):
    result = 0
    for byte in buff[::-1]:
        result <<= 8
        result |= byte

    return result


def _serialize_long(value, size):
    format_string = {
        1: '<B',
        2: '<H',
        4: '<L'
    }[size]

    return struct.pack(format_string, value)


def access(address, width, direction, data):
    return {
        'address': long(address),
        'width': long(width),
        'direction': direction,
        'data': None if data is None else long(data)
    }


def access8(address, direction, data=None):
    return access(address, 8, direction, data)


def access16(address, direction, data=None):
    return access(address, 16, direction, data)


def access32(address, direction, data=None):
    return access(address, 32, direction, data)


def load8(address):
    return access8(address, 'load')


def load16(address):
    return access16(address, 'load')


def load32(address):
    return access32(address, 'load')


def store8(address, data):
    return access8(address, 'store', data)


def store16(address, data):
    return access16(address, 'store', data)


def store32(address, data):
    return access32(address, 'store', data)


class MemoryDevice(object):
    def __init__(self, base, size):
        self._base = base
        self._size = size

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self.base = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def access(self, request):
        raise NotImplementedError

    def load8(self, address):
        return self.access(load8(address))

    def load16(self, address):
        return self.access(load16(address))

    def load32(self, address):
        return self.access(load32(address))

    def store8(self, address, data):
        return self.access(store8(address, data))

    def store16(self, address, data):
        return self.access(store16(address, data))

    def store32(self, address, data):
        return self.access(store32(address, data))

    def update(self):
        pass

class MMU(MemoryDevice):
    def __init__(self, devices=[]):
        super(MMU, self).__init__(0, 0x100000000)

        self._devices = []
        for device in devices:
            self.add_device(device)

    def add_device(self, device):
        # TODO: Store devices as heap
        self._devices.append(device)

    def _address_to_device(self, address):
        for device in self._devices:
            if device.base <= address < device.base + device.size:
                return device

        raise KeyError

    def access(self, request):
        try:
            device = self._address_to_device(request['address'])
        except KeyError:
            raise

        return device.access(request)

    def load_data(self, address, data):
        for offset, byte in enumerate(data):
            self.store8(address + offset, byte)


class RAM(MemoryDevice):
    def __init__(self, base, size):
        super(RAM, self).__init__(base, size)
        self._data = bytearray(size)

    def _address_to_offset(self, address):
        return address - self.base

    @property
    def data(self):
        return bytearray(self._data)

    def access(self, request):
        offset = self._address_to_offset(request['address'])
        size = request['width'] / 8

        if request['direction'] == 'load':
            serialized_data = self._data[offset:offset + size]
            return _deserialize_long(serialized_data)

        elif request['direction'] == 'store':
            serialized_data = _serialize_long(request['data'], size)
            self._data[offset:offset + size] = serialized_data
            return

        raise NotImplementedError


class CodeMemory(MemoryDevice):
    def __init__(self, base, size, data=None):
        super(CodeMemory, self).__init__(base, size)
        self._data = bytearray(size)
        if data is not None:
            self._data = bytearray(data) + bytearray(size - len(data))

    def _address_to_offset(self, address):
        return address - self.base

    def access(self, request):
        offset = self._address_to_offset(request['address'])
        size = request['width'] / 8

        if request['direction'] == 'load':
            serialized_data = self._data[offset:offset + size]
            return _deserialize_long(serialized_data)

        elif request['direction'] == 'store':
            raise MemoryError

        raise NotImplementedError


class DataMemory(MemoryDevice):
    def __init__(self, base, size, zero=False):
        super(DataMemory, self).__init__(base, size)
        if zero:
            self._data = bytearray("\x00" * size)
        else:
            self._data = bytearray(size)

    def _address_to_offset(self, address):
        return address - self.base

    def access(self, request):
        offset = self._address_to_offset(request['address'])
        size = request['width'] / 8

        if request['direction'] == 'load':
            serialized_data = self._data[offset:offset + size]
            return _deserialize_long(serialized_data)

        elif request['direction'] == 'store':
            serialized_data = _serialize_long(request['data'], size)
            self._data[offset:offset + size] = serialized_data
            return

        raise NotImplementedError
