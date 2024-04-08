import utils

class Token:

    # gera as listas de tipos de tokens existentes e palavras reservadas
    types, reserved_words = utils.read_token_types_file("alphabet.txt")

    def __init__(self, token_type: str, value: str):
        if token_type not in Token.types: raise Exception("Tipo de Token inválido: %s" % token_type)
        self.type   : str = token_type  # tipo do Token, tal como inteiro, sinal de mais, etc.
        self.value  : str = value       # valor do Token, para inteiros, o número em si
