from langtokenizer import Tokenizer

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
                    multiplication = True
                    position       = 0
                    continue

                # verifica se é um DIV
                if token.type == "DIV":
                    multiplication = False
                    position       = 0
                    continue

                break
            
        return accumulator
    

    @staticmethod
    def parse_factor():

        Parser.tokenizer.select_next()
        token = Parser.tokenizer.next

        if token.type != "INT":
            raise Exception("Número esperado")
        
        Parser.tokenizer.select_next()
        
        return int(token.value)

    
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