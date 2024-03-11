from langtokenizer import Tokenizer
from langprepro import PrePro

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
                    Parser.tokenizer.select_next()
                    last_sign   = 1
                    position    = 0
                    continue

                # verifica se é um MINUS
                if token.type == "MINUS":
                    Parser.tokenizer.select_next()
                    last_sign   = -1
                    position    = 0
                    continue

                # verifica se é um fechamento de parênteses
                if token.type == "CLOSEPAR":
                    break

                # verifica se é um EOF
                if token.type == "EOF":
                    break
                
                # se chegou aqui, a expressão não é sintaticamente correta
                raise Exception("Erro de sintaxe")
        
        return accumulator
    

    @staticmethod
    def parse_term():
        '''
        Subrotina do parse expression
        Consome os tokens de multiplicação e divisão
        '''

        position       = 0      # posição no diagrama sintático, 0 para esquerda, 1 para direita
        accumulator    = 1      # variável de acumulação da multiplicação
        multiplication = True   # True para multiplicação, False para divisão

        while True:

            # caso do lado esquerdo do diagrama
            if position == 0:

                # chama a subrotina parse factor
                number = Parser.parse_factor()

                # multiplica o valor de saída de factor, levando em conta a operação
                if multiplication: accumulator *= number
                else: accumulator = accumulator // number
                position = 1    # atualiza a posição no diagrama
                continue
            
            # caso do lado direito do diagrama
            if position == 1:

                # processa o próximo token
                token = Parser.tokenizer.next
                
                # verifica se é um MULT
                if token.type == "MULT":
                    Parser.tokenizer.select_next()
                    multiplication = True
                    position       = 0
                    continue

                # verifica se é um DIV
                if token.type == "DIV":
                    Parser.tokenizer.select_next()
                    multiplication = False
                    position       = 0
                    continue
                
                # se não for nenhum, sai da função
                break
        
        return accumulator
    

    @staticmethod
    def parse_factor():

        position    = 0         # posição no diagrama sintático
        accumulator = 0         # variável de acumulação da soma
        last_sign   = 1         # último sinal lido, 1 para mais, -1 para menos
    
        while True:
            
            token = Parser.tokenizer.next

            if position == 0:

                if token.type == "INT":
                    Parser.tokenizer.select_next()
                    accumulator += int(token.value)
                    position = 1
                    continue

                if token.type == "PLUS":
                    Parser.tokenizer.select_next()
                    last_sign = 1
                    posititon = 2
                    continue

                if token.type == "MINUS":
                    Parser.tokenizer.select_next()
                    last_sign = -1
                    position  =  2
                    continue

                if token.type == "OPENPAR":
                    Parser.tokenizer.select_next()
                    position = 3
                    continue

                raise Exception("Erro de sintaxe")
            
            if position == 1: break

            if position == 2:
                number       = Parser.parse_factor()
                accumulator += number * last_sign
                position     = 1
                continue

            if position == 3:
                number       = Parser.parse_expression()
                accumulator += number
                position     = 4
                continue

            if position == 4:
                if token.type != "CLOSEPAR":
                    raise Exception("Parênteses sem fechar")
                Parser.tokenizer.select_next()
                position = 1
                continue


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
        source = PrePro.filter(source)          # remove comentários
        Parser.tokenizer = Tokenizer(source)
        Parser.tokenizer.select_next()
        result = Parser.parse_expression()

        if (Parser.tokenizer.next.type != "EOF"):
            raise Exception("Erro de sintaxe")
        
        return result