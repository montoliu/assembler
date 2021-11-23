// suma los numeros que estan en las posiciones de memoria 0, 1 y 2.
// Pone el resultado en la posicion de memoria 3
// Para que funcione, hay que poner unos numeros en la RAM antes de ejecutar el programa.
@0     // A = 0, M a RAM[0]
D=M    // Ponemos en D el contenido de RAM[A], es decir de RAM[0]
@1     // A = 1, M a RAM[1]
D=D+M  // Ponemos en D, el contenido de D (RAM[0]) mas el contenido de M (RAM[1])
@2     // A = 2, M a RAM[2]
D=D+M  // Ponemos en D, el contenido de D (RAM[0]+RAM[1]) mas el contenido de M (RAM[2])
@3     // A = 3, M a RAM[3]
M=D    // Guardamos en RAM[3] el resultado de la suma (valor en D)
// Al finalizar, en RAM[3] estara el resultado de la suma