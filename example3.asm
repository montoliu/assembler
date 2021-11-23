// Calcula el maximo de dos numeros
// Los numeros estaran en RAM[0] y RAM[1]
// El resultado en RAM[2]

@0
D=M
@1
D=D-M
@PRIMERO
D; JGE
@1
D=M
@2
M=D
@END
0;JMP
(PRIMERO)
@0
D=M
@2
M=D
(END)