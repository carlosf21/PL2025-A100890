program Contas;
var
    num1, num2: integer;
begin
    writeln('Introduza dois números inteiros:');
    readln(num1);
    readln(num2);
    
    writeln('A soma é: ', num1 + num2);
    writeln('A diferença é: ', num1 - num2);
    writeln('O produto é: ', num1 * num2);
    writeln(num1, '+', num1, '*', num2, '=', num1 + num1 * num2);
    writeln(num1, '*', num1, '+', num2, '=', num1 * num1 + num2);
    writeln('A divisão é: ', num1 div num2);
end.