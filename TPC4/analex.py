import ply.lex as lex

# Lista de tokens
tokens = [
    "KEYWORD", "VARIABLE", "PREFIX", "STRING", "NUMBER", "DOT",
    "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COMMENT", "RDF_TYPE"
]

# Expressões regulares para tokens simples
t_KEYWORD = r'select|where|LIMIT'
t_VARIABLE = r'\?[a-zA-Z0-9_]+'  
t_PREFIX = r'[a-zA-Z]+:[a-zA-Z0-9_]+'  
t_STRING = r'"[^"]+"(@[a-zA-Z]+)?'  
t_NUMBER = r'\d+'  
t_DOT = r'\.'  
t_LPAREN = r'\('  
t_RPAREN = r'\)'  
t_LBRACE = r'\{'  
t_RBRACE = r'\}'  
t_RDF_TYPE = r'\ba\b'  # 'a' como RDF_TYPE

t_ignore = ' \t\r\n'

def t_COMMENT(t):
    r'\#.*'
    pass 

def t_error(t):
    print(f"Erro ao analisar o token: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(query):
    lexer.input(query)
    tokens = []
    for tok in lexer:
        tokens.append((tok.value, tok.type))
    return tokens

# Teste
query = """
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist .
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s .
?w foaf:name ?nome .
?w dbo:abstract ?desc
} LIMIT 1000
"""

tokens = tokenize(query)
for token in tokens:
    print(token)
