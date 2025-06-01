import ply.lex as lex
import sys

# Lista de tokens
tokens = [
    'ID', 'NUMBER', 'STRING',
    'GT', 'ST', 'ASSIGN', 'MULT', 'DIV', 'MOD',
    'LPAREN', 'RPAREN', 'DOTDOT', 'OF',
    'SEMICOLON', 'COLON', 'COMMA', 'DOT',
    'EQ', 'NE', 'LE', 'GE', 'PLUS', 'MINUS', 'NOT',
    'LBRACKET', 'RBRACKET',
    # Palavras reservadas
    'PROGRAM', 'VAR', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE',
    'WRITE', 'WRITELN', 'READLN',
    'INTEGER', 'REAL', 'FOR', 'TO', 'DO', 'WHILE', 'AND', 'BOOLEAN', 'ARRAY',
    'FUNCTION', 'TRUE', 'FALSE', 'DOWNTO', 'LENGTH', 'STRING_TYPE'
]

# Símbolos simples
t_ASSIGN    = r':='
t_MULT      = r'\*'
t_DOTDOT     = r'\.\.'
t_DOT       = r'\.'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_SEMICOLON = r';'
t_COLON     = r':'
t_COMMA     = r','
t_EQ        = r'='
t_NE        = r'<>'
t_LE        = r'<='
t_GE        = r'>='
t_GT        = r'>'
t_ST        = r'<'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'

# Palavras reservadas
def t_PROGRAM(t):
    r'[Pp]rogram'
    return t

def t_VAR(t):
    r'[Vv]ar'
    return t

def t_BEGIN(t):
    r'[Bb]egin'
    return t

def t_END(t):
    r'[Ee]nd'
    return t

def t_IF(t):
    r'[Ii]f'
    return t

def t_THEN(t):
    r'[Tt]hen'
    return t

def t_ELSE(t):
    r'[Ee]lse'
    return t

def t_WRITELN(t):
    r'[Ww]rite[Ll]n'
    return t

def t_WRITE(t):
    r'[Ww]rite'
    return t

def t_READLN(t):
    r'[Rr]ead[Ll]n'
    return t

def t_ARRAY(t):
    r'[Aa]rray'
    return t

def t_OF(t):
    r'[Oo]f'
    return t

def t_STRING_TYPE(t):
    r'[Ss]tring'
    return t

def t_INTEGER(t):
    r'[Ii]nteger'
    return t

def t_REAL(t):
    r'[Rr]eal'
    return t

def t_FOR(t):
    r'for'
    return t

def t_TO(t):
    r'to'
    return t

def t_DOWNTO(t):
    r'downto'
    return t

def t_DO(t):
    r'do'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_AND(t):
    r'and'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_LENGTH(t):
    r'length'
    return t

def t_DIV(t):
    r'div'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_NOT(t):
    r'not'
    return t

# Ignorar espaços e tabs
t_ignore = ' \t'

# Comentários 
def t_COMMENT(t):
    r'(\{[^}]*\})|\/\/.*'
    pass  # Ignora comentários

# Strings
def t_STRING(t):
    r'\'[^\']*\''
    t.value = f'"{t.value[1:-1]}"'
    return t

# Números (inteiros e reais)
def t_NUMBER(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Line {t.lexer.lineno}] Illegal character: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()