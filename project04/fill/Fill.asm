// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here:

(LOOP)
    @KBD	//Recupera o valor do teclado
    D=M
    @PRESSIONADO
    D;JGT		//Se pressionado, então pula p/ local certo
    @NAOPRESSIONADO
    D;JEQ		//Se não pressionado, então pula p/ local certo

(PRESSIONADO)
    @R0
    M=-1
    @CONF
    0;JMP

(NAOPRESSIONADO)
    @R0
    M=0
    @CONF
    0;JMP

(CONF)
    @fim
    @total
    @24575
    D=A
    @fim
    M=D		// fim = 245575(fim do mapa de memória da tela)
    @8191
    D=A
    @total
    M=D		// total = 8191 (quantidade de "word")
    @PINTAR
    0;JMP

(PINTAR)
    @R0
    D=M		// recupera o valor de pintar
    @fim
    A=M
    M=D

    @fim
    M=M-1

    D=M
    @total
    D=M-D
    @LOOP
    D;JEQ    
    @PINTAR
    0;JMP