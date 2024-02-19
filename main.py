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

    tokenizer : Tokenizer = None    # instância da classe Tokenizer que irá ler o código fonte e alimentar o Parser

    @staticmethod
    def parse_expression():
        '''
        Consome os tokens do Tokenizer
        Analisa se a sintaxe está aderente à gramática
        Retorna o resultado da expressão analisada
        '''

        position    = 0         # posição no diagrama sintático, 0 para esquerda, 1 para direita
        accumulator = 0         # variável de acumulação da soma
        last_sign   = 1         # último sinal lido, 1 para mais, -1 para menos

        while True:

            # processa o próximo token
            Parser.tokenizer.select_next()
            token = Parser.tokenizer.next

            # caso do lado esquerdo do diagrama
            if position == 0:

                # verifica se é um inteiro
                if token.type != "INT":
                    raise Exception("Número esperado")
                
                # soma o valor do inteiro à varíavel, levando em conta o último sinal
                accumulator += int(token.value) * last_sign
                
                accumulator += int(token.value) # soma o valor do inteiro à variável acumuladora
                position     = 1                # atualiza a posição no diagrama
                continue
            
            # caso do lado direito do diagrama
            if position == 1:
                
                # verifica se é um PLUS
                if token.type == "PLUS":
                    last_sign   = 1
                    position    = 0

                # verifica se é um MINUS
                if token.type == "MINUS":
                    last_sign   = -1
                    position    = 0

                # verifica se é um EOF
                if token.type == "EOF":
                    break

                # se chegou aqui, a expressão não é sintaticamente correta
                raise Exception("Erro de sintaxe")

    
    @staticmethod
    def run(source: str):
        '''
        Recebe o código fonte como argumento
        Inicializa uma instância de Tokenizador
        Posiciona o Tokenizer no primeiro token (feito no inicializador de Tokenizer)
        Verifica se a cadeia foi consumida por completo
        Retorna o resultado do método "parse_expression"
        '''
        Parser.tokenizer = Tokenizer(source)
        result = Parser.parse_expression()

        if (Parser.tokenizer.next.type != "EOF"):
            raise Exception("Erro de sintaxe")
        
        return result