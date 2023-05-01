; ============================================
;	NO TOUCHY ANYTHING IN THIS FILE
;	UNLESS YOU KNOW WHAT YOU ARE DOING!
;		- MrL
; ============================================


;=======================================================================;
;		Super Mario Kart SPC700 Sample Table Control Code				;
;																		;
;			By: MrL314													;
;																		;
;			Last revision: March 30, 2023								;
;																		;
;		Controls for easy addition of samples via .brr files. 			;
;=======================================================================;




; ============================================
;	Macros
; ============================================

!SAMPLE_NUM #= 0

macro sample(file)
	
	!{SAMPLE_!{SAMPLE_NUM}_FILE} = <file>					; file name
	!{SAMPLE_!{SAMPLE_NUM}_LOOP} = readfile2("<file>", 0)	; file loop pointer 
	if !{SAMPLE_!{SAMPLE_NUM}_LOOP} == 0					
		!{SAMPLE_!{SAMPLE_NUM}_LOOP} = filesize("<file>")-2	; if loop pointer is 0, "no loop"
	endif

	!SAMPLE_NUM #= !SAMPLE_NUM+1	; increment sample number
endmacro


; --------------------------------------------


macro sample_loop(lbl,loop_offs)
	dw	<lbl>,<lbl>+<loop_offs>
endmacro



macro sample_NULL()
	dw	$FFFF,$FFFF
endmacro

; --------------------------------------------

macro sample_file(lbl, file)
	<lbl>:
		incbin "<file>":2-0
endmacro

; ============================================



; ============================================
;	BRR Samples List
; ============================================
incsrc "SAMPLE_LIST.asm"
; ============================================





; ============================================
;	Sample Pointer/Loop Table
; ============================================

spcblock $3C00
global SAMPLE_TABLE:
		!a #= 0
		while !a < !SAMPLE_NUM
			%sample_loop(SAMPLE_!{a}, !{SAMPLE_!{a}_LOOP})
			!a #= !a+1
		endwhile

		%sample_NULL()
		%sample_NULL()
endspcblock
; ============================================






; ============================================
;	Sample Data
; ============================================

spcblock $4000
global SAMPLES:
		!a #= 0
		while !a < !SAMPLE_NUM
			%sample_file(SAMPLE_!{a}, !{SAMPLE_!{a}_FILE})
			!a #= !a+1
		endwhile
endspcblock
; ============================================



