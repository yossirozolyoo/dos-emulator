import display
import argparse
import bfarch
import memory

# Fibonacci sequence - BrainF*ck
CODE = bytearray(
    "+++++++++++>+>>>>++++++++++++++++++++++++++++++++++++++++++++>++++++++++++++++++++++++++++++++<<<<<<[>[>>>>>>+>+<<"
    "<<<<<-]>>>>>>>[<<<<<<<+>>>>>>>-]<[>++++++++++[-<-[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<[>>>+<<<-]>>[-]]<<]>>>[>>"
    "+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<+>>[-]]<<<<<<<]>>>>>[++++++++++++++++++++++++++++++++++++++++++++++++.[-]]+++"
    "+++++++<[->-<]>++++++++++++++++++++++++++++++++++++++++++++++++.[-]<<<<<<<<<<<<[>>>+>+<<<<-]>>>>[<<<<+>>>>-]<-[>>."
    ">.<<<[-]]<<[>>+>+<<<-]>>>[<<<+>>>-]<<[<+>-]>[<+>-]<<<-]$")


class ExampleProcessor(object):
    def __init__(self):
        # Init memory devices
        self._mmu = memory.MMU()

        # Harvard architecture - CODE/DATA separation
        self._mmu.add_device(memory.CodeMemory(0, 0x800, data=CODE))
        self._mmu.add_device(memory.DataMemory(0x800, 0x1000, zero=True))

        # Display
        display_device = display.DisplayDevice(0x10000, 640, 480)
        self._mmu.add_device(display_device)

        self._updated_devices = [display_device]

        # Init Core
        self._core = bfarch.BFCore(self._mmu)

    @property
    def mmu(self):
        return self._mmu

    @property
    def core(self):
        return self._core

    def update_devices(self):
        for device in self._updated_devices:
            device.update()


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    processor = ExampleProcessor()

    import time
    while True:
        processor.core.step()
        processor.update_devices()


if __name__ == '__main__':
    main()
