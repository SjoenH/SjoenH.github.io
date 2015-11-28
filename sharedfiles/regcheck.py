## -*- coding: utf-8 -*-
# Denne fila inneholder en kopi av regcheck.py fra BE pakket inn i
# kode som legger til kommandolinje-grensesnitt og ekstra portabilitet.
# Kopien fra BE finnes i blokken REGCHECK-KODE FRA BE.

import re
import subprocess

import sys
import platform
import os


### FINN JLINK-DRIVER - START ###
# For å sette jlink path manuelt, erstatt hele 'FINN JLINK-DRIVER'-blokken med:
# JLINK_EXE = "path/til/jlink/"
def jlink_dir(segger_dir):
    if platform.system() == "Linux":
        pattern = "JLink_LinuxV"
    else:
        pattern = "JLinkARM_V"
    try:
        for d in os.listdir(segger_dir):
            if re.match(pattern, d):
                return segger_dir + d + "/"
    except Exception:
        pass

    return ""

if len(sys.argv) < 2:
    if platform.system() == "Windows":
        program_files = os.getenv("ProgramFiles(x86)")
        if program_files == None:
            program_files = os.getenv("ProgramFiles")
        segger_dir = program_files + "/SEGGER/"
        JLINK_EXE = jlink_dir(segger_dir) + "JLink.exe"
        JLINK_EXE = JLINK_EXE.replace("/", "\\")
    elif platform.system() == "Linux":
        JLINK_EXE = jlink_dir("/opt/jlink/") + "JLinkExe"
else:
    JLINK_EXE = sys.argv[1]
### FINN JLINK-DRIVER - SLUTT ###



### FIKSER KOMPABILITETSPROBLEMER VED PYTHON VERSJON 2 OG 3 - START ###
try:
    input = raw_input
except NameError:
    pass
try:
    bytes("test", "UTF-8")
except TypeError:
    def bytes(str, type):
        return str
### FIKSER INKOMPABILITETSPROBLEMER VED PYTHON VERSJON 2 OG 3 - SLUTT ###



### REGCHECK-KODE FRA BE - START ###
PORT_B  = "GPIO port B"
PORT_E  = "GPIO port E"
CONFIG  = "GPIO config"
SYSTICK = "SysTick"

def register_name(count):
    port_regs = ["CTRL", "MODEL", "MODEH", "DOUT", "DOUTSET", "DOUTCLR", "DOUTTGL", "DIN", "PINLOCKN"]
    config_regs = ["EXTIPSELL", "EXTIPSELH", "EXTIRISE", "EXTIFALL", "IEN", "IF", "IFS", "IFC", "ROUTE", "INSENSE", "LOCK", "CTRL", "CMD", "EM4WUEN", "EM4WUPOL", "EM4WUCAUSE"]
    systick_regs = ["CTRL", "LOAD", "VAL", "CALIB"]

    if count >= 0 and count < len(port_regs):
        group = PORT_B
        name  = port_regs[count]
    elif count >= len(port_regs) and count < len(port_regs) * 2:
        group = PORT_E
        name  = port_regs[count-len(port_regs)]
    elif (count - len(port_regs)*2) < len(config_regs):
        group = CONFIG
        name  = config_regs[count - len(port_regs)*2]
    elif (count - (len(config_regs) + len(port_regs)*2) < len(systick_regs)):
        group = SYSTICK
        name  = systick_regs[count - (len(config_regs) + len(port_regs)*2)]
    else:
        raise Exception("Ukjent register-navn, count er " + str(count) + ". Sjekk at MEM_READ_COMMANDS har riktige counts!")
    return (group, name)

def dump_kit_regs_by_index(index):
    # The "mem32" JLink command takes first a hexidesimal adress, then a
    # hexadesimal count of 32 bit words to get from memory.
    MEM_READ_COMMANDS = "mem32 40006024, 9\n"\
                        "mem32 40006090, 9\n"\
                        "mem32 40006100, 10\n"\
                        "mem32 E000E010, 4\n"

    proc = subprocess.Popen([JLINK_EXE], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    jlink_commands = "selemu USB\n"+ index + "\n" + MEM_READ_COMMANDS + "qc\n"
    output = proc.communicate(input=jlink_commands)[0].split("\n")

    regs = {PORT_B: {}, PORT_E: {}, CONFIG: {}, SYSTICK: {}}

    word_count = 0
    for line in output:
        if re.match("(J-Link\>)?[0-F]{8} = ([0-F]{8} )+", line):
            words = re.sub("[^ ]* = ", "", line).split()
            for word in words:
                rn = register_name(word_count)
                group = rn[0]
                name  = rn[1]
                regs[group][name] = {"value": word, "critical": None}
                word_count = word_count + 1
    return regs

def append_hint(reg, hint):
    if "hint" in reg:
        reg["hint"] += " " + hint
    else:
        reg["hint"] = hint

def set_register_errors(regs, exercise):
    e = ""
    systick_ctrl   = int(regs[SYSTICK]["CTRL"]     ["value"], 16)
    systick_load   = int(regs[SYSTICK]["LOAD"]     ["value"], 16) & int("0b111111111111111111111111",2)
    gpio_extipselh = int(regs[CONFIG] ["EXTIPSELH"]["value"], 16)
    gpio_extifall  = int(regs[CONFIG] ["EXTIFALL"] ["value"], 16)
    gpio_if        = int(regs[CONFIG] ["IF"]       ["value"], 16)
    gpio_ien       = int(regs[CONFIG] ["IEN"]      ["value"], 16)
    gpio_b_modeh   = int(regs[PORT_B] ["MODEH"]    ["value"], 16)
    gpio_e_model   = int(regs[PORT_E] ["MODEL"]    ["value"], 16)

    if exercise == "2" or exercise == "3":
        # SysTick-oppsett
        if (systick_ctrl & int("0b110", 2)) != int("0b110", 2):
            append_hint(regs[SYSTICK]["CTRL"], "Ikke konfigurert (ikke nodvendigvis feil).")
            regs[SYSTICK]["CTRL"]["critical"] = False
        # Knapp PB0 interrupt
        if (gpio_if & (1<<9) != 0):
            append_hint(regs[CONFIG]["IF"], "Har 1 på posisjon for pin 9 (dette skjer noen ganger selv om IF blir riktig oppdatert).")
            regs[CONFIG]["IF"]["critical"] = False
        if (gpio_ien & (1<<9) == 0):
            append_hint(regs[CONFIG]["IEN"], "Ikke satt for pin 9.")
            regs[CONFIG]["IEN"]["critical"] = True
        if ((gpio_extipselh >> 4) & int("0b1111", 2)) != 1:
            append_hint(regs[CONFIG]["EXTIPSELH"], "Feil for pin 9.")
            regs[CONFIG]["EXTIPSELH"]["critical"] = True
        if (gpio_extifall & (1<<9) == 0):
            append_hint(regs[CONFIG]["EXTIFALL"], "Feil for pin 9.")
            regs[CONFIG]["EXTIFALL"]["critical"] = True
    if exercise == "2":
        # SysTick-oppsett
        if (systick_load  != 1400000):
            append_hint(regs[SYSTICK]["LOAD"], "Ikke satt til 10 interrupts per sekund (ikke nodvendigvis feil).")
            regs[SYSTICK]["LOAD"]["critical"] = False
    if exercise == "3":
        # SysTick-oppsett
        if (systick_load  != 14000000):
            append_hint(regs[SYSTICK]["LOAD"], "Ikke satt til 1 interrupt per sekund (ikke nodvendigvis feil).")
            regs[SYSTICK]["LOAD"]["critical"] = False
        # Knapp PB1 interrupt
        if ((gpio_extipselh >> 8) & int("0b1111", 2)) != 1:
            append_hint(regs[CONFIG]["EXTIPSELH"], "Feil for pin 10.")
            regs[CONFIG]["EXTIPSELH"]["critical"] = True
        if (gpio_extifall & (1<<10) == 0):
            append_hint(regs[CONFIG]["EXTIFALL"], "Feil for pin 10.")
            regs[CONFIG]["EXTIFALL"]["critical"] = True
        if (gpio_if & (1<<10) != 0):
            append_hint(regs[CONFIG]["IF"], "Har 1 på posisjon for pin 10 (dette skjer noen ganger selv om IF blir riktig oppdatert).")
            regs[CONFIG]["IF"]["critical"] = False
        if (gpio_ien & (1<<10) == 0):
            append_hint(regs[CONFIG]["IEN"], "Ikke satt for pin 10.")
            regs[CONFIG]["IEN"]["critical"] = True
        if ((gpio_b_modeh >> 8) & int("0b1111", 2)) != 1:
            append_hint(regs[PORT_B]["MODEH"], "Feil for port B pin 10.")
            regs[PORT_B]["MODEH"]["critical"] = True
        # Knapp PB0 interrupt
        if ((gpio_b_modeh >> 4) & int("0b1111", 2)) != 1:
            append_hint(regs[PORT_B]["MODEH"], "Feil for port B pin 9.")
            regs[PORT_B]["MODEH"]["critical"] = True
        # LED
        if ((gpio_e_model >> 8) & int("0b1111", 2)) != int("0b0100", 2):
            append_hint(regs[PORT_E]["MODEL"], "Feil for port E pin 2.")
            regs[PORT_E]["MODEL"]["critical"] = True

def exercise_failed_by_regs(regs):
    for group in regs.values():
        for reg in group.values():
            if reg["critical"]:
                return True
    return False
### REGCHECK-KODE FRA BE - SLUTT ###


def dump_cpu_regs():
    proc = subprocess.Popen([JLINK_EXE], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    jlink_commands = bytes("selemu USB\n0\nh\ng\nqc\n", "UTF-8")
    output = proc.communicate(input=jlink_commands)[0]
    return output[output.index("R0 = ") : output.index("XPSR = ")].replace(", ", "\n")

def test_jlink():
    global JLINK_EXE
    while True:
        try:
            proc = subprocess.Popen([JLINK_EXE], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            jlink_commands = "qc\n"
            proc.communicate(input=jlink_commands)
        except Exception:
            try:
                import Tkinter, tkFileDialog
                print("Finner ikke JLink, gjor ett av folgende:\n\t* Velg JLinkExe fra dialogen\n\t* Start på nytt fra kommandolinjen med path til JLink som argument\n\t* Aapne koden til dette scriptet og sett JLINK_EXE-variabelen manuelt")
                root = Tkinter.Tk()
                root.withdraw()
                JLINK_EXE = tkFileDialog.askopenfilename(initialfile="JLink.exe")
            except Exception:
                JLINK_EXE = input("Finner ikke JLink, gjor ett av folgende:\n\t* Start på nytt fra kommandolinjen med path til JLink som argument\n\t* Aapne koden til dette scriptet og sett JLINK_EXE-variabelen manuelt\n\t* Skriv inn path til JLink under\n>")

        else:
            break

### KOMMANDOLINJE-GRENSESNITT - START ###
def format_regs(regs, include_hints=False):
    s = ""

    # Registere
    for group in regs:
        s = s + group + ":\n"
        for reg in regs[group]:
            s = s + "\t" + reg + ": " + regs[group][reg]["value"] + "\n"
    s += "\n"

    # Sammendrag av feil
    if include_hints:
        hint_kritisk = ""
        hint_ikkekritisk = ""
        for group, groupregs in regs.iteritems():
            for reg, regdata in groupregs.iteritems():
                if "hint" in regdata:
                    hint = "\t* " + group + ", " + reg + ": " + regdata["hint"] + "\n"
                    if regdata["critical"]:
                        hint_kritisk += hint
                    else:
                        hint_ikkekritisk += hint

        if hint_kritisk:
            s += "Fant følgende kritiske feil: \n" + hint_kritisk
        else:
            s += "Fant ingen kritiske feil\n"

        if hint_ikkekritisk:
            s += "Fant følgende ikke-kritiske eller potensielle feil: \n" + hint_ikkekritisk
        else:
            s += "Fant ingen ikke-kritiske/potensielle feil\n"

    return s


print("Tester driver...")
test_jlink()
while True:
    print("\nSkriv kommando og trykk enter:\n"+
          "\t* Trykk enter for å lese uten å sjekke støtte-registre for feil\n"
          "\t* Nummeret for en oving (\"1\", \"2\" eller \"3\") for å teste etter vanlige feil i støtte-registrene\n" +
          "\t* \"cpu\" for å lese CPU-registrene\n" +
          "\t* \"exit\", \"x\" eller \"q\" for å avslutte")
    cmd = input("> ")
    if cmd == "":
        regs = dump_kit_regs_by_index("0")
        print(format_regs(regs))
    elif cmd == "1" or cmd == "2" or cmd == "3":
        regs = dump_kit_regs_by_index("0")
        set_register_errors(regs, cmd)
        print(format_regs(regs, include_hints=True))
    elif cmd == "cpu":
        print(dump_cpu_regs())
    elif cmd == "exit" or cmd == "x" or cmd == "q":
        exit(0)
    else:
        print("Ugyldig kommando: " + cmd)

### KOMMANDOLINJE-GRENSESNITT - SLUTT ###
