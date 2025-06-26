import os
import sys

INSTRUCTION_SET = {
    "LDA": 5,
    "STA": 3,
    "ADD": 1,
    "SUB": 2,
    "INP": "901",
    "OUT": "902",
    "HLT": "000",
    "BRZ": 7,
    "BRP": 8,
    "BRA": 6,
    "DAT": None,
}

LABELS = {}
def decode_labels(mem_addr: int, tokens: str):
    # one pass
    # figure out if firs element is label or opcode
    if tokens[0] not in INSTRUCTION_SET:
        LABELS[tokens[0]] = mem_addr

def assembler(tokens: list) -> str:

    print()
    op = None
    operand = None
    for idx, token in enumerate(tokens):
        # figure out what each token is
        if token in LABELS:
            if idx > 0:
                operand = token
            else:
                continue
        elif token.isdigit():
            operand = token
        elif token in INSTRUCTION_SET:
            op = token
        else:
            raise ValueError("INVALID op")

    # decode opcode
    opcode = 100
    if op and op in {"INP", "OUT", "HLT"}:
        return INSTRUCTION_SET[op]
    elif op and op == "DAT":
        opcode = 0
    else:
        opcode *= INSTRUCTION_SET[op]

    # decode operand and combine with opcode
    if operand:
        if operand.isdigit():
            opcode += int(operand)
        if operand in LABELS:
            opcode += LABELS[operand] 

    return str(opcode)
    


def tokenize(instruction: str) -> list:
    tokens = instruction.split(" ")
    if len(tokens) > 3:
        raise ValueError("INVALID INSTURCTION")
    if len(tokens) == 0:
        return None
    return tokens

def main(argc: int, argv: list) -> int:
    if argc < 2:
        print("Need an .lmc file")
        return 1
    lmc_file = argv[1]
    try:
        with open(lmc_file, "r") as f:
            for line_num, line in enumerate(f):
                if line_num > 99:
                    raise ValueError("INVALID MEMORY ADDRESS USED")
                # ONE PASS
                instruction = line.strip()
                tokens = tokenize(instruction)
                if not tokens: continue
                decode_labels(line_num, tokens)
            
        binary_fp = os.path.join(os.getcwd(), "a.lmcc")
        with open(binary_fp, mode="w") as bf:
            with open(lmc_file, mode="r") as f:
                for line_num, line in enumerate(f):
                    # TWO PASS
                    instruction = line.strip()
                    tokens = tokenize(instruction)
                    if not tokens: continue
                    opcode = assembler(tokens) + " "
                    print(f"opcode: {opcode}")
                    bf.write(opcode)
    except FileNotFoundError as e:
        print(e)
        print(f"Error with opening .lmc file: {lmc_file} from {os.getcwd()}")
        return 1
    except Exception as e:
        print(e)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))