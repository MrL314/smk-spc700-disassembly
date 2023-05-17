# AuDism by MrL314
 Disassembly of Super Mario Kart's SPC700 Audio Driver Code. Please read through the entire ReadMe before continuing!

 Quick Download: [**[here](https://github.com/MrL314/smk-spc700-disassembly/archive/refs/heads/main.zip)**]


## Overview
This repo contains a set of scripts pertaining to the disassembly of the SPC700 Audio Driver for *Super Mario Kart (USA, JPN, PAL)*. The set of scripts included can:
- Extract and disassemble the audio driver
- Assemble and build the disassembled driver, as well as modifications to the disassembly
  - Supports retail USA, JPN, and PAL versions of the driver at the moment
- Add annotations to the disassembly via a custom patching system
- Create annotation patches from modified files to be distributed without containing proprietary code [^1]

[^1]: this system is a mess right now, so if you want to contribute, please contact me!

## Disassembly
The extraction scripts are written in Python, so you will need to install Python 3.8 (or higher) on your system (which you can do [**here**](https://www.python.org/downloads/), MAKE SURE the `Add to PATH` checkbox is checked when installing, and turn off the `App Execution Alias` for windows [see [here](https://www.windowscentral.com/how-manage-app-execution-aliases-windows-10)]!!)

To extract the disassembly, you will need to provide your own copy of a *Super Mario Kart (USA)* ROM. Please put the ROM in the base directory and run `CREATE_DISASSEMBLY.bat`, and follow the instructions provided. The disassembly will be located in the `BUILD` folder, and should contain the following structure after building
```
BUILD\
  asar\
    asar.exe
  define\
    define.def
    dspregs.def
    NSPC.def
    ram_map.def
  driver\
    driver.asm     (+ .patch)
    dsp_shadow.tbl (+ .patch)
    VCMD.asm       (+ .patch)
    VCMD.tbl       (+ .patch)
  macros\
    macros.asm
    nspc_macros.mac
  samples\
    00_skid.brr
    01_splash.brr
    02_engineA.brr
    03_engineB.brr
    04_closed_hihat.brr
    05_reverb_snare.brr
    06_synth_kick.brr
    07_orchestra_hit.brr
    08_synth_brass.brr
    09_clarinet.brr
    10_electric_guitar.brr
    11_piano.brr
    12_synth_bass.brr
    13_marimba.brr
    14_drawbar_organ.brr
    15_human_whistle.brr
    16_bongos.brr
    17_nylon_guitar.brr
    18_underwater.brr
    19_gravel.brr
    20_synth_organ.brr
    21_cowbell.brr
    22_timbale.brr
    23_engineC.brr
    24_engineD.brr
    25_shrill_whistle.brr
    SAMPLE_LIST.asm
    sample_parameters.tbl (+ .patch)
    samples.asm
  songs\
    fanfare.ssf        (+ .patch)
    final_lap.ssf      (+ .patch)
    game_over.ssf      (+ .patch)
    gp_intro.ssf       (+ .patch)
    no_record.ssf      (+ .patch)
    race_qualified.ssf (+ .patch)
    rank_bowser.ssf    (+ .patch)
    rank_dkjr.ssf      (+ .patch)
    rank_koopa.ssf     (+ .patch)
    rank_luigi.ssf     (+ .patch)
    rank_mario.ssf     (+ .patch)
    rank_out.ssf       (+ .patch)
    rank_peach.ssf     (+ .patch)
    rank_toad.ssf      (+ .patch)
    rank_yoshi.ssf     (+ .patch)
    starman.ssf        (+ .patch)
    tt_intro.ssf       (+ .patch)
  tables\
    echo_FIR.tbl (+ .patch)
    pan.tbl      (+ .patch)
    pitch.tbl    (+ .patch)
    susvel.tbl   (+ .patch)
  BUILD SOUND JPN.bat
  BUILD SOUND PAL.bat
  BUILD SOUND USA.bat
  doppler_data.asm   (+ .patch)
  exsfx.asm          (+ .patch)
  routine_tables.asm (+ .patch)
  sfx.asm            (+ .patch)
  sfxctrl.asm        (+ .patch)
  sound.asm          (+ .patch)
  spc700.asm
  util.asm           (+ .patch)
```

## Building
Provided in the `BUILD` folder are 3 build scripts, one for each of the USA, JPN, and PAL releases of the sound driver. To build each version, run the repsective `BUILD SOUND XXX.bat` file for the version you are building for. This will build a contiguous binary called `spc700.sfc` in the `BUILD` folder. To insert this back into a *Super Mario Kart* ROM, copy the first `8000h` bytes from `spc700.sfc` and overwrite the data at offset `28000h` in the SMK ROM, then copy the remaining data from `spc700.sfc` to the offset `38000h` in the SMK ROM.

The sound driver is built using [**Asar 1.9**](https://github.com/RPGHacker/asar), however I had to build v1.9 on my own machine, so at the moment only Windows is supported. If you are using another OS, make sure to build using Asar 1.9. 

## Linux / Unix Support?
Eventually... Need to convert everything to Unix based systems and rebuild Asar 1.9 with Linux. If you'd like to help with this conversion I would **greatly** appreciate it!!

## Special Thanks
- SmorBjorn
- KungFuFurby
- MrPinci19
- The entire Asar development team

## Disclaimer
I am not affiliated with Nintendo, and do not represent Nintendo in any way. The naming conventions used in this disassembly are my own conventions and do not reflect the original views or names of the creators of the original code. This set of programs is provided without proprietary data. By providing your own Super Mario Kart ROM, you do so at your own risk.
