import re
import ply.yacc as yacc
from pascalLexer import tokens, lexer
import sys

# Estado global
stack = []
vm_code = ""
variables = {}
function_definitions = {}
current_if = 0
current_else = 0
current_loop = 0
memory_counter = 0

def reset_globals():
    global vm_code, stack, variables, function_definitions, current_if, current_else, current_loop
    vm_code = ""
    stack = []
    variables = {}
    function_definitions = {}
    current_if = 0
    current_else = 0
    current_loop = 0

def p_program(p):
    '''program : PROGRAM ID SEMICOLON declarations BEGIN statements END DOT'''
    code = "START\n"
    code += p[4] if p[4] else ""
    code += p[6] if p[6] else ""
    code += "STOP\n"
    p[0] = code

def p_declarations(p):
    '''declarations : VAR var_declarations
                    | function_declarations
                    | declarations var_declarations
                    | declarations function_declarations
                    | empty'''
    if len(p) == 2:
        p[0] = p[1] if p[1] else ""
    elif len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_var_declarations(p):
    '''var_declarations : id_list COLON type SEMICOLON
                        | var_declarations id_list COLON type SEMICOLON'''
    # Corrigido: processar todas as variáveis (simples e arrays) na ordem de declaração
    if len(p) == 5:
        prev_code = ""
        id_list = p[1]
        var_type = p[3]
    else:
        prev_code = p[1]
        id_list = p[2]
        var_type = p[4]
    code = prev_code

    for var_name in id_list:
        global memory_counter
        if isinstance(var_type, dict) and var_type.get("is_array"):
            # Array declaration
            array_info = var_type
            total_size = 1
            for dim in array_info["dimensions"]:
                total_size *= (dim["end"] - dim["start"] + 1)
            base_index = memory_counter
            memory_counter += total_size
            variables[var_name] = {
                "type": array_info["element_type"],
                "is_array": True,
                "dimensions": array_info["dimensions"],
                "total_size": total_size,
                "base_index": base_index
            }
            code += f"// Declaring array {var_name}[{total_size}] of {array_info['element_type']}\n"
            # Reserve each position as a global variable
            for i in range(total_size):
                if array_info['element_type'].lower() == "integer":
                    code += f"PUSHI 0     // Initialize {var_name}[{i}] with 0\n"
                elif array_info['element_type'].lower() == "real":
                    code += f"PUSHF 0.0   // Initialize {var_name}[{i}] with 0.0\n"
                elif array_info['element_type'].lower() == "boolean":
                    code += f"PUSHI 0     // Initialize {var_name}[{i}] with false\n"
        else:
            base_index = memory_counter
            memory_counter += 1
            if var_type.lower() == "string":
                variables[var_name] = {"type": "string", "value": "", "base_index": base_index}
                code += f"// Declaring variable {var_name} of type string\n"
                code += f"PUSHS \"\"     // Initialize {var_name} with empty string\n"
                code += f"STOREG {base_index}  // Store in global position {base_index}\n"
            else:
                variables[var_name] = {"type": var_type, "value": 0 if var_type.lower() in ["integer", "real"] else False, "base_index": base_index}
                code += f"// Declaring variable {var_name} of type {var_type}\n"
                if var_type.lower() == "integer":
                    code += f"PUSHI 0     // Initialize {var_name} with 0\n"
                    code += f"STOREG {base_index}  // Store in global position {base_index}\n"
                elif var_type.lower() == "real":
                    code += f"PUSHF 0.0   // Initialize {var_name} with 0.0\n"
                    code += f"STOREG {base_index}  // Store in global position {base_index}\n"
                elif var_type.lower() == "boolean":
                    code += f"PUSHI 0     // Initialize {var_name} with false\n"
                    code += f"STOREG {base_index}  // Store in global position {base_index}\n"
    p[0] = code

def p_id_list(p):
    '''id_list : ID
               | id_list COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type(p):
    '''type : INTEGER
            | REAL
            | BOOLEAN
            | array_type
            | STRING_TYPE'''
    p[0] = p[1]

def p_array_type(p):
    '''array_type : ARRAY LBRACKET array_dimensions RBRACKET OF type'''
    p[0] = {
        "is_array": True,
        "dimensions": p[3],
        "element_type": p[6]
    }

def p_array_dimensions(p):
    '''array_dimensions : array_dimension
                        | array_dimensions COMMA array_dimension'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_array_dimension(p):
    '''array_dimension : NUMBER DOTDOT NUMBER'''
    p[0] = {"start": p[1], "end": p[3]}

def p_function_declarations(p):
    '''function_declarations : FUNCTION ID LPAREN parameters RPAREN COLON type SEMICOLON BEGIN statements END SEMICOLON'''
    func_name = p[2]
    params = p[4]
    return_type = p[7]
    body = p[10]
    function_definitions[func_name] = {"params": params, "return_type": return_type, "body": body}
    code = f"// Function {func_name} definition\n"
    code += f"{func_name}:\n"
    code += body
    code += f"RETURN      // End of function {func_name}\n"
    p[0] = code

def p_parameters(p):
    '''parameters : ID COLON type
                  | parameters SEMICOLON ID COLON type
                  | empty'''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    elif len(p) == 6:
        p[0] = p[1] + [(p[3], p[5])]
    else:
        p[0] = []

def p_statements(p):
    '''statements : statement
                  | statements SEMICOLON statement'''
    if len(p) == 2:
        p[0] = p[1] if p[1] else ""
    else:
        p[0] = p[1] + p[3] if p[3] else p[1]

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | for_statement
                 | write_statement
                 | writeln_statement
                 | readln_statement
                 | function_call
                 | block_statement
                 | empty'''
    p[0] = p[1] if p[1] else ""

def p_block_statement(p):
    '''block_statement : BEGIN statements END'''
    p[0] = p[2] if p[2] else ""

def p_assignment(p):
    '''assignment : ID ASSIGN expression
                  | ID LBRACKET expression_list RBRACKET ASSIGN expression'''
    if len(p) == 4:
        var_name = p[1]
        if var_name not in variables:
            print(f"Error: Variable '{var_name}' not declared")
            return

        if variables[var_name].get("is_array"):
            print(f"Error: Cannot assign to array '{var_name}' directly")
            return

        var_index = variables[var_name]["base_index"]
        var_type = variables[var_name]["type"]
        expr_code, _ = p[3]
        code = f"// Assignment to {var_name}\n"
        code += expr_code
        if var_type.lower() in ["integer", "real", "boolean"]:
            code += f"STOREG {var_index}  // Store value in variable {var_name}\n"
        variables[var_name]["value"] = stack.pop() if stack else None
        p[0] = code
    else:
        #-------------------ARRAY-------------------
        var_name = p[1]
        if var_name not in variables:
            print(f"Error: Variable '{var_name}' not declared")
            return

        if not variables[var_name].get("is_array"):
            print(f"Error: '{var_name}' is not an array")
            return

        array_info = variables[var_name]
        indices_code, indices_count = build_index_code(p[3])
        expr_code, expr_type = p[6]

        if indices_count != len(array_info["dimensions"]):
            print(f"Error: Array '{var_name}' expects {len(array_info['dimensions'])} indices, got {indices_count}")
            return

        # Tenta calcular o índice linear em tempo de compilação
        match = re.search(r'PUSHI (\-?\d+)', indices_code.strip().splitlines()[-1]) if indices_code.strip() else None
        if match:
            # Índice constante
            linear_index = int(match.group(1))
            global_index = array_info["base_index"] + linear_index
            code = f"// Array assignment: {var_name}[{linear_index}] := expression\n"
            code += expr_code  # valor a guardar
            code += f"STOREG {global_index}      // Store value at {var_name}[{linear_index}]\n"
        else:
            # Índice dinâmico não suportado diretamente
            code = f"// ERRO: Atribuição dinâmica a array não suportada nesta VM\n"
            code += f"// Só é possível atribuir arrays com índice constante\n"
        p[0] = code

def build_index_code(expr_list):
    """
    Gera apenas o código para calcular o índice linear de arrays, sem WRITEI, etc.
    expr_list é o que vem de expression_list, ou seja, (code, count)
    """
    # expr_list pode ser (code, count) ou só code
    # Remove qualquer instrução WRITEI/WRITEF/WRITES do código de índices
    if isinstance(expr_list, tuple):
        code = expr_list[0]
        # Remove linhas de escrita
        code = "\n".join(
            line for line in code.splitlines()
            if not line.strip().startswith(("WRITEI", "WRITEF", "WRITES"))
        )
        return code, expr_list[1]
    return expr_list, 1

def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    global current_if, current_else
    expr_code, _ = p[2]
    then_code = p[4]
    code = f"// IF statement\n"
    code += expr_code

    if len(p) == 5:
        # Only "if ... then"
        label_end = f"ENDIF{current_if}"
        code += f"JZ {label_end}    // Jump to end if condition false\n"
        code += then_code
        code += f"{label_end}:      // End of IF\n"
        current_if += 1
    else:
        # "if ... then ... else ..."
        label_else = f"ELSE{current_else}"
        label_end = f"ENDIF{current_if}"
        else_code = p[6]
        code += f"JZ {label_else}   // Jump to ELSE if condition false\n"
        code += then_code
        code += f"JUMP {label_end}  // Skip ELSE part\n"
        code += f"{label_else}:     // ELSE part\n"
        code += else_code
        code += f"{label_end}:      // End of IF-ELSE\n"
        current_if += 1
        current_else += 1

    p[0] = code

def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    global current_loop
    expr_code, _ = p[2]
    stmt = p[4]
    code = f"// WHILE loop {current_loop}\n"
    code += f"WHILE{current_loop}:       // Loop start\n"
    code += expr_code
    code += f"JZ ENDWHILE{current_loop}  // Exit if condition false\n"
    code += stmt
    code += f"JUMP WHILE{current_loop}   // Jump back to condition\n"
    code += f"ENDWHILE{current_loop}:    // End of loop\n"
    current_loop += 1
    p[0] = code

def p_for_statement(p):
    '''for_statement : FOR ID ASSIGN expression TO expression DO statement
                     | FOR ID ASSIGN expression DOWNTO expression DO statement'''
    global current_loop, variables
    var_name = p[2]
    if var_name not in variables:
        print(f"Error: Variable '{var_name}' not declared")
        return
    var_index = list(variables.keys()).index(var_name)
    start_code, _ = p[4]
    end_code, _ = p[6]
    stmt = p[8]
    direction = p[5].lower()
    
    code = f"// FOR loop with variable {var_name}\n"
    code += start_code
    code += f"STOREG {var_index}        // Initialize loop variable\n"
    code += f"WHILE{current_loop}:       // Loop start\n"
    
    if direction == "to":
        code += f"PUSHG {var_index}     // Get loop variable\n"
        code += end_code + "// Get end value\n"
        code += f"INFEQ       // Check if var <= end\n"
    else:  # downto
        code += end_code + "// Get end value\n"
        code += f"PUSHG {var_index}     // Get loop variable\n"
        code += f"INFEQ       // Check if end <= var\n"
    
    code += f"JZ ENDWHILE{current_loop}  // Exit if condition false\n"
    code += stmt
    code += f"PUSHG {var_index}     // Get loop variable\n"
    code += f"PUSHI {'1' if direction == 'to' else '-1'}  // Increment/decrement\n"
    code += f"ADD         // Update loop variable\n"
    code += f"STOREG {var_index}        // Store updated value\n"
    code += f"JUMP WHILE{current_loop}   // Jump back to condition\n"
    code += f"ENDWHILE{current_loop}:    // End of FOR loop\n"
    current_loop += 1
    p[0] = code

def p_write_statement(p):
    '''write_statement : WRITE LPAREN expression_list RPAREN'''
    code, _ = p[3]
    p[0] = f"// WRITE statement\n" + code

def p_writeln_statement(p):
    '''writeln_statement : WRITELN LPAREN expression_list RPAREN'''
    code, _ = p[3]
    code += f"WRITELN     // Print newline\n"
    p[0] = f"// WRITELN statement\n" + code

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    code = ""
    count = 0
    
    if len(p) == 2:
        expr_code, expr_type = p[1]
        code += expr_code
        if expr_type == "integer":
            code += f"WRITEI      // Write integer\n"
        elif expr_type == "real":
            code += f"WRITEF      // Write real\n"
        elif expr_type == "string":
            code += f"WRITES      // Write string\n"
        elif expr_type == "boolean":
            code += f"WRITEI      // Write boolean as integer\n"
        else:
            # Default case - try to determine type from stack
            top_value = stack[-1] if stack else None
            if isinstance(top_value, int):
                code += f"WRITEI      // Write integer (inferred)\n"
            elif isinstance(top_value, float):
                code += f"WRITEF      // Write real (inferred)\n"
            elif isinstance(top_value, str):
                code += f"WRITES      // Write string (inferred)\n"
            elif isinstance(top_value, bool):
                code += f"WRITEI      // Write boolean as integer (inferred)\n"
        stack.pop() if stack else None
        count = 1
    else:
        list_code, list_count = p[1]
        expr_code, expr_type = p[3]
        code += list_code + expr_code
        if expr_type == "integer":
            code += f"WRITEI      // Write integer\n"
        elif expr_type == "real":
            code += f"WRITEF      // Write real\n"
        elif expr_type == "string":
            code += f"WRITES      // Write string\n"
        elif expr_type == "boolean":
            code += f"WRITEI      // Write boolean as integer\n"
        else:
            # Default case
            top_value = stack[-1] if stack else None
            if isinstance(top_value, int):
                code += f"WRITEI      // Write integer (inferred)\n"
            elif isinstance(top_value, float):
                code += f"WRITEF      // Write real (inferred)\n"
            elif isinstance(top_value, str):
                code += f"WRITES      // Write string (inferred)\n"
            elif isinstance(top_value, bool):
                code += f"WRITEI      // Write boolean as integer (inferred)\n"
        stack.pop() if stack else None
        count = list_count + 1
    p[0] = (code, count)

def p_readln_statement(p):
    '''readln_statement : READLN LPAREN ID RPAREN
                        | READLN LPAREN ID LBRACKET expression_list RBRACKET RPAREN'''
    global variables
    code = ""
    var_name = p[3]

    if var_name not in variables:
        print(f"Error: Variable '{var_name}' not declared")
        p[0] = ""
        return

    var_info = variables[var_name]
    var_type = var_info["type"]

    code += f"READ\n"
    #code += f"DUP 1\n"
    #code += f"WRITES\nWRITELN     // Print prompt for input\n"

    if var_type.lower() == "integer":
        code += f"ATOI\n"
    elif var_type.lower() == "real":
        code += f"ATOF\n"
    elif var_type.lower() == "boolean":
        code += f"ATOI\n"
        

    if len(p) == 5:
        if var_info.get("is_array"):
            print(f"Error: '{var_name}' is an array, but accessed as a simple variable.")
            p[0] = ""
            return
        
        var_index = var_info["base_index"]
        code += f"STOREG {var_index}\n"
        
    #-------------------ARRAY-------------------
    else:
        if not var_info.get("is_array"):
            print(f"Error: '{var_name}' is not an array, but accessed with indices.")
            p[0] = ""
            return
        
        indices_code, indices_count = build_index_code(p[5])
        dimensions = var_info["dimensions"]

        if indices_count != len(dimensions):
            print(f"Error: Incorrect number of dimensions for array '{var_name}'. Expected {len(dimensions)}, got {indices_count}.")
            p[0] = ""
            return

        # Tenta calcular o índice linear em tempo de compilação
        match = re.search(r'PUSHI (\-?\d+)', indices_code.strip().splitlines()[-1]) if indices_code.strip() else None
        if match:
            linear_index = int(match.group(1))
            global_index = var_info["base_index"] + linear_index
            code += f"// Array readln: {var_name}[{linear_index}]\n"
            code += f"STOREG {global_index}      // Store value at {var_name}[{linear_index}]\n"
        else:
            pass
        
    p[0] = code

def p_function_call(p):
    '''function_call : ID LPAREN arguments RPAREN'''
    func_name = p[1]
    args = p[3]
    if func_name not in function_definitions:
        print(f"Error: Function '{func_name}' not declared")
        return
    code = f"// Function call: {func_name}\n"
    code += args + "// Arguments prepared\n"
    code += f"PUSHA {func_name}     // Push function address\n"
    code += f"CALL        // Call function\n"
    p[0] = (code, "unknown")

def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression
                 | empty'''
    if len(p) == 2:
        if p[1]:
            code, _ = p[1]
            p[0] = code
        else:
            p[0] = ""
    else:
        arg_code, _ = p[1]
        expr_code, _ = p[3]
        p[0] = arg_code + expr_code

def p_expression(p):
    '''expression : simple_expression
                  | simple_expression EQ simple_expression
                  | simple_expression NE simple_expression
                  | simple_expression LE simple_expression
                  | simple_expression GE simple_expression
                  | simple_expression GT simple_expression
                  | simple_expression ST simple_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        code1, type1 = p[1]
        code2, type2 = p[3]
        code = code1 + code2
        op = p[2]
        expr_type = "boolean"
        is_float = type1 == "real" or type2 == "real"
        
        code += f"// Comparison operation: {op}\n"
        if type1 == "string":
            code += f"CHRCODE\n"
        if type2 == "string":
            code += f"CHRCODE\n"
        if op == '=':
            code += f"EQUAL       // Check equality\n"
        elif op == '<>':
            code += f"EQUAL       // Check equality\n"
            code += f"PUSHI 1     // Push 1\n"
            code += f"SUB         // Negate result (not equal)\n"
        elif op == '<=':
            code += f"INFEQ       // Check less or equal\n"
        elif op == '>=':
            code += f"SUPEQ       // Check greater or equal\n"
        elif op == '>':
            code += f"SUP         // Check greater than\n"
        elif op == '<':
            code += f"INF         // Check less than\n"
        stack.append(None)
        p[0] = (code, expr_type)

def p_simple_expression(p):
    '''simple_expression : term
                         | simple_expression PLUS term
                         | simple_expression MINUS term
                         | simple_expression AND term
                         | NOT simple_expression'''
    if len(p) == 2:
        # Caso simples: apenas um termo
        p[0] = p[1]
    else:
        if p[1] == 'not':
            code, typ = p[2]
            code += "NOT         // Logical NOT\n"
            p[0] = (code, "boolean")
        else:
            code1, type1 = p[1]
            code2, type2 = p[3]
            code = code1 + code2
            op = p[2]
            expr_type = "unknown"

            if op == '+':
                if type1 == "real" or type2 == "real":
                    code += "FADD        // Add real numbers\n"
                    expr_type = "real"
                else:
                    code += "ADD         // Add integers\n"
                    expr_type = "integer"
            elif op == '-':
                if type1 == "real" or type2 == "real":
                    code += "FSUB        // Subtract real numbers\n"
                    expr_type = "real"
                else:
                    code += "SUB         // Subtract integers\n"
                    expr_type = "integer"
            elif op == 'and':
                code += "AND         // Logical AND\n"
                expr_type = "boolean"

            p[0] = (code, expr_type)

def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor
            | term MOD factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        code1, type1 = p[1]
        code2, type2 = p[3]
        code = code1 + code2
        op = p[2]
        expr_type = "unknown"
        
        if op == '*':
            if type1 == "real" or type2 == "real":
                code += f"FMUL        // Multiply real numbers\n"
                expr_type = "real"
            else:
                code += f"MUL         // Multiply integers\n"
                expr_type = "integer"
        elif op == '/':
            code += f"FDIV        // Divide (real result)\n"
            expr_type = "real"
        elif op == 'div':
            code += f"DIV         // Integer division\n"
            expr_type = "integer"
        elif op == 'mod':
            code += f"MOD         // Modulo operation\n"
            expr_type = "integer"
        stack.append(None)
        p[0] = (code, expr_type)

def p_indexed_access(p):
    '''indexed_access : ID LBRACKET expression_list RBRACKET'''
    var_name = p[1]
    
    if var_name not in variables:
        print(f"Error: Variable '{var_name}' not declared")
        p[0] = ("", "error")
        return

    var_info = variables[var_name]
    indices_code, indices_count = build_index_code(p[3]) # p[3] contains (code, count) from expression_list

    if var_info.get("is_array", False):
        # Handle ARRAY access
        dimensions = var_info["dimensions"]
        if indices_count != len(dimensions):
            print(f"Error: Array '{var_name}' expects {len(dimensions)} indices, got {indices_count}")
            p[0] = ("", "error")
            return

        match = re.search(r'PUSHI (\-?\d+)', indices_code.strip().splitlines()[-1]) if indices_code.strip() else None

        if match:
            # Constant index
            linear_index = int(match.group(1))
            global_index = var_info["base_index"] + linear_index
            code = f"// Array access: {var_name}[{linear_index}]\n"
            code += f"PUSHG {global_index}       // Push value at {var_name}[{linear_index}]\n"
        else:
            code = f"// Array access with dynamic index for {var_name}\n"
            code += indices_code 
            code += f"// Placeholder for dynamic array access. Need specific VM instruction.\n"
            code += f"// PUSHG {var_info['base_index']} // Base address (for example)\n"
            p[0] = ("", "error")
            return
            
        p[0] = (code, var_info["type"]) # Return code and element type of the array

    elif var_info["type"].lower() == "string":
        # Handle STRING character access
        if indices_count != 1:
            print(f"Error: String '{var_name}' expects a single index, got {indices_count}")
            p[0] = ("", "error")
            return

        # Generate: string, index, PUSHI 1, SUB, CHARAT
        code = f"// Access string char {var_name}[expr]\n"
        code += f"PUSHG {var_info['base_index']}   // Push string base\n"
        code += indices_code # This is the code for the single index expression
        code += '\nPUSHI 1\nSUB          // convert to 0-based\n'
        code += f"CHARAT         // returns ASCII of char\n"
        p[0] = (code, "integer")

    else:
        print(f"Error: Variable '{var_name}' is not an array or string, but accessed with indices.")
        p[0] = ("", "error")

def p_factor(p):
    '''factor : NUMBER
              | LPAREN expression RPAREN
              | TRUE
              | FALSE
              | ID
              | STRING
              | LENGTH LPAREN expression RPAREN
              | function_call
              | indexed_access''' 
    
    if len(p) == 2:
        # Handle NUMBER, TRUE, FALSE, ID, STRING, function_call
        if isinstance(p[1], bool):
            code = f"PUSHI {1 if p[1] else 0}      // Push boolean {p[1]}\n"
            expr_type = "boolean"
        elif isinstance(p[1], (int, float)): # NUMBER could be int or float
            if isinstance(p[1], int):
                code = f"PUSHI {p[1]}         // Push integer {p[1]}\n"
                expr_type = "integer"
            else:
                code = f"PUSHF {p[1]}         // Push real {p[1]}\n"
                expr_type = "real"
        elif isinstance(p[1], str):
            if p[1].startswith('"') and p[1].endswith('"'): # STRING literal
                code = f"PUSHS {p[1]}         // Push string {p[1]}\n"
                expr_type = "string"
            elif p[1] in variables: # Variable access (simple ID)
                var_info = variables[p[1]]
                if var_info.get("is_array"):
                    # This case should ideally not be hit if indexed_access is used for arrays
                    # but it's a good safeguard for non-indexed array usage.
                    print(f"Error: Cannot use array '{p[1]}' without indices")
                    return ("", "error") # Indicate an error
                var_index = var_info["base_index"]
                var_type = var_info["type"]
                code = f"PUSHG {var_index}      // Push variable {p[1]}\n"
                expr_type = var_type.lower()
            else:
                print(f"Error: Variable '{p[1]}' not declared")
                return ("", "error")
        elif isinstance(p[1], tuple): # This handles function_call and now indexed_access
            code, expr_type = p[1]
        else:
            print(f"SyntaxError: Unknown factor type for {p[1]}")
            return ("", "error")
        p[0] = (code, expr_type)

    elif len(p) == 4 and p[1] == '(' and p[3] == ')': # Parenthesized expression
        code, expr_type = p[2]
        code = f"// Parenthesized expression\n" + code
        p[0] = (code, expr_type)

    elif len(p) == 5 and p[1].lower() == 'length': # LENGTH function
        code, typ = p[3]
        if typ != 'string':
            print(f"TypeError: LENGTH function applied to non-string type '{typ}'")
            return ("", "error")
        code += "STRLEN          // Get length of string\n"
        p[0] = (code, 'integer')
    
    elif len(p) == 3:
        print("Warning: unexpected len 3 in factor rule, likely a misplaced 'NOT'")
        p[0] = (p[1], "unknown") # Fallback

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}: '{p.value}'")
    else:
        print("Syntax error: unexpected end of input")
    parser.errok()

parser = yacc.yacc()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.pas> [output_file.vm]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit('.', 1)[0] + '.vm'
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            pascal_code = f.read()
        global vm_code
        vm_code = ""
        result = parser.parse(pascal_code, lexer=lexer)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result if result else vm_code)
        print(f"VM code successfully written to {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()