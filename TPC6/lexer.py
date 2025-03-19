import ply.lex as lex

tokens = (
    'NUM',
    'PLUS',
    'MINUS',
    'TIMES'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
