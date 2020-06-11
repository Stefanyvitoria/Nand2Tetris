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

CODIGO = {
'add' : """//add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=D+A
@SP
A=M
M=D
@SP
M=M+1
""", 

'sub' : """//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=A-D
@SP
A=M
M=D
@SP
M=M+1
""",

'neg' : """//neg
@SP
M=M-1
A=M
D=M
D=!D
D=D+1
@SP
A=M
M=D
@SP
M=M+1
""",

'eq' : """//eq
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D-M
@SP
M=M-1
M=M-1
@TRUE{}
D;JEQ
@SP
A=M
M=0
@END{}
0;JMP
(TRUE{})
@SP
A=M
M=-1
(END{})
@SP
M=M+1
""",

'lt' : """//lt
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D-M
@SP
M=M-1
M=M-1
@TRUE{}
D;JLT
@SP
A=M
M=0
@END{}
0;JMP
(TRUE{})
@SP
A=M
M=-1
(END{})
@SP
M=M+1
""",

'gt' : """//gt
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D-M
@SP
M=M-1
M=M-1
@TRUE{}
D;JGT
@SP
A=M
M=0
@END{}
0;JMP
(TRUE{})
@SP
A=M
M=-1
(END{})
@SP
M=M+1
""",

'and' : """//and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=D&A
@SP
A=M
M=D
@SP
M=M+1
""",

'or' : """//or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=D|A
@SP
A=M
M=D
@SP
M=M+1
""",

'not' : """//not
@SP
M=M-1
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1
""",

'push_basico': """//push {} {}
@{}
D=A
@{}
D=D+M
@R13
M=D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
""",

'push_const': """//push const {}
@{}
D=A
@SP
A=M
M=D
@SP
M=M+1
""",

'push_static': """//push static {}
@{}
D=M
@SP
A=M
M=D
@SP
M=M+1
""",

'push_temp' : """//push temp {}
@{}
D=A
@5
D=D+A
@R13
M=D
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
""",

'push_pointer' : """//push pointer {}
@{}
D=M
@SP
A=M
M=D
@SP
M=M+1
""",

'pop_basico' : """//pop {} {}
@{}
D=A
@{}
D=D+M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
""",

'pop_static' :  """//pop static {}
@SP
M=M-1
A=M
D=M
@{}
M=D
""",

'pop_temp' : """//pop temp {}
@{}
D=A
@5
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
""",

'pop_pointer' : """//pop pointer {}
@{}
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
"""
}