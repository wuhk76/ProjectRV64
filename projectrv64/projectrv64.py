class RV64:
    def __init__(self):
        self.arch = 'RISC-V RV64IM'
        self.registers = {'zero': 0, 'ra': 0, 'sp': 0, 'gp': 0, 'tp': 0, 't0': 0, 't1': 0, 't2': 0, 's0': 0, 's1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 0, 'a6': 0, 'a7': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0, 's9': 0, 's10': 0, 's11': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0}
        self.pcount = 0
        self.mem = bytearray(0x1000000)
        self.opcodes = {
            'LUI': self.LUI,
            'AUIPC': self.AUIPC,
            'JAL': self.JAL,
            'JALR': self.JALR,
            'BEQ': self.BEQ,
            'BNE': self.BNE,
            'BLT': self.BLT,
            'BGE': self.BGE,
            'BLTU': self.BLTU,
            'BGEU': self.BGEU,
            'LB': self.LB,
            'LD': self.LD,
            'LH': self.LH,
            'LW': self.LW,
            'LWU': self.LWU,
            'LBU': self.LBU,
            'LHU': self.LHU,
            'SB': self.SB,
            'SH': self.SH,
            'SW': self.SW,
            'ADDI': self.ADDI,
            'ADDIW': self.ADDIW,
            'SLTI': self.SLTI,
            'SLTIU': self.SLTIU,
            'XORI': self.XORI,
            'ORI': self.ORI,
            'ANDI': self.ANDI,
            'SD': self.SD,
            'SLLI': self.SLLI,
            'SLLIW': self.SLLIW,
            'SRLI': self.SRLI,
            'SRLIW': self.SRLIW,
            'SRAI': self.SRAI,
            'SRAIW': self.SRAIW,
            'ADD': self.ADD,
            'ADDW': self.ADDW,
            'SUB': self.SUB,
            'SUBW': self.SUBW,
            'SLL': self.SLL,
            'SLLW': self.SLLW,
            'SLT': self.SLT,
            'SLTU': self.SLTU,
            'XOR': self.XOR,
            'SRL': self.SRL,
            'SRLW': self.SRLW,
            'SRA': self.SRA,
            'SRAW': self.SRAW,
            'OR': self.OR,
            'AND': self.AND,
            'MUL': self.MUL,
            'MULW': self.MULW,
            'MULH': self.MULH,
            'MULHSU': self.MULHSU,
            'MULHU': self.MULHU,
            'DIV': self.DIV,
            'DIVW': self.DIVW,
            'DIVU': self.DIVU,
            'DIVUW': self.DIVUW,
            'REM': self.REM,
            'REMW': self.REMW,
            'REMU': self.REMU,
            'REMUW': self.REMUW
        }
    def LUI(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = imm << 12
    def AUIPC(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.pcount + (imm << 12)
    def JAL(self, rd, imm):
        pc = self.pcount
        if rd != 'zero':
            self.registers[rd] = pc + 4
        self.pcount = pc + imm
    def JALR(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.pcount + 4
        self.pcount = (self.registers[rs1] + imm) & ~1
    def BEQ(self, rs1, rs2, imm):
        if self.registers[rs1] == self.registers[rs2]:
            self.pcount += imm
        else:
            self.pcount += 4
    def BNE(self, rs1, rs2, imm):
        if self.registers[rs1] != self.registers[rs2]:
            self.pcount += imm
        else:
            self.pcount += 4
    def BLT(self, rs1, rs2, imm):
        if self.registers[rs1] < self.registers[rs2]:
            self.pcount += imm
        else:
            self.pcount += 4
    def BGE(self, rs1, rs2, imm):
        if self.registers[rs1] >= self.registers[rs2]:
            self.pcount += imm
        else:
            self.pcount += 4
    def BLTU(self, rs1, rs2, imm):
        if self.registers[rs1] & 0xFFFFFFFFFFFFFFFF < self.registers[rs2] & 0xFFFFFFFFFFFFFFFF:
            self.pcount += imm
        else:
            self.pcount += 4
    def BGEU(self, rs1, rs2, imm):
        if self.registers[rs1] & 0xFFFFFFFFFFFFFFFF >= self.registers[rs2] & 0xFFFFFFFFFFFFFFFF:
            self.pcount += imm
        else:
            self.pcount += 4
    def LB(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.mem[address]
        if value & 0x80:
            value -= 256
        if rd != 'zero':
            self.registers[rd] = value
    def LD(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address+8], 'little', signed=True)
        if rd != 'zero':
            self.registers[rd] = value
    def LH(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address+2], 'little', signed=True)
        if rd != 'zero':
            self.registers[rd] = value
    def LW(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address+4], 'little', signed=True)
        if rd != 'zero':
            self.registers[rd] = value
    def LWU(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address+4], 'little', signed=False)
        if rd != 'zero':
            self.registers[rd] = value
    def LBU(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.mem[address]
        if rd != 'zero':
            self.registers[rd] = value
    def LHU(self, rd, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address+2], 'little', signed=False)
        if rd != 'zero':
            self.registers[rd] = value
    def SB(self, rs2, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        self.mem[address] = self.registers[rs2] & 0xFF
    def SH(self, rs2, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        self.mem[address:address+2] = self.registers[rs2].to_bytes(2, 'little', signed=True)
    def SW(self, rs2, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        self.mem[address:address+4] = self.registers[rs2].to_bytes(4, 'little', signed=True)
    def ADDI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] + imm
    def ADDIW(self, rd, rs1, imm):
        if rd != 'zero':
            val = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
            val = (val & 0xFFFFFFFF)
            if val & 0x80000000:
                val -= 0x100000000
            self.registers[rd] = val
    def SLTI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = 1 if self.registers[rs1] < imm else 0
    def SLTIU(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = 1 if (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) < (imm & 0xFFFFFFFFFFFFFFFF) else 0
    def XORI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] ^ imm
    def ORI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] | imm
    def ANDI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] & imm
    def SD(self, rs2, rs1, imm):
        address = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        self.mem[address:address+8] = self.registers[rs2].to_bytes(8, 'little', signed=True)
    def SLLI(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x3F
            result = (self.registers[rs1] << shamt) & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = result
    def SLLIW(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x1F
            val = self.registers[rs1] & 0xFFFFFFFF
            result = (val << shamt) & 0xFFFFFFFF
            if result & 0x80000000:
                result -= 0x100000000
            self.registers[rd] = result
    def SRLI(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x3F
            val = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
            result = val >> shamt
            self.registers[rd] = result
    def SRLIW(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x1F
            val = self.registers[rs1] & 0xFFFFFFFF
            result = val >> shamt
            self.registers[rd] = result
    def SRAI(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x3F
            val = self.registers[rs1]
            if val & (1 << 63):
                val = val - (1 << 64)
            result = val >> shamt
            self.registers[rd] = result & 0xFFFFFFFFFFFFFFFF
    def SRAIW(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x1F
            val = self.registers[rs1] & 0xFFFFFFFF
            if val & 0x80000000:
                val -= 0x100000000
            result = val >> shamt
            self.registers[rd] = result & 0xFFFFFFFFFFFFFFFF
    def ADD(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
    def ADDW(self, rd, rs1, rs2):
        if rd != 'zero':
            val = (self.registers[rs1] + self.registers[rs2]) & 0xFFFFFFFF
            if val & 0x80000000:
                val -= 0x100000000
            self.registers[rd] = val
    def SUB(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
    def SUBW(self, rd, rs1, rs2):
        if rd != 'zero':
            val = (self.registers[rs1] - self.registers[rs2]) & 0xFFFFFFFF
            if val & 0x80000000:
                val -= 0x100000000
            self.registers[rd] = val
    def SLL(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x3F
            result = (self.registers[rs1] << shamt) & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = result
    def SLLW(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x1F
            val = self.registers[rs1] & 0xFFFFFFFF
            result = (val << shamt) & 0xFFFFFFFF
            if result & 0x80000000:
                result -= 0x100000000
            self.registers[rd] = result
    def SLT(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0
    def SLTU(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = 1 if (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) < (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF) else 0
    def XOR(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
    def SRL(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x3F
            val = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
            result = val >> shamt
            self.registers[rd] = result
    def SRLW(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x1F
            val = self.registers[rs1] & 0xFFFFFFFF
            result = val >> shamt
            self.registers[rd] = result
    def SRA(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x3F
            val = self.registers[rs1]
            if val & (1 << 63):
                val = val - (1 << 64)
            result = val >> shamt
            self.registers[rd] = result & 0xFFFFFFFFFFFFFFFF
    def SRAW(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x1F
            val = self.registers[rs1] & 0xFFFFFFFF
            if val & 0x80000000:
                val -= 0x100000000
            result = val >> shamt
            self.registers[rd] = result & 0xFFFFFFFFFFFFFFFF
    def OR(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] | self.registers[rs2]
    def AND(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] & self.registers[rs2]
    def MUL(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] * self.registers[rs2]
    def MULW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            if a & 0x80000000:
                a -= 0x100000000
            b = self.registers[rs2] & 0xFFFFFFFF
            if b & 0x80000000:
                b -= 0x100000000
            product = (a * b) & 0xFFFFFFFF
            if product & 0x80000000:
                product -= 0x100000000
            self.registers[rd] = product
    def MULH(self, rd, rs1, rs2):
        def signextend(value):
            if value & (1 << 63):
                return value - (1 << 64)
            else:
                    return value
        if rd != 'zero':
            a = signextend(self.registers[rs1])
            b = signextend(self.registers[rs2])
            product = a * b
            high = (product >> 64) & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = high
    def MULHSU(self, rd, rs1, rs2):
        def signextend(value):
            if value & (1 << 63):
                return value - (1 << 64)
            else:
                return value
        if rd != 'zero':
            a = signextend(self.registers[rs1])
            b = self.registers[rs2] & 0xFFFFFFFFFFFFFFFF
            product = a * b
            high = (product >> 64) & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = high
    def MULHU(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFFFFFFFFFF
            product = a * b
            high = (product >> 64) & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = high
    def DIV(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = 0xFFFFFFFFFFFFFFFF
            else:
                self.registers[rd] = self.registers[rs1] // self.registers[rs2]
    def DIVW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            if a & 0x80000000:
                a -= 0x100000000
            b = self.registers[rs2] & 0xFFFFFFFF
            if b & 0x80000000:
                b -= 0x100000000
            if b == 0:
                self.registers[rd] = 0xFFFFFFFFFFFFFFFF
            elif a == -0x80000000 and b == -1:
                self.registers[rd] = a & 0xFFFFFFFFFFFFFFFF
            else:
                q = int(a / b)
                if q < 0:
                    q += 0x100000000
                self.registers[rd] = q & 0xFFFFFFFFFFFFFFFF
    def DIVU(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = 0xFFFFFFFFFFFFFFFF
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) // (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF)
    def DIVUW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFF
            if b == 0:
                self.registers[rd] = 0xFFFFFFFFFFFFFFFF
            else:
                q = a // b
                self.registers[rd] = q & 0xFFFFFFFFFFFFFFFF
    def REM(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = self.registers[rs1]
            else:
                self.registers[rd] = self.registers[rs1] % self.registers[rs2]
    def REMW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            if a & 0x80000000:
                a -= 0x100000000
            b = self.registers[rs2] & 0xFFFFFFFF
            if b & 0x80000000:
                b -= 0x100000000
            if b == 0:
                r = a
            elif a == -0x80000000 and b == -1:
                r = 0
            else:
                r = a % b
            if r < 0:
                r += 0x100000000
            self.registers[rd] = r & 0xFFFFFFFFFFFFFFFF
    def REMU(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = self.registers[rs1]
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) % (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF)
    def REMUW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFF
            if b == 0:
                self.registers[rd] = a & 0xFFFFFFFFFFFFFFFF
            else:
                r = a % b
                self.registers[rd] = r & 0xFFFFFFFFFFFFFFFF
    def execute(self, asmpath, pc = 0, mem = None, imax = 0, debug = False):
        def parsevalue(x):
            try:
                return int(x.strip(), 0)
            except:
                return x
        self.pcount = int(pc) if int(pc) > 0 else 0
        self.mem = bytearray(0x1000000) if mem is None else mem
        self.registers = {key: 0 for key in self.registers}
        aliases = [key for key in self.registers]
        if imax > 0:
            icount = 0
        if isinstance(asmpath, list):
            asm = asmpath
        else:
            with open(asmpath, 'r') as asm:
                asm = asm.readlines()
        asm = [line.strip() for line in asm]
        asm = [line for line in asm if line and not line.startswith(('#', '//', ';', '.'))]
        asm = [line.split('#')[0].strip() if '#' in line else line for line in asm]
        asm = [line.split('//')[0].strip() if '//' in line else line for line in asm]
        asm = [line.split(';')[0].strip() if ';' in line else line for line in asm]
        cleaned = []
        labels = {}
        pc = 0
        for line in asm:
            if line.endswith(':'):
                labels[line[:-1].strip()] = pc
            else:
                cleaned.append(line)
                pc += 4
        asm = cleaned
        while self.pcount // 4 < len(asm):
            self.registers['zero'] = 0
            line = asm[self.pcount // 4]
            if line.upper() == 'EBREAK':
                break
            try:
                opcode, args = line.split(' ', 1)
            except ValueError:
                opcode, args = line, ''
            opcode = opcode.upper().strip()
            args = args.split(',')
            if len(args) > 0:
                if "(" in args[-1] and args[-1].endswith(")"):
                    imm, args[-1] = args[-1].split("(")
                    args[-1] = args[-1].rstrip(")")
                    args.append(imm)
            args = [parsevalue(arg.strip()) for arg in args]
            args = [aliases[int(arg.replace('x', ''))] if isinstance(arg, str) and arg.startswith('x') else arg for arg in args]
            args = [labels[arg] - self.pcount if isinstance(arg, str) and arg in labels else arg for arg in args]
            argerrors = [arg for arg in args if isinstance(arg, str) and arg not in self.registers]
            args = [arg for arg in args if (isinstance(arg, str) and arg in self.registers) or isinstance(arg, int)]
            prepcount = self.pcount
            try:
                self.opcodes[opcode](*args)
                if debug:
                    print(f"{hex(self.pcount)}: {opcode} {', '.join(map(str, args))}")
                if imax > 0:
                    icount += 1
                    if imax == icount:
                        break
                if prepcount == self.pcount:
                    self.pcount += 4
            except Exception as e:
                print(f'Error {hex(self.pcount)}: {line}')
                if isinstance(e, KeyError):
                    print(f'Invalid Opcode {opcode}')
                elif isinstance(e, TypeError):
                    print(f"Invalid Argument {', '.join(argerrors)}")
                else:
                    print('')
                break
rv64 = RV64()