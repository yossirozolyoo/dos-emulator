import sys

import core


class BFCore(core.Core):
    # BrainF*ck registers
    __REGISTERS__ = ['DP', 'PC']

    # BrainF*ck single instruction size
    __BF_INSTRUCTION_SIZE__ = 1

    # BrainF*ck register's reset value
    __BF_DP_RESET_VALUE__ = 0x800
    __BF_PC_RESET_VALUE__ = 0

    def __init__(self, *args, **kwargs):
        core.Core.__init__(self, *args, **kwargs)
        self.reset_registers_state()

    def reset_registers_state(self):
        """
        Sets the core's registers to their power-up/RESET values
        """
        self.state['PC'] = self.__BF_PC_RESET_VALUE__
        self.state['DP'] = self.__BF_DP_RESET_VALUE__

    def fetch_and_decode(self):
        raw_instruction = self._mmu.load8(self.state['PC'])
        opcode = raw_instruction & 0xFF
        instruction = _INSTRUCTION_FROM_OPCODE[opcode]()

        return instruction

    def step(self):
        next_instruction = self.fetch_and_decode()
        next_instruction.execute(self)

    def find_matched_close_bracket(self):
        """
        An helper function for finding the matching close bracket (]) of the current open bracket ([)
        :return:
        """
        found = False
        counter = 1
        depth = 1

        while not found:
            current_byte = self.mmu.load8(self.state['PC'] + counter)
            if ord('[') == current_byte:
                depth += 1
            elif ord(']') == current_byte:
                depth -= 1
            if 0 == depth:
                found = True
            counter += 1

        return counter - 1

    def find_matched_open_bracket(self):
        """
        An helper function for finding the matching open bracket ([) of the current close bracket (])
        :return:
        """
        found = False
        counter = 1
        depth = 1

        while not found:
            current_byte = self.mmu.load8(self.state['PC'] - counter)
            if ord(']') == current_byte:
                depth += 1
            elif ord('[') == current_byte:
                depth -= 1
            if 0 == depth:
                found = True
            counter += 1

        return counter - 1


class IncDataPointerInstruction(core.Instruction):
    """
    BrainF*ck '>' Command - increment the data pointer (to point to the next cell to the right).
    """
    __OPCODE__ = ord('>')

    def execute(self, core):
        core.state['DP'] += 1
        core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class DecDataPointerInstruction(core.Instruction):
    """
    BrainF*ck '<' Command - decrement the data pointer (to point to the next cell to the left).
    """
    __OPCODE__ = ord('<')

    def execute(self, core):
        core.state['DP'] -= 1
        core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class IncDataAtDataPointerInstruction(core.Instruction):
    """
    BrainF*ck '+' Command - increment (increase by one) the byte at the data pointer.
    """
    __OPCODE__ = ord('+')

    def execute(self, core):
        data = core.mmu.load8(core.state['DP'])
        data += long(1)
        data &= 0xFF
        core.mmu.store8(core.state['DP'], data)
        core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class DecDataAtDataPointerInstruction(core.Instruction):
    """
    BrainF*ck '-' Command - decrement (decrease by one) the byte at the data pointer.
    """
    __OPCODE__ = ord('-')

    def execute(self, core):
        data = core.mmu.load8(core.state['DP'])
        data -= long(1)
        data &= 0xFF
        core.mmu.store8(core.state['DP'], data)
        core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class OpenBracketInstruction(core.Instruction):
    """
    BrainF*ck '[' Command - if the byte at the data pointer is zero, then instead of moving the instruction pointer
    forward to the next command, jump it forward to the command after the matching ] command
    """
    __OPCODE__ = ord('[')

    def execute(self, core):
        data = core.mmu.load8(core.state['DP'])
        if 0 == data:
            core.state['PC'] += (core.find_matched_close_bracket() + 1)
        else:
            core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class CloseBracketInstruction(core.Instruction):
    """
    BrainF*ck ']' Command - if the byte at the data pointer is nonzero, then instead of moving the instruction pointer
    forward to the next command, jump it back to the command after the matching [ command.
    """
    __OPCODE__ = ord(']')

    def execute(self, core):
        data = core.mmu.load8(core.state['DP'])

        if 0 < data:
            core.state['PC'] -= (core.find_matched_open_bracket() - 1)
        else:
            core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class OutputByteAtDataPointerInstruction(core.Instruction):
    """
    BrainF*ck '.' Command - output the byte at the data pointer.
    """
    __OPCODE__ = ord('.')

    def execute(self, core):
        data = core.mmu.load8(core.state['DP'])
        sys.stdout.write(chr(data))
        core.state['PC'] += BFCore.__BF_INSTRUCTION_SIZE__


class HaltInstruction(core.Instruction):
    """
    New BrainF*ck '$' Command - halt the core
    """
    __OPCODE__ = ord('$')

    def execute(self, core):
        print "\nBye-bye :-)\n"
        exit(0)


_OPCODES = [
    IncDataPointerInstruction,
    DecDataPointerInstruction,
    IncDataAtDataPointerInstruction,
    DecDataAtDataPointerInstruction,
    OpenBracketInstruction,
    CloseBracketInstruction,
    OutputByteAtDataPointerInstruction,
    HaltInstruction
]

_INSTRUCTION_FROM_OPCODE = {opcode.__OPCODE__: opcode for opcode in _OPCODES}
