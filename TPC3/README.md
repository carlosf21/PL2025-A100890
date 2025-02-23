# TPC3: Conversor de MarkDown para HTML

- **Data:** 23 de fevereiro de 2025
- **Autor:** Carlos Eduardo Martins de Sá Fernandes :: A100890

<img src="../carlos.jpg" width=200px>

## Resumo

O programa desenvolvido trata-se de um conversor de MarkDown para HTML para os elementos descritos na "Basic Syntax" da Cheat Sheet e funciona da seguinte forma:

1. **Cabeçalhos**: O padrão `^# (.+)$` captura linhas que começam com `#` (cabeçalho de nível 1) e transforma em `<h1>`. O `(.+)` captura o texto depois do `#`, e `\1` é utilizado para inseri-lo dentro da tag HTML. A flag `re.M` permite que o `^` e `$` funcionem para múltiplas linhas.

2. **Negrito**: O padrão `\*\*(.+?)\*\*` captura o texto entre `**`, substituindo por `<b>`.

3. **Itálico**: O padrão `\*(.+?)\*` captura o texto entre `*` (para itálico) e converte para `<i>`.

4. **Lista numerada**: O padrão `^\d+\.\s+(.+)$` captura itens de listas numeradas (ex: `1. item`) e os coloca-os em `<li>`. O grupo `(\n<li>.+?</li>)+` agrupa esses itens numa lista ordenada (`<ol>`).

5. **Links**: O padrão `\[(.*?)\]\((.*?)\)` captura links no formato `[texto](url)` e converte para `<a href="url">texto</a>`.

6. **Imagens**: O padrão `!\[(.*?)\]\((.*?)\)` captura imagens e converte para a tag `<img>`.

O programa lê um ficheiro Markdown passado como argumento, aplica estas substituições e guarda o resultado num ficheiro HTML:

> python conversor.py teste.md

## Lista de Resultados

O HTML resultante da conversão do ficheiro [teste.md](./teste.md) é o seguinte:
[teste.html](./teste.html)
