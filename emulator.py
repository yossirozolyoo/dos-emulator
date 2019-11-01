import argparse
import dosarch
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

        # Init Core
        self._core = bfarch.BFCore(self._mmu)

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

    while True:
        processor.core.step()


if __name__ == '__main__':
    main()
