TABELA_SIMBOLOS = {
"THIS": 3,
"THAT": 4,
"local": "LCL",
"argument": "ARG",
"this": "THIS",
"that": "THAT",
"0": "THIS",
"1": "THAT"
}

ADD = """//add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1
"""

SUB = """//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
"""

NEG = """//neg
@SP
M=M-1
A=M
D=-M
M=D
@SP
M=M+1
"""

# EQ - Recebe indice customizado.
EQ = """//eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@EQUAL{}
D;JEQ
D=0
@FINAL{}
0;JEQ
(EQUAL{})
D=-1
(FINAL{})
@SP
A=M
M=D
@SP
M=M+1
"""

# GT - Recebe indice customizado.
GT = """//gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@GREATER_THAN{}
D;JGT
D=0
@END{}
0;JEQ
(GREATER_THAN{})
D=-1
(END{})
@SP
A=M
M=D
@SP
M=M+1
"""

# LT - Recebe indice customizado.
LT = """//lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LESS_THAN{}
D;JLT
D=0
@END{}
0;JEQ
(LESS_THAN{})
D=-1
(END{})
@SP
A=M
M=D
@SP
M=M+1
"""

AND = """//and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D&M
M=D
@SP
M=M+1
"""

OR = """//or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D|M
M=D
@SP
M=M+1
"""

NOT = """//not
@SP
M=M-1
A=M
D=!M
M=D
@SP
M=M+1
"""

#Push constant - Recebe argumento 2 (2 vezes) || *SP = i, SP++
#Push temp - Recebe argumento 2 (2 vezes) || addr = 5 + i, *SP = *addr, SP++
#Push pointer - Recebe Tabela_simbolos[argumento_2] || *SP = THIS/THAT, SP++
#Push static - Recebe Nomedo arquivo e argumento 2.
#Push basico - Recebe argumento 2, Tabela_simbolos[segmento]

PUSH =  { 'constant' : """//push constant {}
@{}
D=A
@SP
A=M
M=D
@SP
M=M+1
""",

'temp' : """//push temp {}
@{}
D=A
@5
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
""",
'pointer' : """@{}
D=M
@SP
A=M
M=D
@SP
M=M+1
""",
'static' : """@{}.{}
D=M
@SP
A=M
M=D
@SP
M=M+1
""", 
'basico' : """@{}
D=A
@{}
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
}

#POP temp - Recebe argumento 2.
#POP pointer - Recebe Tabela_Simbolos[segmento].
#POP static - Recebe nome do arquivo, argumento 2.
#POP basico - argumento 2, Tabela_simbolos[segmento].
POP = {'temp' : """@{}
D=A
@5
D=D+A
@frame
M=D
@SP
M=M-1
A=M
D=M
@frame
A=M
M=D
""",

'pointer' : """@SP
M=M-1
A=M
D=M
@{}
M=D
""",

'static' : """@SP
M=M-1
A=M
D=M
@{}.{}
M=D
""",

'basico': """@{}
D=A
@{}
D=D+M
@frame
M=D
@SP
M=M-1
A=M
D=M
@frame
A=M
M=D
"""
}

#Pode vir com o nome da função
LABEL = """({})
"""

#Pode vir com o nome da função
IFGOTO = """@SP
M=M-1
A=M
D=M
@{}
D;JNE
"""

#Pode vir com o nome da função
GOTO = """@{}
0;JMP
"""

# FUNCTION - Recebe o nome da função
#a parte dois é escrita * o numero de variáveis
FUNCTION= {'parte1': """({})
""",
'parte2' : """@0
D=A
@SP
A=M
M=D
@SP
M=M+1
"""
}

RETURN = """@LCL
D=M
@frame
M=D
@5
D=D-A
A=D
D=M
@return
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@return
A=M
0;JMP
"""

#CALL - Recebe o nome da função e indice, numero de argumentos+5,nome da função, nome da função e indice de funções
CALL = """@{}$ret.{}
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
D=M
@{}
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@{}
0;JMP
({}$ret.{})
"""

BOOTSTRAP = """//SP=256
@256
D=A
@SP
M=D
//call Sys.init 0
@Bootstrap$ret
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Bootstrap$ret)
"""