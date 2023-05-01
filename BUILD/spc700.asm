;=======================================================================;
;		Super Mario Kart SPC700 Main File								;
;																		;
;			By: MrL314													;
;																		;
;			Last revision: April 3, 2023								;
;																		;
;		Main file for assembly of SMK's SPC700 sound binary.			;
;=======================================================================;


; ============================================
;	Includes/Macros
; ============================================
incsrc "define/define.def"
incsrc "define/ram_map.def"
incsrc "define/dspregs.def"
incsrc "define/NSPC.def"

incsrc "macros/macros.asm"
incsrc "macros/nspc_macros.mac"
; ============================================

norom
org	0
arch spc700



if not(defined("JPN_VER"))
	!JPN_VER = 0
endif
if not(defined("USA_VER"))
	!USA_VER = 0
endif
if not(defined("PAL_VER"))
	!PAL_VER = 0
endif

if !JPN_VER == 0 && !USA_VER == 0 && !PAL_VER == 0
	!USA_VER = 1	; sorry, I usually work with the US version :)
endif






; ============================================
; DATA TABLES 1
; ============================================
spcblock $3C70
	incsrc "tables/susvel.tbl"
	incsrc "samples/sample_parameters.tbl"

	incsrc "songs/rank_toad.ssf"
	incsrc "songs/final_lap.ssf"

	incsrc "tables/echo_FIR.tbl"
	incsrc "tables/pitch.tbl"

	global VERSION_ID: 
		db	"*Ver S1.20*"		; pretty much unused :p

	incsrc "tables/pan.tbl"

	incsrc "driver/VCMD.tbl"
	incsrc "driver/dsp_shadow.tbl"
endspcblock
; ============================================



; ============================================
;	Song Sets
; ============================================
if !USA_VER == 1
	spcblock $03DB
else
	spcblock $03DC
endif
	incsrc "songs/no_record.ssf"
	incsrc "songs/rank_bowser.ssf"
	incsrc "songs/rank_koopa.ssf"
	incsrc "songs/rank_out.ssf"
	incsrc "songs/tt_intro.ssf"
endspcblock

spcblock $D783
	incsrc "songs/gp_intro.ssf"
	incsrc "songs/rank_peach.ssf"
	incsrc "songs/race_qualified.ssf"
	incsrc "songs/rank_luigi.ssf"
	incsrc "songs/rank_mario.ssf"
	incsrc "songs/game_over.ssf"
endspcblock

spcblock $FF00
	incsrc "songs/fanfare.ssf"
endspcblock 
; ============================================



; ============================================
;	SPC700 Driver Code
; ============================================
spcblock $0800
	incsrc "driver/driver.asm"

	incsrc "songs/starman.ssf"
	incsrc "songs/rank_dkjr.ssf"
	incsrc "songs/rank_yoshi.ssf"

	incsrc "doppler_data.asm"
	incsrc "routine_tables.asm"
	incsrc "sound.asm"
	incsrc "exsfx.asm"
	incsrc "sfx.asm"
	incsrc "util.asm"
endspcblock
; ============================================



; ============================================
;	SAMPLES DATA
; ============================================
incsrc "samples/samples.asm"
; ============================================


dw	$0000, CODE_ENTRY		; SPC execute point









