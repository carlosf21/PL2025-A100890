# PascalCompiler
### Grupo 18
- A104445-Alexandre Marques Miranda
- A100818-André Miguel Alves de Carvalho
- A100890-Carlos Eduardo Martins de Sá Fernandes

## Introdução: Objetivo e contexto do projeto

O objetivo principal deste projeto foi desenvolver um compilador funcional para uma linguagem baseada em Pascal, recorrendo a ferramentas da biblioteca `PLY` (Python Lex-Yacc).

O projeto foi realizado no contexto da unidade curricular de Processamento de Linguagens e envolveu um esforço conjunto na modelação da gramática, na verificação semântica detalhada e na criação de um gerador de código que produz instruções compatíveis com uma máquina virtual.

Ao longo do desenvolvimento, foram abordados conceitos fundamentais como: construção do *lexer* e do *parser*, verificação de tipos, gestão de memória, manipulação de arrays e strings, entre outros.

## Análise Léxica: Implementação do lexer com ply.lex, identificação de tokens

A análise léxica do compilador foi realizada com a biblioteca `ply.lex`, responsável por transformar o código-fonte em tokens, que são as unidades básicas de sintaxe da linguagem. O lexer desenvolvido identifica tanto símbolos simples como palavras-chave e tipos, distinguindo entre identificadores, operadores, literais e comentários.

#### Tokens definidos

A lista de tokens abrange:

- **Identificadores e literais**: `ID`, `NUMBER`, `STRING`
- **Operadores e símbolos**: `+`, `-`, `*`, `/`, `:=`, `=`, `<>`, `>=`, `<=`, `>`, `<`, `(`, `)`, `[`, `]`, `;`, `:`, `,`, `.`, `..`
- **Palavras-chave**: `PROGRAM`, `VAR`, `BEGIN`, `END`, `IF`, `THEN`, `ELSE`, `WRITE`, `WRITELN`, `READLN`, `FOR`, `TO`, `DOWNTO`, `DO`, `WHILE`, `AND`, `NOT`, `DIV`, `MOD`, `BOOLEAN`, `INTEGER`, `REAL`, `ARRAY`, `OF`, `STRING_TYPE`, `FUNCTION`, `LENGTH`, `TRUE`, `FALSE`

### Principais aspetos da implementação

- **Expressões regulares** são utilizadas para definir cada token de forma precisa.
- **Palavras-chave** são tratadas com funções individuais (`t_IF`, `t_VAR`, etc.) permitindo distinção mesmo em caso de letras minúsculas e maiúsculas misturadas.
- **Literals numéricos** são reconhecidos como `int` ou `float` dependendo do formato (`123` vs `123.45`).
- **Strings** são aceites entre aspas simples (`'texto'`) e convertidas para o formato de aspas duplas (`"texto"`).
- **Comentários** são ignorados e podem ter a forma Pascal `{ ... }` ou `// ...`.

### Tratamento de erros e estrutura

- **Caracteres ilegais** são identificados com mensagens de erro informativas, sem interromper o processamento.
- **Espaços e tabs** são ignorados (`t_ignore = ' \t'`), e quebras de linha são usadas para atualizar o número de linha (`t_newline`).
- O lexer é criado com `lex.lex()` no final do ficheiro.

Esta implementação oferece uma base sólida e extensível para as fases seguintes do compilador, garantindo que o parser receba tokens corretamente classificados e com valores já pré-processados (por exemplo, conversão de strings e números).

## Análise Sintática: Parser com ply.yacc, validação da gramática.

A análise sintática é a etapa responsável por verificar se a sequência de tokens gerada pelo lexer está de acordo com as regras definidas pela gramática da linguagem. Para este fim, foi utilizada a biblioteca `ply.yacc`.

Esta biblioteca implementa um parser do tipo `LALR(1)` (Look-Ahead LR), capaz de processar uma ampla classe de gramáticas. 

### Validação da gramática

A validação da gramática é feita através da funções cujo nome começa com `p_`, por exemplo, `p_program` e `p_declarations`. Cada uma destas funções representa uma regra gramatical que especifica quais dos tokens e das sub-regras é que o programa espera, bem como a sua ordem. Durante a análise, o parser utiliza essas funções para verificar a conformidade do código com a gramática. Os eventuais erros sintáticos são capturados pela função `p_error`.

#### Regras gramaticais

Atendendo à extensão da gramática definida, não se procede à descrição exaustiva de todas as regras, focando-se este relatório naquelas que melhor exemplificam a estrutura e validação da linguagem.

##### p_program 

- Declaração da regra: 
```
program : PROGRAM ID SEMICOLON declarations BEGIN statements END DOT
```

- Esta regra significa que: 
    - O programa deve começar com a palavra `PROGRAM`, seguida de um `ID` e um `;`.
    - Seguem-se as `declarations` (declarações de variáveis, funções, etc).
    - A palavra `BEGIN`
    - Os `STATEMENTS` (instruções do programa)
    - E termine com a palavra `END` seguida de um `.`.

##### p_var_declarations

- Declaração da regra: 
```
var_declarations : id_list COLON type SEMICOLON 
                 | var_declarations id_list COLON type SEMICOLON 
```

- Esta regra define como podem ser feitas as declarações de variáveis no programa, existindo duas formas:

    - A forma simples: uma lista de identificadores (`id_list`), seguida de `:`, o tipo (`type`) e terminada com `;`. Esta forma é usada quando se declara apenas uma linha de variáveis.

    - A forma recursiva: permite declarar múltiplas variáveis, repetindo a estrutura anterior.

##### p_assignment

- Declaração da regra: 
```
assignment : ID ASSIGN expression 
           | ID LBRACKET expression_list RBRACKET ASSIGN expression
```

- Esta regra define a forma como são feitas as atribuições, isto é, quando se pretende associar o resultado de uma expressão a uma variável. Existem duas formas principais de atribuição:

    - Atribuição simples: consiste no `ID`, seguido do símbolo de atribuição (`ASSIGN`, ou seja, `:=`), e de uma expressão (`expression`).
    Exemplo: x := 10

    - Atribuição a um elemento de array: começa com o nome do array (`ID`), `[ ]` contendo a lista de expressões que representam os índices (`expression_list`), depois o símbolo de atribuição (`ASSIGN`) e por fim a expressão a atribuir.
    Exemplo: a[2] := 5

##### p_for_statement

- Declaração da regra: 
 
```
for_statement : FOR ID ASSIGN expression TO expression DO statement 
              | FOR ID ASSIGN expression DOWNTO expression DO statement
``` 
  
- Esta regra define um ciclo `for` que permite repetir um conjunto de instruções um determinado número de vezes. Existem dois tipos: 

  - `FOR...TO`: representa um ciclo crescente, em que a variável de controlo (`ID`) é inicializada com o valor de uma expressão e incrementada até atingir o valor final especificado após a palavra-chave `TO`.

  - `FOR...DOWNTO`: representa um ciclo decrescente, em que a variável de controlo é inicializada e decrementada até atingir o valor final especificado após a palavra-chave `DOWNTO`.

- Em ambos os casos, após a *keyword* `DO` é apresentada a instrução (`statement`) que deve ser executada durante as iterações do ciclo.

##### p_expression

- Declaração da regra:
```
expression : simple_expression 
           | simple_expression EQ simple_expression 
           | simple_expression NE simple_expression 
           | simple_expression LE simple_expression 
           | simple_expression GE simple_expression 
           | simple_expression GT simple_expression 
           | simple_expression ST simple_expression
```


- Esta regra define as expressões do programa. Estas expressões podem ser: 

  - Simples: correspondem a um valor ou cálculo representado por uma `simple_expression`.
  - Compostas: comparações entre expressões simples utilizando os seguintes operadores: `EQ` (igual), `NE` (diferente), `LE` (menor ou igual), `GE` (maior ou igual), `GT` (maior do que), `ST` (menor do que). Estas comparações avaliam a relação entre as duas expressões, retornando um valor booleano.

##### p_function_declarations

- Declaração da regra: 
```
function_declarations : FUNCTION ID LPAREN parameters RPAREN COLON type SEMICOLON BEGIN statements END SEMICOLON
```

- Esta regra define a sintaxe para a declaração de funções no programa, que consiste em: 
    - A palavra reservada `FUNCTION` seguida do nome da função (`ID`).
    - A lista de parâmetros da função (`parameters`) dentro de parênteses. 
    - Dois pontos `:` seguidos do tipo de retorno da função (`type`) e de um ponto e vírgula `;` para terminar a assinatura da função.
    - O corpo da função começa com a palavra `Begin` seguida das instruções (`statements`) e termina com a palavra `END` seguida de um `;`
 
Tal como foi dito anteriormente esta lista nao é exaustiva existindo ainda várias regras auxiliares para listas de identificadores, dimensões de arrays, blocos de instruções, entre outras, que ajudam a estruturar corretamente a gramática.

## Análise Semântica: Verificação de tipos, variáveis e coerência.
A análise semântica abrange verificação de tipos, *scope management* e acesso a arrays/strings.

### Declaração

#### Variáveis Simples 
- **Descrição**: Regista variáveis simples (ex.: `var x: integer`) no dicionário global `variables`, armazenando:
  - Tipo: `integer`, `real`, `boolean` ou `string`.
  - Valor Inicial: 0 para integer/real, `False` para boolean, `""` para string.
  - Índice de Memória: Atribuído sequencialmente via `memory_counter` (`base_index`).
 
- **Verificação Semântica**: Confirma se a variável está declarada antes de operações como atribuição, leitura ou escrita. Emite erros como Error: `Variable 'x' not declared` caso contrário.

#### Arrays 
- **Descrição**: Suporta arrays multidimensionais (ex.: `VAR arr: ARRAY[1..10, 1..5] OF REAL`). Calcula o tamanho total (produto das dimensões) e armazena em `variables`:
  - Tipo do elemento (`element_type`).
  - Dimensões (`dimensions`, com start e end).
  - Tamanho total (`total_size`) e índice base (`base_index`).
  
- **Inicialização**: Cada posição é inicializada com valores predefinidos (ex.: `0` para `integer`, `0.0` para `real`).
- **Verificação Semântica**: Valida dimensões declaradas e aloca memória suficiente. Emite erros se o array for acedido como variável simples (ex.: `Error: Cannot assign to array 'arr' directly`).

### Verificação de Tipos

#### Expressões
- **Descrição**: Analisa operações aritméticas (`+`, `-`, `*`, `/`, `div`, `mod`) e comparações (`=`, `<>`, `<=`, `>=`, `>`, `<`). Determina o tipo resultante:
  - `+`, `-`, `*`: Retorna real se algum operando for real, senão integer.
  - `/`: Sempre retorna real.
  - `div`, `mod`: Retorna integer.
  - comparações: Retorna boolean.
  
- **Verificação Semântica**: Gera instruções específicas (ex.: FADD para real, ADD para integer). Para strings em comparações, usa CHRCODE para converter a valores numéricos.

#### Atribuições
- **Descrição**: Processa atribuições como `x := 5` ou `arr[1] := 10`. Verifica a existência da variável/array e a compatibilidade de tipos.
- **Verificação Semântica**: Impede atribuições a arrays sem índices e valida o número de índices para arrays. Emite erros como `Error: Array 'arr' expects 1 indices, got 0`

#### Função LENGTH
- **Descrição**: Aplica-se a strings (ex.: `LENGTH("abc")`), retornando um integer com o comprimento.
- **Verificação Semântica**: Emite erro se o argumento não for string (`TypeError: LENGTH function applied to non-string type`).

### Acesso a Arrays e Strings

#### Arrays 
- Verifica o número de índices em relação às dimensões declaradas. Suporta índices constantes, emitindo erros para índices dinâmicos.
#### Strings 
- Valida o acesso a caracteres com um único índice, gerando código para `CHARAT`.

### Estruturas de Controlo

#### IF/WHILE/FOR 
- Assume que expressões em IF e WHILE são booleanas, sem validação explícita. Para FOR, verifica se a variável de controlo está declarada.

#### Entrada/Saída

- **WRITE/WRITELN**: Gera instruções (WRITEI, WRITEF, WRITES) com base no tipo da expressão.

- **READLN**: Converte entradas com ATOI/ATOF e valida a variável/array de destino.

### Erros Semânticos

- Emite erros para variáveis/funções não declaradas, tipos incompatíveis, índices incorretos e uso indevido de arrays/strings.

### Geração de Código

- **Descrição**: Gera instruções como `PUSHI, PUSHF, PUSHS, PUSHG, STOREG, ADD, FADD, JZ, JUMP, etc`. Usa `memory_counter` para alocar memória e stack para rastrear valores durante a geração.

- **Verificação Semântica**: Mantém coerência entre tipos das variáveis/expressões e instruções geradas, garantindo que operações como `FADD` sejam usadas para real e `ADD` para integer.

### Limitações

- **Verificação de Tipos Implícita**: Não valida explicitamente se expressões em IF/WHILE são booleanas, o que pode permitir erros.

- **Âmbito Global**: Variáveis são armazenadas globalmente em variables, sem suporte claro para variáveis locais em funções, o que pode causar conflitos de nomes.

- **Erro de Diagnóstico**: Algumas mensagens de erro são genéricas, dificultando a identificação precisa de problemas.

## Testes: Programas Pascal testados, validação de saídas.
Para além dos exemplos 1 a 6 do enunciado o compilador desenvolvido, mostrou-se capaz para os seguintes testes:
### Expressões aritméticas
Este excerto foi utilizado para testar a correta ordem de operações aritméticas, além da escrita das variáveis com `writeln`.

#### Input

    program Contas;
    var
        num1, num2: integer;
    begin
        writeln('Introduza dois números inteiros:');
        readln(num1);
        readln(num2);
        
        writeln(num1, '+', num1, '*', num2, '=', num1 + num1 * num2);
        writeln(num1, '*', num1, '+', num2, '=', num1 * num1 + num2);
    end.

#### Output

    START
    // Declaring variable num1 of type integer
    PUSHI 0     // Initialize num1 with 0
    STOREG 0  // Store in global position 0
    // Declaring variable num2 of type integer
    PUSHI 0     // Initialize num2 with 0
    STOREG 1  // Store in global position 1
    // WRITELN statement
    PUSHS "Introduza dois números inteiros:"         // Push string "Introduza dois números inteiros:"
    WRITES      // Write string
    WRITELN     // Print newline
    READ
    ATOI
    STOREG 0
    READ
    ATOI
    STOREG 1
    // WRITELN statement
    PUSHG 0      // Push variable num1
    WRITEI      // Write integer
    PUSHS "+"         // Push string "+"
    WRITES      // Write string
    PUSHG 0      // Push variable num1
    WRITEI      // Write integer
    PUSHS "*"         // Push string "*"
    WRITES      // Write string
    PUSHG 1      // Push variable num2
    WRITEI      // Write integer
    PUSHS "="         // Push string "="
    WRITES      // Write string
    PUSHG 0      // Push variable num1
    PUSHG 0      // Push variable num1
    PUSHG 1      // Push variable num2
    MUL         // Multiply integers
    ADD         // Add integers
    WRITEI      // Write integer
    WRITELN     // Print newline
    // WRITELN statement
    PUSHG 0      // Push variable num1
    WRITEI      // Write integer
    PUSHS "*"         // Push string "*"
    WRITES      // Write string
    PUSHG 0      // Push variable num1
    WRITEI      // Write integer
    PUSHS "+"         // Push string "+"
    WRITES      // Write string
    PUSHG 1      // Push variable num2
    WRITEI      // Write integer
    PUSHS "="         // Push string "="
    WRITES      // Write string
    PUSHG 0      // Push variable num1
    PUSHG 0      // Push variable num1
    MUL         // Multiply integers
    PUSHG 1      // Push variable num2
    ADD         // Add integers
    WRITEI      // Write integer
    WRITELN     // Print newline
    STOP

### Condicionais
Para testar os condicionais, para além dos exemplos do enunciado, foi utilizado este código com *if's* aninhados:

#### Input 
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

#### Output
    START
    // Declaring variable x of type integer
    PUSHI 0     // Initialize x with 0
    STOREG 0  // Store in global position 0
    // Assignment to x
    PUSHI 15         // Push integer 15
    STOREG 0  // Store value in variable x
    // IF statement
    PUSHG 0      // Push variable x
    PUSHI 10         // Push integer 10
    // Comparison operation: >
    SUP         // Check greater than
    JZ ENDIF1    // Jump to end if condition false
    // IF statement
    PUSHG 0      // Push variable x
    PUSHI 20         // Push integer 20
    // Comparison operation: <
    INF         // Check less than
    JZ ELSE0   // Jump to ELSE if condition false
    // WRITELN statement
    PUSHS "x está entre 10 e 20"         // Push string "x está entre 10 e 20"
    WRITES      // Write string
    WRITELN     // Print newline
    JUMP ENDIF0  // Skip ELSE part
    ELSE0:     // ELSE part
    // WRITELN statement
    PUSHS "x é maior ou igual a 20"         // Push string "x é maior ou igual a 20"
    WRITES      // Write string
    WRITELN     // Print newline
    ENDIF0:      // End of IF-ELSE
    ENDIF1:      // End of IF
    STOP


### Ciclos
Para teste do ciclo for com downto foi utilizado o seguinte código:
#### Input

    program testDownto;
    var
    i: integer;
    begin
        for i := 5 downto 1 do
            writeln(i);
    end.

#### Output

    START
    // Declaring variable i of type integer
    PUSHI 0     // Initialize i with 0
    STOREG 0  // Store in global position 0
    // FOR loop with variable i
    PUSHI 5         // Push integer 5
    STOREG 0        // Initialize loop variable
    WHILE0:       // Loop start
    PUSHI 1         // Push integer 1
    // Get end value
    PUSHG 0     // Get loop variable
    INFEQ       // Check if end <= var
    JZ ENDWHILE0  // Exit if condition false
    // WRITELN statement
    PUSHG 0      // Push variable i
    WRITEI      // Write integer
    WRITELN     // Print newline
    PUSHG 0     // Get loop variable
    PUSHI -1  // Increment/decrement
    ADD         // Update loop variable
    STOREG 0        // Store updated value
    JUMP WHILE0   // Jump back to condition
    ENDWHILE0:    // End of FOR loop
    STOP

### Teste de Erros Semânticos
Para testar os erros semanticos foi utilizado o seguinte programa:
#### Input

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

#### Output

    Error: Variable 'y' not declared
    Error: Cannot assign to array 'arr' directly
    TypeError: LENGTH function applied to non-string type 'integer'
    Error during processing: cannot unpack non-iterable NoneType object

### Teste Arrays
Para testar a atribuição e acesso ao arrays foi feito o seguinte teste:

#### Input 
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

#### Output 

    START
    // Declaring array vetor[3] of integer
    PUSHI 0     // Initialize vetor[0] with 0
    PUSHI 0     // Initialize vetor[1] with 0
    PUSHI 0     // Initialize vetor[2] with 0
    // Declaring variable i of type integer
    PUSHI 0     // Initialize i with 0
    STOREG 3  // Store in global position 3
    // Declaring variable soma of type integer
    PUSHI 0     // Initialize soma with 0
    STOREG 4  // Store in global position 4
    // Array assignment: vetor[1] := expression
    PUSHI 10         // Push integer 10
    STOREG 1      // Store value at vetor[1]
    // Array assignment: vetor[2] := expression
    PUSHI 5         // Push integer 5
    STOREG 2      // Store value at vetor[2]
    // Array assignment: vetor[3] := expression
    PUSHI 20         // Push integer 20
    STOREG 3      // Store value at vetor[3]
    // WRITELN statement
    PUSHS "vetor[1]: "         // Push string "vetor[1]: "
    WRITES      // Write string
    // Array access: vetor[1]
    PUSHG 1       // Push value at vetor[1]
    WRITEI      // Write integer
    WRITELN     // Print newline
    // WRITELN statement
    PUSHS "vetor[2]: "         // Push string "vetor[2]: "
    WRITES      // Write string
    // Array access: vetor[2]
    PUSHG 2       // Push value at vetor[2]
    WRITEI      // Write integer
    WRITELN     // Print newline
    // WRITELN statement
    PUSHS "vetor[3]: "         // Push string "vetor[3]: "
    WRITES      // Write string
    // Array access: vetor[3]
    PUSHG 3       // Push value at vetor[3]
    WRITEI      // Write integer
    WRITELN     // Print newline
    // Assignment to soma
    // Array access: vetor[1]
    PUSHG 1       // Push value at vetor[1]
    // Array access: vetor[3]
    PUSHG 3       // Push value at vetor[3]
    ADD         // Add integers
    STOREG 4  // Store value in variable soma
    // WRITELN statement
    PUSHS "Soma de vetor[1] e vetor[3]: "         // Push string "Soma de vetor[1] e vetor[3]: "
    WRITES      // Write string
    PUSHG 4      // Push variable soma
    WRITEI      // Write integer
    WRITELN     // Print newline
    STOP

# Conclusão: Resultados, desafios e melhorias futuras

O compilador desenvolvido mostrou-se funcional em múltiplos testes, incluindo programas com expressões aritméticas complexas, estruturas de controlo (`if`, `while`, `for`), operações com arrays e strings, e tratamento de erros semânticos.

## Resultados alcançados

- Foi possível compilar e gerar instruções para vários programas em Pascal.
- A geração de código demonstrou coerência com os tipos envolvidos, utilizando instruções específicas para `integer`, `real` e `string`.
- Foram identificados e reportados diversos erros semânticos com mensagens claras.

## Desafios encontrados

- **Acesso e verificação de strings**: Requereu lógica específica para operações como `LENGTH` e `CHARAT`.
- **Limitações no âmbito das variáveis**: A ausência de suporte a funções e tratamento específico para variáveis locais aumentou a complexidade da gestão de nomes.
- **Verificações booleanas implícitas**: Algumas condições (`if`, `while`) não são verificadas explicitamente quanto ao tipo booleano.

## Melhorias futuras

- Implementação de **funções e procedimentos** com âmbito local.
- Melhor **diagnóstico de erros**, com mensagens mais precisas e localizadas.
- Expansão da **verificação semântica** para incluir tipos em expressões condicionais.
- Introdução de **otimizações na geração de código** e suporte a tipos definidos pelo utilizador.

Este projeto permitiu um contacto prático com os principais conceitos de compiladores e consolidou o entendimento do processo de transformação de uma linguagem de alto nível em código executável.
