def somador_on_off(texto):
    soma = 0
    i = 0
    flag = True # True -> On, False -> Off

    while i < len(texto):
        if texto[i:i+2].lower() == "on": # lower() para funcionar em qualquer combinação de maiúsculas e minúsculas
            flag = True # ativa a flag
            i += 2 # avança 2 posições
        elif texto[i:i+3].lower() == "off":
            flag = False # desativa a flag
            i += 3 # avança 3 posições
        elif texto[i] == "=":
            print(f'> {soma}')
            i += 1
        elif flag and texto[i] in "0123456789": # se a flag estiver a True e o caráter for um dígito
            digitos = "" # incializa a string que acumula os digitos
            while i < len(texto) and texto[i] in "0123456789":
                digitos += texto[i] # adiciona o digito à string
                i += 1 # avança para o próximo caráter
            if digitos:
                soma += int(digitos) # coverte para int e soma
        else:
            i += 1 # avança para o próximo caráter se não for nenhum dos casos acima


# Testes
if __name__ == "__main__":
    texto1 = "10 20Off30 40On50=Off60On70="
    texto2 = "10abc20Off30xyz40On50=Off60On70=80On90Off100=110On120Off130On140=150Off160On170=180On190Off200=abc"
    #resultado = somador_on_off(texto1)
    resultado = somador_on_off(texto2)