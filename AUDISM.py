
from UTIL import ARAM, APPLY_DIFF, APPLY_SPACING, APPLY_COMMENTS
from DECOMPOSE import SONG

import traceback

PRINT_BYTE_DEBUG = False






OP_TO_NAME = [
	# 00      01       02      03      04      05      06      07      08      09      0A      0B      0C      0D      0E      0F
	"NOP" , "CALL", "SET" , "BBS" , "OR"  , "OR"  , "OR"  , "OR"  , "OR"  , "OR"  , "OR"  , "ASL" , "ASL" , "PUSH", "TSET", "BRK" ,  # 00
	"BPL" , "CALL", "CLR" , "BBC" , "OR"  , "OR"  , "OR"  , "OR"  , "OR"  , "OR"  , "DEC" , "ASL" , "ASL" , "DEC" , "CMP" , "JMP" ,  # 10
	"CLR" , "CALL", "SET" , "BBS" , "AND" , "AND" , "AND" , "AND" , "AND" , "AND" , "OR"  , "ROL" , "ROL" , "PUSH", "CBNE", "BRA" ,  # 20
	"BMI" , "CALL", "CLR" , "BBC" , "AND" , "AND" , "AND" , "AND" , "AND" , "AND" , "INC" , "ROL" , "ROL" , "INC" , "CMP" , "CALL",  # 30
	"SET" , "CALL", "SET" , "BBS" , "EOR" , "EOR" , "EOR" , "EOR" , "EOR" , "EOR" , "AND" , "LSR" , "LSR" , "PUSH", "TCLR", "CALL",  # 40
	"BVC" , "CALL", "CLR" , "BBC" , "EOR" , "EOR" , "EOR" , "EOR" , "EOR" , "EOR" , "CMP" , "LSR" , "LSR" , "MOV" , "CMP" , "JMP" ,  # 50
	"CLR" , "CALL", "SET" , "BBS" , "CMP" , "CMP" , "CMP" , "CMP" , "CMP" , "CMP" , "AND" , "ROR" , "ROR" , "PUSH", "DBNZ", "RET" ,  # 60
	"BVS" , "CALL", "CLR" , "BBC" , "CMP" , "CMP" , "CMP" , "CMP" , "CMP" , "CMP" , "ADDW", "ROR" , "ROR" , "MOV" , "CMP" , "RET" ,  # 70
	"SET" , "CALL", "SET" , "BBS" , "ADC" , "ADC" , "ADC" , "ADC" , "ADC" , "ADC" , "EOR" , "DEC" , "DEC" , "MOV" , "POP" , "MOV" ,  # 80
	"BCC" , "CALL", "CLR" , "BBC" , "ADC" , "ADC" , "ADC" , "ADC" , "ADC" , "ADC" , "SUBW", "DEC" , "DEC" , "MOV" , "DIV" , "XCN" ,  # 90
	"EI"  , "CALL", "SET" , "BBS" , "SBC" , "SBC" , "SBC" , "SBC" , "SBC" , "SBC" , "MOV" , "INC" , "INC" , "CMP" , "POP" , "MOV" ,  # A0
	"BCS" , "CALL", "CLR" , "BBC" , "SBC" , "SBC" , "SBC" , "SBC" , "SBC" , "SBC" , "MOV" , "INC" , "INC" , "MOV" , "DAS" , "MOV" ,  # B0
	"DI"  , "CALL", "SET" , "BBS" , "MOV" , "MOV" , "MOV" , "MOV" , "CMP" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "POP" , "MUL" ,  # C0
	"BNE" , "CALL", "CLR" , "BBC" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "DEC" , "MOV" , "CBNE", "DAA" ,  # D0
	"CLR" , "CALL", "SET" , "BBS" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "NOT" , "MOV" , "MOV" , "NOT" , "POP" , "SLEEP", # E0
	"BEQ" , "CALL", "CLR" , "BBC" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "MOV" , "INC" , "MOV" , "DBNZ", "STOP",  # F0
]


GET_OP_PARAMS = {
	"ADC": {
		0x99: {"size": 1, "op": "ADC  (X), (Y)"},
		0x88: {"size": 2, "op": "ADC  A, #$_r0_"},
		0x86: {"size": 1, "op": "ADC  A, (X)"},
		0x97: {"size": 2, "op": "ADC  A, ($_r0_)+Y"},
		0x87: {"size": 2, "op": "ADC  A, ($_r0_+X)"},
		0x84: {"size": 2, "op": "ADC  A, $_r0_"},
		0x94: {"size": 2, "op": "ADC  A, $_r0_+X"},
		0x85: {"size": 3, "op": "ADC  A, $_r1__r0_"},
		0x95: {"size": 3, "op": "ADC  A, $_r1__r0_+X"},
		0x96: {"size": 3, "op": "ADC  A, $_r1__r0_+Y"},
		0x89: {"size": 3, "op": "ADC  $_r1_, $_r0_"},
		0x98: {"size": 3, "op": "ADC  $_r1_, #$_r0_"},
	},
	"ADDW": {
		0x7A: {"size": 2, "op": "ADDW YA, $_r0_"},
	},
	"AND": {
		0x39: {"size": 1, "op": "AND  (X), (Y)"},
		0x28: {"size": 2, "op": "AND  A, #$_r0_"},
		0x26: {"size": 1, "op": "AND  A, (X)"},
		0x37: {"size": 2, "op": "AND  A, ($_r0_)+Y"},
		0x27: {"size": 2, "op": "AND  A, ($_r0_+X)"},
		0x24: {"size": 2, "op": "AND  A, $_r0_"},
		0x34: {"size": 2, "op": "AND  A, $_r0_+X"},
		0x25: {"size": 3, "op": "AND  A, $_r1__r0_"},
		0x35: {"size": 3, "op": "AND  A, $_r1__r0_+X"},
		0x36: {"size": 3, "op": "AND  A, $_r1__r0_+Y"},
		0x29: {"size": 3, "op": "AND  $_r1_, $_r0_"},
		0x38: {"size": 3, "op": "AND  $_r1_, #$_r0_"},
		0x6A: {"size": 3, "op": "AND1 C, !$_r1__r0_"},
		0x4A: {"size": 3, "op": "AND1 C, $_r1__r0_"},
	},
	"ASL": {
		0x1C: {"size": 1, "op": "ASL  A"},
		0x0B: {"size": 2, "op": "ASL  $_r0_"},
		0x1B: {"size": 2, "op": "ASL  $_r0_+X"},
		0x0C: {"size": 3, "op": "ASL  $_r1__r0_"},
	},
	"BBC": {
		0x13: {"size": 3, "op": "BBC0 $_r0_, _REL_", "rel": True},
		0x33: {"size": 3, "op": "BBC1 $_r0_, _REL_", "rel": True},
		0x53: {"size": 3, "op": "BBC2 $_r0_, _REL_", "rel": True},
		0x73: {"size": 3, "op": "BBC3 $_r0_, _REL_", "rel": True},
		0x93: {"size": 3, "op": "BBC4 $_r0_, _REL_", "rel": True},
		0xB3: {"size": 3, "op": "BBC5 $_r0_, _REL_", "rel": True},
		0xD3: {"size": 3, "op": "BBC6 $_r0_, _REL_", "rel": True},
		0xF3: {"size": 3, "op": "BBC7 $_r0_, _REL_", "rel": True},
	},
	"BBS": {
		0x03: {"size": 3, "op": "BBS0 $_r0_, _REL_", "rel": True},
		0x23: {"size": 3, "op": "BBS1 $_r0_, _REL_", "rel": True},
		0x43: {"size": 3, "op": "BBS2 $_r0_, _REL_", "rel": True},
		0x63: {"size": 3, "op": "BBS3 $_r0_, _REL_", "rel": True},
		0x83: {"size": 3, "op": "BBS4 $_r0_, _REL_", "rel": True},
		0xA3: {"size": 3, "op": "BBS5 $_r0_, _REL_", "rel": True},
		0xC3: {"size": 3, "op": "BBS6 $_r0_, _REL_", "rel": True},
		0xE3: {"size": 3, "op": "BBS7 $_r0_, _REL_", "rel": True},
	},
	"BCC": {
		0x90: {"size": 2, "op": "BCC  _REL_", "rel": True},
	},
	"BCS": {
		0xB0: {"size": 2, "op": "BCS  _REL_", "rel": True},
	},
	"BEQ": {
		0xF0: {"size": 2, "op": "BEQ  _REL_", "rel": True},
	},
	"BMI": {
		0x30: {"size": 2, "op": "BMI  _REL_", "rel": True},
	},
	"BNE": {
		0xD0: {"size": 2, "op": "BNE  _REL_", "rel": True},
	},
	"BPL": {
		0x10: {"size": 2, "op": "BPL  _REL_", "rel": True},
	},
	"BVC": {
		0x50: {"size": 2, "op": "BVC  _REL_", "rel": True},
	},
	"BVS": {
		0x70: {"size": 2, "op": "BVS  _REL_", "rel": True},
	},
	"BRA": {
		0x2F: {"size": 2, "op": "BRA  _REL_", "rel": True},
	},
	"BRK": {
		0x0F: {"size": 1, "op": "BRK"},
	},
	"CALL": {		# includes TCALL and PCALL
		0x3F: {"size": 3, "op": "CALL $_r1__r0_"},
		0x4F: {"size": 2, "op": "PCALL $_r0_"},
		0x01: {"size": 1, "op": "TCALL 0"},
		0x11: {"size": 1, "op": "TCALL 1"},
		0x21: {"size": 1, "op": "TCALL 2"},
		0x31: {"size": 1, "op": "TCALL 3"},
		0x41: {"size": 1, "op": "TCALL 4"},
		0x51: {"size": 1, "op": "TCALL 5"},
		0x61: {"size": 1, "op": "TCALL 6"},
		0x71: {"size": 1, "op": "TCALL 7"},
		0x81: {"size": 1, "op": "TCALL 8"},
		0x91: {"size": 1, "op": "TCALL 9"},
		0xA1: {"size": 1, "op": "TCALL 10"},
		0xB1: {"size": 1, "op": "TCALL 11"},
		0xC1: {"size": 1, "op": "TCALL 12"},
		0xD1: {"size": 1, "op": "TCALL 13"},
		0xE1: {"size": 1, "op": "TCALL 14"},
		0xF1: {"size": 1, "op": "TCALL 15"},
	},
	"CBNE": {
		0xDE: {"size": 3, "op": "CBNE $_r0_+X, _REL_", "rel": True},
		0x2E: {"size": 3, "op": "CBNE $_r0_, _REL_", "rel": True},
	},
	"CLR": {
		0x12: {"size": 2, "op": "CLR0 $_r0_"},
		0x32: {"size": 2, "op": "CLR1 $_r0_"},
		0x52: {"size": 2, "op": "CLR2 $_r0_"},
		0x72: {"size": 2, "op": "CLR3 $_r0_"},
		0x92: {"size": 2, "op": "CLR4 $_r0_"},
		0xB2: {"size": 2, "op": "CLR5 $_r0_"},
		0xD2: {"size": 2, "op": "CLR6 $_r0_"},
		0xF2: {"size": 2, "op": "CLR7 $_r0_"},
		0x60: {"size": 1, "op": "CLRC"},
		0x20: {"size": 1, "op": "CLRP"},
		0xE0: {"size": 1, "op": "CLRV"},
	},
	"CMP": {
		0x79: {"size": 1, "op": "CMP  (X), (Y)"},
		0x68: {"size": 2, "op": "CMP  A, #$_r0_"},
		0x66: {"size": 1, "op": "CMP  A, (X)"},
		0x77: {"size": 2, "op": "CMP  A, ($_r0_)+Y"},
		0x67: {"size": 2, "op": "CMP  A, ($_r0_+X)"},
		0x64: {"size": 2, "op": "CMP  A, $_r0_"},
		0x74: {"size": 2, "op": "CMP  A, $_r0_+X"},
		0x65: {"size": 3, "op": "CMP  A, $_r1__r0_"},
		0x75: {"size": 3, "op": "CMP  A, $_r1__r0_+X"},
		0x76: {"size": 3, "op": "CMP  A, $_r1__r0_+Y"},
		0x69: {"size": 3, "op": "CMP  $_r1_, $_r0_"},
		0x78: {"size": 3, "op": "CMP  $_r1_, #$_r0_"},
		0xC8: {"size": 2, "op": "CMP  X, #$_r0_"},
		0x3E: {"size": 2, "op": "CMP  X, $_r0_"},
		0x1E: {"size": 3, "op": "CMP  X, $_r1__r0_"},
		0xAD: {"size": 2, "op": "CMP  Y, #$_r0_"},
		0x7E: {"size": 2, "op": "CMP  Y, $_r0_"},
		0x5E: {"size": 3, "op": "CMP  Y, $_r1__r0_"},
		0x5A: {"size": 2, "op": "CMPW YA, $_r0_"},

	},
	"DAA": {
		0xDF: {"size": 1, "op": "DAA  A"},
	},
	"DAS": {
		0xBE: {"size": 1, "op": "DAS  A"},
	},
	"DBNZ": {
		0xFE: {"size": 2, "op": "DBNZ Y, _REL_", "rel": True},
		0x6E: {"size": 3, "op": "DBNZ $_r0_, _REL_", "rel": True},
	},
	"DEC": {
		0x9C: {"size": 1, "op": "DEC  A"},
		0x1D: {"size": 1, "op": "DEC  X"},
		0xDC: {"size": 1, "op": "DEC  Y"},
		0x8B: {"size": 2, "op": "DEC  $_r0_"},
		0x9B: {"size": 2, "op": "DEC  $_r0_+X"},
		0x8C: {"size": 3, "op": "DEC  $_r1__r0_"},
		0x1A: {"size": 2, "op": "DECW $_r0_"},
	},
	"DI": {
		0xC0: {"size": 1, "op": "DI"},
	},
	"DIV": {
		0x9E: {"size": 1, "op": "DIV  YA, X"},
	},
	"EI": {
		0xA0: {"size": 1, "op": "EI"},
	},
	"EOR": {
		0x59: {"size": 1, "op": "EOR  (X), (Y)"},
		0x48: {"size": 2, "op": "EOR  A, #$_r0_"},
		0x46: {"size": 1, "op": "EOR  A, (X)"},
		0x57: {"size": 2, "op": "EOR  A, ($_r0_)+Y"},
		0x47: {"size": 2, "op": "EOR  A, ($_r0_+X)"},
		0x44: {"size": 2, "op": "EOR  A, $_r0_"},
		0x54: {"size": 2, "op": "EOR  A, $_r0_+X"},
		0x45: {"size": 3, "op": "EOR  A, $_r1__r0_"},
		0x55: {"size": 3, "op": "EOR  A, $_r1__r0_+X"},
		0x56: {"size": 3, "op": "EOR  A, $_r1__r0_+Y"},
		0x49: {"size": 3, "op": "EOR  $_r1_, $_r0_"},
		0x58: {"size": 3, "op": "EOR  $_r1_, #$_r0_"},
		0x8A: {"size": 3, "op": "EOR1 C, $_r1__r0_"},
	},
	"INC": {
		0xBC: {"size": 1, "op": "INC  A"},
		0x3D: {"size": 1, "op": "INC  X"},
		0xFC: {"size": 1, "op": "INC  Y"},
		0xAB: {"size": 2, "op": "INC  $_r0_"},
		0xBB: {"size": 2, "op": "INC  $_r0_+X"},
		0xAC: {"size": 3, "op": "INC  $_r1__r0_"},
		0x3A: {"size": 2, "op": "INCW $_r0_"},
	},
	"JMP": {
		0x1F: {"size": 3, "op": "JMP  ($_r1__r0_+X)"},
		0x5F: {"size": 3, "op": "JMP  $_r1__r0_"},
	},
	"LSR": {
		0x5C: {"size": 1, "op": "LSR  A"},
		0x4B: {"size": 2, "op": "LSR  $_r0_"},
		0x5B: {"size": 2, "op": "LSR  $_r0_+X"},
		0x4C: {"size": 3, "op": "LSR  $_r1__r0_"},
	},
	"MOV": {
		0xAF: {"size": 1, "op": "MOV  (X+), A"},
		0xC6: {"size": 1, "op": "MOV  (X), A"},
		0xD7: {"size": 2, "op": "MOV  ($_r0_)+Y, A"},
		0xC7: {"size": 2, "op": "MOV  ($_r0_+X), A"},
		0xE8: {"size": 2, "op": "MOV  A, #$_r0_"},
		0xE6: {"size": 1, "op": "MOV  A, (X)"},
		0xBF: {"size": 1, "op": "MOV  A, (X+)"},
		0xF7: {"size": 2, "op": "MOV  A, ($_r0_)+Y"},
		0xE7: {"size": 2, "op": "MOV  A, ($_r0_+X)"},
		0x7D: {"size": 1, "op": "MOV  A, X"},
		0xDD: {"size": 1, "op": "MOV  A, Y"},
		0xE4: {"size": 2, "op": "MOV  A, $_r0_"},
		0xF4: {"size": 2, "op": "MOV  A, $_r0_+X"},
		0xE5: {"size": 3, "op": "MOV  A, $_r1__r0_"},
		0xF5: {"size": 3, "op": "MOV  A, $_r1__r0_+X"},
		0xF6: {"size": 3, "op": "MOV  A, $_r1__r0_+Y"},
		0xBD: {"size": 1, "op": "MOV  SP, X"},
		0xCD: {"size": 2, "op": "MOV  X, #$_r0_"},
		0x5D: {"size": 1, "op": "MOV  X, A"},
		0x9D: {"size": 1, "op": "MOV  X, SP"},
		0xF8: {"size": 2, "op": "MOV  X, $_r0_"},
		0xF9: {"size": 2, "op": "MOV  X, $_r0_+Y"},
		0xE9: {"size": 3, "op": "MOV  X, $_r1__r0_"},
		0x8D: {"size": 2, "op": "MOV  Y, #$_r0_"},
		0xFD: {"size": 1, "op": "MOV  Y, A"},
		0xEB: {"size": 2, "op": "MOV  Y, $_r0_"},
		0xFB: {"size": 2, "op": "MOV  Y, $_r0_+X"},
		0xEC: {"size": 3, "op": "MOV  Y, $_r1__r0_"},
		0xFA: {"size": 3, "op": "MOV  $_r1_, $_r0_"},
		0xD4: {"size": 2, "op": "MOV  $_r0_+X, A"},
		0xDB: {"size": 2, "op": "MOV  $_r0_+X, Y"},
		0xD9: {"size": 2, "op": "MOV  $_r0_+Y, X"},
		0x8F: {"size": 3, "op": "MOV  $_r1_, #$_r0_"},
		0xC4: {"size": 2, "op": "MOV  $_r0_, A"},
		0xD8: {"size": 2, "op": "MOV  $_r0_, X"},
		0xCB: {"size": 2, "op": "MOV  $_r0_, Y"},
		0xD5: {"size": 3, "op": "MOV  $_r1__r0_+X, A"},
		0xD6: {"size": 3, "op": "MOV  $_r1__r0_+Y, A"},
		0xC5: {"size": 3, "op": "MOV  $_r1__r0_, A"},
		0xC9: {"size": 3, "op": "MOV  $_r1__r0_, X"},
		0xCC: {"size": 3, "op": "MOV  $_r1__r0_, Y"},
		0xAA: {"size": 3, "op": "MOV1 C, $_r1__r0_"},
		0xCA: {"size": 3, "op": "MOV1 $_r1__r0_, C"},
		0xBA: {"size": 2, "op": "MOVW YA, $_r0_"},
		0xDA: {"size": 2, "op": "MOVW $_r0_, YA"},
	},
	"MUL": {
		0xCF: {"size": 1, "op": "MUL  YA"},
	},
	"NOP": {
		0x00: {"size": 1, "op": "NOP"},
	},
	"NOT": {
		0xEA: {"size": 3, "op": "NOT1 $_r1__r0_"},
		0xED: {"size": 1, "op": "NOTC"},
	},
	"OR": {
		0x19: {"size": 1, "op": "OR   (X), (Y)"},
		0x08: {"size": 2, "op": "OR   A, #$_r0_"},
		0x06: {"size": 1, "op": "OR   A, (X)"},
		0x17: {"size": 2, "op": "OR   A, ($_r0_)+Y"},
		0x07: {"size": 2, "op": "OR   A, ($_r0_+X)"},
		0x04: {"size": 2, "op": "OR   A, $_r0_"},
		0x14: {"size": 2, "op": "OR   A, $_r0_+X"},
		0x05: {"size": 3, "op": "OR   A, $_r1__r0_"},
		0x15: {"size": 3, "op": "OR   A, $_r1__r0+X"},
		0x16: {"size": 3, "op": "OR   A, $_r1__r0+Y"},
		0x09: {"size": 3, "op": "OR   $_r1_, $_r0_"},
		0x18: {"size": 3, "op": "OR   $_r1_, #$_r0_"},
		0x2A: {"size": 3, "op": "OR1  C, !$_r1__r0_"},
		0x0A: {"size": 3, "op": "OR1  C, $_r1__r0_"},
	},
	"POP": {
		0xAE: {"size": 1, "op": "POP  A"},
		0x8E: {"size": 1, "op": "POP  P"},
		0xCE: {"size": 1, "op": "POP  X"},
		0xEE: {"size": 1, "op": "POP  Y"},
	},
	"PUSH": {
		0x2D: {"size": 1, "op": "PUSH A"},
		0x0D: {"size": 1, "op": "PUSH P"},
		0x4D: {"size": 1, "op": "PUSH X"},
		0x6D: {"size": 1, "op": "PUSH Y"},
	},
	"RET": {
		0x6F: {"size": 1, "op": "RET"},
		0x7F: {"size": 1, "op": "RETI"},
	},
	"ROL": {
		0x3C: {"size": 1, "op": "ROL  A"},
		0x2B: {"size": 2, "op": "ROL  $_r0_"},
		0x3B: {"size": 2, "op": "ROL  $_r0_+X"},
		0x2C: {"size": 3, "op": "ROL  $_r1__r0_"},
	},
	"ROR": {
		0x7C: {"size": 1, "op": "ROR  A"},
		0x6B: {"size": 2, "op": "ROR  $_r0_"},
		0x7B: {"size": 2, "op": "ROR  $_r0_+X"},
		0x6C: {"size": 3, "op": "ROR  $_r1__r0_"},
	},
	"SBC": {
		0xB9: {"size": 1, "op": "SBC  (X), (Y)"},
		0xA8: {"size": 2, "op": "SBC  A, #$_r0_"},
		0xA6: {"size": 1, "op": "SBC  A, (X)"},
		0xB7: {"size": 2, "op": "SBC  A, ($_r0_)+Y"},
		0xA7: {"size": 2, "op": "SBC  A, ($_r0_+X)"},
		0xA4: {"size": 2, "op": "SBC  A, $_r0_"},
		0xB4: {"size": 2, "op": "SBC  A, $_r0_+X"},
		0xA5: {"size": 3, "op": "SBC  A, $_r1__r0_"},
		0xB5: {"size": 3, "op": "SBC  A, $_r1__r0_+X"},
		0xB6: {"size": 3, "op": "SBC  A, $_r1__r0_+Y"},
		0xA9: {"size": 3, "op": "SBC  $_r1_, $_r0_"},
		0xB8: {"size": 3, "op": "SBC  $_r1_, #$_r0_"},
	},
	"SET": {
		0x02: {"size": 2, "op": "SET0 $_r0_"},
		0x22: {"size": 2, "op": "SET1 $_r0_"},
		0x42: {"size": 2, "op": "SET2 $_r0_"},
		0x62: {"size": 2, "op": "SET3 $_r0_"},
		0x82: {"size": 2, "op": "SET4 $_r0_"},
		0xA2: {"size": 2, "op": "SET5 $_r0_"},
		0xC2: {"size": 2, "op": "SET6 $_r0_"},
		0xE2: {"size": 2, "op": "SET7 $_r0_"},
		0x80: {"size": 1, "op": "SETC"},
		0x40: {"size": 1, "op": "SETP"},
	},
	"SLEEP": {
		0xEF: {"size": 1, "op": "SLEEP"},
	},
	"STOP": {
		0xFF: {"size": 1, "op": "STOP"},
	},
	"SUBW": {
		0x9A: {"size": 2, "op": "SUBW YA, $_r0_"},
	},
	"TCLR": {
		0x4E: {"size": 3, "op": "TCLR $_r1__r0_, A"},
	},
	"TSET": {
		0x0E: {"size": 3, "op": "TSET $_r1__r0_, A"},
	},
	"XCN": {
		0x9F: {"size": 1, "op": "XCN  A"},
	},
}


REL_OPS = {
	0x13,0x33,0x53,0x73,0x93,0xB3,0xD3,0xF3,	# BBC
	0x03,0x23,0x43,0x63,0x83,0xA3,0xC3,0xE3,	# BBS
	0x90,	# BCC
	0xB0,	# BCS
	0xF0,	# BEQ
	0x30,	# BMI
	0xD0,	# BNE
	0x10,	# BPL
	0x50,	# BVC
	0x70,	# BVS
	0x2F,	# BRA
	#0x3F,		# PCALL
	0x2E,0xDE,	# CBNE
	0x6E,0xFE,	# DBNZ
}


REL_AND_ADDR_OPS = {
	0x13,0x33,0x53,0x73,0x93,0xB3,0xD3,0xF3,	# BBC
	0x03,0x23,0x43,0x63,0x83,0xA3,0xC3,0xE3,	# BBS
	0xDE,
	0x2E,
	0x6E,
}


KNOWN_TABLES = {}

KNOWN_LABELS = {}

LABEL_OBJS = {}

USED_LABELS = {}


def is_special(OP):
	if OP in REL_OPS:
		return True

	return False






ERROR_HEAD = '[ERROR] '


TYPE_NUM = type(0)
TYPE_LIST = type(list())
TYPE_TUPLE = type(tuple())
LIST_TYPES = { TYPE_LIST, TYPE_TUPLE }


def FRMT_WORD(n):
	if type(n) == TYPE_NUM:
		return format(n, '04x').upper()
	elif type(n) == LIST_TYPES:
		return 

def FRMT_BYTE(n):
	return format(n, '02x').upper()


def TO_WORD(l):
	return l[0] + (l[1] << 8)




def get_hierarchy(LABEL_HIERARCHY, label=None):

	if label != None:
		sub_level = 0
		while label[0] == ".":
			sub_level += 1
			label = label[1:]

		for i in range(sub_level, 4):
			LABEL_HIERARCHY[i] = ""

		LABEL_HIERARCHY[sub_level] = label

	FULL_LABEL = ""

	first = True
	for l in LABEL_HIERARCHY:
		if l != "":
			if first: first = False
			else:	FULL_LABEL += "_"
			FULL_LABEL += l

	return FULL_LABEL

def SET_HIERARCHY(label):
	global CURRENT_HIERARCHY

	if label[0] == "#" or label[0] == "+" or label[0] == "-":
		pass
	else:

		sub_level = 0
		while label[0] == ".":
			sub_level += 1
			label = label[1:]

		for i in range(sub_level, 4):
			CURRENT_HIERARCHY[i] = ""

		CURRENT_HIERARCHY[sub_level] = label





CURRENT_HIERARCHY = ["", "", "", ""]


def expand_sub_label(sub_label):
	return get_hierarchy(CURRENT_HIERARCHY, label=sub_label)




def get_label(addr):
	lbl_list = KNOWN_LABELS[addr]

	OUT_LABEL = None

	def get_prio(lbl_obj):
		if lbl_obj["is_pos_neg"] == True: return 10
		if lbl_obj["is_sublabel"] == True:
			if expand_sub_label(lbl_obj["label"]) == lbl_obj["FULL_LABEL"]: return 9

		if lbl_obj["is_global"] == True: return 8

		if lbl_obj["is_inplace"] == True: return 1

		if lbl_obj["is_sublabel"] == True: return 2

		return 5


	for FULL_LABEL in lbl_list:
		lbl_obj = LABEL_OBJS[FULL_LABEL]

		if OUT_LABEL == None:
			OUT_LABEL = lbl_obj
		elif get_prio(lbl_obj) > get_prio(OUT_LABEL):
			OUT_LABEL = lbl_obj

	
	if OUT_LABEL["is_inplace"]:
		lbl = OUT_LABEL["label"]
		if lbl[0] == "#": lbl = lbl[1:]
		return lbl
	elif OUT_LABEL["is_sublabel"]:
		if expand_sub_label(OUT_LABEL["label"]) == OUT_LABEL["FULL_LABEL"]:
			return OUT_LABEL["label"]
		else:
			return OUT_LABEL["FULL_LABEL"]
	elif OUT_LABEL["is_pos_neg"]:
		return OUT_LABEL["label"]
	else:
		return OUT_LABEL["FULL_LABEL"]









def ADD_KNOWN_LABEL(addr, label, FULL_LABEL=None, is_global=False, is_pos_neg=False, is_inplace=False, is_sublabel=False):
	global KNOWN_LABELS
	global LABEL_OBJS


	if FULL_LABEL == None: FULL_LABEL = label

	if addr in KNOWN_LABELS:
		KNOWN_LABELS[addr].append(FULL_LABEL)
	else:
		KNOWN_LABELS[addr] = [FULL_LABEL]


	LABEL_OBJS[FULL_LABEL] = {
		"addr": addr,
		"is_global": is_global,
		"is_pos_neg": is_pos_neg,
		"is_inplace": is_inplace,
		"is_sublabel": is_sublabel,
		"label": label,
		"FULL_LABEL": FULL_LABEL,
	}


def DISASSEMBLE_SPC(SPC_DATA, START_ADDRESS=0x800):

	global KNOWN_LABELS
	global KNOWN_TABLES
	global USED_LABELS
	global CURRENT_HIERARCHY

	
	DATA = SPC_DATA

	DATA_IND = 0

	DISASSEMBLED_LINES = []

	ROM_SIZE = len(DATA)


	CURRENT_HIERARCHY = ["", "", "", ""]


	while DATA_IND < ROM_SIZE:

		ADDR = DATA_IND + START_ADDRESS
			

		if ADDR in KNOWN_TABLES:
			

			TABLE_TYPE = TABLE_NAMES[KNOWN_TABLES[ADDR]]


			if ADDR in KNOWN_LABELS:
				line_header = ""
				for l in KNOWN_LABELS[ADDR]:
					lbl_obj = LABEL_OBJS[l]

					if line_header != "":
						DISASSEMBLED_LINES.append(line_header)

					line_header = lbl_obj["label"] + ":"


			else:
				#KNOWN_LABELS[ADDR] = "TABLE_" + FRMT_WORD(ADDR)
				line_header = "TABLE_" + FRMT_WORD(ADDR) + ":" 


			E = ROM_SIZE - DATA_IND

			SIZE = 0
			for _ in range(E):
				SIZE += 1
				if ADDR + SIZE in KNOWN_LABELS: 
					break
					#if KNOWN_LABELS[ADDR+SIZE].split("_")[0] != "UNKNOWN":	# nice job... >_>
					#	break

			L = len(line_header)
			if L % 4 != 0:
				line_header += "\t"
				L = ((L // 4)+1)*4

			while L < 16:
				line_header += "\t"
				L += 4

			DISASSEMBLED_LINES.append(line_header)

			TBL_DATA = DATA[DATA_IND:DATA_IND+SIZE]
			DATA_IND += SIZE

			if TABLE_TYPE == BYTE_TBL:
				while True:
					row_end = min(8, len(TBL_DATA))
					if row_end == 0: break
					row = TBL_DATA[:row_end]
					TBL_DATA = TBL_DATA[row_end:]

					DISASSEMBLED_LINES.append("\t"*4 + "db\t$" + ",$".join([FRMT_BYTE(x) for x in row]))

					if row_end < 8: break

			elif TABLE_TYPE == WORD_TBL:
				while True:
					row_end = min(16, len(TBL_DATA))
					if row_end == 0: break
					row = TBL_DATA[:row_end]
					TBL_DATA = TBL_DATA[row_end:]


					DISASSEMBLED_LINES.append("\t"*4 + "dw\t$" + ",$".join([FRMT_WORD(row[(i*2)+0] + (row[(i*2)+1] << 8)) for i in range(len(row)//2)]))
					if row_end < 16: break

			elif TABLE_TYPE == PNTR_TBL:
				while True:
					row_end = min(16, len(TBL_DATA))
					if row_end == 0: break
					row = TBL_DATA[:row_end]
					TBL_DATA = TBL_DATA[row_end:]

					
					LINE = "\t"*4 + "dw\t"

					for i in range(len(row)//2):
						word_addr = TO_WORD(row[i*2:(i+1)*2])

						if word_addr in KNOWN_LABELS:
							word_addr = get_label(word_addr)
						else:
							word_addr = "$" + FRMT_WORD(word_addr)

						LINE += word_addr + ","

					if LINE[-1] == ",": LINE = LINE[:-1]
					

					DISASSEMBLED_LINES.append(LINE)
					if row_end < 16: break



			continue








		# get opcode

		OP = DATA[DATA_IND]
		DATA_IND += 1

		FRMT = GET_OP_PARAMS[OP_TO_NAME[OP]][OP]

		ARG_SIZE = FRMT["size"] - 1
		OUT_TXT = FRMT["op"]


		if is_special(OP):
			# special opcode

			if OP in REL_AND_ADDR_OPS:
				# addr and REL, do the addr first
				arg0 = DATA[DATA_IND]
				DATA_IND += 1
				wrote_r0 = False
				if "$_r0_" in OUT_TXT and not "#$_r0_" in OUT_TXT:
					if arg0 in KNOWN_LABELS:
						OUT_TXT = OUT_TXT.replace("$_r0_", get_label(arg0))
						wrote_r0 = True


				if not wrote_r0:
					OUT_TXT = OUT_TXT.replace("_r0_", FRMT_BYTE(arg0))

				ARG_SIZE -= 1


			if ARG_SIZE == 1:
				rel_addr = DATA[DATA_IND]
				DATA_IND += 1

				if rel_addr > 0x7F:
					rel_addr -= 0x100

				rel_addr += DATA_IND + START_ADDRESS


				if rel_addr in KNOWN_LABELS:
					rel_addr = get_label(rel_addr)
				else:
					#KNOWN_LABELS[rel_addr] = "CODE_" + FRMT_WORD(rel_addr)
					rel_addr = "CODE_" + FRMT_WORD(rel_addr)


				OUT_TXT = OUT_TXT.replace("_REL_", rel_addr)

				

			elif ARG_SIZE == 2:
				print("WOAH 2 BYTE REL UH OH @ address " + FRMT_WORD(ADDR) + " / offset " + FRMT_WORD(ADDR - START_ADDRESS))
				DATA_IND += 2


		else:
			# regular opcode

			if ARG_SIZE == 1:
				# 1 byte of args

				arg0 = DATA[DATA_IND]
				DATA_IND += 1

				wrote_r0 = False
				if "$_r0_" in OUT_TXT and not "#$_r0_" in OUT_TXT:
					if arg0 in KNOWN_LABELS:
						OUT_TXT = OUT_TXT.replace("$_r0_", get_label(arg0))
						wrote_r0 = True


				if not wrote_r0:
					OUT_TXT = OUT_TXT.replace("_r0_", FRMT_BYTE(arg0))


			elif ARG_SIZE == 2:
				# 2 bytes of args

				if "_r1__r0_" in OUT_TXT:
					# word addr
					arg0 = DATA[DATA_IND]
					DATA_IND += 1
					arg1 = DATA[DATA_IND]
					DATA_IND += 1

					word_addr = arg0 + (arg1 << 8)

					if OP == 0x3F or OP == 0x5F:
						# CALL or JMP
						if word_addr < 0x100: 
							space_ind = OUT_TXT.find(" ")
							OUT_TXT = OUT_TXT[:space_ind] + ".W" + OUT_TXT[space_ind:]

						if word_addr in KNOWN_LABELS:
							word_addr = get_label(word_addr)
						else:
							#ADD_KNOWN_LABEL(word_addr, "CODE_" + FRMT_WORD(word_addr))
							word_addr = "CODE_" + FRMT_WORD(word_addr)

						OUT_TXT = OUT_TXT.replace("$_r1__r0_", word_addr)

					else:

						if word_addr < 0xF0: 
							space_ind = OUT_TXT.find(" ")

							if OP == 0xE5:
								OUT_TXT = OUT_TXT[:space_ind] + ".W" + OUT_TXT[space_ind:]

						if word_addr in KNOWN_LABELS:
							addr = word_addr
							word_addr = get_label(word_addr)

						else:
							if word_addr <= 0x03DB:
								#ADD_KNOWN_LABEL(word_addr, "!RAM_" + FRMT_WORD(word_addr))
								word_addr = "!RAM_" + FRMT_WORD(word_addr)
							else:
								#ADD_KNOWN_LABEL(word_addr, "UNKNOWN_" + FRMT_WORD(word_addr))
								word_addr = "$" + FRMT_WORD(word_addr)

						OUT_TXT = OUT_TXT.replace("$_r1__r0_", word_addr)

				else:
					# 2 byte values
					arg0 = DATA[DATA_IND]
					DATA_IND += 1
					arg1 = DATA[DATA_IND]
					DATA_IND += 1

					wrote_r0 = False
					if "$_r0_" in OUT_TXT and not "#$_r0_" in OUT_TXT:
						if arg0 in KNOWN_LABELS:
							OUT_TXT = OUT_TXT.replace("$_r0_", get_label(arg0))
							wrote_r0 = True

					if not wrote_r0:
						OUT_TXT = OUT_TXT.replace("_r0_", FRMT_BYTE(arg0))



					wrote_r1 = False
					if "$_r1_" in OUT_TXT and not "#$_r1_" in OUT_TXT:
						if arg1 in KNOWN_LABELS:
							OUT_TXT = OUT_TXT.replace("$_r1_", get_label(arg1))
							wrote_r1 = False
					
					if not wrote_r1:
						OUT_TXT = OUT_TXT.replace("_r1_", FRMT_BYTE(arg1))

			else:
				# no args
				pass


		if ADDR in KNOWN_LABELS:

			line_header = ""
			for l in KNOWN_LABELS[ADDR]:

				if line_header != "":
					DISASSEMBLED_LINES.append(line_header)
					line_header = ""

				lbl_obj = LABEL_OBJS[l]

				lbl = lbl_obj["label"]

				line_header = lbl
				if lbl_obj["is_pos_neg"]:
					line_header = "\t\t" + line_header
				else:
					if "UNKNOWN" in line_header:
						line_header = ""
					else:
						line_header += ":"

						if lbl_obj["is_global"]: line_header = "global " + line_header

						if line_header[0] == ".":
							line_header = "\t" + line_header

						DISASSEMBLED_LINES.append(line_header)

						line_header = ""

						SET_HIERARCHY(lbl)

		else:
			line_header = ""


		L = len(line_header)

		if L != 0:
			i = 0
			while line_header[i] == "\t":
				L += 3
				i += 1

		if L % 4 != 0:
			line_header += "\t"
			L = ((L // 4)+1)*4

		while L < 16:
			line_header += "\t"
			L += 4

		OUT_LINE = line_header




		OUT_LINE += OUT_TXT

		#OUT_LINE += "; "


		'''
		if PRINT_BYTE_DEBUG:

			OUT_LINE += FRMT_WORD(ADDR) + " : "


			DATA_OFFS = ADDR - START_ADDRESS

			num_bytes = FRMT["size"]

			for offs in range(3):

				if num_bytes != 0:
					OUT_LINE += FRMT_BYTE(DATA[DATA_OFFS + offs])
					num_bytes -= 1
				else:
					OUT_LINE += "  "

				OUT_LINE += " "

			OUT_LINE += "; "
		'''

		DISASSEMBLED_LINES.append(OUT_LINE)

	return DISASSEMBLED_LINES













BYTE_TBL = 0
WORD_TBL = 1
PNTR_TBL = 2

TABLE_NAMES = {
	"SONG_TABLE": PNTR_TBL,
	"SFX_TABLE": PNTR_TBL,
	"SFXCTRL_TABLE": PNTR_TBL,
	"EXSFX_TABLE": PNTR_TBL,
	"DOPPLER_PITCH_LOW": BYTE_TBL,
	"DOPPLER_PITCH_HIGH": BYTE_TBL,
	"DOPPLER_DIST_RATIO": BYTE_TBL,
	"DOPPLER_PANVOL_L": BYTE_TBL,
	"DOPPLER_PANVOL_R": BYTE_TBL,
	"PRIORITY_SFX": BYTE_TBL,
	"TIMED_SFX": BYTE_TBL,
	"SFX_TIME": BYTE_TBL,
	"ECHO_FIR_COEFFS": BYTE_TBL,
	"PAN_TABLE": BYTE_TBL,
	"NOTE_PITCH": WORD_TBL,
	"SUS_TABLE": BYTE_TBL,
	"VEL_TABLE": BYTE_TBL,
	"INSTR_PRMS": BYTE_TBL,
	"DSP_REGS_TBL": BYTE_TBL,
	"DSP_MIRROR_TBL": BYTE_TBL,
	"VCMD_TABLE": PNTR_TBL,
	"VCMD_NUM_ARGS": BYTE_TBL

}


FILE_ASM = 0
FILE_BRR = 1
FILE_SSF = 2



INCSRC = -1
NO_LOOP = -1





global FILE_DATA

FILE_DATA = (
	(FILE_ASM, "BUILD/driver/driver.asm", [(0x0800, 0x0B99), (INCSRC, "VCMD.asm"), (0x0DEB, 0x10BF)]),
	(FILE_ASM, "BUILD/driver/dsp_shadow.tbl", [(0x3FEC, 0x4000)]),
	(FILE_ASM, "BUILD/driver/VCMD.asm", [(0x0B99, 0x0DEB)]),
	(FILE_ASM, "BUILD/driver/VCMD.tbl", [(0x3F9B, 0x3FEC)]),
	(FILE_ASM, "BUILD/samples/sample_parameters.tbl", [(0x3C88, 0x3D24)]),
	(FILE_ASM, "BUILD/tables/echo_FIR.tbl", [(0x3F31, 0x3F51)]),
	(FILE_ASM, "BUILD/tables/pan.tbl", [(0x3F86, 0x3F9B)]),
	(FILE_ASM, "BUILD/tables/pitch.tbl", [(0x3F51, 0x3F7B)]),
	(FILE_ASM, "BUILD/tables/susvel.tbl", [(0x3C70, 0x3C88)]),
	(FILE_ASM, "BUILD/sound.asm", [(0x1664, 0x16B8), (INCSRC, "sfxctrl.asm"), (0x1797, 0x23A8)]),
	(FILE_ASM, "BUILD/sfxctrl.asm", [(0x16B8, 0x1797)]),
	(FILE_ASM, "BUILD/exsfx.asm", [(0x23A8, 0x2CEC)]),
	(FILE_ASM, "BUILD/sfx.asm", [(0x2CEC, 0x3B43)]),
	(FILE_ASM, "BUILD/util.asm", [(0x3B43, 0x3BD7)]),
	(FILE_ASM, "BUILD/routine_tables.asm", [(0x1566, 0x1664)]),
	(FILE_ASM, "BUILD/doppler_data.asm", [(0x1526, 0x1566)]),

	(FILE_BRR, "BUILD/samples/00_skid.brr", [(0x4000, 0x45CD), 0]),
	(FILE_BRR, "BUILD/samples/01_splash.brr", [(0x45CD, 0x4B1C), 1]),
	(FILE_BRR, "BUILD/samples/02_engineA.brr", [(0x4B1C, 0x4F6F), 2]),
	(FILE_BRR, "BUILD/samples/03_engineB.brr", [(0x4F6F, 0x5413), 3]),
	(FILE_BRR, "BUILD/samples/04_closed_hihat.brr", [(0x5413, 0x5878), 4]),
	(FILE_BRR, "BUILD/samples/05_reverb_snare.brr", [(0x5878, 0x7570), 5]),
	(FILE_BRR, "BUILD/samples/06_synth_kick.brr", [(0x7570, 0x7648), 6]),
	(FILE_BRR, "BUILD/samples/07_orchestra_hit.brr", [(0x7648, 0x81EB), 7]),
	(FILE_BRR, "BUILD/samples/08_synth_brass.brr", [(0x81EB, 0x89B0), 8]),
	(FILE_BRR, "BUILD/samples/09_clarinet.brr", [(0x89B0, 0x89E6), 9]),
	(FILE_BRR, "BUILD/samples/10_electric_guitar.brr", [(0x89E6, 0x998B), 10]),
	(FILE_BRR, "BUILD/samples/11_piano.brr", [(0x998B, 0xA0FF), 11]),
	(FILE_BRR, "BUILD/samples/12_synth_bass.brr", [(0xA0FF, 0xA5BE), 12]),
	(FILE_BRR, "BUILD/samples/13_marimba.brr", [(0xA5BE, 0xA6F9), 13]),
	(FILE_BRR, "BUILD/samples/14_drawbar_organ.brr", [(0xA6F9, 0xA74A), 14]),
	(FILE_BRR, "BUILD/samples/15_human_whistle.brr", [(0xA74A, 0xAB55), 15]),
	(FILE_BRR, "BUILD/samples/16_bongos.brr", [(0xAB55, 0xB014), 16]),
	(FILE_BRR, "BUILD/samples/17_nylon_guitar.brr", [(0xB014, 0xB31A), 17]),
	(FILE_BRR, "BUILD/samples/18_underwater.brr", [(0xB31A, 0xB701), 18]),
	(FILE_BRR, "BUILD/samples/19_gravel.brr", [(0xB701, 0xB9EC), 19]),
	(FILE_BRR, "BUILD/samples/20_synth_organ.brr", [(0xB9EC, 0xBA10), 20]),
	(FILE_BRR, "BUILD/samples/21_cowbell.brr", [(0xBA10, 0xBDE5), 21]),
	(FILE_BRR, "BUILD/samples/22_timbale.brr", [(0xBDE5, 0xC280), 22]),
	(FILE_BRR, "BUILD/samples/23_engineC.brr", [(0xC280, 0xC712), 23]),
	(FILE_BRR, "BUILD/samples/24_engineD.brr", [(0xC712, 0xC952), 24]),
	(FILE_BRR, "BUILD/samples/25_shrill_whistle.brr", [(0xC952, 0xD000), 25]),

	(FILE_SSF, "BUILD/songs/fanfare.ssf", [(0xFF00, 0xFFC0), "FANFARE", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/final_lap.ssf", [(0x3E45, 0x3F31), "FINAL_LAP", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/game_over.ssf", [(0xDE33, 0xDEFA), "GAME_OVER", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/gp_intro.ssf", [(0xD783, 0xD989), "GP_INTRO", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/no_record.ssf", [(0x03DB, 0x0506), "NO_RECORD", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/race_qualified.ssf", [(0xDAF9, 0xDC37), "QUALIFIED", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/rank_bowser.ssf", [(0x0506, 0x05FE), "RANK_BOWSER", 2]),
	(FILE_SSF, "BUILD/songs/rank_dkjr.ssf", [(0x124E, 0x13D7), "RANK_DKJR", 2]),
	(FILE_SSF, "BUILD/songs/rank_koopa.ssf", [(0x05FE, 0x06F0), "RANK_KOOPA", 2]),
	(FILE_SSF, "BUILD/songs/rank_luigi.ssf", [(0xDC37, 0xDD3B), "RANK_LUIGI", 2]),
	(FILE_SSF, "BUILD/songs/rank_mario.ssf", [(0xDD3B, 0xDE33), "RANK_MARIO", 2]),
	(FILE_SSF, "BUILD/songs/rank_out.ssf", [(0x06F0, 0x07CA), "RANK_OUT", NO_LOOP]),
	(FILE_SSF, "BUILD/songs/rank_peach.ssf", [(0xD989, 0xDAF9), "RANK_PEACH", 2]),
	(FILE_SSF, "BUILD/songs/rank_toad.ssf", [(0x3D24, 0x3E45), "RANK_TOAD", 2]),
	(FILE_SSF, "BUILD/songs/rank_yoshi.ssf", [(0x13D7, 0x1526), "RANK_YOSHI", 2]),
	(FILE_SSF, "BUILD/songs/starman.ssf", [(0x10BF, 0x124E), "STARMAN", 2]),
	(FILE_SSF, "BUILD/songs/tt_intro.ssf", [(0x07CA, 0x07FD), "TT_INTRO", NO_LOOP]),
)



def PRINT_EXC(e, error_head=ERROR_HEAD):
	print('\t' + error_head + ('\n\t' + error_head).join(''.join(traceback.format_exception(e)).split('\n')))





def EXTRACT_SPC_UPLOAD(SMK_filename):

	ROM_DATA = []

	with open(SMK_filename, 'rb') as f:

		ROM_DATA = f.read()

	L = len(ROM_DATA)

	if L == 0x080000:
		HEADER_OFFSET = 0
	elif L == 0x080200:
		HEADER_OFFSET = 0x200
	else:
		print('[ERROR] SPC Extraction Failed: Invalid SMK File!')
		return



	SPC = ARAM()
	SPC.upload_spc(ROM_DATA[0x28000+HEADER_OFFSET:0x30000+HEADER_OFFSET] + ROM_DATA[0x38000+HEADER_OFFSET:0x3D450+HEADER_OFFSET])

	return SPC





def USE_SYMBOLS_MAP(symbols_map_file):
	global KNOWN_TABLES

	LINES = []
	with open(symbols_map_file, 'r') as f:
		for line in f:
			if line.rstrip() != "":
				LINES.append(line)


	for line in LINES:
		addr, g_char, lbl, FULL_LABEL = line.rstrip().split()

		is_global = False
		if g_char == "g": is_global = True

		is_sublabel = False
		is_pos_neg = False
		is_inplace = False
		if lbl[0] == ":":
			if lbl[1:4] == "pos":
				is_pos_neg = True
				FULL_LABEL = lbl
				lbl = "+"*int(lbl.split("_")[1])
			elif lbl[1:4] == "neg":
				is_pos_neg = True
				FULL_LABEL = lbl
				lbl = "-"*int(lbl.split("_")[1])
		elif lbl[0] == "#":
			is_inplace = True
		elif lbl[0] == ".":
			is_sublabel = True

		addr = int(addr, 16)


		ADD_KNOWN_LABEL(addr, lbl, FULL_LABEL, is_global=is_global, is_pos_neg=is_pos_neg, is_inplace=is_inplace, is_sublabel=is_sublabel)


		if lbl in TABLE_NAMES:
			KNOWN_TABLES[addr] = lbl




def USE_RAM_MAP(ram_map_file):

	LINES = []
	with open(ram_map_file, 'r') as f:
		for line in f:
			LINES.append(line)


	for line in LINES:
		line = line.split(";")[0].replace("\n", "")

		if "=" in line:

			var, addr = line.split("=")

			var = var.lstrip().rstrip()
			addr = addr.lstrip().rstrip().replace("$", "")

			ADD_KNOWN_LABEL(int(addr, 16), var)






def RUN_DISASSEMBLY(SPC, test_patches=False):

	USE_SYMBOLS_MAP("SYMBOLS_MAP.txt")

	USE_RAM_MAP("BUILD/define/ram_map.def")




	





	



	for FILE_TYPE, OUT_FILE, CHUNKS in FILE_DATA:
		if FILE_TYPE == FILE_ASM:
			print("[INFO] DISASSEMBLING " + OUT_FILE)

			DISM_LINES = []

			for START, END in CHUNKS:
				if START != INCSRC:
					DISM_LINES += DISASSEMBLE_SPC(SPC.read(START, END-START), START_ADDRESS=START)
				else:
					DISM_LINES += ["incsrc \"" + END + "\""]

			if test_patches: OUT_FILE += ".ADSM"

			with open(OUT_FILE, 'w') as f:
				f.write("\n".join(DISM_LINES))

		elif FILE_TYPE == FILE_BRR:
			print("[INFO] EXTRACTING " + OUT_FILE)

			FILE_OFFS = CHUNKS[0]
			SAMPLE_NUM = CHUNKS[1]

			addr = SPC.read(0x3C00 + SAMPLE_NUM*4, 2)
			loop = SPC.read(0x3C02 + SAMPLE_NUM*4, 2)

			ADDR = addr[0] + (addr[1] << 8)
			LOOP = (loop[0] + (loop[1] << 8)) - ADDR

			with open(OUT_FILE, 'wb') as f:
				f.write(bytes([LOOP & 0xFF, (LOOP >> 8) & 0xFF]))
				f.write(SPC.read(FILE_OFFS[0], FILE_OFFS[1]-FILE_OFFS[0]))

		elif FILE_TYPE == FILE_SSF:
			print("[INFO] DECOMPOSING " + OUT_FILE)

			FILE_OFFS = CHUNKS[0]
			SONG_NAME = CHUNKS[1]
			LOOP_PTR = CHUNKS[2]

			jump_ptrs = {}

			if LOOP_PTR != -1:
				jump_ptrs[FILE_OFFS[0] + LOOP_PTR] = (0, '.loop')

			S = SONG(SPC.read(FILE_OFFS[0], FILE_OFFS[1]-FILE_OFFS[0]), FILE_OFFS[0], jump_ptrs, SONG_NAME)

			if test_patches: OUT_FILE += ".ADSM"

			with open(OUT_FILE, 'w') as file:
				file.write(S.disassemble_song())






def APPLY_PATCH(filename, test_patch=False):

	print('[INFO]', "APPLYING PATCH TO", filename)

	Failed = False

	FILE_NAME = filename
	if test_patch: FILE_NAME += ".ADSM"

	patch_stage = 1 # stage 1
	try:
		FILE_LINES = []

		with open(FILE_NAME, 'r') as f:
			for line in f:
				FILE_LINES.append(line.replace('\r', ''))

		if FILE_LINES[-1] == "": FILE_LINES[-1] += "\n"
		elif FILE_LINES[-1][-1] != "\n": FILE_LINES[-1] += "\n"
	except Exception as e:
		PRINT_EXC(e)
		print('\t' + ERROR_HEAD + 'COULD NOT PROPERLY OPEN', FILE_NAME)
		print('[INFO]', 'PATCH NOT APPLIED TO', filename)
		Failed = True

	if Failed: return patch_stage





	patch_stage += 1 # stage 2
	try:
		PATCH_LINES = []
		with open(filename + ".patch", 'r') as f:
			for line in f:
				PATCH_LINES.append(line)
	except Exception as e:
		PRINT_EXC(e)
		print('[ERROR]', 'PATCH FILE NOT FOUND:', filename + '.patch')
		print('[INFO]', 'PATCH NOT APPLIED TO', filename)
		Failed = True

	if Failed: return patch_stage





	
	patch_stage += 1 # stage 3
	try:
		#PATCH_LINE_IDX = 0
		DIFF_CONTROL = PATCH_LINES[0]
		SPACING_CONTROL = PATCH_LINES[1]
		COMMENTS = PATCH_LINES[2:]
	except Exception as e:
		PRINT_EXC(e)
		print('[ERROR]', 'UNABLE TO PARSE PATCH INSTRUCTIONS FOR', filename + '.patch')
		print('[INFO]', 'PATCH NOT APPLIED TO', filename)
		Failed = True

	if Failed: return patch_stage





	
	patch_stage += 1 # stage 4
	if test_patch: print('\t[DEBUG]', "APPLYING DIFF STRUCTURE")
	try:
		DIFF_APPLIED = APPLY_DIFF(''.join(FILE_LINES), DIFF_CONTROL)
	except Exception as e:
		PRINT_EXC(e)
		print('\t' + ERROR_HEAD + 'ERROR WHILE APPLYING DIFF STRUCTURE FOR', filename)
		print('[INFO]', 'PATCH NOT APPLIED TO', filename)
		Failed = True

	# for debugging patches :)
	if test_patch:
		with open(filename + ".DIFF_APPLIED", 'w', encoding="utf-8") as f:
			for line in DIFF_APPLIED:
				f.write(line)

	if Failed: return patch_stage

	



	patch_stage += 1 # stage 5
	if test_patch: print('\t[DEBUG]', "APPLYING SPACING")
	try:
		SPACING_APPLIED = APPLY_SPACING(DIFF_APPLIED, SPACING_CONTROL)
	except Exception as e:
		PRINT_EXC(e)
		print('\t' + ERROR_HEAD + 'ERROR WHILE APPLYING SPACING STRUCTURE FOR', filename)
		print('[INFO]', 'PATCH NOT APPLIED TO', filename)
		Failed = True

	
	if test_patch and not Failed:
		with open(filename + ".SPACING", 'w', encoding="utf-8") as f:
			for line in '\n'.join(SPACING_APPLIED):
				f.write(line)
	

	if Failed: return patch_stage




	patch_stage += 1 # stage 6
	if test_patch: print('\t[DEBUG]', "APPLYING COMMENTS")
	try:
		COMMENTS_APPLIED = APPLY_COMMENTS(SPACING_APPLIED, COMMENTS)
	except Exception as e:
		PRINT_EXC(e)
		print('\t' + ERROR_HEAD + 'ERROR WHILE APPLYING COMMENTS TO', filename)
		print('[INFO]', 'PATCH NOT APPLIED TO', filename)
		Failed = True

	test_ext = ""
	if test_patch: test_ext = ".TEST"

	if test_patch and not Failed:
		with open(filename + test_ext, 'w', encoding="utf-8") as f:
			for line in COMMENTS_APPLIED:
				f.write(line)

	if Failed: return patch_stage



	return 0	# Patch successful :)




		






def APPLY_PATCHES(test_patches=False):

	for FILE_TYPE, OUT_FILE, CHUNKS in FILE_DATA:
		if FILE_TYPE in {FILE_ASM, FILE_SSF}:
			try:
				status = APPLY_PATCH(OUT_FILE, test_patch=test_patches)

				if status == 0: print('[INFO] SUCCESSFULLY PATCHED', OUT_FILE)
			except Exception as e:
				PRINT_EXC(e)
				print('\t' + ERROR_HEAD + 'UNHANDLED ERROR WHILE APPLYING PATCH TO', filename)
				print('[INFO]', 'PATCH NOT APPLIED TO', filename)

		










if __name__ == "__main__":

	SMK_FILE_NAME = input("Drag Super Mario Kart (USA) File here and press [ENTER]").replace("\"", "").replace("\'", "")

	SPC = EXTRACT_SPC_UPLOAD(SMK_FILE_NAME)

	test_patches = False

	if SPC != None:
		RUN_DISASSEMBLY(SPC, test_patches=test_patches)
		APPLY_PATCHES(test_patches=test_patches)

	






