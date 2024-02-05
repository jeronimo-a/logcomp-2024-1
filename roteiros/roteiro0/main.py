import sys

input_string = sys.argv[1]  # extrai o argumento

input_string = input_string.replace(" ", "")    # remove os espaços em branco
input_string = input_string.replace("+", " +")  # adiciona um espaço antes de cada operador de soma
input_string = input_string.replace("-", " -")  # adiciona um espaço antes de cada operador de subtração

tokens = input_string.split(" ")    # separa os números com seus respectivos sinais em itens de uma lista

soma = int(tokens[0])   # inicializa a variável acumuladora com o primeiro número, que é sempre positivo

for token in tokens[1:]:    # loop de soma de todos os tokens
    if token[0] == "+":         # se for positivo, soma
        soma += int(token[1:])
    elif token[0] == "-":       # se for negativo, subtrai
        soma -= int(token[1:])

print(soma)