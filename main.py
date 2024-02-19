import sys

class Token:

    def __init__(self, token_type: str, value: str):
        self.type   : str = token_type  # tipo do Token, tal como inteiro, sinal de mais, etc.
        self.value  : str = value       # valor do Token, para inteiros, o número em si


class Tokenizer:

    def __init__(self, source: str):
        self.source     : str   = source    # o código fonte
        self.position   : int   = 0         # posição atual que está sendo separada
        self.next       : Token = None      # o último token separado
    
    def select_next(self):
        pass


class Parser:

    def __init__(self):
        self.tokenizer  : Tokenizer = None  # instância da classe Tokenizer que irá ler o código fonte e alimentar o Parser

    @staticmethod
    def parseExpression():
        pass

    @staticmethod
    def run(source: str):
        pass