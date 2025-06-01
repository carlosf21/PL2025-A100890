program TesteArraysSimples;
var
    vetor: array[1..3] of integer;
    i, soma: integer;
begin
    { Inicialização do array }
    vetor[1] := 10;
    vetor[2] := 5;
    vetor[3] := 20;
    
    { Teste 1: Escrita de elementos do array }
    writeln('vetor[1]: ', vetor[1]);
    writeln('vetor[2]: ', vetor[2]);
    writeln('vetor[3]: ', vetor[3]);
    
    { Teste 2: Soma de elementos do array }
    soma := vetor[1] + vetor[3];
    writeln('Soma de vetor[1] e vetor[3]: ', soma);
end.