# TPC1: Somador On/Off

- **Data:** 12 de fevereiro de 2025
- **Autor:** Carlos Eduardo Martins de Sá Fernandes :: A100890

<img src="../carlos.jpg" width=200px>

## Resumo
**O programa desenvolvido soma todas as sequências de dígitos que encontre num texto, somando apenas os valores encontrados quando a soma está ativada. Ele interpreta as strings "on" e "off" para controlar o estado da soma e exibe o resultado sempre que encontra o caráter "=".**

#### Exemplo:
##### Dado o seguinte input:
"10 20Off30 40On50=Off60On70="
##### O resultado será:
> 80
> 150<br>

#### Explicação:
No código, são iniciadas três variáveis principais: soma, que acumula a soma dos números encontrados no texto; i, que serve como índice para percorrer o texto; e flag, que indica se a soma está ativada (True para "on" e False para "off"). O ciclo principal percorre cada caráter do texto até o final. Durante esse processo, ele deteta diferentes comandos: se encontrar "on" (ignorando maiúsculas e minúsculas), ativa a flag (flag = True) e avança o índice em 2 posições; se encontrar "off", desativa a flag (flag = False) e avança o índice em 3 posições; se encontrar "=", escreve na saída a soma acumulada até o momento e avança o índice 1 posição. Quando a flag está ativa (flag == True) e o caráter atual é um dígito (in "0123456789"), o programa inicia a leitura de um número. Ele acumula os dígitos numa string e, enquanto o caráter atual for um dígito, continua a concatenar à string e a incrementar o índice. Após identificar o número completo, converte-o para inteiro e adiciona à soma (soma += int(digitos)). Se nenhuma das condições anteriores for atendida, o índice avança 1 posição.
Todo o código está devidamente comentado para garantir uma compreensão clara das implementações realizadas neste trabalho.

## Resultados
#### Ficheiro com programa e testes desenvolvidos
##### [somador_on_off.py](./somador_on_off.py)

#### Output do testes
##### [Output do texto 1](./resultados/output_texto1.png)
##### [Output do texto 2](./resultados/output_texto2.png)



