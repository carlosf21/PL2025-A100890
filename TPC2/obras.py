import re
import os

csv_file = "obras.csv"
resultado_dir = "resultados"

os.makedirs(resultado_dir, exist_ok=True)

def ler_csv(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()

def limpar_linhas(linhas):
    # junta linhas que pertencem à mesma entrada (quando começam com tabulação ou espaço)
    texto = "\n".join(linhas)
    entradas = re.split(r"\n(?=[^\t\s])", texto)
    return [re.sub(r"\n\s+", " ", entrada).strip() for entrada in entradas]

def dividir_linha(linha):
    # divide a linha considerando campos entre aspas como únicos
    pattern = r'"([^"]*)"|([^;]+)'
    return [match[0] if match[0] else match[1] for match in re.findall(pattern, linha)]

def validar_periodo(periodo):
    # verifica o período da obra
    return re.fullmatch(r"Medieval|Renascimento|Barroco|Clássico|Romântico|Século XX|Contemporâneo", periodo) is not None

def processar_csv(linhas):
    # obtém os índices das colunas necessárias
    header = dividir_linha(linhas[0].strip())
    idx_nome, idx_compositor, idx_periodo = header.index("nome"), header.index("compositor"), header.index("periodo")
    
    compositores = set()
    distribuicao_periodo = {}
    obras_por_periodo = {}
    
    for linha in linhas[1:]:
        # divide os campos da linha
        campos = dividir_linha(linha.strip())
        if len(campos) < len(header):
            continue
        
        compositor, nome, periodo = campos[idx_compositor].strip(), campos[idx_nome].strip(), campos[idx_periodo].strip()
        
        # verifica se o período é válido
        if not validar_periodo(periodo):
            continue
        
        # adiciona compositor à lista de compositores únicos
        compositores.add(compositor)
        
        # atualiza a contagem de obras por período
        distribuicao_periodo[periodo] = distribuicao_periodo.get(periodo, 0) + 1
        
        # adiciona o nome da obra ao respetivo período
        obras_por_periodo.setdefault(periodo, []).append(nome)
    
    return compositores, distribuicao_periodo, obras_por_periodo

def escrever_ficheiro(nome_ficheiro, conteudo):
    # escreve os dados processados num ficheiro .txt
    caminho_ficheiro = os.path.join(resultado_dir, nome_ficheiro)
    with open(caminho_ficheiro, "w", encoding="utf-8") as f:
        if isinstance(conteudo, list):
            f.write("\n".join(conteudo))
        elif isinstance(conteudo, dict):
            for chave, valor in conteudo.items():
                if isinstance(valor, int):
                    f.write(f"{chave}: {valor}\n")
                else:
                    f.write(f"{chave}:\n")
                    for item in sorted(valor):
                        f.write(f"  - {item}\n")
                    f.write("\n")

def main():
    linhas = ler_csv(csv_file)
    linhas_limpas = limpar_linhas(linhas)
    compositores, distribuicao_periodo, obras_por_periodo = processar_csv(linhas_limpas)
    
    escrever_ficheiro("compositores.txt", sorted(compositores))
    escrever_ficheiro("distribuicao_periodo.txt", distribuicao_periodo)
    escrever_ficheiro("obras_por_periodo.txt", obras_por_periodo)
    
    print(f"Resultados gerados na pasta '{resultado_dir}'.")

if __name__ == "__main__":
    main()
