---
layout: post
title:  "Exercises in DigDat"
date:   2015-11-27 13:36:00 +0100
categories: DigDat
---
<!-- Doesn't work. -->
<!-- Here is the [exercise paper](~/sharedfiles/Digdat/exercise4-2.pdf). -->

Given is the following assembly program:

    0x00 ldi %r2, 1
    0x04 ldi %r1, 1
    0x08 mul %r2, %r2, %r0
    0x0C sub %r0, %r0, %r1
    0x10 cmp %r3, %r0, %r1
    0x14 jgt %r3, -16

The first column of a line denotes the address of an instruction in memory, the second column the kind of instruction, and everything else that follows on a line are the operands.


Exercise 4
-
Use the instruction set architecture in Section 1 to translate the assembly to machine instructions. The machine instruc- tions must be written in binary format. Use ’X’ to denote unused bits. A register maps to its corresponding binary num- ber. For example, the assembly instruction add %r7, %r8, %r9 translates to 00001001110100001001XXXXXXXXXXXX.

**Submission**:
Hand in a plain text file with ONLY one machine instruction per line. Don’t put the address before the instruction.

Exercise 5
-
Assume that register %r0 contains 2 before the program is executed. What would be the value in register %r2 once the program reaches the instruction at address 0x18, i.e. the branch at address 0x14 is not taken. What would be the value in %r2, if %r0 would contain 3, 4, 9?

**Submission**:
Hand in a plain text file with the corresponding values per line, i.e. the value for 2 on the first line, the value for 3 on the second, etc.

Exercise 6
-
Assume that register %r0 contains 1 before the program is executed. Given the microarchitecture in Section 2 and the control unit’s state machine in Section 3, write down the values of the control unit’s output signals for each executed instruction in the following order: imm, alu, regw, branch.

**Submission**:
Hand in a plain text file with the values for each executed instruction per line.
