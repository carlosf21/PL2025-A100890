program TesteIfAninhado;
var
    x: integer;
begin
    x := 15;
    if x > 10 then
        if x < 20 then
            writeln('x está entre 10 e 20')
        else
            writeln('x é maior ou igual a 20');
end.