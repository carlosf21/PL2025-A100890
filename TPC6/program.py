from parser import parser

def evaluate(expression):
    return parser.parse(expression)

if __name__ == "__main__":
    expr = input("Introduza uma expressão: ")
    try:
        result = evaluate(expr)
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"Erro: {e}")
