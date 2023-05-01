

SUPPRESS_NOT_FOUND_LABEL_WARNING = True



from UTIL import CREATE_DIFF, APPLY_DIFF
from AUDISM import RUN_DISASSEMBLY, APPLY_PATCH,EXTRACT_SPC_UPLOAD

import os

CONTROL_SYMBOLS = {
	'{', '}', '!'
}

CONTROL_TAGS = {
	'if', 'else', 'elseif', 'endif', 'while', 'endwhile'
	'macro', 'endmacro',
	'incsrc', 'incbin',
	'undef',
	'spcblock', 'endspcblock'
	'norom',
	'arch',
	'org',
	'error',
	'warning',
	'print'

}



class DISASSEMBLY_ENCODER:


	def __init__(self, file=""):

		self._file = ""
		self._LABELS = []
		self._RAW_LINES = []

		self._init_file(file)


	def _init_file(self, file):

		if file != "":
			self._file = file
			self._RAW_LINES = []

			with open(file, "r") as f:
				for line in f:
					#self._RAW_LINES.append(line.replace("\n", ""))
					self._RAW_LINES.append(line.replace('\r', ''))


	def set_raw_lines(self, raw_lines):

		self._RAW_LINES = []
		for line in raw_lines:
			self._RAW_LINES.append(line.replace('\r', ''))




	def ENCODE_LABELS(self, file=None, do_nested_incsrc=False):

		RAW_LINES = [x.replace('\n', '') for x in self._RAW_LINES]

		if file != None:
			self._init_file(file)


		TEST_LINES = []

		LINE_NUM = 0
		_NUM_LINES_ = len(RAW_LINES)

		RAWLINE_count = 0

		CURR_SPC_ADDR = -1


		IS_GLOBAL = False
		IN_MULTILINE = False
		IS_CONDENSED_LINE = False

		LABEL_HIERARCHY = ["", "", "", ""]

		while LINE_NUM < _NUM_LINES_:


			if not IN_MULTILINE:
				IS_GLOBAL = False
				IS_CONDENSED_LINE = False

			sp = RAW_LINES[LINE_NUM].split(';')

			comm = ""
			pre_comm = ""
			line_lead_ws = ""

			pre_comm = sp[0]
			if len(sp) > 1:
				comm = ';' + ';'.join(sp[1:])

			NON_COMM = pre_comm.rstrip()
			comm = pre_comm[len(NON_COMM):] + comm

			pre_comm = NON_COMM
			NON_COMM = pre_comm.lstrip()

			line_lead_ws += pre_comm[:-len(NON_COMM)]


			# check if line is a raw line
			is_raw = False
			
			if NON_COMM != "":
				if NON_COMM[0] in CONTROL_SYMBOLS:
					comm = NON_COMM + comm
					NON_COMM = ""
					is_raw = True
				elif NON_COMM.split()[0].lower() in CONTROL_TAGS:
					if do_nested_incsrc and NON_COMM.split()[0].lower() == "incsrc":
						sub_file = self._file.replace("\\", "/").replace("//", "/")
						file_folder = "/".join(sub_file.split("/")[:-1])
						if file_folder != "": file_folder += "/"

						after_incsrc = " ".join(NON_COMM.split()[1:]).replace("\'", "\"")
						if not "\"" in after_incsrc: 
							filename = after_incsrc
						else:
							after_incsrc = after_incsrc[after_incsrc.find("\"")+1:]
							filename = after_incsrc[:after_incsrc.find("\"")]
						
						ENC = DISASSEMBLY_ENCODER(file_folder + filename)
						
						SUB_LINES = ENC.ENCODE_LABELS(do_nested_incsrc=True)
						
						for line in SUB_LINES:
							TEST_LINES.append(line)


					comm = NON_COMM + comm
					NON_COMM = ""
					is_raw = True

			else:
				is_raw = True



			# if line is a raw line, add it to the "raw line" group
			if is_raw:
				comm = line_lead_ws + NON_COMM + comm
				NON_COMM = ""
				line_lead_ws = ""
				RAWLINE_count += 1

				#TEST_LINES.append(self._RAW_LINES[LINE_NUM])
				

				#TEST_LINES.append(comm)


				LINE_NUM += 1
				continue



			# check if line is a global label line
			if NON_COMM != "":
				if NON_COMM.split()[0].lower() == "global":
					IS_GLOBAL = True
					NON_COMM = NON_COMM[6:]
					line_lead_ws += "global"

					pre_comm = NON_COMM
					NON_COMM = pre_comm.lstrip()
					line_lead_ws += pre_comm[:-len(NON_COMM)]



			LINE_LABEL = ""
			LINE_ASM = ""

			is_pos_lbl = False
			is_neg_lbl = False

			# check if line is a label, and parse if so
			if NON_COMM != "":

				if len(NON_COMM) > 0:
					while len(NON_COMM) > 0 and NON_COMM[0] == "-":
						is_neg_lbl = True
						LINE_LABEL += "-"
						NON_COMM = NON_COMM[1:]

				if len(NON_COMM) > 0:
					while len(NON_COMM) > 0 and NON_COMM[0] == "+":
						is_pos_lbl = True
						LINE_LABEL += "+"
						NON_COMM = NON_COMM[1:]

				if is_neg_lbl or is_pos_lbl:
					if len(NON_COMM) > 0:
						if NON_COMM[0] == ":":
							LINE_LABEL += ":"
							NON_COMM = NON_COMM[1:]

					pre_comm = NON_COMM
					LINE_ASM = pre_comm.lstrip()
					LINE_LABEL += pre_comm[:-len(LINE_ASM)]

				else:
					if NON_COMM[0] == ".":
						# sublabel moment
						space_index = NON_COMM.find(" ")
						tab_index = NON_COMM.find("\t")
						if space_index < 0: space_index = tab_index
						elif tab_index >= 0 and tab_index < space_index: space_index = tab_index
						colon_index = NON_COMM.find(":")
						if colon_index >= 0 and colon_index < space_index: space_index = colon_index

						if space_index <= 0: space_index = len(NON_COMM)

						if not (NON_COMM[space_index-1] == " " or NON_COMM[space_index-1] == "\t"):
							LINE_LABEL = NON_COMM[:space_index+1]
							NON_COMM = NON_COMM[space_index+1:]

							pre_comm = NON_COMM
							LINE_ASM = pre_comm.lstrip()
							LINE_LABEL += pre_comm[:-len(LINE_ASM)]
					
					elif ':' in NON_COMM:
						colon_index = NON_COMM.find(":")
						if colon_index <= 0:
							# raise error here because wtf
							pass

						if not (NON_COMM[colon_index-1] == " " or NON_COMM[colon_index-1] == "\t"):
							LINE_LABEL = NON_COMM[:colon_index+1]
							NON_COMM = NON_COMM[colon_index+1:]

							pre_comm = NON_COMM
							LINE_ASM = pre_comm.lstrip()
							LINE_LABEL += pre_comm[:-len(LINE_ASM)]

					else:
						LINE_ASM = NON_COMM




			'''
			# CONVERT TABS TO SPACES (FOR TESTING)
			temp_asm = LINE_ASM
			LINE_ASM = ""
			temp_len = 0
			for c in temp_asm:
				if c != '\t':
					LINE_ASM += c
					temp_len += 1
				else:
					num_spaces = 4 - (temp_len % 4)
					LINE_ASM += " "*num_spaces
					temp_len += num_spaces

			OUT_ASM = ""
			for c in LINE_ASM:
				if c == " ":
					OUT_ASM += " "
				else:
					OUT_ASM += "X"
			# FOR TESTING
			#TEST_LINES.append(line_lead_ws + LINE_LABEL + OUT_ASM + comm)
			TEST_LINES.append(line_lead_ws + LINE_LABEL + OUT_ASM)
			'''

			




			#CLEAN_LINE = ' '.join(self._RAW_LINES[LINE_NUM].split())

			##TEST_LINES.append(' '.join(self._RAW_LINES[LINE_NUM].split()))

			#if NON_COMM == "":
			#	TEST_LINES.append(self._RAW_LINES[LINE_NUM])

			if LINE_LABEL != "":
				TEST_LINES.append(line_lead_ws + LINE_LABEL)

			if LINE_ASM != "":
				while LINE_ASM.rstrip()[-1] == "\\":
					next_line = RAW_LINES[LINE_NUM + 1].lstrip().rstrip()
					if next_line != "":
						next_line = next_line.split(";")[0].rstrip()
					LINE_ASM = LINE_ASM.rstrip()[:-1] + next_line
					LINE_NUM += 1


			LINE_NUM += 1





		return TEST_LINES


	def GET_FORMATTED(self, file=None):

		if file != None:
			self._init_file(file)

		PRE_COMM = []
		COMM = []
		COMM_SPACING_LIST = []

		SPCHR = "\x02"


		PREV_WAS_ASM = False

		NUM_NO_PRECOMM = 0
		NUM_NO_COMMENT = 0
		NUM_EMPTY_COMMENT = 0

		NO_PRECOMM_DESIGNATOR = '\x05'
		NO_COMMENT_DESIGNATOR = '\x06'
		EMPTY_COMMENT_DESIGNATOR = '\x07'


		LAST_NO_PRECOMM_IDX = -1
		

		LINE_NUM = 0
		PREV_LINE = ""

		RAW_LINES = self._RAW_LINES
		if RAW_LINES[-1][-1] == "\n":
			RAW_LINES.append("")
		RAW_LINES.append("▼")

		for line in RAW_LINES:
			LINE_NUM += 1
			line = line.replace('\n', '')

			if ";" in line:
				sp = line.split(";")

				pre_comm = sp[0]
				comm = ";" + ';'.join(sp[1:])
			else:
				pre_comm = line
				comm = ""



			CONTEXT_SWAP = False

			if PREV_WAS_ASM and pre_comm == "": CONTEXT_SWAP = True
			# always swap context on end of file
			if pre_comm == "▼": 

				CONTEXT_SWAP = True	
				#print("NUM_NO_PRECOMM:", NUM_NO_PRECOMM)
				#print("NUM_NO_COMMENT:", NUM_NO_COMMENT)
				#print("NUM_EMPTY_COMMENT:", NUM_EMPTY_COMMENT)
				if NUM_NO_COMMENT == 1:
					COMM.append("")
					NUM_NO_COMMENT -= 1
				elif NUM_NO_COMMENT > 0:
					NUM_NO_COMMENT -= 1



			if CONTEXT_SWAP:
				if NUM_NO_COMMENT != 0:
					COMM.append(NO_COMMENT_DESIGNATOR + str(NUM_NO_COMMENT))
					NUM_NO_COMMENT = 0

				if NUM_EMPTY_COMMENT != 0:
					if NUM_EMPTY_COMMENT == 1:
						COMM.append(';')
					else:
						COMM.append(EMPTY_COMMENT_DESIGNATOR + str(NUM_EMPTY_COMMENT))
					NUM_EMPTY_COMMENT = 0





			if pre_comm == "":
				# no assembly on this line
				if LAST_NO_PRECOMM_IDX == -1:
					LAST_NO_PRECOMM_IDX = len(COMM)
					COMM.append("")

				NUM_NO_PRECOMM += 1
			else:

				if NUM_NO_PRECOMM != 0:
					COMM[LAST_NO_PRECOMM_IDX] = NO_PRECOMM_DESIGNATOR + str(NUM_NO_PRECOMM)
					NUM_NO_PRECOMM = 0

				LAST_NO_PRECOMM_IDX = -1





			raw_comm = True

			

			if comm == "":
				# no comment!
				raw_comm = False
				NUM_NO_COMMENT += 1

			else:
				if NUM_NO_COMMENT != 0:
					COMM.append(NO_COMMENT_DESIGNATOR + str(NUM_NO_COMMENT))
					NUM_NO_COMMENT = 0


			if comm == ";":
				# blank comment!
				raw_comm = False
				NUM_EMPTY_COMMENT += 1
			else:
				if NUM_EMPTY_COMMENT != 0:
					if NUM_EMPTY_COMMENT == 1:
						COMM.append(';')
					else:
						COMM.append(EMPTY_COMMENT_DESIGNATOR + str(NUM_EMPTY_COMMENT))
					NUM_EMPTY_COMMENT = 0







			

			# not an empty line or blank comment now :)

			# end of file, just break
			if pre_comm == "▼": break

			PREV_LINE = line

			# only add comment if it's a non-empty/non-blank comment
			if raw_comm:
				COMM.append(comm)


			# skip adding line to assembly if line is empty
			if pre_comm == "": 
				PREV_WAS_ASM = False
				continue

			PREV_WAS_ASM = True

			end_space = pre_comm
			pre_comm = pre_comm.rstrip()
			PRE_COMM.append(pre_comm)
			end_space = end_space[len(pre_comm):]
			spacing_list = ""

			p_char = "~"	# null non-spacing character :p
			n_tab = 0
			n_space = 0

			while end_space != "":
				c = end_space[0]

				if c != p_char:
					if n_tab != 0:
						spacing_list += "t" + str(n_tab) + SPCHR
						n_tab = 0
					elif n_space != 0:
						spacing_list += "s" + str(n_space) + SPCHR
						n_space = 0

				if c == "\t": 
					n_tab += 1
					end_space = end_space[1:]
				elif c == " ": 
					n_space += 1
					end_space = end_space[1:]
				#else:
				#	print('[ERROR] INVALID CHARACTER:', str(c))
				#	raise ValueError("FUCK")

				p_char = c

			if n_tab != 0:
				spacing_list += "t" + str(n_tab) + SPCHR
				n_tab = 0
			elif n_space != 0:
				spacing_list += "s" + str(n_space) + SPCHR
				n_space = 0

			spacing_list += "n"

			COMM_SPACING_LIST.append(spacing_list)



		return (PRE_COMM, COMM, COMM_SPACING_LIST)










	










def get_label_symbols_initial(filename):
	labels = []

	in_labels = False
	line_num = 0

	with open(filename, 'r') as f:
		for line in f:
			line_num += 1
			line = line.rstrip().split(";")[0].rstrip()
			if line == "": continue

			elif line[0] == "[":
				if line == "[labels]":
					in_labels = True
					continue
				else:
					in_labels = False
					continue

			elif not in_labels:
				continue
			

			# lines should now only be contents of [labels] section

			sp = line.split(" ")
			if len(sp) != 2: 
				print("[WARNING] Unable to parse label line " + str(line_num) + ":\n\t" + str(line))
				continue

			#print("[DEBUG]", line)

			addr = int(sp[0][3:], 16)
			is_global = True
			if ":SPCBLOCK:_" in sp[1]: is_global = False
			if sp[1][:4] == ":pos": is_global = False
			if sp[1][:4] == ":neg": is_global = False

			label = sp[1].rstrip().replace(":SPCBLOCK:_", "")

			labels.append((addr, label, is_global))


	labels.sort(key=lambda a: a[0])

	SORTED_LABELS = []


	P_ADDR = -1

	LABEL_BLOCK = []

	labels.append((-1, "", False))


	for addr, label, is_global in labels:

		if addr != P_ADDR:
			if P_ADDR != -1:
				LABEL_BLOCK.sort(key=lambda a: a[1])

				for i in range(len(LABEL_BLOCK)-1, -1, -1):
					pnchk = LABEL_BLOCK[i][1][:4].lower()
					if pnchk == ":neg" or pnchk == ":pos":
						LABEL_BLOCK.append(LABEL_BLOCK[i])
						del LABEL_BLOCK[i]

				for addr2, label2, is_global2 in LABEL_BLOCK:
					SORTED_LABELS.append((addr2, label2, is_global2))

			LABEL_BLOCK = []

		P_ADDR = addr
		LABEL_BLOCK.append((addr, label, is_global))

	return SORTED_LABELS



def sort_output_labels(labels):

	labels.sort(key=lambda a: a[0])

	SORTED_LABELS = []


	P_ADDR = -1

	LABEL_BLOCK = []

	labels.append((-1, "", False, "", -1))

	for addr, label, is_global, FULL_LABEL, lbl_idx in labels:

		if addr != P_ADDR:
			if P_ADDR != -1:
				LABEL_BLOCK.sort(key=lambda a: a[4])

				for addr2, label2, is_global2, FULL_LABEL2, lbl_idx2 in LABEL_BLOCK:
					SORTED_LABELS.append((addr2, label2, is_global2, FULL_LABEL2))

			LABEL_BLOCK = []

		P_ADDR = addr
		LABEL_BLOCK.append((addr, label, is_global, FULL_LABEL, lbl_idx))

	return SORTED_LABELS






def GENERATE_SYMBOLS_FILE(main_asm_file, in_symbols_file, out_symbols_file="SYMBOLS_MAP.txt"):

	# get labels from symbols file
	INITIAL_LABELS = get_label_symbols_initial(in_symbols_file)

	ARAM_LABEL_ORDER = []

	POS_LBLS = []
	NEG_LBLS = []

	LABEL_OBJS = {}

	LBL_IDX = 0
	for addr, lbl, is_global in INITIAL_LABELS:

		ARAM_LABEL_ORDER.append(lbl)

		LABEL_OBJS[lbl] = {"idx": LBL_IDX, "addr": addr, "is_global": is_global}

		if lbl[:4] == ":pos":
			POS_LBLS.append((lbl, addr))
		elif lbl[:4] == ":neg":
			NEG_LBLS.append((lbl, addr))

		LBL_IDX += 1

	POS_LBLS.sort(key=lambda a: a[1])
	NEG_LBLS.sort(key=lambda a: a[1])






	# parse actual label order from code

	ENC = DISASSEMBLY_ENCODER(main_asm_file)

	TEST_OUT = ENC.ENCODE_LABELS(do_nested_incsrc=True)

	LABEL_IDX = 0

	LABELS_LIST = []

	LABEL_HIERARCHY = ["", "", "", ""]
	CURR_ADDR = 0

	for line in TEST_OUT:

		line = line.lstrip().rstrip()

		if line == "": continue

		if line[-1] == ":": line = line[:-1]

		sp = line.split()

		is_global = False
		if len(sp) > 1:
			if sp[0].lower() == "global":
				is_global = True
				label = sp[1]
			else:
				print("[WARNING] LABEL HAS SPACE :(")
				print(line)
		else:
			label = sp[0]


		#CURRENT_HIERARCHY = "_".join(LABEL_HIERARCHY)


		is_inplace = False
		if label[0] == "#":
			is_inplace = True
			label = label[1:]


		is_pos_neg = False

		# WARNING: THIS WILL BREAK IF THE FIRST EVER LABEL IS A "-" OR "+" LABEL
		if label[0] == "-":
			# handle neg label bleh
			is_pos_neg = True
			for lbl, addr in NEG_LBLS:
				if addr >= CURR_ADDR: 
					label = lbl
					break

		elif label[0] == "+":
			# handle pos label bleh
			is_pos_neg = True
			for lbl, addr in POS_LBLS:
				if addr >= CURR_ADDR: 
					label = lbl
					break


		if is_inplace:
			FULL_LABEL = label
			label = "#" + label
		elif is_pos_neg:
			FULL_LABEL = label

		else:
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

			label = "."*(sub_level) + label


		try:
			LBL_OBJ = LABEL_OBJS[FULL_LABEL]

			addr = LBL_OBJ["addr"]

			LABELS_LIST.append((LBL_OBJ["addr"], label, LBL_OBJ["is_global"], FULL_LABEL, LABEL_IDX))

			#USED_LABELS.append(FULL_LABEL)

			CURR_ADDR = addr

			LABEL_IDX += 1
		except Exception:
			if not SUPPRESS_NOT_FOUND_LABEL_WARNING:
				print("[WARNING] UNABLE TO FIND LABEL:", FULL_LABEL, ". SKIPPING PARSING")


	LABELS_LIST = sort_output_labels(LABELS_LIST)

	with open(out_symbols_file, 'w') as f:
		first = True
		for addr, label, is_global, FULL_LABEL in LABELS_LIST:
			if first: first = False
			else: f.write('\n')
			gchar = "l"
			if is_global: gchar = "g"
			f.write(format(addr, "04X") + " " + gchar + " " + label + " " + FULL_LABEL)






def CREATE_PATCH_FILES(FILE_LIST, test_patches=False):

	from difflib import unified_diff

	SPC = EXTRACT_SPC_UPLOAD("Super Mario Kart (USA).sfc")

	def remove_file(filename):
		try: os.remove(filename)
		except FileNotFoundError: pass

	for filename in FILE_LIST:
		remove_file(filename + ".diff")
		remove_file(filename + ".ADSM")
		remove_file(filename + ".DIFF_APPLIED")
		remove_file(filename + ".SPACING")
		remove_file(filename + ".TEST")


	RUN_DISASSEMBLY(SPC, test_patches=test_patches) # generate raw disassembly to compare against to create patches

	DSM = DISASSEMBLY_ENCODER()

	SOURCE_BUILD_FOLDER = "../"


	for filename in FILE_LIST:
		print('[INFO]', "CREATING PATCH FILE FOR", filename)

		raw, comm, spacing = DSM.GET_FORMATTED(SOURCE_BUILD_FOLDER + filename)


		LINES_A = []
		FILE_NAME = filename
		if test_patches: FILE_NAME += ".ADSM"
		with open(FILE_NAME, 'r') as f:
			for line in f:
				LINES_A.append(line.replace('\r', ''))

		if LINES_A[-1] == "": LINES_A[-1] += "\n"
		elif LINES_A[-1][-1] != "\n": LINES_A[-1] += "\n"

		LINES_B = []
		for r in raw:
			LINES_B.append(r + "\n")

		


		#DIFF_TEXT = CREATE_DIFF(LINES_A, LINES_B)

		#DIFF_TEXT = CREATE_DIFF(LINES_A, LINES_B, diff_type='unified_line')


		#DIFF_TEXT = CREATE_DIFF(LINES_A, LINES_B, diff_type='smart_unified_line')
		

		DIFF_TEXT = CREATE_DIFF(LINES_A, LINES_B, diff_type='unified_char_smart_line')


		
		out_spacing = []

		num_newline = 0
		for chunk in '\x02'.join(spacing).split('\x02') + ['#']:
			if chunk[0] == 'n':
				num_newline += 1
			else:
				if num_newline != 0:
					num_char = ""
					if num_newline != 1: num_char = str(num_newline)
					out_spacing.append('n' + num_char)
					num_newline = 0

				if chunk[0] != '#': 
					tag = chunk[0]
					num = chunk[1:]
					if num == "1": num = ""
					out_spacing.append(tag + num)

		
		#out_spacing = spacing



		with open(filename + ".patch", 'w') as f:
			f.write(DIFF_TEXT + '\n')
			#f.write('\x02'.join(out_spacing) + "\n")
			f.write(''.join(out_spacing) + "\n")
			f.write("\n".join(comm))
			

		#if "fanfare" in filename: break



		if test_patches:

			print('[DEBUG]', "TESTING PATCH FOR", filename)

			status = APPLY_PATCH(filename, test_patch=True)


			if status != 0 and status < 4: return

			#print('[DEBUG] INTERMEDIATE TEST OF PATCH:', filename)

			DEBUG_DIFF_LINES = []
			ONLY_DIFF_LINES = []
			with open(filename + ".DIFF_APPLIED", 'r', encoding="utf-8") as f:
				for line in f:
					ONLY_DIFF_LINES.append(line.replace('\r', ''))


			difference_found = False
			for line in unified_diff(LINES_B, ONLY_DIFF_LINES, n=0):
				DEBUG_DIFF_LINES.append(line.replace("\n", '▼'))
				difference_found = True


			if difference_found:
				print('[ERROR] DIFFERENCES FOUND BETWEEN LINES_B AND DIFF_APPLIED')
				with open(filename + ".diff", 'w', encoding="utf-8") as f:
					f.write("\n".join(DEBUG_DIFF_LINES))
				return


			if status != 0 and status < 6: return

			OG_FILE = SOURCE_BUILD_FOLDER + filename
			NEW_FILE = filename + ".TEST"

			OG_LINES = []
			with open(OG_FILE, 'r') as f:
				for line in f:
					OG_LINES.append(line.replace('\r', ''))

			NEW_LINES = []
			with open(NEW_FILE, 'r') as f:
				for line in f:
					NEW_LINES.append(line.replace('\r', ''))

			difference_found = False

			DIFF_LINES = []

			for line in unified_diff(OG_LINES, NEW_LINES, n=0):
				DIFF_LINES.append(line.replace("\n", '▼'))
				difference_found = True

			if difference_found:
				print('[ERROR] DIFFERENCES FOUND BETWEEN SOURCE AND PATCHED')
				with open(filename + ".diff", 'w', encoding="utf-8") as f:
					f.write("\n".join(DEBUG_DIFF_LINES))
			else:
				print('[INFO] PATCH APPLIED SUCCESSFULLY, BUILDS MATCH')






