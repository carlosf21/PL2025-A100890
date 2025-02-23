import re
import sys

def converter_md_para_html(markdown):
    # cabeçalhos
    markdown = re.sub(r'^# (.+)$', r'<h1>\1</h1>', markdown, flags=re.M)
    markdown = re.sub(r'^## (.+)$', r'<h2>\1</h2>', markdown, flags=re.M)
    markdown = re.sub(r'^### (.+)$', r'<h3>\1</h3>', markdown, flags=re.M)

    # bold
    markdown = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', markdown)
    
    # itálico
    markdown = re.sub(r'\*(.+?)\*', r'<i>\1</i>', markdown)

    # lista numerada
    markdown = re.sub(r'(?m)^\d+\.\s+(.+)$', r'<li>\1</li>', markdown)
    markdown = re.sub(r'(\n<li>.+?</li>)+', r'\n<ol>\g<0>\n</ol>', markdown)
    
    # link
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown)

    # imagem
    markdown = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', markdown)

    return markdown

def main(args):
    if len(args) == 2 and args[1].endswith(".md"):
        try:
            with open(args[1], "r", encoding="utf-8") as md_file:
                md = md_file.read()

            name = args[1].replace(".md", ".html")
            with open(name, "w", encoding="utf-8") as html_file:
                html_file.write(converter_md_para_html(md))
                print(f"HTML file saved as {name}")
        except FileNotFoundError:
            print("md file not found.")
    else:
        print("Usage: python conversor.py file.md")

if __name__ == "__main__":
    main(sys.argv)
