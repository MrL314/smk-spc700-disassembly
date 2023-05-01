

#DEST_CONSOLE = 0
#DEST_FILE = 1





note_names = ('C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B')


NOTES = {}

for OCT in range(6):
	octave = str(OCT+1)
	for offset in range(12):
		NOTES[0x80 + OCT*12 + offset] = note_names[offset] + octave


INSTR_SET_CMD = "instrument"
PAN_SET_CMD = "pan"
PAN_FADE_CMD = "fade_pan"
VIBRA_SET_CMD = "vibrato"
VIBRA_OFF_CMD = "vibrato_OFF"
MVOL_SET_CMD = "music_volume"
MVOL_FADE_CMD = "fade_music_volume"
TEMPO_SET_CMD = "tempo"
TEMPO_FADE_CMD = "fade_tempo"
GLOBAL_TRANSPOSE_CMD = "transpose_all"
VOICE_TRANSPOSE_CMD = "transpose_voice"
TREMO_SET_CMD = "tremolo"
TREMO_OFF_CMD = "tremolo_OFF"
VVOL_SET_CMD = "voice_volume"
VVOL_FADE_CMD = "fade_voice_volume"
CALL_CMD = "CALL"
VIBRA_FADE_CMD = "fade_vibrato"
BEND_OUT_CMD = "bend_out"
BEND_IN_CMD = "bend_in"
BEND_OFF_CMD = "bend_OFF"
TUNING_CMD = "tune"
ECHO_VOL_CMD = "echo_set"
ECHO_OFF_CMD = "echo_OFF"
ECHO_PARAMS_CMD = "echo_settings"
EVOL_FADE_CMD = "fade_echo"
PORTA_CMD = "portamento"
PERC_BASE_CMD = "set_percussion_base"


ARG_INSTRUMENT = "ARG_instr"
ARG_PERC_INSTRUMENT = "ARG_instr_perc"
ARG_BITFIELD = "ARG_bitfield"
ARG_BYTE = "ARG_byte"
ARG_NOTE = "ARG_note"
ARG_DEC = "ARG_dec"
ARG_DEC_SIGNED = "ARG_dec_s"
ARG_FIR = "ARG_fir"
ARG_VOCFIELD = "ARG_vfield"



VCMDs = {
	0xE0: {
		"CMD": INSTR_SET_CMD,
		"args": [ARG_INSTRUMENT]
	},
	0xE2: {
		"CMD": PAN_FADE_CMD,
		"args": [ARG_DEC, ARG_DEC],
	},
	0xE3: {
		"CMD": VIBRA_SET_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_DEC],
	},
	0xE4: {
		"CMD": VIBRA_OFF_CMD,
		"args": [],
	},
	0xE5: {
		"CMD": MVOL_SET_CMD,
		"args": [ARG_DEC],
	},
	0xE6: {
		"CMD": MVOL_FADE_CMD,
		"args": [ARG_DEC, ARG_DEC],
	},
	0xE7: {
		"CMD": TEMPO_SET_CMD,
		"args": [ARG_DEC],
	},
	0xE8: {
		"CMD": TEMPO_FADE_CMD,
		"args": [ARG_DEC, ARG_DEC],
	},
	0xE9: {
		"CMD": GLOBAL_TRANSPOSE_CMD,
		"args": [ARG_DEC_SIGNED],
	},
	0xEA: {
		"CMD": VOICE_TRANSPOSE_CMD,
		"args": [ARG_DEC_SIGNED],
	},
	0xEB: {
		"CMD": TREMO_SET_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_DEC],
	},
	0xEC: {
		"CMD": TREMO_OFF_CMD,
		"args": [],
	},
	0xED: {
		"CMD": VVOL_SET_CMD,
		"args": [ARG_DEC],
	},
	0xEE: {
		"CMD": VVOL_FADE_CMD,
		"args": [ARG_DEC, ARG_DEC],
	},
	0xF0: {
		"CMD": VIBRA_FADE_CMD,
		"args": [ARG_DEC],
	},
	0xF1: {
		"CMD": BEND_OUT_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_DEC_SIGNED],
	},
	0xF2: {
		"CMD": BEND_IN_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_DEC_SIGNED],
	},
	0xF3: {
		"CMD": BEND_OFF_CMD,
		"args": [],
	},
	0xF4: {
		"CMD": TUNING_CMD,
		"args": [ARG_DEC],
	},
	0xF5: {
		"CMD": ECHO_VOL_CMD,
		"args": [ARG_VOCFIELD, ARG_DEC, ARG_DEC],
	},
	0xF6: {
		"CMD": ECHO_OFF_CMD,
		"args": [],
	},
	0xF7: {
		"CMD": ECHO_PARAMS_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_DEC],
	},
	0xF8: {
		"CMD": EVOL_FADE_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_DEC],
	},
	0xF9: {
		"CMD": PORTA_CMD,
		"args": [ARG_DEC, ARG_DEC, ARG_NOTE],
	},
	0xFA: {
		"CMD": PERC_BASE_CMD,
		"args": [ARG_PERC_INSTRUMENT],
	}
}


INSTRUMENTS = [
	"!srcn_skid",
	"!srcn_splash",
	"!srcn_engine_1",
	"!srcn_engine_2",
	"!srcn_hihat",
	"!srcn_snare",
	"!srcn_kick",
	"!srcn_orch_hit",
	"!srcn_brass",
	"!srcn_clarinet",
	"!srcn_e_guitar",
	"!srcn_piano",
	"!srcn_bass",
	"!srcn_marimba",
	"!srcn_drawbar",
	"!srcn_whistle",
	"!srcn_bongo",
	"!srcn_guitar",
	"!srcn_water",
	"!srcn_gravel",
	"!srcn_organ",
	"!srcn_cowbell",
	"!srcn_timbale",
	"!srcn_engine_3",
	"!srcn_engine_4",
	"!srcn_shrill",
]






IN_SONG_BLOCK = 0
IN_PHRASE_BLOCK = 1
IN_VOICE_BLOCK = 2

class SONG:

	def __init__(self, data_buff=None, start_addr=None, jump_ptrs=None, song_name=None):

		if data_buff == None: data_buff = []
		self.data_buff = data_buff
		self.data_len = len(self.data_buff)
		if start_addr == None: start_addr = 0
		self.start_addr = start_addr
		if song_name == None: song_name = ""
		self.song_name = song_name


		self.block_ptrs = {}
		self.voice_ptrs = {}
		self.routine_ptrs = {}
		if jump_ptrs == None: jump_ptrs = {}
		self.jump_ptrs = jump_ptrs

		self.DISASSEMBLED_TEXT = ""


	def get_byte(self, addr):
		return self.data_buff[addr]

	def get_word(self, addr):
		return self.data_buff[addr] + (self.data_buff[addr+1]<<8)

	def WRITE(self, *args, end="\n", **kwargs):
		#if PRINT_DEST == DEST_CONSOLE:
		#	print(*args, end=end, **kwargs)
		#elif PRINT_DEST == DEST_FILE:
		#	self.OUT_FILE.write(' '.join([x for x in args]))
		#	self.OUT_FILE.write(end)
		#else:
		#	raise KeyError("Unknown print destination: " + str(PRINT_DEST))
		self.DISASSEMBLED_TEXT += ' '.join([x for x in args])
		self.DISASSEMBLED_TEXT += end


	def disassemble_song(self):


		lines = []

		ptr = 0



		block_num = 0
		voice_num = 0
		call_num = 0


		while ptr < self.data_len:

			if ptr == 0:
				if self.song_name == "":
					self.WRITE("SONG:")
				else:
					self.WRITE("SONG_" + self.song_name + ":")

				while ptr < self.data_len:
					if ptr + self.start_addr in self.jump_ptrs:
						self.WRITE(".loop:")

					if ptr + self.start_addr in self.block_ptrs: break
					if ptr + self.start_addr in self.voice_ptrs: break
					if ptr + self.start_addr in self.routine_ptrs: break


					wptr = self.get_word(ptr)
					ptr += 2

					if wptr == 0:
						self.WRITE("\t%stop()")
						break

					loop_amt = -1
					
					if wptr < 0xFF:
						loop_amt = wptr
						wptr = self.get_word(ptr)
						ptr += 2
					elif wptr == 0xFF:
						self.WRITE("\t%jump(.loop)")
						wptr = self.get_word(ptr)
						ptr += 2
						if wptr not in self.jump_ptrs:
							self.jump_ptrs[wptr] = (0, ".loop")
							#break
						continue	# break?


					if wptr not in self.block_ptrs:
						self.block_ptrs[wptr] = (block_num, ".BLOCK_" + str(block_num))
						block_num += 1

					name = self.block_ptrs[wptr][1]

					if loop_amt == -1:
						self.WRITE("\t%play_block(" + name + ")")
					else:
						self.WRITE("\t%play_block(" + name + ", " + str(loop_amt) + ")")




			elif ptr + self.start_addr in self.block_ptrs:
				self.WRITE("")

				self.WRITE(self.block_ptrs[ptr + self.start_addr][1] + ":")
				self.WRITE("\t%p_block(", end="")

				for i in range(8):
					if i != 0:
						self.WRITE(", ", end="")
					wptr = self.get_word(ptr)
					ptr += 2

					if wptr == 0:
						self.WRITE("$0000", end="")
					else:

						if wptr not in self.voice_ptrs:
							self.voice_ptrs[wptr] = (voice_num, ".VOICE_" + str(voice_num))
							voice_num += 1

						self.WRITE(self.voice_ptrs[wptr][1], end="")

				self.WRITE(")")


			elif ptr + self.start_addr in self.voice_ptrs or ptr + self.start_addr in self.routine_ptrs:
				#break

				IN_ROUTINE = ((ptr + self.start_addr) in self.routine_ptrs)

				self.WRITE("")

				if not IN_ROUTINE:
					self.WRITE(self.voice_ptrs[ptr + self.start_addr][1] + ":")
				else:
					self.WRITE(self.routine_ptrs[ptr + self.start_addr][1] + ":")

				self.WRITE("\t%CLR_DSV()")

				
				while ptr < self.data_len:

					op = self.get_byte(ptr)
					ptr += 1

					if op == 0:
						if IN_ROUTINE:
							self.WRITE("\t%RETURN()")
						else:
							self.WRITE("\t%END()")

					elif op < 0x80:
						duration = op

						if self.get_byte(ptr) < 0x80:
							sv = self.get_byte(ptr)
							ptr += 1
							sustain = (sv & 0x70) >> 4
							velocity = (sv & 0xF)
							self.WRITE("\t%set_note_params(" + str(duration) + ", " + str(sustain) + ", " + str(velocity) + ")")
						else:
							self.WRITE("\t%set_note_params(" + str(duration) + ")")

					elif op < 0xC8:    # Note
						self.WRITE("\t%play(" + NOTES[op] + ")")

					elif op == 0xC8:   # Tie
						self.WRITE("\t%tie()")

					elif op == 0xC9:   # Rest
						self.WRITE("\t%rest()")

					elif op < 0xE0:    # percussion note
						self.WRITE("\t%percussion(P" + str(op - 0xCA) + ")")

					elif op == 0xE1:   # pan
						pan = self.get_word(ptr)
						ptr += 1

						phaserev = (pan&0b11000000)>>6
						if phaserev == 0:
							self.WRITE("\t%pan(" + str(pan & 0b00111111) + ")")
						else:
							self.WRITE("\t%pan(" + str(pan & 0b00111111) + ", PHASEREV(", end="")
							if phaserev & 1 != 0: self.WRITE("!ON", end=",")
							else: self.WRITE("!OFF", end=",")
							if phaserev & 2 != 0: self.WRITE("!ON", end=")")
							else: self.WRITE("!OFF", end=")")
							self.WRITE(")")


					elif op == 0xEF:	# Call
						call_addr = self.get_word(ptr)
						ptr += 2
						call_amt = self.get_byte(ptr)
						ptr += 1

						if call_addr not in self.routine_ptrs:
							if call_addr in self.voice_ptrs:
								self.routine_ptrs[call_addr] = (call_num, self.voice_ptrs[call_addr][1])
							else:
								self.routine_ptrs[call_addr] = (call_num, ".SUBRT_" + str(call_num))
							call_num += 1

						if call_amt != 0:
							self.WRITE("\t%CALL(" + self.routine_ptrs[call_addr][1] + ", " + str(call_amt+1) + ")")
						else:
							self.WRITE("\t%CALL(" + self.routine_ptrs[call_addr][1] + ")")

					elif op >= 0xFB:
						self.WRITE("\tdb\t$" + format(op, "02x") + "\t;INVALID NSPC BYTE")

					else:
						vcmd = VCMDs[op]

						self.WRITE("\t%" + vcmd["CMD"] + "(", end="")

						for arg in range(len(vcmd['args'])):
							val = self.get_byte(ptr)
							ptr += 1

							if arg != 0: self.WRITE(", ", end="")

							argtype = vcmd['args'][arg]

							if argtype == ARG_INSTRUMENT:
								try:
									v = INSTRUMENTS[val]
									self.WRITE(v, end="")
								except Exception:
									self.WRITE("$" + format(val, "02x"), end="")
							elif argtype == ARG_PERC_INSTRUMENT:
								try:
									v = INSTRUMENTS[val-1]
									self.WRITE(v + "+1", end="")
								except Exception:
									self.WRITE("$" + format(val, "02x"), end="")
							elif argtype == ARG_BITFIELD:
								self.WRITE("%" + format(val, "08b"), end="")
							elif argtype == ARG_BYTE:
								self.WRITE("$" + format(val, "02x"), end="")
							elif argtype == ARG_NOTE:
								self.WRITE(NOTES[val], end="")
							elif argtype == ARG_DEC:
								self.WRITE(str(val), end="")
							elif argtype == ARG_DEC_SIGNED:
								if val > 0x7F: val -= 0x100
								self.WRITE(str(val), end="")
							elif argtype == ARG_FIR:
								self.WRITE("FIR(" + str(val) + ")", end="")
							elif argtype == ARG_VOCFIELD:
								self.WRITE("EN(", end="")
								for i in range(8):
									if i != 0: self.WRITE(",", end="")
									if val & 1 == 0:
										self.WRITE("!OFF", end="")
									else:
										self.WRITE("!ON", end="")
									val >>= 1
								self.WRITE(")", end="")
							else:
								self.WRITE("[ARGTYPE " + argtype + " " + format(val, "02x") + "]", end="")


						self.WRITE(")")





					if (ptr + self.start_addr) in self.block_ptrs: break
					if (ptr + self.start_addr) in self.voice_ptrs: break
					if (ptr + self.start_addr) in self.routine_ptrs: break
				




			else:
				self.WRITE("db\t$" + format(self.get_byte(ptr)) + "\t\t; UNKNOWN @ " + format(ptr + self.start_addr, "04X"))
				ptr += 1

		'''
		if PRINT_DEST == DEST_CONSOLE:
			print("\n\n\n\n\n==================================\n\n")

		print("self.block_ptrs = {")
		for p in self.block_ptrs:
			print("\t0x" + format(p, "04X") + ":", self.block_ptrs[p], end=",\n")
		print("}")

		print("self.voice_ptrs = {")
		for p in self.voice_ptrs:
			print("\t0x" + format(p, "04X") + ":", self.voice_ptrs[p], end=",\n")
		print("}")

		print("self.routine_ptrs = {")
		for p in self.routine_ptrs:
			print("\t0x" + format(p, "04X") + ":", self.routine_ptrs[p], end=",\n")
		print("}")

		print("self.jump_ptrs = {")
		for p in self.jump_ptrs:
			print("\t0x" + format(p, "04X") + ":", self.jump_ptrs[p], end=",\n")
		print("}")
		'''

		return self.DISASSEMBLED_TEXT












if __name__ == "__main__":

	sng_name = "spooky"
	sng_offs = 0xD000

	#OUT_FILE = open(sng_name + '.ssf', 'w')

	data = []
	with open(sng_name + ".bin", 'rb') as f:
		data = f.read()



	# ONLY IF HAS HEADER AND FOOTER!!!
	#data = data[4:-4]




	dsong = SONG(data, 0xD000, {}, "")

	dsong.disassemble_song()


	#OUT_FILE.close()
