import sys
import argparse

class RAM:
    SIZE = 100

    def __init__(self):
        self.memory = [0] * self.SIZE    # 0..99 address space init with 000

    def write(self, mem_addr: int, data: int) -> int:
        if self.SIZE < mem_addr < 0:
            return 1
        self.memory[mem_addr] = data
        return 0

    def read(self, mem_addr: int) -> int:
        return self.memory[mem_addr]

class CPU:
    # ref: https://www.yorku.ca/sychen/research/LMC/LMCInstructions.html

    def __init__(self):
        self.pc = 0                 # program counter
        self.i_reg = 0              # instruction register
        self.addr_reg = 0           # address register
        self.accum = 0              # accumulator
        self.halted = False         # state

    def fetch_cycle(self, ram: RAM) -> int:
        """Fetch next CPU instruction from RAM"""
        if self.halted:
            return None
        instruction = ram.memory[self.pc]
        self.pc += 1
        self.i_reg = instruction // 100
        self.addr_reg = instruction % 100
        return instruction

    def execute_instruction(self, ram: RAM):
        """Execute CPU loaded instructions that where fetched from RAM"""
        if self.halted:
            return None
        match self.i_reg:
            case 0: #hlt 000
                print("hlt")
                self.halted = True
            case 1: # add
                print("add")
                self.accum += ram.read(self.addr_reg)
            case 2: # sub
                print("sub")
                self.accum -= ram.read(self.addr_reg)
            case 3: # sta
                print("sta")
                ram.write(self.addr_reg, self.accum)
            case 5: # lda
                print("lda")
                self.accum = ram.read(self.addr_reg)
            case 6: # bra
                print("bra")
            case 7: # brz
                print("brz")
            case 8: # brp
                print("brp")
            case 9: # io
                print("io")
                if self.addr_reg == 2: # out 902
                    print(f"OUTPUT: {self.accum}")
                elif self.addr_reg == 1: # inp 901
                    self.accum = int(input("INPUT: "))

class LMCParser:
    """
    Parses everything of the .lmc file into a 'compiled' file if wanted with the instructions.
    After creating the compiled file it can be loaded into memory by the LMC.
    Maybe this way it might be more flexible
    """
    ...

class LMC:
    OPCODE_SET = {
        "HLT": 000,
        "ADD": 1,
        "SUB": 2,
        "STA": 3,
        "STO": 3,
        "LDA": 5,
        "BRA": 6,
        "BRZ": 7,
        "BRP": 8,
        "INP": 901,
        "OUT": 902,
        "OTC": 9,
        "DAT": 0
    }

    def __init__(self):
        self.ram = RAM()
        self.cpu = CPU()

    def parse_line(self, line: str) -> int:
        words = line.split()

        # get opcode from mnemonic
        mnemonic = words[0].upper()
        if mnemonic in ("HLT", "INP", "OUT"):
            # return preset instruction (opcode + operand)
            return self.OPCODE_SET[mnemonic]
        # TODO: case for DAT
        opcode = self.OPCODE_SET[mnemonic] * 100

        # get operand and create complete instruction code
        operand = int(words[1])
        instruction = opcode + operand
        return instruction

    def load_lmc(self, rel_file_path):
        """Load .lmc file into RAM"""
        # TODO: make rel_file_path OS agnostic
        mem_addr = 0    # each line is a corresponding memory address
        with open(rel_file_path) as f:
            for line in f:
                instruction = self.parse_line(line)
                self.ram.write(mem_addr, instruction)
                mem_addr += 1
        print("LOADED MEM:\n", self.ram.memory)

    def execute(self):
        """Execute .lmc code that was loaded into RAM"""
        while True:
            if not self.cpu.fetch_cycle(self.ram):
                break
            self.cpu.execute_instruction(self.ram)


def main(args) -> int:
    lmc = LMC()
    lmc.load_lmc(args.lmc_file)
    print("File parsed to virtual Memory")
    print("execute file")
    lmc.execute()
    return 0

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple Little Man Computer (LMC) simulation")
    parser.add_argument("lmc_file", help="LMC code file")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    sys.exit(main(args))