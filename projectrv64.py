class RV64:
    def __init__(self):
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
            'SLTI': self.SLTI,
            'SLTIU': self.SLTIU,
            'XORI': self.XORI,
            'ORI': self.ORI,
            'ANDI': self.ANDI,
            'SD': self.SD,
            'SLLI': self.SLLI,
            'SRLI': self.SRLI,
            'SRAI': self.SRAI,
            'ADD': self.ADD,
            'SUB': self.SUB,
            'SLL': self.SLL,
            'SLT': self.SLT,
            'SLTU': self.SLTU,
            'XOR': self.XOR,
            'SRL': self.SRL,
            'SRA': self.SRA,
            'OR': self.OR,
            'AND': self.AND,
            'MUL': self.MUL,
            'MULH': self.MULH,
            'MULHSU': self.MULHSU,
            'MULHU': self.MULHU,
            'DIV': self.DIV,
            'DIVU': self.DIVU,
            'REM': self.REM,
            'REMU': self.REMU
        }
    def LUI(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = imm << 12
    def AUIPC(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.pcount + (imm << 12)
    def JAL(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.pcount + 4
        self.pcount += imm
    def JALR(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.pcount + 4
        self.pcount = (self.registers[rs1] + imm) & ~1
    def BEQ(self, rs1, rs2, imm):
        if self.registers[rs1] == self.registers[rs2]:
            self.pcount += imm
    def BNE(self, rs1, rs2, imm):
        if self.registers[rs1] != self.registers[rs2]:
            self.pcount += imm
    def BLT(self, rs1, rs2, imm):
        if self.registers[rs1] < self.registers[rs2]:
            self.pcount += imm
    def BGE(self, rs1, rs2, imm):
        if self.registers[rs1] >= self.registers[rs2]:
            self.pcount += imm
    def BLTU(self, rs1, rs2, imm):
        if self.registers[rs1] & 0xFFFFFFFFFFFFFFFF < self.registers[rs2] & 0xFFFFFFFFFFFFFFFF:
            self.pcount += imm
    def BGEU(self, rs1, rs2, imm):
        if self.registers[rs1] & 0xFFFFFFFFFFFFFFFF >= self.registers[rs2] & 0xFFFFFFFFFFFFFFFF:
            self.pcount += imm
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
    def SRLI(self, rd, rs1, shamt):
        if rd != 'zero':
            shamt &= 0x3F
            val = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
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
    def ADD(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
    def SUB(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
    def SLL(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x3F
            result = (self.registers[rs1] << shamt) & 0xFFFFFFFFFFFFFFFF
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
    def SRA(self, rd, rs1, rs2):
        if rd != 'zero':
            shamt = self.registers[rs2] & 0x3F
            val = self.registers[rs1]
            if val & (1 << 63):
                val = val - (1 << 64)
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
    def DIVU(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = 0xFFFFFFFFFFFFFFFF
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) // (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF)
    def REM(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = self.registers[rs1]
            else:
                self.registers[rd] = self.registers[rs1] % self.registers[rs2]
    def REMU(self, rd, rs1, rs2):
        if rd != 'zero':
            if self.registers[rs2] == 0:
                self.registers[rd] = self.registers[rs1]
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) % (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF)
    def execute(self, asmpath):
        def parsevalue(x):
            try:
                return int(x, 0)
            except:
                return x
        self.registers = {key: 0 for key in self.registers}
        self.pcount = 0
        self.mem = bytearray(0x1000000)
        with open(asmpath, 'r') as asm:
            asm = asm.readlines()
            asm = [line.strip() for line in asm if line.strip() != '' and not line.startswith('//')]
            while self.pcount // 4 < len(asm):
                self.registers['zero'] = 0
                line = asm[self.pcount // 4]
                line = line.strip()
                line = line.split('//')[0].strip()
                try:
                    opcode, args = line.split(' ', 1)
                except ValueError:
                    opcode, args = line, ''
                opcode = opcode.upper().strip()
                args = args.split(',')
                args = [parsevalue(arg.strip()) for arg in args]
                prepcount = self.pcount
                if len(args) == 2:
                    self.opcodes[opcode](args[0], args[1])
                    if self.pcount == prepcount:
                        self.pcount += 4
                elif len(args) == 3:
                    self.opcodes[opcode](args[0], args[1], args[2])
                    if self.pcount == prepcount:
                        self.pcount += 4
                else:
                    pass
rv64 = RV64()