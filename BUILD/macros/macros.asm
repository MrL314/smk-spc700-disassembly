;=======================================================================;
;		Super Mario Kart SPC700 Helper Macros and Functions				;
;																		;
;			By: MrL314													;
;																		;
;			Last revision: March 17, 2023								;
;																		;
;		Some helper macros and functions for the sound binary build.	;
;=======================================================================;

if not(defined("MACROS_INCLUDED"))
{

!MACROS_INCLUDED = 1


; ============================================
;	General Functions
; ============================================

function low(addr) = (addr&$FF)
function high(addr) = ((addr>>8)&$FF)

; ============================================




; ============================================
;	ADSR functions
; ============================================

function ADSR1(EN,DR,AR) = ((EN&$01)<<7)|((DR&$07)<<4)|((AR&$0F)<<0)
function ADSR2(SL,SR) = ((SL&$07)<<5)|((SR&$1F)<<0)

; ============================================




; ============================================
;	Word Macros
; ============================================


macro MOVW_YA_CONST(w)
	MOV  A, #low(<w>)
	MOV  Y, #high(<w>)
endmacro


macro MOVW_YA_ADDR(addr)
	MOV  A, <addr>+0
	MOV  Y, <addr>+1
endmacro

macro MOVW_ADDR_YA(addr)
	MOV  <addr>+0, A
	MOV  <addr>+1, Y
endmacro

macro MOVW_ADDR_CONST(addr,w)
	MOV  <addr>+0, #low(<w>)
	MOV  <addr>+1, #high(<w>)
endmacro


; ============================================





; ============================================
;	SFX parameter Macros
; ============================================

macro p_byte(addr,val)
	MOV  <addr>, #<val>
endmacro

macro p_word(addr,val)
	MOV  <addr>+0, #low(<val>)
	MOV  <addr>+1, #high(<val>)
endmacro


macro note(p)
	%MOVW_YA_CONST(<p>)
endmacro

macro get_note(p)
	%MOVW_YA_ADDR(<p>)
endmacro


macro pitch(p)
	%MOVW_YA_CONST(<p>)
endmacro

macro get_pitch(p)
	%MOVW_YA_ADDR(<p>)
endmacro


macro delta(p)
	%MOVW_YA_CONST(<p>)
endmacro

; ============================================





; ==============================================;
macro def_sequence()							;
	!note1     = !temp_buffA+2	;(W)			;
	!note2     = !temp_buffA+4	;(W)			;
	!note3     = !temp_buffA+6	;(W)			;
	!note4     = !temp_buffA+8	;(W)			;
	!vol       = !temp_buffA+10	;(B)			;
	!adsr1     = !temp_buffA+11	;(B)			;
	!adsr2     = !temp_buffA+12	;(B)			;
	!srcn      = !temp_buffA+13	;(B)			;
	!ratio     = !temp_buffA+14	;(B)			;
	!attk      = !temp_buffA+15	;(B)			;
	; - - - - -									;
	!CNT      = 0		; continuous			;
	!ATK      = 1		; pulsed				;
endmacro										;
; ----------------------------------------------;
macro undef_sequence()							;
	undef "note1"								;
	undef "note2"								;
	undef "note3"								;
	undef "note4"								;
	undef "vol"									;
	undef "adsr1"								;
	undef "adsr2"								;
	undef "srcn"								;
	undef "ratio"								;
	undef "attk"								;
	; - - - - -									;
	undef "CNT"									;
	undef "ATK"									;
endmacro										;
; ==============================================;



; ==============================================;
macro def_repeat()								;
	!pitch    = !temp_buffA+2	;(W)			;
	!ratio    = !temp_buffA+4	;(B)			;
	!vol      = !temp_buffA+5	;(B)			;
	!adsr1    = !temp_buffA+6	;(B)			;
	!adsr2    = !temp_buffA+7	;(B)			;
	!srcn     = !temp_buffA+8	;(B)			;
	!attk     = !temp_buffA+9	;(B)			;
	; - - - - -									;
	!CNT      = 0		; continuous			;
	!ATK      = 1		; pulsed				;
endmacro										;
; ----------------------------------------------;
macro undef_repeat()							;
	undef "pitch"								;
	undef "ratio"								;
	undef "vol"									;
	undef "adsr1"								;
	undef "adsr2"								;
	undef "srcn"								;
	undef "attk"								;
	; - - - - -									;
	undef "CNT"									;
	undef "ATK"									;
endmacro										;
; ==============================================;






; ==================================================;
macro define_ghost()								;
	!note1 = !temp_buffA+0	;(W)					;
	!note2 = !temp_buffA+2	;(W)					;
	!note3 = !temp_buffA+4	;(W)					;
	!note4 = !temp_buffA+6	;(W)					;
	!note5 = !temp_buffA+8	;(W)					;
	!note6 = !temp_buffA+10	;(W)					;
	!note7 = !temp_buffA+12	;(W)					;
	!note8 = !temp_buffA+14	;(W)					;
	!note9 = !temp_buffB+0	;(W)					;
endmacro											;
; --------------------------------------------------;
macro undef_ghost()									;
	undef "note1"									;
	undef "note2"									;
	undef "note3"									;
	undef "note4"									;
	undef "note5"									;
	undef "note6"									;
	undef "note7"									;
	undef "note8"									;
	undef "note9"									;
endmacro											;
; ==================================================;





; ==================================================;
macro define_two_note()								;
	!time_A    = !temp_buffA+0	;(B)				;
	!time_B    = !temp_buffA+1	;(B)				;
	!pitch_A   = !temp_buffA+2	;(W)				;
	!pitch_B   = !temp_buffA+4	;(W)				;
	!vol       = !temp_buffA+6	;(B)				;
	!adsr1     = !temp_buffA+7	;(B)				;
	!adsr2     = !temp_buffA+8	;(B)				;
	!srcn_A    = !temp_buffA+9	;(B)				;
	!srcn_B    = !temp_buffA+10	;(B)				;
	!attk      = !temp_buffA+11	;(B)				;
	; - - - - - -									;
	!CNT       = 0	; don't attack on second note	;
	!ATK       = 1	; attack on second note			;
endmacro											;
; --------------------------------------------------;
macro undef_two_note()								;
	undef "time_A"									;
	undef "time_B"									;
	undef "pitch_A"									;
	undef "pitch_B"									;
	undef "vol"										;
	undef "adsr1"									;
	undef "adsr2"									;
	undef "srcn_A"									;
	undef "srcn_B"									;
	undef "attk"									;
	undef "CNT"										;
	undef "ATK"										;
endmacro											;
; ==================================================;




; ==================================================;
macro define_linear_1()								;
	!time   = !temp_buffA+0	;(B)					;
	!pitch  = !temp_buffA+1	;(W)					;
	!delta  = !temp_buffA+3	;(W)					;
	!adsr1  = !temp_buffA+5	;(B)					;
	!adsr2  = !temp_buffA+6	;(B)					;
	!vol    = !temp_buffA+7	;(B)					;
	!srcn   = !temp_buffA+8	;(B)					;
	!dir    = !temp_buffA+9	;(B)					;
	; - - - - - -									;
	!UP     = 0										;
	!DOWN   = 1										;
endmacro											;
; --------------------------------------------------;
macro undef_linear_1()								;
	undef "time"									;
	undef "pitch"									;
	undef "delta"									;
	undef "adsr1"									;
	undef "adsr2"									;
	undef "vol"										;
	undef "srcn"									;
	undef "dir"										;
	undef "UP"										;
	undef "DOWN"									;
endmacro											;
; ==================================================;





; ==================================================;
macro define_bilinear()								;
	!time_A    = !temp_buffA+0	;(B)				;
	!time_B    = !temp_buffA+1	;(B)				;
	!pitch_A   = !temp_buffA+2	;(W)				;
	!pitch_B   = !temp_buffA+4	;(W)				;
	!delta_A   = !temp_buffA+6	;(W)				;
	!dir_A     = !temp_buffA+8	;(B)				;
	!delta_B   = !temp_buffA+9	;(W)				;
	!dir_B     = !temp_buffA+11	;(B)				;
	!vol_A     = !temp_buffA+12	;(B)				;
	!vol_B     = !temp_buffA+13	;(B)				;
	!adsr1     = !temp_buffA+14	;(B)				;
	!adsr2     = !temp_buffA+15	;(B)				;
	; - - - - - -									;
	!srcn_A    = !temp_buffB+0	;(B)				;
	!srcn_B    = !temp_buffB+1	;(B)				;
	!attk      = !temp_buffB+2	;(B)				;
	; - - - - - -									;
	!UP        = 0									;
	!DOWN      = 1									;
	; - - - - - -									;
	!CNT       = 0	; don't attack on second note	;
	!ATK       = 1	; attack on second note			;
endmacro											;
; --------------------------------------------------;
macro undef_bilinear()								;
	undef "time_A"									;
	undef "time_B"									;
	undef "pitch_A"									;
	undef "pitch_B"									;
	undef "delta_A"									;
	undef "dir_A"									;
	undef "delta_B"									;
	undef "dir_B"									;
	undef "vol_A"									;
	undef "vol_B"									;
	undef "adsr1"									;
	undef "adsr2"									;
	undef "srcn_A"									;
	undef "srcn_B"									;
	undef "attk"									;
	undef "UP"										;
	undef "DOWN"									;
	undef "CNT"										;
	undef "ATK"										;
endmacro											;
; ==================================================;






; ==================================================;
macro define_hit_wobble()							;
	!pitch_A   = !temp_buffA+2	;(W)				;
	!pitch_B   = !temp_buffA+4	;(W)				;
	!time_A    = !temp_buffA+6	;(B)				;
	!time_B    = !temp_buffA+7	;(B)				;
	!delta_B   = !temp_buffA+8	;(W)				;
	!vol       = !temp_buffA+10	;(B)				;
	!adsr1     = !temp_buffA+11	;(B)				;
	!adsr2     = !temp_buffA+12	;(B)				;
	!srcn_A    = !temp_buffA+13	;(B)				;
	!srcn_B    = !temp_buffA+14	;(B)				;
	!attk      = !temp_buffA+15	;(B)				;
	; - - - - - -									;
	!CNT       = 0	; don't attack on second note	;
	!ATK       = 1	; attack on second note			;
endmacro											;
; --------------------------------------------------;
macro undef_hit_wobble()							;
	undef "pitch_A"									;
	undef "pitch_B"									;
	undef "time_A"									;
	undef "time_B"									;
	undef "delta_B"									;
	undef "vol"										;
	undef "adsr1"									;
	undef "adsr2"									;
	undef "srcn_A"									;
	undef "srcn_B"									;
	undef "attk"									;
	undef "CNT"										;
	undef "ATK"										;
endmacro											;
; ==================================================;


}
endif