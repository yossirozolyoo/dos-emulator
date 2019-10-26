import core


class DosCore(core.Core):
    __REGISTERS__ = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
                     'R7', 'R8', 'R9', 'R10', 'R11', 'R12',
                     'SP', 'LR', 'PC']

    def fetch_and_decode(self):
        raw_instruction = self._mmu.load32(self.state['PC'])
        opcode = raw_instruction & 0xFF
        instruction = _INSTRUCTION_FROM_OPCODE[opcode](raw_instruction)

        return instruction

    def step(self):
        next_instruction = self.fetch_and_decode()
        next_instruction.execute(self)


class IncInstruction(core.Instruction):
    __OPCODE__ = 1

    def __init__(self, raw):
        self._register = DosCore.__REGISTERS__[(raw >> 8) & 0xF]

    def execute(self, core):
        core.state[self._register] += 1
        core.state['PC'] += 4


_OPCODES = [
    IncInstruction
]


_INSTRUCTION_FROM_OPCODE = {opcode.__OPCODE__: opcode for opcode in _OPCODES}