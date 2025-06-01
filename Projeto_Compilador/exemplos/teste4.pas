program TesteErros;
var
    x: integer;
    arr: array[1..2] of integer;
begin
    y := 10; {Variável não declarada}
    arr := 5; {Atribuição direta a array}
    writeln(length(x)); {LENGTH em não-string}
    arr[1, 2] := 10; {Número incorreto de índices}
end.