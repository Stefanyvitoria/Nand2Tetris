// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@SOMA
M=0 //SOMA = 0

(LOOP)
@R0
D=M
@ADD
D;JEQ // if RAM[0] = 0 fim do loop

@R0
D=M
M=D-1 // RAM[0] = -1

@R1
D=M
@SOMA
M=M+D // SOMA = SOMA+RAM[1]
@LOOP
0;JMP


(ADD) // adiciona o resultado em RAM[2]
@SOMA
D=M
@R2
M=D

(END)
@END
0;JMP