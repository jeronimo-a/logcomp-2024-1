import sys


def main():
    source = sys.argv[1]
    result = Parser.run(source)
    print(result)

class Token:

    def __init__(self, token_type: str, value: str):
        self.type   : str = token_type  # tipo do Token, tal como inteiro, sinal de mais, etc.
        self.value  : str = value       # valor do Token, para inteiros, o número em si


class Tokenizer:

    def __init__(self, source: str):
        self.source     : str   = source    # o código fonte
        self.position   : int   = 0         # posição atual que está sendo separada
        self.next       : Token = None      # o último token separado

    def over(self):
        return self.position == len(self.source)
    
    def select_next(self):

        token_value = str()
        token_type  = str()

        if self.over():
            self.next = Token("EOF", "")
            return

        # se for espaço, pula
        while self.source[self.position] == " ":
            self.position += 1
            if self.over():
                self.next = Token("EOF", "")
                return
        
        # se o caractere atual for um caractere numérico, concatena todos ao token_value até que não seja mais numérico
        while self.source[self.position].isnumeric():
            token_type       = "INT" 
            token_value     += self.source[self.position]
            self.position   += 1
            if self.over(): break
        
        # se o token já tiver sido definido como inteiro, cria o token e termina a função
        if token_type == "INT":
            self.next   = Token(token_type, token_value)
            return
        
        # se for mais, cria o token e termina a função
        if self.source[self.position] == "+":
            self.next        = Token("PLUS", "+")
            self.position   += 1
            return
        
        # se for menos, cria o token e termina a função
        if self.source[self.position] == "-":
            self.next        = Token("MINUS", "-")
            self.position   += 1
            return
        
        # se for vezes, cria o token e termina a função
        if self.source[self.position] == "*":
            self.next       = Token("MULT", "*")
            self.position  += 1
            return
        
        # se for divisão, cria o token e termina a função
        if self.source[self.position] == "/":
            self.next       = Token("DIV", "/")
            self.position  += 1
            return
        
        # se for abertura de parênteses, cria o token e termina a função
        if self.source[self.position] == "(":
            self.next       = Token("OPENPAR", "(")
            self.position  += 1
            return
        
        # se for fechamento de parênteses, cria o token e termina a função
        if self.source[self.position] == ")":
            self.next       = Token("CLOSEPAR", ")")
            self.position  += 1
            return
        
        # se chegou até aqui, o caractere não pertence ao alfabeto
        raise Exception("Erro léxico")


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

            # caso do lado esquerdo do diagrama
            if position == 0:

                # chama a subrotina parse term
                number = Parser.parse_term()

                # soma o valor de saída de term, levando em conta o último sinal
                accumulator += number * last_sign
                position     = 1                # atualiza a posição no diagrama
                continue
            
            # caso do lado direito do diagrama
            if position == 1:

                # processa o próximo token
                token = Parser.tokenizer.next
                
                # verifica se é um PLUS
                if token.type == "PLUS":
                    last_sign   = 1
                    position    = 0
                    continue

                # verifica se é um MINUS
                if token.type == "MINUS":
                    last_sign   = -1
                    position    = 0
                    continue

                # verifica se é um EOF
                if token.type == "EOF":
                    break
                
                # se chegou aqui, a expressão não é sintaticamente correta
                raise Exception("Erro de sintaxe")
            
        return accumulator
    

    @staticmethod
    def parse_term():
        '''
        Subrotina do parse expression que consome os tokens de multiplicação e divisão
        '''

        position       = 0      # posição no diagrama sintático, 0 para esquerda, 1 para direita
        accumulator    = 1      # variável de acumulação da multiplicação
        multiplication = True   # True para multiplicação, False para divisão

        while True:

            # processa o próximo token
            Parser.tokenizer.select_next()
            token = Parser.tokenizer.next

            # caso do lado esquerdo do diagrama
            if position == 0:

                # verifica se é um inteiro
                if token.type != "INT":
                    raise Exception("Número esperado")
                
                # multiplica ou divide o valor do inteiro à variável de acumulação
                if multiplication: accumulator *= int(token.value)
                else: accumulator = accumulator // int(token.value)
                position = 1    # atualiza a posição no diagrama
                continue
            
            # caso do lado direito do diagrama
            if position == 1:
                
                # verifica se é um MULT
                if token.type == "MULT":
                    multiplication = True
                    position       = 0
                    continue

                # verifica se é um DIV
                if token.type == "DIV":
                    multiplication = False
                    position       = 0
                    continue

                # verifica se é um EOF
                if token.type == "EOF":
                    break

                break
            
        return accumulator

    
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
    

if __name__ == "__main__":
    main()