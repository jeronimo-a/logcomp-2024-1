import sys

alphabet = "+-1234567890 "

def soma():

    try: input_string = sys.argv[1]     # extrai o argumento
    except IndexError: raise Exception  # se não houver argumento, dá erro

    # filtra os tokens desconhecidos
    for token in input_string:
        if token not in alphabet:
            raise Exception     # token desconhecido

    input_string = input_string.replace("+", " + ") # insere espaços no símbolo da soma, para remover casos tipo "1+1"
    input_string = input_string.replace("-", " - ") # insere espaços no símbolo da subtração, para remover casos tipo "1-1"
    elements = input_string.split(" ")              # divide a string em uma lista de elementos a partir dos espaços
    elements = [i for i in elements if i != ""]     # remove as strings vazias

    # a entrada deve ter um número ímpar de elementos
    # se o número for par, adiciona um elemento inválido
    if len(elements) % 2 == 0:
        elements.append("-")

    # verifica se o primeiro elemento é um número
    if not elements[0].isdigit():
        raise Exception
    
    soma = int(elements[0])                     # incializa o acumulável como o primeiro elemento
    for i in range(len(elements) - 1, 1, -2):   # itera sobre os elementos pares, que devem ser números

        signal = elements[i - 1]
        number = elements[i]
        
        # verifica a validade do sinal e do número
        if signal.isdigit() or not number.isdigit():
            raise Exception
        
        soma += int(signal + number)

    return soma


if __name__ == "__main__":
    print(soma())
