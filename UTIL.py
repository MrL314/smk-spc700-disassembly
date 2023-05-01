




DEBUG_MODE = False



def print_debug(*args, end="\n", **kwargs):

	if DEBUG_MODE:
		print(*args, end=end, **kwargs)


class ARAM:

	def __init__(self):
		self._ARAM = bytearray(0x10000)


	def clear(self):
		self._ARAM = bytearray(0x10000)


	def upload_file(self, file):

		print_debug("[INFO] ATTEMPTING TO UPLOAD FILE: " + str(file))

		d = []

		with open(file, 'rb') as f:
			d = f.read()

		self.upload_spc(d)



	def upload_spc(self, data):
		L = len(data)
		p = 0

		print_debug("[INFO] BEGIN SPC BLOCK UPLOAD")

		while p < L:

			BLOCK_LEN = data[p+0] | (data[p+1] << 8)
			BLOCK_ADDR = data[p+2] | (data[p+3] << 8)
			p += 4

			if BLOCK_LEN == 0: 
				print_debug("[" + format(p, "04X") + "] END SPC UPLOAD BLOCK, EXECUTE @ $" + format(BLOCK_ADDR, "04X"))
				break

			print_debug("[" + format(p, "04X") + "] UPLOAD " + format(BLOCK_LEN, "04X") + "h bytes to $" + format(BLOCK_ADDR, "04X"))
			self.write(BLOCK_ADDR, data[p:p+BLOCK_LEN], BLOCK_LEN)
			p += BLOCK_LEN



	def write(self, addr, data, data_len=None):
		if data_len == None: data_len = len(data)
		self._ARAM[addr:addr+data_len] = data


	def read(self, addr, n):
		return self._ARAM[addr:addr+n]

	def read_byte(self, addr):
		return self._ARAM[addr]

	def read_word(self, addr):
		return self._ARAM[addr] | (self._ARAM[addr+1] << 8)


	def DEBUG_READ(self, addr, n=1):
		return "[$" + format(addr, "04x") + "," + str(n) + "] " + ' '.join([format(x, "02X") for x in self.read(addr, n)])






def APPLY_DIFF(raw_text, DIFF_TEXT):


	lookup_dictionary = ""


	diff_type = DIFF_TEXT[0]


	#return DIFF_APPLY



	REMOVES = []
	INSERTS = []



	DIFF_TEXT = DIFF_TEXT.rstrip().replace("\x03", "\n").replace("\x04", "\t")

	diff_idx = 0
	diff_chunks = DIFF_TEXT.split('\x02')
	diff_len = len(diff_chunks)

	raw_text = [c for c in raw_text]


	LAST_REM_IDX = 0
	LAST_ADD_IDX = 0


	prev_lookup_offset = 0

	while diff_idx < diff_len:
		chunk = diff_chunks[diff_idx]

		if chunk[0] == 'r':
			try: rem_len = int(chunk[1:])
			except Exception: rem_len = 1
			rem_idx = int(diff_chunks[diff_idx + 1])

			REMOVES.append((rem_len, rem_idx - 1 + LAST_REM_IDX))

			LAST_REM_IDX += rem_idx

			#for _ in range(rem_len):
			#	del raw_text[rem_idx]

			diff_idx += 2

		elif chunk[0] == "i":

			try: add_len = int(chunk[1:])
			except Exception: add_len = 1
			add_idx = int(diff_chunks[diff_idx + 1])
			add_txt = diff_chunks[diff_idx + 2]

			INSERTS.append((add_len, add_idx + LAST_ADD_IDX, add_txt))

			LAST_ADD_IDX += add_idx

			lookup_dictionary += add_txt

			#for c in reversed(add_txt):
			#	raw_text.insert(add_idx, c)

			diff_idx += 3

		elif chunk[0] == 's':

			try: add_len = int(chunk[1:])
			except Exception: add_len = 1
			add_idx = int(diff_chunks[diff_idx + 1])

			INSERTS.append((add_len, add_idx + LAST_ADD_IDX, ' '*add_len))

			LAST_ADD_IDX += add_idx

			diff_idx += 2

		elif chunk[0] == 't':

			try: add_len = int(chunk[1:])
			except Exception: add_len = 1
			add_idx = int(diff_chunks[diff_idx + 1])

			INSERTS.append((add_len, add_idx + LAST_ADD_IDX, '\t'*add_len))

			LAST_ADD_IDX += add_idx

			diff_idx += 2

		elif chunk[0] == 'n':

			try: add_len = int(chunk[1:])
			except Exception: add_len = 1
			add_idx = int(diff_chunks[diff_idx + 1])

			INSERTS.append((add_len, add_idx + LAST_ADD_IDX, '\n'*add_len))

			LAST_ADD_IDX += add_idx

			diff_idx += 2

		elif chunk[0] == 'c':

			try: add_len = int(chunk[1:])
			except Exception: add_len = 1
			add_idx = int(diff_chunks[diff_idx + 1])

			INSERTS.append((add_len, add_idx + LAST_ADD_IDX, ','*add_len))

			LAST_ADD_IDX += add_idx

			diff_idx += 2

		elif chunk[0] == 'd':

			try: add_len = int(chunk[1:])
			except Exception: add_len = 1
			add_idx = int(diff_chunks[diff_idx + 1])
			lookup_offset = int(diff_chunks[diff_idx + 2])
			txt = lookup_dictionary[lookup_offset:lookup_offset+add_len]

			lookup_dictionary += txt

			INSERTS.append((add_len, add_idx + LAST_ADD_IDX, txt))

			LAST_ADD_IDX += add_idx

			diff_idx += 3





		else:
			print("HUH")
			diff_idx += 1

	for LEN, IDX in reversed(REMOVES):
		for _ in range(LEN):
			del raw_text[IDX]


	for LEN, IDX, TXT in INSERTS:
		#print("INSERTING", TXT, "AT IDX", IDX)
		for c in reversed(TXT):
			raw_text.insert(IDX, c)
		#pass

	return ''.join(raw_text)






'''
def CREATE_UNIFIED_RAW_DIFF(TXT_A, TXT_B):


	pass




def CREATE_UNIFIED_INLINE_DIFF(TXT_A, TXT_B):


	pass



'''


def DIFF_SMART_UNIFIED_LINE(TXT_A, TXT_B):

	from difflib import unified_diff

	from ENCODER import DISASSEMBLY_ENCODER

	NUM_LINES_A = len(TXT_A)
	NUM_LINES_B = len(TXT_B)


	# parse by label first

	ENC_A = DISASSEMBLY_ENCODER("")
	ENC_B = DISASSEMBLY_ENCODER("")

	ENC_A.set_raw_lines(TXT_A)
	ENC_B.set_raw_lines(TXT_B)

	# gather all labels
	LABELS_A = [line.lstrip().rstrip() for line in ENC_A.ENCODE_LABELS()]
	LABELS_B = [line.lstrip().rstrip() for line in ENC_B.ENCODE_LABELS()]


	# keep track of which line each label came from
	LABELS_TO_LINES_A = []
	LABELS_TO_LINES_B = []


	LABEL_A_IDX = 0
	LINE_A = 0

	RAW_A_ENC = DISASSEMBLY_ENCODER("")

	for label in LABELS_A:
		found = False
		while LINE_A < NUM_LINES_A:
			lines = []
			i = 0
			while '\\' in TXT_A[LINE_A + i]: 
				lines.append(TXT_A[LINE_A + i])
				i += 1
			lines.append(TXT_A[LINE_A + i])

			RAW_A_ENC.set_raw_lines(lines)
			encoded_line = RAW_A_ENC.ENCODE_LABELS()

			if encoded_line == []:
				LINE_A += len(lines)
				continue

			if encoded_line[0].lstrip().rstrip() == label:
				found = True
				break

			LINE_A += len(lines)

		if not found:
			raise KeyError('[ERROR] COULD NOT SUITABLY FIND LABEL ' + label + ' AT LABEL INDEX ' + str(LABEL_A_IDX) + ' IN FILE LABELS A :(')

		LABELS_TO_LINES_A.append(LINE_A)

		LINE_A += 1
		LABEL_A_IDX += 1



	LABEL_B_IDX = 0
	LINE_B = 0

	RAW_B_ENC = DISASSEMBLY_ENCODER("")

	for label in LABELS_B:
		found = False
		while LINE_B < NUM_LINES_B:
			lines = []
			i = 0
			while '\\' in TXT_B[LINE_B + i]: 
				lines.append(TXT_B[LINE_B + i])
				i += 1
			lines.append(TXT_B[LINE_B + i])

			RAW_B_ENC.set_raw_lines(lines)
			encoded_line = RAW_B_ENC.ENCODE_LABELS()

			if encoded_line == []:
				LINE_B += len(lines)
				continue

			if encoded_line[0].lstrip().rstrip() == label:
				found = True
				break

			LINE_B += len(lines)

		if not found:
			raise KeyError('[ERROR] COULD NOT SUITABLY FIND LABEL ' + label + ' AT LABEL INDEX ' + str(LABEL_B_IDX) + ' IN FILE LABELS B :(')

		LABELS_TO_LINES_B.append(LINE_B)

		LINE_B += 1
		LABEL_B_IDX += 1


	#for i in range(len(LABELS_A)):
	#	print(str(LABELS_TO_LINES_A[i] + 1).ljust(4) + " " + LABELS_A[i])

	#for i in range(len(LABELS_B)):
	#	print(str(LABELS_TO_LINES_B[i] + 1).ljust(4) + " " + LABELS_B[i])


	LBL_dff = unified_diff(LABELS_A, LABELS_B, n=0)

	#DEBUG_LOG = open("DEBUG_LOG.diff", 'w', encoding='utf-8')

	def DEBUG(*args, end='\n', **kwargs):
		#DEBUG_LOG.write(' '.join([x for x in args]) + end)
		pass


	REM_LIST_A = []
	REM_LIST_B = []

	for line in LBL_dff:
		if line == "--- \n": continue
		if line == "+++ \n": continue
		#DEBUG(line.replace('\n', '▼'))

		if line[0] == "@":
			_,rem,add,_ = line.split()

			rem_sp = rem.split(",")
			add_sp = add.split(",")
			rem_cnt = 1
			add_cnt = 1
			if len(rem_sp) > 1: rem_cnt = int(rem_sp[1])
			if len(add_sp) > 1: add_cnt = int(add_sp[1])
			rem_idx = int(rem_sp[0][1:]) - 1
			add_idx = int(add_sp[0][1:]) - 1

			if rem_cnt != 0: REM_LIST_A.append((rem_idx, rem_cnt))
			if add_cnt != 0: REM_LIST_B.append((add_idx, add_cnt))

	
	for idx, cnt in reversed(REM_LIST_A):
		for _ in range(cnt):
			del LABELS_TO_LINES_A[idx]
			del LABELS_A[idx]

	for idx, cnt in reversed(REM_LIST_B):
		for _ in range(cnt):
			del LABELS_TO_LINES_B[idx]
			del LABELS_B[idx]
	

	'''
	for idx, cnt in reversed(REM_LIST_B):
		for _ in range(cnt):
			del LABELS_TO_LINES_A[idx]
			del LABELS_A[idx]

	for idx, cnt in reversed(REM_LIST_A):
		for _ in range(cnt):
			del LABELS_TO_LINES_B[idx]
			del LABELS_B[idx]
	'''

	LABELS_TO_LINES_A.append(NUM_LINES_A)
	LABELS_TO_LINES_B.append(NUM_LINES_B)

	if LABELS_TO_LINES_A[0] != 0 or LABELS_TO_LINES_B[0] != 0:
		LABELS_TO_LINES_A.insert(0, 0)
		LABELS_TO_LINES_B.insert(0, 0)



	# now parse diff by label chunk!

	DIFF_LINES = []

	for chunk_num in range(len(LABELS_TO_LINES_A) - 1):
		START_A = LABELS_TO_LINES_A[chunk_num+0]
		END_A = LABELS_TO_LINES_A[chunk_num+1]
		START_B = LABELS_TO_LINES_B[chunk_num+0]
		END_B = LABELS_TO_LINES_B[chunk_num+1]

		CHUNK_DIFF = unified_diff(TXT_A[START_A:END_A], TXT_B[START_B:END_B], n=0)


		for line in CHUNK_DIFF:
			if line == "--- \n": continue
			if line == "+++ \n": continue

			if line[0] == "@":
				#if line[-1] == "\n": line = line[:-1]

				_,rem,add,_ = line.split()

				rem_sp = rem.split(",")
				add_sp = add.split(",")
				rem_cnt = 1
				add_cnt = 1
				if len(rem_sp) > 1: rem_cnt = int(rem_sp[1])
				if len(add_sp) > 1: add_cnt = int(add_sp[1])
				rem_idx = int(rem_sp[0][1:]) + START_A
				add_idx = int(add_sp[0][1:]) + START_B

				real_instr = "@@"
				real_instr += " -" + str(rem_idx)
				if rem_cnt != 1: real_instr += "," + str(rem_cnt)
				real_instr += " +" + str(add_idx)
				if add_cnt != 1: real_instr += "," + str(add_cnt)
				real_instr += " @@"
				DIFF_LINES.append(real_instr)
				DEBUG(real_instr)

			elif line[0] == "-":
				DIFF_LINES.append(line)
				DEBUG(line.replace('\n', '▼'))

			elif line[0] == "+":
				DIFF_LINES.append(line)
				DEBUG(line.replace('\n', '▼'))


	#DEBUG_LOG.close()

	return DIFF_LINES






JUNK_CHARS = {'\n', '\t', ' ', '$', '#', ':', '%', '!', '(', ')', '[', ']', '{', '}'}

def GET_JUNK(s):
	if s in JUNK_CHARS: return True
	return False

def DIFF_CHAR_SMART(TXT_A, TXT_B):

	from difflib import SequenceMatcher

	MATCHER = SequenceMatcher(isjunk=GET_JUNK, a=''.join(TXT_A), b=''.join(TXT_B))


	DIFF_LINES = []

	A_OFF = 0
	B_OFF = 0

	for TAG, r0, r1, a0, a1 in MATCHER.get_opcodes():

		if TAG == 'equal': continue

		rem_idx = r0
		rem_cnt = r1 - r0
		add_idx = a0
		add_cnt = a1 - a0

		diff_instr = "@@"
		diff_instr += " -" + str(rem_idx + 1)
		if rem_cnt != 1: diff_instr += "," + str(rem_cnt)
		diff_instr += " +" + str(add_idx + 1)
		if add_cnt != 1: diff_instr += "," + str(add_cnt)
		diff_instr += " @@"
		DIFF_LINES.append(diff_instr)


		if rem_cnt != 0:
			for i in range(r0, r1):
				DIFF_LINES.append("-" + TXT_A[i])

		if add_cnt != 0:
			for i in range(a0, a1):
				DIFF_LINES.append("+" + TXT_B[i])


	return DIFF_LINES









wschars = {' ', '\t', '\n', ',', '(', ')'}


def generate_compressed_insertion_sequence(txt, start_offset, dictionary):

	SPCHR = '\x02'

	#from difflib import SequenceMatcher

	#print("INPUT DIFFERENCE:", txt.replace("\n", '▼'))


	insertion_sequence = ""
	current_chunk = ""
	chunk_addr = 0

	quick_ws = True

	txt_idx = 0
	L = len(txt)
	while txt_idx < L:
		if current_chunk != "": quick_ws = False

		if txt[txt_idx] == ' ':
			spc_cnt = 1
			end = 1
			while end < L - txt_idx and txt[txt_idx + end] == ' ':
				spc_cnt += 1
				end += 1

			if quick_ws or (current_chunk == "" and end > 1): 
				num_char = str(end)
				if end == 1: num_char = ""
				insertion_sequence += "s" + num_char + SPCHR + str(start_offset + txt_idx) + SPCHR
				chunk_addr = txt_idx + end
			else:	current_chunk += ' '*end
			txt_idx += end
			continue

		if txt[txt_idx] == '\t':
			spc_cnt = 1
			end = 1
			while end < L - txt_idx and txt[txt_idx + end] == '\t':
				spc_cnt += 1
				end += 1
			if quick_ws or (current_chunk == "" and end > 1): 
				num_char = str(end)
				if end == 1: num_char = ""
				insertion_sequence += "t" + num_char + SPCHR + str(start_offset + txt_idx) + SPCHR
				chunk_addr = txt_idx + end
			else:	current_chunk += '\t'*end
			txt_idx += end
			continue

		if txt[txt_idx] == '\n':
			spc_cnt = 1
			end = 1
			while end < L - txt_idx and txt[txt_idx + end] == '\n':
				spc_cnt += 1
				end += 1
			if quick_ws or (current_chunk == "" and end > 1): 
				num_char = str(end)
				if end == 1: num_char = ""
				insertion_sequence += "n" + num_char + SPCHR + str(start_offset + txt_idx) + SPCHR
				chunk_addr = txt_idx + end
			else:	current_chunk += '\n'*end
			txt_idx += end
			continue

		if txt[txt_idx] == ',':
			spc_cnt = 1
			end = 1
			while end < L - txt_idx and txt[txt_idx + end] == ',':
				spc_cnt += 1
				end += 1
			if quick_ws or (current_chunk == "" and end > 1): 
				num_char = str(end)
				if end == 1: num_char = ""
				insertion_sequence += "c" + num_char + SPCHR + str(start_offset + txt_idx) + SPCHR
				chunk_addr = txt_idx + end
			else:	current_chunk += ','*end
			txt_idx += end
			continue

		quick_ws = False

		# check max callback status
		temp_dict = dictionary + current_chunk
		end = 0
		junk_stop = False
		longest_match = 0
		dict_offset = 0
		prev_longest = 0
		p_dict_offset = 0
		while end < L - txt_idx + 1:
			# stop on junk characters

			dict_offset = temp_dict.find(txt[txt_idx:txt_idx+end])

			if dict_offset != -1:
				p_dict_offset = dict_offset
				longest_match = end
			else:
				#longest_match = prev_longest
				dict_offset = p_dict_offset
				break

			end += 1



		use_lookup = False


		if longest_match > 3: 
			end = longest_match
			use_lookup = True
			#print("longest match:", longest_match, ' - ', txt[txt_idx:txt_idx+end])
		

		if use_lookup:	
			if current_chunk != "":
				num_char = str(len(current_chunk))
				if len(current_chunk) == 1: num_char = ""
				insertion_sequence += "i" + num_char + SPCHR + str(start_offset + chunk_addr) + SPCHR + current_chunk + SPCHR

				dictionary += current_chunk
				current_chunk = ""

			num_char = str(end)
			if end == 1: num_char = ""
			insertion_sequence += "d" + num_char + SPCHR + str(start_offset + txt_idx) + SPCHR + str(dict_offset) + SPCHR

			dictionary += txt[txt_idx:txt_idx+end]
			txt_idx += end
			chunk_addr = txt_idx

		else:
			#current_chunk += txt[txt_idx:txt_idx+end]
			#txt_idx += end
			current_chunk += txt[txt_idx]
			txt_idx += 1

		

					

	if current_chunk != "":
		num_char = str(len(current_chunk))
		if len(current_chunk) == 1: num_char = ""
		insertion_sequence += "i" + num_char + SPCHR + str(start_offset + chunk_addr) + SPCHR + current_chunk + SPCHR
		dictionary += current_chunk

	#print("INSERTION SEQUENCE:", insertion_sequence.replace('\n', '▼').replace(SPCHR, ' '))
	#print("DICTIONARY:", dictionary.replace('\n', '▼').replace('\t', '\\t'))

	return (insertion_sequence, dictionary)
















def DIFF_UNIFIED_LINE(TXT_A, TXT_B):

	from difflib import unified_diff


	DIFF = unified_diff(TXT_A, TXT_B, n=0)

	OUT_DIFF_LINES = []

	for line in DIFF:
		if line == "--- \n": continue
		elif line == "+++ \n": continue

		if line[0] == "@":
			if line[-1] == "\n": line = line[:-1]
			OUT_DIFF_LINES.append(line)

		elif line[0] == "-":
			OUT_DIFF_LINES.append(line)

		elif line[0] == "+":
			OUT_DIFF_LINES.append(line)

	return OUT_DIFF_LINES




def LINE_BASED_DIFF(TXT_A, TXT_B, DIFF_ALG):

	DEBUG_LOG = open("DEBUG_LOG.diff", 'w', encoding='utf-8')

	def DEBUG(*args, end='\n', **kwargs):
		DEBUG_LOG.write(' '.join([x for x in args]) + end)
		pass


	LINE_OFFSETS_A = []
	LINE_OFFSETS_B = []

	offset_A = 0
	for line in TXT_A:
		LINE_OFFSETS_A.append(offset_A)
		offset_A += len(line)
	LINE_OFFSETS_A.append(offset_A)

	offset_B = 0
	for line in TXT_B:
		LINE_OFFSETS_B.append(offset_B)
		offset_B += len(line)# - 1
	LINE_OFFSETS_B.append(offset_B)


	LINE_A_OFFSET = 0
	LINE_B_OFFSET = 0


	DIFF = DIFF_ALG(TXT_A, TXT_B) + ["#"]

	prev_sym = ""
	rem_changes = ""
	add_changes = ""
	rem_idx = 0
	add_idx = 0
	P_NEW_LINE = True

	SPCHR = '\x02'
	DIFF_TEXT = ""

	DICTIONARY = ""


	for line in DIFF:

		#parse_block = False

		if line[0] == "-":
			rem_changes += line[1:]
			if not P_NEW_LINE: DEBUG('', end='\n')
			if line[-1] == "\n": P_NEW_LINE = True
			else: P_NEW_LINE = False
			DEBUG(line.replace("\n", "▼\n"), end='')
			prev_sym = "-"

		elif line[0] == "+":
			add_changes += line[1:]
			if not P_NEW_LINE: DEBUG('', end='\n')
			if line[-1] == "\n": P_NEW_LINE = True
			else: P_NEW_LINE = False
			DEBUG(line.replace("\n", "▼\n"), end='')
			prev_sym = "+"


		elif line[0] == "@" or line[0] == "#":
			# block write :)

			if rem_changes != "" and add_changes != "":
				if not P_NEW_LINE: DEBUG('', end='\n')
				real_instr = "; @@"
				real_instr += " -" + str(rem_idx)
				if len(rem_changes) != 1: real_instr += "," + str(len(rem_changes))
				real_instr += " +" + str(add_idx + 1)
				if len(add_changes) != 1: real_instr += "," + str(len(add_changes))
				real_instr += " @@"
				DEBUG(real_instr, end='\n')
				P_NEW_LINE = True

			if rem_changes != "":
				num_char = str(len(rem_changes))
				if len(rem_changes) == 1: num_char = ""
				DIFF_TEXT += "r" + num_char + SPCHR + str(rem_idx) + SPCHR
			if add_changes != "":
				#DIFF_TEXT += "i" + str(len(add_changes)) + SPCHR + str(add_idx) + SPCHR + add_changes + SPCHR
				new_text, DICTIONARY = generate_compressed_insertion_sequence(add_changes, add_idx, DICTIONARY)
				DIFF_TEXT += new_text



			if line[0] == "@":

				_,rem,add,_ = line.split()

				rem_sp = rem.split(",")
				add_sp = add.split(",")
				rem_cnt = 1
				add_cnt = 1
				if len(rem_sp) > 1: rem_cnt = int(rem_sp[1])
				if len(add_sp) > 1: add_cnt = int(add_sp[1])
				rem_idx = int(rem_sp[0][1:])
				add_idx = int(add_sp[0][1:])# - 1

				if rem_idx == 0: rem_idx = 1	# to fix "start of file" additions :p

				LINE_A_OFFSET = LINE_OFFSETS_A[rem_idx-1]
				LINE_B_OFFSET = LINE_OFFSETS_B[add_idx-1]

				rem_idx = LINE_A_OFFSET
				add_idx = LINE_B_OFFSET# - 1





				if not P_NEW_LINE: DEBUG('', end='\n')
				DEBUG("; - - - - - - - - - - - -")
				DEBUG(line)
				DEBUG("; - - - - - - - - - - - -")
				P_NEW_LINE = True


			rem_changes = ""
			add_changes = ""
			prev_sym = line[0]


	if DIFF_TEXT != "" and DIFF_TEXT[-1] == SPCHR: DIFF_TEXT = DIFF_TEXT[:-1]

	DEBUG_LOG.close()

	return DIFF_TEXT.replace("\n", "\x03").replace("\t", "\x04")





def CHAR_BASED_DIFF(TXT_A, TXT_B, DIFF_ALG):

	DEBUG_LOG = open("DEBUG_LOG.diff", 'w', encoding='utf-8')

	def DEBUG(*args, end='\n', **kwargs):
		DEBUG_LOG.write(' '.join([x for x in args]) + end)

	P_NEW_LINE = True

	prev_line_rem = ""
	prev_line_add = ""
	prev_line_sym = "@"
	add_line_idx = 0
	rem_line_idx = 0

	SPCHR = '\x02'
	DIFF_TEXT = ""

	LINE_OFFSETS_A = []
	LINE_OFFSETS_B = []

	offset_A = 0
	for line in TXT_A:
		LINE_OFFSETS_A.append(offset_A)
		offset_A += len(line)
	LINE_OFFSETS_A.append(offset_A)

	offset_B = 0
	for line in TXT_B:
		LINE_OFFSETS_B.append(offset_B)
		offset_B += len(line)# - 1
	LINE_OFFSETS_B.append(offset_B)


	LINE_A_OFFSET = 0
	LINE_B_OFFSET = 0



	DIFF = DIFF_ALG(TXT_A, TXT_B) + ["#"]



	DICTIONARY = ""




	for dline in DIFF:

		if dline[0] == '-':
			#if not P_NEW_LINE: DEBUG('', end='\n')
			#if dline[-1] == '\n': P_NEW_LINE = True
			#else: P_NEW_LINE = False
			#DEBUG(dline.replace('\n', '▼' + '\n'), end='')
			
			prev_line_rem += dline[1:]
			prev_line_sym = '-'


		elif dline[0] == '+':
			#if not P_NEW_LINE: DEBUG('', end='\n')
			#if dline[-1] == '\n': P_NEW_LINE = True
			#else: P_NEW_LINE = False
			#DEBUG(dline.replace('\n', '▼' + '\n'), end='')

			prev_line_add += dline[1:]
			prev_line_sym = '+'


		elif dline[0] == "@" or dline[0] == "#":

			if prev_line_rem != "" or prev_line_add != "": 

				# parse sub diff here!

				#if not P_NEW_LINE: DEBUG('', end='\n')
				#DEBUG("; --------------------------------------\n")
				#P_NEW_LINE = True

				prev_rem = ""
				prev_add = ""
				prev_sym = "@"
				add_idx = 0
				rem_idx = 0

				CDIFF = DIFF_CHAR_SMART([r for r in prev_line_rem], [a for a in prev_line_add]) + ["#"]
				#CDIFF = DIFF_UNIFIED_LINE([r for r in prev_line_rem], [a for a in prev_line_add]) + ["#"]


				for line in CDIFF:


					if line[0] == '-':
						if P_NEW_LINE: DEBUG('-', end='')
						elif prev_sym != '-': DEBUG('\n-', end='')
						if line[-1] == "\n": P_NEW_LINE = True
						else: P_NEW_LINE = False
						DEBUG(line[1:].replace('\n', '▼\n'), end='')
						prev_rem += line[1]
						prev_sym = '-'

					elif line[0] == '+':
						if P_NEW_LINE: DEBUG('+', end='')
						elif prev_sym != '+': DEBUG('\n+', end='')
						if line[-1] == "\n": P_NEW_LINE = True
						else: P_NEW_LINE = False
						DEBUG(line[1:].replace('\n', '▼\n'), end='')
						prev_add += line[1]
						prev_sym = '+'

					elif line[0] == '@' or line[0] == '#':

						if prev_rem != "":
							num_char = str(len(prev_rem))
							if len(prev_rem) == 1: num_char = ""
							DIFF_TEXT += "r" + num_char + SPCHR + str(rem_idx) + SPCHR
						if prev_add != "":
							#DIFF_TEXT += "i" + str(len(prev_add)) + SPCHR + str(add_idx) + SPCHR + prev_add + SPCHR
							new_text, DICTIONARY = generate_compressed_insertion_sequence(prev_add, add_idx, DICTIONARY)
							DIFF_TEXT += new_text

						if line[0] == '#':
							prev_sym = '#'
							prev_rem = ""
							prev_add = ""
							break



						_,rem,add,_ = line.split()

						rem_sp = rem.split(",")
						add_sp = add.split(",")
						rem_cnt = 1
						add_cnt = 1
						if len(rem_sp) > 1: rem_cnt = int(rem_sp[1])
						if len(add_sp) > 1: add_cnt = int(add_sp[1])
						rem_idx = int(rem_sp[0][1:]) + LINE_A_OFFSET
						add_idx = int(add_sp[0][1:]) + LINE_B_OFFSET - 1	# offset by 1, since unified diff is 1-indexed

						if not (rem_cnt == 0 and add_cnt == 0):
							if not P_NEW_LINE: DEBUG('', end='\n')
							DEBUG("; - - - - - - - - - - - -")
							#DEBUG(line.replace('\n', ''))
							real_instr = "@@"
							real_instr += " -" + str(rem_idx)
							if rem_cnt != 1: real_instr += "," + str(rem_cnt)
							real_instr += " +" + str(add_idx)
							if add_cnt != 1: real_instr += "," + str(add_cnt)
							real_instr += " @@"
							#DEBUG("; " + real_instr.replace('\n', ''))
							DEBUG(real_instr)
							DEBUG("; - - - - - - - - - - - -")
							P_NEW_LINE = True

						prev_sym = '@'
						prev_rem = ""
						prev_add = ""




			#if not P_NEW_LINE: DEBUG('', end='\n')
			#DEBUG("; = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")

			if dline[0] == "#":
				prev_line_sym = '#'
				prev_line_rem = ""
				prev_line_add = ""
				break

			# set up next section
			_,rem,add,_ = dline.split()

			rem_sp = rem.split(",")
			add_sp = add.split(",")
			rem_cnt = 1
			add_cnt = 1
			if len(rem_sp) > 1: rem_cnt = int(rem_sp[1])
			if len(add_sp) > 1: add_cnt = int(add_sp[1])
			rem_idx = int(rem_sp[0][1:])
			add_idx = int(add_sp[0][1:])

			if rem_idx == 0: rem_idx = 1	# to fix "start of file" additions :p

			LINE_A_OFFSET = LINE_OFFSETS_A[rem_idx-1]
			LINE_B_OFFSET = LINE_OFFSETS_B[add_idx-1]

			#if not (rem_cnt == 0 and add_cnt == 0):
			#	DEBUG("\n\n\n\n\n\n\n")
			#	DEBUG("; = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
			#	DEBUG(dline.replace('\n', ''))
			#	DEBUG("; " + str(LINE_A_OFFSET) + " " + str(LINE_B_OFFSET))
			#	DEBUG("; = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
			
			#P_NEW_LINE = True

			prev_line_sym = "@"
			prev_line_rem = ""
			prev_line_add = ""












	if DIFF_TEXT != "" and DIFF_TEXT[-1] == SPCHR: DIFF_TEXT = DIFF_TEXT[:-1]

	DEBUG_LOG.close()

	return DIFF_TEXT.replace("\n", "\x03").replace("\t", "\x04")









def CREATE_UNIFIED_LINE_DIFF(TXT_A, TXT_B):
	return LINE_BASED_DIFF(TXT_A, TXT_B, DIFF_UNIFIED_LINE)


def CREATE_SMART_UNIFIED_LINE_DIFF(TXT_A, TXT_B):
	return LINE_BASED_DIFF(TXT_A, TXT_B, DIFF_SMART_UNIFIED_LINE)



def CREATE_UNIFIED_CHAR_SMART_LINE_DIFF(TXT_A, TXT_B):
	return CHAR_BASED_DIFF(TXT_A, TXT_B, DIFF_SMART_UNIFIED_LINE)




DIFF_ALGS = {
	"unified_line": CREATE_UNIFIED_LINE_DIFF,
	"smart_unified_line": CREATE_SMART_UNIFIED_LINE_DIFF,
	"unified_char_smart_line": CREATE_UNIFIED_CHAR_SMART_LINE_DIFF

}









def CREATE_DIFF(TXT_A, TXT_B, diff_type="unified_raw"):

	SPCHR = "\x02"

	TXT_A = [A.replace('\r', '') for A in TXT_A]
	TXT_B = [B.replace('\r', '') for B in TXT_B]

	DIFF_TEXT = DIFF_ALGS[diff_type](TXT_A, TXT_B)

	LAST_REM_IDX = 0
	LAST_ADD_IDX = 0

	DIFF_CHUNKS = DIFF_TEXT.split(SPCHR)
	NUM_CHUNKS = len(DIFF_CHUNKS)

	chunk_idx = 0

	#OUT_CHUNKS = []

	while chunk_idx < NUM_CHUNKS:

		d_type = DIFF_CHUNKS[chunk_idx][0]

		if d_type == "r":
			rem_idx = int(DIFF_CHUNKS[chunk_idx + 1])
			DIFF_CHUNKS[chunk_idx + 1] = str(rem_idx - LAST_REM_IDX)
			LAST_REM_IDX = rem_idx
			chunk_idx += 2

		elif d_type in {'i', 'd'}:
			add_idx = int(DIFF_CHUNKS[chunk_idx + 1])
			DIFF_CHUNKS[chunk_idx + 1] = str(add_idx - LAST_ADD_IDX)
			LAST_ADD_IDX = add_idx
			chunk_idx += 3

		elif d_type in {'s', 't', 'n', 'c'}:
			add_idx = int(DIFF_CHUNKS[chunk_idx + 1])
			DIFF_CHUNKS[chunk_idx + 1] = str(add_idx - LAST_ADD_IDX)
			LAST_ADD_IDX = add_idx
			chunk_idx += 2

		else:
			print('HUH?')
			chunk_idx += 1






	return SPCHR.join(DIFF_CHUNKS)


	





def APPLY_SPACING(raw_text, SP_CTRL):

	if SP_CTRL != "" and SP_CTRL[-1] == '\n': SP_CTRL = SP_CTRL[:-1]

	SP_CONTROLS = []
	L = len(SP_CTRL)
	sp_idx = 0

	spchrs = {'n', 's', 't'}

	while sp_idx < L:
		tag = SP_CTRL[sp_idx]

		sp_idx += 1

		t_size = ""
		end = 0
		while sp_idx + end < L:
			if SP_CTRL[sp_idx + end] in spchrs: break
			t_size += SP_CTRL[sp_idx + end]
			end += 1

		if t_size == "": t_size = "1"
		SP_CONTROLS.append(tag + t_size)

		sp_idx += end





	#SP_CONTROLS = SP_CTRL.split("\x02")

	LINES = [l.replace('\n', "") for l in raw_text.replace('\r', '').split("\n")]

	LINE_NUM = 0

	for CTRL in SP_CONTROLS:

		if CTRL[0] == "t":
			LINES[LINE_NUM] += "\t"*int(CTRL[1:])
		elif CTRL[0] == "s":
			LINES[LINE_NUM] += " "*int(CTRL[1:])
		elif CTRL[0] == "n":
			LINE_NUM += int(CTRL[1:])

	return LINES


def APPLY_COMMENTS(LINES, COMMENTS):

	NO_PRECOMM_DESIGNATOR = '\x05'
	NO_COMMENT_DESIGNATOR = '\x06'
	EMPTY_COMMENT_DESIGNATOR = '\x07'

	LINE_IDX = 0

	for i in range(len(COMMENTS)):

		if COMMENTS[i][0] == NO_PRECOMM_DESIGNATOR:
			NUM_EMPTY = int(COMMENTS[i][1:].rstrip())

			for _ in range(NUM_EMPTY):
				LINES.insert(LINE_IDX, '')


		elif COMMENTS[i][0] == NO_COMMENT_DESIGNATOR:
			NUM_NO_COMMENT = int(COMMENTS[i][1:].rstrip())

			for _ in range(NUM_NO_COMMENT):
				LINES[LINE_IDX] += '\n'
				LINE_IDX += 1


		elif COMMENTS[i][0] == EMPTY_COMMENT_DESIGNATOR:
			NUM_EMPTY_COMMENT = int(COMMENTS[i][1:].rstrip())

			for _ in range(NUM_EMPTY_COMMENT):
				LINES[LINE_IDX] += ';\n'
				LINE_IDX += 1

		else:
			LINES[LINE_IDX] += COMMENTS[i]

			LINE_IDX += 1

	return LINES