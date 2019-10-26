import argparse
import dosarch
import memory


CODE = bytearray(''.join(['\x01\x00\x00\x00',
                 '\x01\x01\x00\x00']))


class ExampleProcessor(object):
    def __init__(self):
        # Init memory devices
        self._mmu = memory.MMU()
        self._mmu.add_device(memory.RAM(0, 0x1000))

        # Init Core
        self._core = dosarch.DosCore(self._mmu)

    @property
    def mmu(self):
        return self._mmu

    @property
    def core(self):
        return self._core


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    processor = ExampleProcessor()
    processor.mmu.load_data(0, CODE)
    processor.core.step()
    processor.core.step()
    print processor.core.state


if __name__ == '__main__':
    main()