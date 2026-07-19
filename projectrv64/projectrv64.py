class RV64:
    def __init__(self, sizeofmem):
        self.arch = 'RISC-V RV64G'
        self.registers = {'zero': 0, 'ra': 0, 'sp': 0, 'gp': 0, 'tp': 0, 't0': 0, 't1': 0, 't2': 0, 's0': 0, 's1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 0, 'a6': 0, 'a7': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0, 's9': 0, 's10': 0, 's11': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 'ft0': 0.0, 'ft1': 0.0, 'ft2': 0.0, 'ft3': 0.0, 'ft4': 0.0, 'ft5': 0.0, 'ft6': 0.0, 'ft7': 0.0, 'fs0': 0.0, 'fs1': 0.0, 'fa0': 0.0, 'fa1': 0.0, 'fa2': 0.0, 'fa3': 0.0, 'fa4': 0.0, 'fa5': 0.0, 'fa6': 0.0, 'fa7': 0.0, 'fs2': 0.0, 'fs3': 0.0, 'fs4': 0.0, 'fs5': 0.0, 'fs6': 0.0, 'fs7': 0.0, 'fs8': 0.0, 'fs9': 0.0, 'fs10': 0.0, 'fs11': 0.0, 'ft8': 0.0, 'ft9': 0.0, 'ft10': 0.0, 'ft11': 0.0}
        self.integerregisters = list(self.registers)[:32]
        self.floatregisters = list(self.registers)[32:]
        self.floatraw = {key: 0 for key in self.floatregisters}
        self.csrnames = {'fflags': 0x001, 'frm': 0x002, 'fcsr': 0x003, 'cycle': 0xC00, 'time': 0xC01, 'instret': 0xC02}
        self.csrs = {0x001: 0, 0x002: 0, 0x003: 0}
        self.environmentcall = False
        self.breakpoint = False
        self.halted = False
        self.instructions = 0
        self.reservation = None
        self.pcount = 0
        self.mem = bytearray(sizeofmem)
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
            'REMUW': self.REMUW,
            'LR.D': self.LRD,
            'SC.D': self.SCD,
            'AMOSWAP.D': self.AMOSWAPD,
            'AMOADD.D': self.AMOADDD,
            'AMOXOR.D': self.AMOXORD,
            'AMOAND.D': self.AMOANDD,
            'AMOOR.D': self.AMOORD,
            'AMOMIN.D': self.AMOMIND,
            'AMOMAX.D': self.AMOMAXD,
            'AMOMINU.D': self.AMOMINUD,
            'AMOMAXU.D': self.AMOMAXUD,
            'LR.W': self.LRW,
            'SC.W': self.SCW,
            'AMOSWAP.W': self.AMOSWAPW,
            'AMOADD.W': self.AMOADDW,
            'AMOXOR.W': self.AMOXORW,
            'AMOAND.W': self.AMOANDW,
            'AMOOR.W': self.AMOORW,
            'AMOMIN.W': self.AMOMINW,
            'AMOMAX.W': self.AMOMAXW,
            'AMOMINU.W': self.AMOMINUW,
            'AMOMAXU.W': self.AMOMAXUW,
            'FCVT.L.S': self.FCVTLS,
            'FCVT.LU.S': self.FCVTLUS,
            'FCVT.S.L': self.FCVTSL,
            'FCVT.S.LU': self.FCVTSLU,
            'FLW': self.FLW,
            'FLD': self.FLD,
            'FSW': self.FSW,
            'FSD': self.FSD,
            'FADD.S': self.FADDS,
            'FSUB.S': self.FSUBS,
            'FMUL.S': self.FMULS,
            'FDIV.S': self.FDIVS,
            'FSQRT.S': self.FSQRTS,
            'FMIN.S': self.FMINS,
            'FMAX.S': self.FMAXS,
            'FCLASS.S': self.FCLASSS,
            'FCVT.W.S': self.FCVTWS,
            'FCVT.WU.S': self.FCVTWUS,
            'FCVT.S.W': self.FCVTSW,
            'FCVT.S.WU': self.FCVTSWU,
            'FMV.X.W': self.FMVXW,
            'FMV.W.X': self.FMVWX,
            'FEQ.S': self.FEQS,
            'FLT.S': self.FLTS,
            'FLE.S': self.FLES,
            'FSGNJ.S': self.FSGNJS,
            'FSGNJN.S': self.FSGNJNS,
            'FSGNJX.S': self.FSGNJXS,
            'FADD.D': self.FADDD,
            'FSUB.D': self.FSUBD,
            'FMUL.D': self.FMULD,
            'FDIV.D': self.FDIVD,
            'FSQRT.D': self.FSQRTD,
            'FMIN.D': self.FMIND,
            'FMAX.D': self.FMAXD,
            'FCLASS.D': self.FCLASSD,
            'FCVT.S.D': self.FCVTSD,
            'FCVT.D.S': self.FCVTDS,
            'FCVT.W.D': self.FCVTWD,
            'FCVT.WU.D': self.FCVTWUD,
            'FCVT.D.W': self.FCVTDW,
            'FCVT.D.WU': self.FCVTDWU,
            'FEQ.D': self.FEQD,
            'FLT.D': self.FLTD,
            'FLE.D': self.FLED,
            'FSGNJ.D': self.FSGNJD,
            'FSGNJN.D': self.FSGNJND,
            'FSGNJX.D': self.FSGNJXD,
            'FENCE': self.FENCE,
            'FENCE.I': self.FENCEI,
            'FENCE.TSO': self.FENCETSO,
            'ECALL': self.ECALL,
            'SCALL': self.ECALL,
            'EBREAK': self.EBREAK,
            'SBREAK': self.EBREAK,
            'CSRRW': self.CSRRW,
            'CSRRS': self.CSRRS,
            'CSRRC': self.CSRRC,
            'CSRRWI': self.CSRRWI,
            'CSRRSI': self.CSRRSI,
            'CSRRCI': self.CSRRCI,
            'FMADD.S': self.FMADDS,
            'FMSUB.S': self.FMSUBS,
            'FNMSUB.S': self.FNMSUBS,
            'FNMADD.S': self.FNMADDS,
            'FMADD.D': self.FMADDD,
            'FMSUB.D': self.FMSUBD,
            'FNMSUB.D': self.FNMSUBD,
            'FNMADD.D': self.FNMADDD,
            'FCVT.L.D': self.FCVTLD,
            'FCVT.LU.D': self.FCVTLUD,
            'FCVT.D.L': self.FCVTDL,
            'FCVT.D.LU': self.FCVTDLU,
            'FMV.X.D': self.FMVXD,
            'FMV.D.X': self.FMVDX,
            'UNIMP': self.UNIMP,
            'NOP': self.NOP,
            'LI': self.LI,
            'MV': self.MV,
            'MOVE': self.MV,
            'NOT': self.NOT,
            'NEG': self.NEG,
            'NEGW': self.NEGW,
            'SEXT.B': self.SEXTB,
            'SEXT.H': self.SEXTH,
            'SEXT.W': self.SEXTW,
            'ZEXT.B': self.ZEXTB,
            'ZEXT.H': self.ZEXTH,
            'ZEXT.W': self.ZEXTW,
            'SEQZ': self.SEQZ,
            'SNEZ': self.SNEZ,
            'SLTZ': self.SLTZ,
            'SGTZ': self.SGTZ,
            'SGT': self.SGT,
            'SGTU': self.SGTU,
            'BEQZ': self.BEQZ,
            'BNEZ': self.BNEZ,
            'BLEZ': self.BLEZ,
            'BGEZ': self.BGEZ,
            'BLTZ': self.BLTZ,
            'BGTZ': self.BGTZ,
            'BGT': self.BGT,
            'BLE': self.BLE,
            'BGTU': self.BGTU,
            'BLEU': self.BLEU,
            'J': self.J,
            'JR': self.JR,
            'RET': self.RET,
            'CALL': self.CALL,
            'TAIL': self.TAIL,
            'JUMP': self.JUMP,
            'LA': self.LA,
            'LLA': self.LLA,
            'LGA': self.LGA,
            'LA.TLS.GD': self.LATLSGD,
            'LA.TLS.IE': self.LATLSIE,
            'RDCYCLE': self.RDCYCLE,
            'RDINSTRET': self.RDINSTRET,
            'RDTIME': self.RDTIME,
            'CSRR': self.CSRR,
            'CSRW': self.CSRW,
            'CSRS': self.CSRS,
            'CSRC': self.CSRC,
            'CSRWI': self.CSRWI,
            'CSRSI': self.CSRSI,
            'CSRCI': self.CSRCI,
            'FRCSR': self.FRCSR,
            'FRSR': self.FRCSR,
            'FSCSR': self.FSCSR,
            'FSSR': self.FSCSR,
            'FRRM': self.FRRM,
            'FSRM': self.FSRM,
            'FSRMI': self.FSRMI,
            'FRFLAGS': self.FRFLAGS,
            'FSFLAGS': self.FSFLAGS,
            'FSFLAGSI': self.FSFLAGSI,
            'FMV.X.S': self.FMVXW,
            'FMV.S.X': self.FMVWX,
            'FMV.S': self.FMVS,
            'FNEG.S': self.FNEGS,
            'FABS.S': self.FABSS,
            'FMV.D': self.FMVD,
            'FNEG.D': self.FNEGD,
            'FABS.D': self.FABSD,
            'FGT.S': self.FGTS,
            'FGE.S': self.FGES,
            'FGT.D': self.FGTD,
            'FGE.D': self.FGED,
            'PAUSE': self.PAUSE,
        }
    def LUI(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(imm << 12, 32)
    def AUIPC(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.pcount + self.signed(imm << 12, 32), 64)
    def JAL(self, rd, imm = None):
        if imm is None:
            imm = rd
            rd = 'ra'
        pc = self.pcount
        if rd != 'zero':
            self.registers[rd] = pc + 4
        self.pcount = pc + imm
    def JALR(self, rd, rs1 = None, imm = 0):
        if rs1 is None:
            rs1 = rd
            rd = 'ra'
        elif isinstance(rs1, int):
            imm = rs1
            rs1 = rd
            rd = 'ra'
        target = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFE
        link = self.pcount + 4
        if rd != 'zero':
            self.registers[rd] = link
        self.pcount = target
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
        if self.signed(self.registers[rs1], 64) < self.signed(self.registers[rs2], 64):
            self.pcount += imm
        else:
            self.pcount += 4
    def BGE(self, rs1, rs2, imm):
        if self.signed(self.registers[rs1], 64) >= self.signed(self.registers[rs2], 64):
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
    def LB(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.mem[address]
        if value & 0x80:
            value -= 0x100
        if rd != 'zero':
            self.registers[rd] = value
    def LD(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 8], 'little', signed = True)
        if rd != 'zero':
            self.registers[rd] = value
    def LH(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 2], 'little', signed = True)
        if rd != 'zero':
            self.registers[rd] = value
    def LW(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 4], 'little', signed = True)
        if rd != 'zero':
            self.registers[rd] = value
    def LWU(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 4], 'little', signed = False)
        if rd != 'zero':
            self.registers[rd] = value
    def LBU(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.mem[address]
        if rd != 'zero':
            self.registers[rd] = value
    def LHU(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 2], 'little', signed = False)
        if rd != 'zero':
            self.registers[rd] = value
    def SB(self, rs2, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.registers[rs2] & 0xff
        self.mem[address:address + 1] = value.to_bytes(1, 'little', signed = False)
        self.invalidatereservation(address, 1)
    def SH(self, rs2, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.registers[rs2] & 0xffff
        self.mem[address:address + 2] = value.to_bytes(2, 'little', signed = False)
        self.invalidatereservation(address, 2)
    def SW(self, rs2, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.registers[rs2] & 0xffffffff
        self.mem[address:address + 4] = value.to_bytes(4, 'little', signed = False)
        self.invalidatereservation(address, 4)
    def ADDI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] + imm, 64)
    def ADDIW(self, rd, rs1, imm):
        if rd != 'zero':
            val = (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
            val = (val & 0xFFFFFFFF)
            if val & 0x80000000:
                val -= 0x100000000
            self.registers[rd] = val
    def SLTI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = int(self.signed(self.registers[rs1], 64) < self.signed(imm, 64))
    def SLTIU(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = 1 if (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) < (imm & 0xFFFFFFFFFFFFFFFF) else 0
    def XORI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] ^ imm, 64)
    def ORI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] | imm, 64)
    def ANDI(self, rd, rs1, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] & imm, 64)
    def SD(self, rs2, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        value = self.registers[rs2] & 0xffffffffffffffff
        self.mem[address:address + 8] = value.to_bytes(8, 'little', signed = False)
        self.invalidatereservation(address, 8)
    def SLLI(self, rd, rs1, shamt):
        if rd != 'zero':
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) << (shamt & 0x3F), 64)
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
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) >> (shamt & 0x3F), 64)
    def SRLIW(self, rd, rs1, shamt):
        if rd != 'zero':
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFF) >> (shamt & 0x1F), 32)
    def SRAI(self, rd, rs1, shamt):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.signed(self.registers[rs1], 64) >> (shamt & 0x3F), 64)
    def SRAIW(self, rd, rs1, shamt):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.signed(self.registers[rs1], 32) >> (shamt & 0x1F), 32)
    def ADD(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.ADDI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] + self.registers[rs2], 64)
    def ADDW(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.ADDIW(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] + self.registers[rs2], 32)
    def SUB(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] - self.registers[rs2], 64)
    def SUBW(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] - self.registers[rs2], 32)
    def SLL(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SLLI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) << (self.registers[rs2] & 0x3F), 64)
    def SLLW(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SLLIW(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFF) << (self.registers[rs2] & 0x1F), 32)
    def SLT(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SLTI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = int(self.signed(self.registers[rs1], 64) < self.signed(self.registers[rs2], 64))
    def SLTU(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SLTIU(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = int((self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) < (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF))
    def XOR(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.XORI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] ^ self.registers[rs2], 64)
    def SRL(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SRLI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) >> (self.registers[rs2] & 0x3F), 64)
    def SRLW(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SRLIW(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed((self.registers[rs1] & 0xFFFFFFFF) >> (self.registers[rs2] & 0x1F), 32)
    def SRA(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SRAI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.signed(self.registers[rs1], 64) >> (self.registers[rs2] & 0x3F), 64)
    def SRAW(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.SRAIW(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.signed(self.registers[rs1], 32) >> (self.registers[rs2] & 0x1F), 32)
    def OR(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.ORI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] | self.registers[rs2], 64)
    def AND(self, rd, rs1, rs2):
        if isinstance(rs2, int):
            self.ANDI(rd, rs1, rs2)
        elif rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] & self.registers[rs2], 64)
    def MUL(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1] * self.registers[rs2], 64)
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
        if rd != 'zero':
            product = self.signed(self.registers[rs1], 64) * self.signed(self.registers[rs2], 64)
            self.registers[rd] = self.signed(product >> 64, 64)
    def MULHSU(self, rd, rs1, rs2):
        if rd != 'zero':
            product = self.signed(self.registers[rs1], 64) * (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF)
            self.registers[rd] = self.signed(product >> 64, 64)
    def MULHU(self, rd, rs1, rs2):
        if rd != 'zero':
            product = (self.registers[rs1] & 0xFFFFFFFFFFFFFFFF) * (self.registers[rs2] & 0xFFFFFFFFFFFFFFFF)
            self.registers[rd] = self.signed(product >> 64, 64)
    def DIV(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.signed(self.registers[rs1], 64)
            b = self.signed(self.registers[rs2], 64)
            if b == 0:
                result = -1
            elif a == -0x8000000000000000 and b == -1:
                result = a
            else:
                result = abs(a) // abs(b)
                if (a < 0) != (b < 0):
                    result = -result
            self.registers[rd] = self.signed(result, 64)
    def DIVW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.signed(self.registers[rs1], 32)
            b = self.signed(self.registers[rs2], 32)
            if b == 0:
                result = -1
            elif a == -0x80000000 and b == -1:
                result = a
            else:
                result = abs(a) // abs(b)
                if (a < 0) != (b < 0):
                    result = -result
            self.registers[rd] = self.signed(result, 32)
    def DIVU(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = self.signed(0xFFFFFFFFFFFFFFFF if b == 0 else a // b, 64)
    def DIVUW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFF
            self.registers[rd] = self.signed(0xFFFFFFFF if b == 0 else a // b, 32)
    def REM(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.signed(self.registers[rs1], 64)
            b = self.signed(self.registers[rs2], 64)
            if b == 0:
                result = a
            elif a == -0x8000000000000000 and b == -1:
                result = 0
            else:
                quotient = abs(a) // abs(b)
                if (a < 0) != (b < 0):
                    quotient = -quotient
                result = a - quotient * b
            self.registers[rd] = self.signed(result, 64)
    def REMW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.signed(self.registers[rs1], 32)
            b = self.signed(self.registers[rs2], 32)
            if b == 0:
                result = a
            elif a == -0x80000000 and b == -1:
                result = 0
            else:
                quotient = abs(a) // abs(b)
                if (a < 0) != (b < 0):
                    quotient = -quotient
                result = a - quotient * b
            self.registers[rd] = self.signed(result, 32)
    def REMU(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFFFFFFFFFF
            self.registers[rd] = self.signed(a if b == 0 else a % b, 64)
    def REMUW(self, rd, rs1, rs2):
        if rd != 'zero':
            a = self.registers[rs1] & 0xFFFFFFFF
            b = self.registers[rs2] & 0xFFFFFFFF
            self.registers[rd] = self.signed(a if b == 0 else a % b, 32)
    def signed(self, value, bits):
        value &= (1 << bits) - 1
        if value & (1 << (bits - 1)):
            value -= 1 << bits
        return value
    def floatbits(self, value, bits):
        value = float(value)
        sign = 1 if value.hex().startswith('-') else 0
        value = -value if sign else value
        exponentbits = 8 if bits == 32 else 11
        fractionbits = 23 if bits == 32 else 52
        exponentmax = (1 << exponentbits) - 1
        bias = (1 << (exponentbits - 1)) - 1
        if value != value:
            return (sign << (bits - 1)) | (exponentmax << fractionbits) | (1 << (fractionbits - 1))
        if value == float('inf'):
            return (sign << (bits - 1)) | (exponentmax << fractionbits)
        if value == 0.0:
            return sign << (bits - 1)
        numerator, denominator = value.as_integer_ratio()
        exponent = numerator.bit_length() - denominator.bit_length()
        if exponent >= 0:
            if numerator < denominator << exponent:
                exponent -= 1
        elif numerator << -exponent < denominator:
            exponent -= 1
        minimumexponent = 1 - bias
        if exponent < minimumexponent:
            shift = fractionbits - minimumexponent
            scalednumerator = numerator << shift if shift >= 0 else numerator
            scaleddenominator = denominator if shift >= 0 else denominator << -shift
            quotient, remainder = divmod(scalednumerator, scaleddenominator)
            if remainder * 2 > scaleddenominator or remainder * 2 == scaleddenominator and quotient & 1:
                quotient += 1
            if quotient >= 1 << fractionbits:
                exponentfield = 1
                fraction = 0
            else:
                exponentfield = 0
                fraction = quotient
        else:
            shift = fractionbits - exponent
            scalednumerator = numerator << shift if shift >= 0 else numerator
            scaleddenominator = denominator if shift >= 0 else denominator << -shift
            significand, remainder = divmod(scalednumerator, scaleddenominator)
            if remainder * 2 > scaleddenominator or remainder * 2 == scaleddenominator and significand & 1:
                significand += 1
            if significand == 1 << (fractionbits + 1):
                significand >>= 1
                exponent += 1
            exponentfield = exponent + bias
            if exponentfield >= exponentmax:
                return (sign << (bits - 1)) | (exponentmax << fractionbits)
            fraction = significand - (1 << fractionbits)
        return (sign << (bits - 1)) | (exponentfield << fractionbits) | fraction
    def bitsfloat(self, value, bits):
        exponentbits = 8 if bits == 32 else 11
        fractionbits = 23 if bits == 32 else 52
        exponentmax = (1 << exponentbits) - 1
        bias = (1 << (exponentbits - 1)) - 1
        sign = -1.0 if value >> (bits - 1) else 1.0
        exponent = (value >> fractionbits) & exponentmax
        fraction = value & ((1 << fractionbits) - 1)
        if exponent == exponentmax:
            return sign * float('inf') if fraction == 0 else float('nan')
        if exponent == 0:
            result = fraction * 2.0 ** (1 - bias - fractionbits)
        else:
            result = (1.0 + fraction / (1 << fractionbits)) * 2.0 ** (exponent - bias)
        return sign * result
    def f32(self, value):
        return self.bitsfloat(self.floatbits(value, 32), 32)
    def floatdiv(self, a, b):
        if a != a or b != b:
            return float('nan')
        if b == 0.0:
            if a == 0.0:
                return float('nan')
            negative = (self.floatbits(a, 64) ^ self.floatbits(b, 64)) >> 63
            return -float('inf') if negative else float('inf')
        return a / b
    def exactfloatbits(self, numerator, denominator, bits, zerosign = 0):
        sign = 1 if numerator < 0 else zerosign
        numerator = abs(numerator)
        exponentbits = 8 if bits == 32 else 11
        fractionbits = 23 if bits == 32 else 52
        exponentmax = (1 << exponentbits) - 1
        bias = (1 << (exponentbits - 1)) - 1
        if numerator == 0:
            return sign << (bits - 1)
        exponent = numerator.bit_length() - denominator.bit_length()
        if exponent >= 0:
            if numerator < denominator << exponent:
                exponent -= 1
        elif numerator << -exponent < denominator:
            exponent -= 1
        minimumexponent = 1 - bias
        if exponent < minimumexponent:
            shift = fractionbits - minimumexponent
            scalednumerator = numerator << shift if shift >= 0 else numerator
            scaleddenominator = denominator if shift >= 0 else denominator << -shift
            quotient, remainder = divmod(scalednumerator, scaleddenominator)
            if remainder * 2 > scaleddenominator or remainder * 2 == scaleddenominator and quotient & 1:
                quotient += 1
            if quotient >= 1 << fractionbits:
                exponentfield = 1
                fraction = 0
            else:
                exponentfield = 0
                fraction = quotient
        else:
            shift = fractionbits - exponent
            scalednumerator = numerator << shift if shift >= 0 else numerator
            scaleddenominator = denominator if shift >= 0 else denominator << -shift
            significand, remainder = divmod(scalednumerator, scaleddenominator)
            if remainder * 2 > scaleddenominator or remainder * 2 == scaleddenominator and significand & 1:
                significand += 1
            if significand == 1 << (fractionbits + 1):
                significand >>= 1
                exponent += 1
            exponentfield = exponent + bias
            if exponentfield >= exponentmax:
                return (sign << (bits - 1)) | (exponentmax << fractionbits)
            fraction = significand - (1 << fractionbits)
        return (sign << (bits - 1)) | (exponentfield << fractionbits) | fraction
    def fmabits(self, a, b, c, bits):
        fractionbits = 23 if bits == 32 else 52
        exponentmax = 0xFF if bits == 32 else 0x7FF
        quietnan = (exponentmax << fractionbits) | (1 << (fractionbits - 1))
        abits = self.floatbits(a, bits)
        bbits = self.floatbits(b, bits)
        cbits = self.floatbits(c, bits)
        if a != a or b != b or c != c:
            return quietnan
        productnegative = (abits ^ bbits) >> (bits - 1)
        ainf = a == float('inf') or a == -float('inf')
        binf = b == float('inf') or b == -float('inf')
        cinf = c == float('inf') or c == -float('inf')
        if ainf and b == 0.0 or binf and a == 0.0:
            return quietnan
        if ainf or binf:
            if cinf and cbits >> (bits - 1) != productnegative:
                return quietnan
            return (productnegative << (bits - 1)) | (exponentmax << fractionbits)
        if cinf:
            return cbits
        anumerator, adenominator = a.as_integer_ratio()
        bnumerator, bdenominator = b.as_integer_ratio()
        cnumerator, cdenominator = c.as_integer_ratio()
        numerator = anumerator * bnumerator * cdenominator + cnumerator * adenominator * bdenominator
        denominator = adenominator * bdenominator * cdenominator
        productzero = a == 0.0 or b == 0.0
        zerosign = productnegative if numerator == 0 and productzero and c == 0.0 and productnegative == cbits >> (bits - 1) else 0
        return self.exactfloatbits(numerator, denominator, bits, zerosign)
    def invalidatereservation(self, address, size):
        if self.reservation is None:
            return
        reservedaddress, reservedsize = self.reservation
        if address < reservedaddress + reservedsize and reservedaddress < address + size:
            self.reservation = None
    def LRD(self, rd, rs1):
        address = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 8], 'little', signed = True)
        self.reservation = (address, 8)
        if rd != 'zero':
            self.registers[rd] = value
    def SCD(self, rd, rs2, rs1):
        address = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
        success = self.reservation == (address, 8)
        if success:
            value = self.registers[rs2] & 0xFFFFFFFFFFFFFFFF
            self.mem[address:address + 8] = value.to_bytes(8, 'little', signed = False)
        self.reservation = None
        if rd != 'zero':
            self.registers[rd] = 0 if success else 1
    def LRW(self, rd, rs1):
        address = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
        value = int.from_bytes(self.mem[address:address + 4], 'little', signed = True)
        self.reservation = (address, 4)
        if rd != 'zero':
            self.registers[rd] = value
    def SCW(self, rd, rs2, rs1):
        address = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
        success = self.reservation == (address, 4)
        if success:
            value = self.registers[rs2] & 0xFFFFFFFF
            self.mem[address:address + 4] = value.to_bytes(4, 'little', signed = False)
        self.reservation = None
        if rd != 'zero':
            self.registers[rd] = 0 if success else 1
    def amo(self, rd, rs2, rs1, bits, operation, unsigned = False):
        size = bits // 8
        mask = (1 << bits) - 1
        address = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
        oldraw = int.from_bytes(self.mem[address:address + size], 'little', signed = False)
        sourceraw = self.registers[rs2] & mask
        oldvalue = oldraw if unsigned else self.signed(oldraw, bits)
        sourcevalue = sourceraw if unsigned else self.signed(sourceraw, bits)
        newvalue = operation(oldvalue, sourcevalue) & mask
        self.mem[address:address + size] = newvalue.to_bytes(size, 'little', signed = False)
        self.invalidatereservation(address, size)
        if rd != 'zero':
            self.registers[rd] = self.signed(oldraw, bits)
    def AMOSWAPD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, lambda old, source: source)
    def AMOADDD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, lambda old, source: old + source)
    def AMOXORD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, lambda old, source: old ^ source, True)
    def AMOANDD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, lambda old, source: old & source, True)
    def AMOORD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, lambda old, source: old | source, True)
    def AMOMIND(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, min)
    def AMOMAXD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, max)
    def AMOMINUD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, min, True)
    def AMOMAXUD(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 64, max, True)
    def AMOSWAPW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, lambda old, source: source)
    def AMOADDW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, lambda old, source: old + source)
    def AMOXORW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, lambda old, source: old ^ source, True)
    def AMOANDW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, lambda old, source: old & source, True)
    def AMOORW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, lambda old, source: old | source, True)
    def AMOMINW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, min)
    def AMOMAXW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, max)
    def AMOMINUW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, min, True)
    def AMOMAXUW(self, rd, rs2, rs1):
        self.amo(rd, rs2, rs1, 32, max, True)
    def FLW(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        raw = int.from_bytes(self.mem[address:address + 4], 'little', signed = False)
        self.setfloat(rd, self.bitsfloat(raw, 32), 32, raw)
    def FSW(self, rs2, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        self.mem[address:address + 4] = self.getfloatbits(rs2, 32).to_bytes(4, 'little', signed = False)
        self.invalidatereservation(address, 4)
    def FLD(self, rd, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        raw = int.from_bytes(self.mem[address:address + 8], 'little', signed = False)
        self.setfloat(rd, self.bitsfloat(raw, 64), 64, raw)
    def FSD(self, rs2, rs1, imm = 0):
        address = self.pcount + rs1 if isinstance(rs1, int) else (self.registers[rs1] + imm) & 0xFFFFFFFFFFFFFFFF
        self.mem[address:address + 8] = self.getfloatbits(rs2, 64).to_bytes(8, 'little', signed = False)
        self.invalidatereservation(address, 8)
    def FADDS(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 32) + self.getfloat(rs2, 32), 32)
    def FSUBS(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 32) - self.getfloat(rs2, 32), 32)
    def FMULS(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 32) * self.getfloat(rs2, 32), 32)
    def FDIVS(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.floatdiv(self.getfloat(rs1, 32), self.getfloat(rs2, 32)), 32)
    def FSQRTS(self, rd, rs1, rm = 7):
        value = self.getfloat(rs1, 32)
        self.setfloat(rd, value ** 0.5 if value >= 0.0 else float('nan'), 32)
    def FMINS(self, rd, rs1, rs2):
        self.setfloat(rd, self.fmin(self.getfloat(rs1, 32), self.getfloat(rs2, 32)), 32)
    def FMAXS(self, rd, rs1, rs2):
        self.setfloat(rd, self.fmax(self.getfloat(rs1, 32), self.getfloat(rs2, 32)), 32)
    def FADDD(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 64) + self.getfloat(rs2, 64), 64)
    def FSUBD(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 64) - self.getfloat(rs2, 64), 64)
    def FMULD(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 64) * self.getfloat(rs2, 64), 64)
    def FDIVD(self, rd, rs1, rs2, rm = 7):
        self.setfloat(rd, self.floatdiv(self.getfloat(rs1, 64), self.getfloat(rs2, 64)), 64)
    def FSQRTD(self, rd, rs1, rm = 7):
        value = self.getfloat(rs1, 64)
        self.setfloat(rd, value ** 0.5 if value >= 0.0 else float('nan'), 64)
    def fmin(self, a, b):
        if a != a:
            return b
        if b != b:
            return a
        if a == b == 0.0:
            return -0.0 if self.floatbits(a, 64) >> 63 or self.floatbits(b, 64) >> 63 else 0.0
        return min(a, b)
    def fmax(self, a, b):
        if a != a:
            return b
        if b != b:
            return a
        if a == b == 0.0:
            return 0.0 if self.floatbits(a, 64) >> 63 == 0 or self.floatbits(b, 64) >> 63 == 0 else -0.0
        return max(a, b)
    def FMIND(self, rd, rs1, rs2):
        self.setfloat(rd, self.fmin(self.getfloat(rs1, 64), self.getfloat(rs2, 64)), 64)
    def FMAXD(self, rd, rs1, rs2):
        self.setfloat(rd, self.fmax(self.getfloat(rs1, 64), self.getfloat(rs2, 64)), 64)
    def fclass(self, value, bits = 64):
        raw = value if isinstance(value, int) else self.floatbits(value, bits)
        exponentbits = 8 if bits == 32 else 11
        fractionbits = 23 if bits == 32 else 52
        sign = raw >> (bits - 1)
        exponent = raw >> fractionbits & ((1 << exponentbits) - 1)
        fraction = raw & ((1 << fractionbits) - 1)
        if exponent == (1 << exponentbits) - 1:
            if fraction == 0:
                return 1 << (0 if sign else 7)
            return 1 << (9 if fraction & (1 << (fractionbits - 1)) else 8)
        if exponent == 0:
            if fraction == 0:
                return 1 << (3 if sign else 4)
            return 1 << (2 if sign else 5)
        return 1 << (1 if sign else 6)
    def FCLASSS(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.fclass(self.getfloatbits(rs1, 32), 32)
    def FCLASSD(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.fclass(self.getfloatbits(rs1, 64), 64)
    def FCVTLS(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 32), 64, False, rm), 64)
    def FCVTLUS(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 32), 64, True, rm), 64)
    def FCVTSL(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.signed(self.registers[rs1], 64)), 32)
    def FCVTSLU(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.registers[rs1] & 0xFFFFFFFFFFFFFFFF), 32)
    def FCVTWS(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 32), 32, False, rm), 32)
    def FCVTWUS(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 32), 32, True, rm), 32)
    def FCVTSW(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.signed(self.registers[rs1], 32)), 32)
    def FCVTSWU(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.registers[rs1] & 0xFFFFFFFF), 32)
    def FCVTWD(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 64), 32, False, rm), 32)
    def FCVTWUD(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 64), 32, True, rm), 32)
    def FCVTDW(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.signed(self.registers[rs1], 32)), 64)
    def FCVTDWU(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.registers[rs1] & 0xFFFFFFFF), 64)
    def FCVTSD(self, rd, rs1, rm = 7):
        self.setfloat(rd, self.getfloat(rs1, 64), 32)
    def FCVTDS(self, rd, rs1):
        self.setfloat(rd, self.getfloat(rs1, 32), 64)
    def FMVXW(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.getfloatbits(rs1, 32), 32)
    def FMVWX(self, rd, rs1):
        raw = self.registers[rs1] & 0xFFFFFFFF
        self.setfloat(rd, self.bitsfloat(raw, 32), 32, raw)
    def FEQS(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = int(self.getfloat(rs1, 32) == self.getfloat(rs2, 32))
    def FLTS(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = int(self.getfloat(rs1, 32) < self.getfloat(rs2, 32))
    def FLES(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = int(self.getfloat(rs1, 32) <= self.getfloat(rs2, 32))
    def FEQD(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = int(self.getfloat(rs1, 64) == self.getfloat(rs2, 64))
    def FLTD(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = int(self.getfloat(rs1, 64) < self.getfloat(rs2, 64))
    def FLED(self, rd, rs1, rs2):
        if rd != 'zero':
            self.registers[rd] = int(self.getfloat(rs1, 64) <= self.getfloat(rs2, 64))
    def fsgnj(self, rd, rs1, rs2, bits, mode):
        mask = 1 << (bits - 1)
        a = self.getfloatbits(rs1, bits)
        b = self.getfloatbits(rs2, bits)
        if mode == 0:
            sign = b & mask
        elif mode == 1:
            sign = ~b & mask
        else:
            sign = (a ^ b) & mask
        raw = (a & ~mask) | sign
        self.setfloat(rd, self.bitsfloat(raw, bits), bits, raw)
    def FSGNJS(self, rd, rs1, rs2):
        self.fsgnj(rd, rs1, rs2, 32, 0)
    def FSGNJNS(self, rd, rs1, rs2):
        self.fsgnj(rd, rs1, rs2, 32, 1)
    def FSGNJXS(self, rd, rs1, rs2):
        self.fsgnj(rd, rs1, rs2, 32, 2)
    def FSGNJD(self, rd, rs1, rs2):
        self.fsgnj(rd, rs1, rs2, 64, 0)
    def FSGNJND(self, rd, rs1, rs2):
        self.fsgnj(rd, rs1, rs2, 64, 1)
    def FSGNJXD(self, rd, rs1, rs2):
        self.fsgnj(rd, rs1, rs2, 64, 2)
    def setfloat(self, rd, value, bits, raw = None):
        raw = self.floatbits(value, bits) if raw is None else raw & ((1 << bits) - 1)
        self.floatraw[rd] = 0xFFFFFFFF00000000 | raw if bits == 32 else raw
        self.registers[rd] = self.bitsfloat(raw, bits)
    def getfloatbits(self, register, bits):
        raw = self.floatraw.get(register, 0)
        if bits == 32:
            return raw & 0xFFFFFFFF if raw >> 32 == 0xFFFFFFFF else 0x7FC00000
        return raw & 0xFFFFFFFFFFFFFFFF
    def getfloat(self, register, bits):
        return self.bitsfloat(self.getfloatbits(register, bits), bits)
    def roundinteger(self, value, rm = 7):
        rm = self.readcsr('frm') if rm == 7 else rm
        if rm == 1:
            return int(value)
        integer = int(value)
        if rm == 2:
            return integer - 1 if value < integer else integer
        if rm == 3:
            return integer + 1 if value > integer else integer
        if rm == 4:
            magnitude = abs(value)
            rounded = int(magnitude)
            if magnitude - rounded >= 0.5:
                rounded += 1
            return -rounded if value < 0 else rounded
        return round(value)
    def fcvtint(self, value, bits, unsigned, rm = 7):
        minimum = 0 if unsigned else -(1 << (bits - 1))
        maximum = (1 << bits) - 1 if unsigned else (1 << (bits - 1)) - 1
        if value != value:
            self.setfflags(0x10)
            return maximum
        if value == float('inf'):
            self.setfflags(0x10)
            return maximum
        if value == -float('inf'):
            self.setfflags(0x10)
            return minimum
        result = self.roundinteger(value, rm)
        if result < minimum:
            self.setfflags(0x10)
            return minimum
        if result > maximum:
            self.setfflags(0x10)
            return maximum
        if result != value:
            self.setfflags(0x01)
        return result
    def csrnumber(self, csr):
        return self.csrnames.get(csr.lower(), csr) if isinstance(csr, str) else csr
    def readcsr(self, csr):
        csr = self.csrnumber(csr)
        if csr in (0xC00, 0xC01, 0xC02):
            return self.instructions & 0xFFFFFFFFFFFFFFFF
        if csr == 0x003:
            return (self.csrs.get(0x002, 0) << 5) | self.csrs.get(0x001, 0)
        return self.csrs.get(csr, 0)
    def writecsr(self, csr, value):
        csr = self.csrnumber(csr)
        value &= 0xFFFFFFFFFFFFFFFF
        if csr == 0x001:
            self.csrs[0x001] = value & 0x1F
        elif csr == 0x002:
            self.csrs[0x002] = value & 0x7
        elif csr == 0x003:
            self.csrs[0x001] = value & 0x1F
            self.csrs[0x002] = value >> 5 & 0x7
    def setfflags(self, flags):
        self.csrs[0x001] = self.csrs.get(0x001, 0) | flags & 0x1F
    def FENCE(self):
        pass
    def FENCEI(self):
        pass
    def FENCETSO(self):
        pass
    def PAUSE(self):
        pass
    def ECALL(self):
        self.environmentcall = True
        self.halted = True
    def EBREAK(self):
        self.breakpoint = True
        self.halted = True
    def UNIMP(self):
        self.breakpoint = True
        self.halted = True
    def CSRRW(self, rd, csr, rs1):
        old = self.readcsr(csr)
        self.writecsr(csr, self.registers[rs1])
        if rd != 'zero':
            self.registers[rd] = self.signed(old, 64)
    def CSRRS(self, rd, csr, rs1):
        old = self.readcsr(csr)
        if rs1 != 'zero':
            self.writecsr(csr, old | self.registers[rs1])
        if rd != 'zero':
            self.registers[rd] = self.signed(old, 64)
    def CSRRC(self, rd, csr, rs1):
        old = self.readcsr(csr)
        if rs1 != 'zero':
            self.writecsr(csr, old & ~self.registers[rs1])
        if rd != 'zero':
            self.registers[rd] = self.signed(old, 64)
    def CSRRWI(self, rd, csr, imm):
        old = self.readcsr(csr)
        self.writecsr(csr, imm & 0x1F)
        if rd != 'zero':
            self.registers[rd] = self.signed(old, 64)
    def CSRRSI(self, rd, csr, imm):
        old = self.readcsr(csr)
        if imm:
            self.writecsr(csr, old | (imm & 0x1F))
        if rd != 'zero':
            self.registers[rd] = self.signed(old, 64)
    def CSRRCI(self, rd, csr, imm):
        old = self.readcsr(csr)
        if imm:
            self.writecsr(csr, old & ~(imm & 0x1F))
        if rd != 'zero':
            self.registers[rd] = self.signed(old, 64)
    def FMADDS(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(self.getfloat(rs1, 32), self.getfloat(rs2, 32), self.getfloat(rs3, 32), 32)
        self.setfloat(rd, self.bitsfloat(raw, 32), 32, raw)
    def FMSUBS(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(self.getfloat(rs1, 32), self.getfloat(rs2, 32), -self.getfloat(rs3, 32), 32)
        self.setfloat(rd, self.bitsfloat(raw, 32), 32, raw)
    def FNMSUBS(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(-self.getfloat(rs1, 32), self.getfloat(rs2, 32), self.getfloat(rs3, 32), 32)
        self.setfloat(rd, self.bitsfloat(raw, 32), 32, raw)
    def FNMADDS(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(-self.getfloat(rs1, 32), self.getfloat(rs2, 32), -self.getfloat(rs3, 32), 32)
        self.setfloat(rd, self.bitsfloat(raw, 32), 32, raw)
    def FMADDD(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(self.getfloat(rs1, 64), self.getfloat(rs2, 64), self.getfloat(rs3, 64), 64)
        self.setfloat(rd, self.bitsfloat(raw, 64), 64, raw)
    def FMSUBD(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(self.getfloat(rs1, 64), self.getfloat(rs2, 64), -self.getfloat(rs3, 64), 64)
        self.setfloat(rd, self.bitsfloat(raw, 64), 64, raw)
    def FNMSUBD(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(-self.getfloat(rs1, 64), self.getfloat(rs2, 64), self.getfloat(rs3, 64), 64)
        self.setfloat(rd, self.bitsfloat(raw, 64), 64, raw)
    def FNMADDD(self, rd, rs1, rs2, rs3, rm = 7):
        raw = self.fmabits(-self.getfloat(rs1, 64), self.getfloat(rs2, 64), -self.getfloat(rs3, 64), 64)
        self.setfloat(rd, self.bitsfloat(raw, 64), 64, raw)
    def FCVTLD(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 64), 64, False, rm), 64)
    def FCVTLUD(self, rd, rs1, rm = 7):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.fcvtint(self.getfloat(rs1, 64), 64, True, rm), 64)
    def FCVTDL(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.signed(self.registers[rs1], 64)), 64)
    def FCVTDLU(self, rd, rs1, rm = 7):
        self.setfloat(rd, float(self.registers[rs1] & 0xFFFFFFFFFFFFFFFF), 64)
    def FMVXD(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.getfloatbits(rs1, 64), 64)
    def FMVDX(self, rd, rs1):
        raw = self.registers[rs1] & 0xFFFFFFFFFFFFFFFF
        self.setfloat(rd, self.bitsfloat(raw, 64), 64, raw)
    def NOP(self):
        pass
    def LI(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.signed(imm, 64)
    def MV(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1]
    def NOT(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(~self.registers[rs1], 64)
    def NEG(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(-self.registers[rs1], 64)
    def NEGW(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(-self.registers[rs1], 32)
    def SEXTB(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1], 8)
    def SEXTH(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1], 16)
    def SEXTW(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.registers[rs1], 32)
    def ZEXTB(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] & 0xFF
    def ZEXTH(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] & 0xFFFF
    def ZEXTW(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = self.registers[rs1] & 0xFFFFFFFF
    def SEQZ(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = int(self.registers[rs1] == 0)
    def SNEZ(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = int(self.registers[rs1] != 0)
    def SLTZ(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = int(self.signed(self.registers[rs1], 64) < 0)
    def SGTZ(self, rd, rs1):
        if rd != 'zero':
            self.registers[rd] = int(self.signed(self.registers[rs1], 64) > 0)
    def SGT(self, rd, rs1, rs2):
        self.SLT(rd, rs2, rs1)
    def SGTU(self, rd, rs1, rs2):
        self.SLTU(rd, rs2, rs1)
    def BEQZ(self, rs1, imm):
        self.BEQ(rs1, 'zero', imm)
    def BNEZ(self, rs1, imm):
        self.BNE(rs1, 'zero', imm)
    def BLEZ(self, rs1, imm):
        self.BGE('zero', rs1, imm)
    def BGEZ(self, rs1, imm):
        self.BGE(rs1, 'zero', imm)
    def BLTZ(self, rs1, imm):
        self.BLT(rs1, 'zero', imm)
    def BGTZ(self, rs1, imm):
        self.BLT('zero', rs1, imm)
    def BGT(self, rs1, rs2, imm):
        self.BLT(rs2, rs1, imm)
    def BLE(self, rs1, rs2, imm):
        self.BGE(rs2, rs1, imm)
    def BGTU(self, rs1, rs2, imm):
        self.BLTU(rs2, rs1, imm)
    def BLEU(self, rs1, rs2, imm):
        self.BGEU(rs2, rs1, imm)
    def J(self, imm):
        self.JAL('zero', imm)
    def JR(self, rs1, imm = 0):
        self.JALR('zero', rs1, imm)
    def RET(self):
        self.JALR('zero', 'ra', 0)
    def CALL(self, rd, imm = None):
        if imm is None:
            imm = rd
            rd = 'ra'
        self.JAL(rd, imm)
    def TAIL(self, imm):
        self.JAL('zero', imm)
    def JUMP(self, imm, rs1):
        self.JAL('zero', imm)
    def LA(self, rd, imm):
        if rd != 'zero':
            self.registers[rd] = self.pcount + imm
    def LLA(self, rd, imm):
        self.LA(rd, imm)
    def LGA(self, rd, imm):
        self.LA(rd, imm)
    def LATLSGD(self, rd, imm):
        self.LA(rd, imm)
    def LATLSIE(self, rd, imm):
        self.LA(rd, imm)
    def RDCYCLE(self, rd):
        if rd != 'zero':
            self.registers[rd] = self.signed(self.instructions, 64)
    def RDINSTRET(self, rd):
        self.RDCYCLE(rd)
    def RDTIME(self, rd):
        self.RDCYCLE(rd)
    def CSRR(self, rd, csr):
        self.CSRRS(rd, csr, 'zero')
    def CSRW(self, csr, rs1):
        self.CSRRW('zero', csr, rs1)
    def CSRS(self, csr, rs1):
        self.CSRRS('zero', csr, rs1)
    def CSRC(self, csr, rs1):
        self.CSRRC('zero', csr, rs1)
    def CSRWI(self, csr, imm):
        self.CSRRWI('zero', csr, imm)
    def CSRSI(self, csr, imm):
        self.CSRRSI('zero', csr, imm)
    def CSRCI(self, csr, imm):
        self.CSRRCI('zero', csr, imm)
    def FRCSR(self, rd):
        self.CSRR(rd, 'fcsr')
    def FSCSR(self, rd, rs1 = None):
        if rs1 is None:
            rs1 = rd
            rd = 'zero'
        self.CSRRW(rd, 'fcsr', rs1)
    def FRRM(self, rd):
        self.CSRR(rd, 'frm')
    def FSRM(self, rd, rs1 = None):
        if rs1 is None:
            rs1 = rd
            rd = 'zero'
        self.CSRRW(rd, 'frm', rs1)
    def FSRMI(self, rd, imm = None):
        if imm is None:
            imm = rd
            rd = 'zero'
        self.CSRRWI(rd, 'frm', imm)
    def FRFLAGS(self, rd):
        self.CSRR(rd, 'fflags')
    def FSFLAGS(self, rd, rs1 = None):
        if rs1 is None:
            rs1 = rd
            rd = 'zero'
        self.CSRRW(rd, 'fflags', rs1)
    def FSFLAGSI(self, rd, imm = None):
        if imm is None:
            imm = rd
            rd = 'zero'
        self.CSRRWI(rd, 'fflags', imm)
    def FMVS(self, rd, rs1):
        self.FSGNJS(rd, rs1, rs1)
    def FNEGS(self, rd, rs1):
        self.FSGNJNS(rd, rs1, rs1)
    def FABSS(self, rd, rs1):
        self.FSGNJXS(rd, rs1, rs1)
    def FMVD(self, rd, rs1):
        self.FSGNJD(rd, rs1, rs1)
    def FNEGD(self, rd, rs1):
        self.FSGNJND(rd, rs1, rs1)
    def FABSD(self, rd, rs1):
        self.FSGNJXD(rd, rs1, rs1)
    def FGTS(self, rd, rs1, rs2):
        self.FLTS(rd, rs2, rs1)
    def FGES(self, rd, rs1, rs2):
        self.FLES(rd, rs2, rs1)
    def FGTD(self, rd, rs1, rs2):
        self.FLTD(rd, rs2, rs1)
    def FGED(self, rd, rs1, rs2):
        self.FLED(rd, rs2, rs1)
    def execute(self, asmpath, pc = 0, mem = None, imax = 0, debug = False):
        def parsevalue(x):
            try:
                return int(x.strip(), 0)
            except:
                return x
        self.pcount = int(pc) if int(pc) > 0 else 0
        self.mem = bytearray(0x1000000) if mem is None else mem
        self.registers = {key: 0.0 if key in self.floatregisters else 0 for key in self.registers}
        self.floatraw = {key: 0 for key in self.floatregisters}
        self.csrs = {0x001: 0, 0x002: 0, 0x003: 0}
        self.reservation = None
        self.environmentcall = False
        self.breakpoint = False
        self.halted = False
        self.instructions = 0
        aliases = self.integerregisters
        icount = 0
        if isinstance(asmpath, list):
            asm = asmpath
        else:
            with open(asmpath, 'r') as asm:
                asm = asm.readlines()
        asm = [line.strip() for line in asm]
        asm = [line.split('#')[0].strip() if '#' in line else line for line in asm]
        asm = [line.split('//')[0].strip() if '//' in line else line for line in asm]
        asm = [line.split(';')[0].strip() if ';' in line else line for line in asm]
        asm = [line for line in asm if line and (line.endswith(':') or not line.startswith(('#', '//', ';', '.')))]
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
            try:
                opcode, args = line.split(None, 1)
            except ValueError:
                opcode, args = line, ''
            opcode = opcode.upper().strip()
            if opcode.endswith(('.AQRL', '.AQ', '.RL')):
                opcode = opcode.rsplit('.', 1)[0]
            args = args.split(',')
            if len(args) > 0:
                if "(" in args[-1] and args[-1].endswith(")"):
                    imm, args[-1] = args[-1].split("(")
                    args[-1] = args[-1].rstrip(")")
                    args.append(imm)
            args = [parsevalue(arg.strip()) for arg in args]
            args = [arg[:-4] if isinstance(arg, str) and arg.endswith('@plt') else arg for arg in args]
            args = ['s0' if arg == 'fp' else arg for arg in args]
            args = [aliases[int(arg[1:])] if isinstance(arg, str) and arg.startswith('x') and arg[1:].isdigit() else self.floatregisters[int(arg[1:])] if isinstance(arg, str) and arg.startswith('f') and arg[1:].isdigit() else arg for arg in args]
            rounding = {'rne': 0, 'rtz': 1, 'rdn': 2, 'rup': 3, 'rmm': 4, 'dyn': 7}
            args = [rounding.get(arg.lower(), arg) if isinstance(arg, str) else arg for arg in args]
            if (opcode.startswith('LR.') or opcode.startswith('SC.') or opcode.startswith('AMO')) and args and args[-1] == 0:
                args.pop()
            args = [labels[arg] - self.pcount if isinstance(arg, str) and arg in labels else arg for arg in args]
            argerrors = [arg for arg in args if isinstance(arg, str) and arg not in self.registers and arg.lower() not in self.csrnames]
            args = [arg for arg in args if (isinstance(arg, str) and (arg in self.registers or arg.lower() in self.csrnames)) or isinstance(arg, int)]
            prepcount = self.pcount
            try:
                self.opcodes[opcode](*args)
                self.instructions += 1
                if debug:
                    print(f"{hex(self.pcount)}: {opcode} {', '.join(map(str, args))}")
                icount += 1
                if imax > 0 and imax == icount:
                    break
                if self.halted:
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