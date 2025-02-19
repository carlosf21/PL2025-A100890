# TPC2: Análise de um dataset de obras musicais

- **Data:** 19 de fevereiro de 2025
- **Autor:** Carlos Eduardo Martins de Sá Fernandes :: A100890

<img src="../carlos.jpg" width=200px>

## Resumo

### Objetivo:
#### Ler o dataset `obras.csv`, processá-lo e criar os seguintes resultados:
#####  . Lista ordenada alfabeticamente dos compositores musicais;
#####  . Distribuição das obras por período: quantas obras catalogadas em cada período;
#####  . Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período.

### Explicação:
O código processa um dataset no formato CSV que contém informações sobre obras musicais e cria diversos resultados. Primeiramente, `ler_csv()` lê o ficheiro e retorna as linhas. Como algumas entradas podem ocupar várias linhas, `limpar_linhas()` une as que pertencem à mesma entrada, identificadas por tabulações ou espaços iniciais. A função `dividir_linha()` utiliza uma expressão regular para separar corretamente os campos, preservando valores entre aspas. Para validar os períodos musicais, `validar_periodo()` usa outra expressão regular, garantindo que apenas periodos reconhecidos sejam considerados. A função principal, `processar_csv()`, percorre os dados, extrai os compositores, distribui as obras por período e armazena as informações. Para o output, a `escrever_ficheiro()` gera três ficheiros: `compositores.txt` (lista de compositores ordenada), `distribuicao_periodo.txt` (contagem de obras por período) e `obras_por_periodo.txt` (obras organizadas por período).

## Resultados
#### [Lista de Resultados](./resultados)
##### [Lista ordenada alfabeticamente dos compositores musicais](./resultados/compositores.txt)
##### [Distribuição das obras por período: quantas obras catalogadas em cada período](./resultados/distribuicao_periodo.txt)
##### [Dicionário em que a cada período está a associada uma lista alfabética dos títulos das obras desse período](./resultados/obras_por_periodo.txt)


