class Token:

    # gera a lista de tipos de tokens válidos definida em tokentypes.txt
    with open("tokentypes.txt") as file:
        types = file.read().split("\n")

    def __init__(self, token_type: str, value: str):
        if token_type not in Token.types: raise Exception("Tipo de Token inválido: %s" % token_type)
        self.type   : str = token_type  # tipo do Token, tal como inteiro, sinal de mais, etc.
        self.value  : str = value       # valor do Token, para inteiros, o número em si
    
