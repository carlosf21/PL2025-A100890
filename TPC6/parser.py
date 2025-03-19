import ply.yacc as yacc
from lexer import tokens

def print_recognized(token_type, token_value):
    print(f"Reconhecido {token_type}: {token_value}")
    
def p_expression_plus(p):
    "expression : expression PLUS term"
    print_recognized("PLUS", p[2])
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    "expression : expression MINUS term"
    print_recognized("MINUS", p[2])
    p[0] = p[1] - p[3]

def p_expression_term(p):
    "expression : term"
    p[0] = p[1]

def p_term_times(p):
    "term : term TIMES factor"
    print_recognized("TIMES", p[2])
    p[0] = p[1] * p[3]

def p_term_factor(p):
    "term : factor"
    p[0] = p[1]

def p_factor_num(p):
    "factor : NUM"
    print_recognized("NUM", p[1])
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe! Token inesperado: {p.type} ({p.value})")
    else:
        print("Erro de sintaxe! Fim inesperado do input.")

parser = yacc.yacc()
