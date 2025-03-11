import json
from datetime import datetime
import ply.lex as lex

STOCK_FILE = "stock.json"
COINS = {"1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1}

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'CODIGO',
    'VALOR',
    'PONTOS'	
)

t_ignore = " \t"

def t_LISTAR(t):
    r'LISTAR'
    return t

def t_MOEDA(t):
    r'MOEDA'
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    return t

def t_SAIR(t):
    r'SAIR'
    return t

def t_CODIGO(t):
    r'[A-Z]\d{2,3}'
    return t

def t_VALOR(t):
    r'\d+e|\d+c'
    return t

def t_PONTOS(t):
    r'\. \. \.'
    return t


def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def carregar_stock():
    try:
        with open(STOCK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_stock(stock):
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4)

def listar_produtos(stock):
    print("maq:")
    print("+------+---------------------+------------+-------+")
    print("| Cód  | Nome                | Quantidade | Preço |")
    print("+------+---------------------+------------+-------+")
    for produto in stock:
        print(f"| {produto['cod']:<4} | {produto['nome']:<19} | {produto['quant']:^10} | {produto['preco']:^5} |")
    print("+------+---------------------+------------+-------+")

def adicionar_moedas(moedas, saldo):
    for moeda in moedas:
        if moeda in COINS:
            saldo += COINS[moeda]
    return saldo

def selecionar_produto(stock, codigo, saldo):
    for produto in stock:
        if produto["cod"] == codigo:
            if produto["quant"] == 0:
                print("maq: Produto esgotado.")
                return saldo
            preco_cent = int(produto["preco"] * 100)
            if saldo >= preco_cent:
                produto["quant"] -= 1
                saldo -= preco_cent
                print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
            else:
                print(f"maq: Saldo insuficiente. Saldo = {saldo}c; Pedido = {preco_cent}c")
            return saldo
    print("maq: Produto inexistente.")
    return saldo

def calcular_troco(saldo):
    troco = {}
    for moeda, valor in COINS.items():
        while saldo >= valor:
            saldo -= valor
            troco[moeda] = troco.get(moeda, 0) + 1
    return troco

def processar_comando(comando, saldo, stock):
    lexer.input(comando)
    tokens = [tok for tok in lexer]
    
    
    if tokens and tokens[0].type == "PONTOS":
        print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
        return saldo
    
    if not tokens:
        return saldo

    if tokens[0].type == "LISTAR":
        listar_produtos(stock)
    elif tokens[0].type == "MOEDA":
        valores = [tok.value for tok in tokens[1:] if tok.type == "VALOR"]
        saldo = adicionar_moedas(valores, saldo)
        print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
    elif tokens[0].type == "SELECIONAR" and len(tokens) > 1:
        saldo = selecionar_produto(stock, tokens[1].value, saldo)
        print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
    elif tokens[0].type == "SAIR":
        troco = calcular_troco(saldo)
        troco_str = ", ".join([f"{v}x {k}" for k, v in troco.items()])
        print(f"maq: Pode retirar o troco: {troco_str}.")
        print("maq: Até à próxima")
        return -1
    
    return saldo

def main():
    stock = carregar_stock()
    print(f"maq: {datetime.today().strftime('%Y-%m-%d')}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    saldo = 0
    while True:
        comando = input(">> ").strip()
        saldo = processar_comando(comando, saldo, stock)
        if saldo == -1:
            break
    salvar_stock(stock)

if __name__ == "__main__":
    main()