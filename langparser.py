from langtokenizer import Tokenizer
from langprepro import PrePro
from langnodes import *


class Parser:

    tokenizer : Tokenizer = None    # instância da classe Tokenizer que irá ler o código fonte e alimentar o Parser

    @staticmethod
    def run(source: str):
        '''
        Recebe o código fonte como argumento
        Remove comentários
        Inicializa uma instância de Tokenizador
        Posiciona o Tokenizer no primeiro token (feito no inicializador de Tokenizer)
        Verifica se a cadeia foi consumida por completo
        Constrói a árvore AST
        Retorna o resultado do método Evaluate do Node raíz da árvore
        '''

        #source = PrePro.filter(source)
        Parser.tokenizer = Tokenizer(source)
        Parser.tokenizer.select_next()
        root = Parser.parse_term()
        result = root.Evaluate()

        if (Parser.tokenizer.next.type != "EOF"):
            raise Exception("Erro de sintaxe")
        
        return root, result


    @staticmethod
    def parse_expression(root=None):
        '''
        Consome os tokens do Tokenizer
        Analisa se a sintaxe está aderente à gramática
        Retorna o resultado da expressão analisada
        '''

        position = 0        # posição no diagrama sintático, 0 para esquerda, 1 para direita
        new_node = None     # último Node gerado

        while True:

            token = Parser.tokenizer.next

            # caso do lado esquerdo do diagrama
            if position == 0:

                # chama a subrotina parse term
                new_node = Parser.parse_term(root)

                # atualiza a posição e reinicia o loop
                position = 1
                continue
            
            # caso do lado direito do diagrama
            if position == 1:
                
                # verifica se é um PLUS ou MINUS
                if token.type == "PLUS" or token.type == "MINUS":

                    # consome um token e cria um Node BinOp
                    Parser.tokenizer.select_next()
                    root = BinOp(token.value)
                    root.children.append(new_node)

                    # atualiza a posição e reinicia o loop
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
        
        root = new_node
        return root
    

    @staticmethod
    def parse_term():
        '''
        Implementação do term do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position    = 0     # posição no diagrama sintático, vide diagrama_sintatico.png
        latest_node = None  # último node gerado
        factor_node = None  # node gerado pelo factor

        # loop de percorrimento do diagrama sintático
        while True:

            token = Parser.tokenizer.next   # último token

            # comportamento na primeira parte do diagrama sintático na parte term
            if position == 0:
                factor_node = Parser.parse_factor()             # chama parse_factor
                try:
                    latest_node.children.append(factor_node)    # se já existir o latest node, appenda o novo factor aos filhos
                    factor_node = latest_node                   # o latest node vira o factor node
                except: pass
                position = 1                                    # vai para a segunda parte do diagrama
                continue                                        # reinicia o loop

            # comportamento na segunda parte do diagrama sintático na parte term
            if position == 1:

                # lida com os operadores binários
                if token.type == "DIV" or token.type == "MULT":
                    Parser.tokenizer.select_next()              # consome o token
                    latest_node = BinOp(token.value)            # cria o novo node do operador binário
                    latest_node.children.append(factor_node)    # adiciona o resultado do parse_factor aos filhos do operador binário
                    position = 0                                # volta para a primeira parte do diagrama na parte term
                    continue                                    # reinicia o loop
                    
                # se chegou aqui, termina a função
                break

        return latest_node
    

    @staticmethod
    def parse_factor():
        '''
        Implementação do factor do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position    = 0     # posição no diagrama sintático, vide diagrama_sintatico.png
        latest_node = None  # último node gerado

        # loop de percorrimento do diagrama sintático
        while True:

            token = Parser.tokenizer.next   # último token

            # comportamento da posição inicial do diagrama na parte factor
            if position == 0:
                
                # lida com números
                if token.type == "INT":
                    Parser.tokenizer.select_next()          # consome o token
                    latest_node = IntVal(int(token.value))  # cria o novo node
                    position = 1                            # vai para a posição 1 do diagrama
                    continue                                # reinicia o loop

                # lida com operadores unários
                if token.type == "PLUS" or token.type == "MINUS":
                    Parser.tokenizer.select_next()      # consome o token
                    latest_node = UnOp(token.value)     # cria o novo node
                    position = 2                        # vai para a posição 2 do diagrama
                    continue                            # reinicia o loop

                # lida com parênteses
                if token.type == "OPENPAR":
                    Parser.tokenizer.select_next()  # consome o token
                    position = 3                    # vai para a posição 3 do diagrama
                    continue                        # reinicia o loop

                # gera erro caso chegar aqui
                raise Exception("Erro de sintaxe")
            
            # comportamento da posição final do diagrama na parte factor
            if position == 1:
                break   # apenas sai do loop

            # comportamento da posição 2 do diagrama na parte factor, vide diagrama_sintatico.png
            if position == 2:
                subroutine_node = Parser.parse_factor()         # chama parse_factor de novo
                latest_node.children.append(subroutine_node)    # adiciona o resultado da subrotina aos filhos do node desse escopo
                position = 1                                    # vai para a posição final do diagrama na parte factor
                continue                                        # reinicia o loop

            # comportamento da posição 3 do diagrama na parte factor, vide diagrama_sintatico.png
            if position == 3:
                subroutine_node = Parser.parse_expression()     # chama parse_expression de novo
                latest_node.children.append(subroutine_node)    # adiciona o resultado da subrotina aos filhos do node desse escopo
                position = 4                                    # vai para a posição 4 do diagrama na parte factor
                continue                                        # reinicia o loop

            # comportamento da posição 4 do diagram na parte factor, vide diagrama_sintatico.png
            if position == 4:
                if token.type != "CLOSEPAR":                    # verifica se é fechamento de parênteses
                    raise Exception("Parênteses sem fechar")    # se não for, gera um erro
                Parser.tokenizer.select_next()                  # consome o token
                position = 1                                    # vai para a posição 1 do diagrama na parte factor
                continue                                        # reinicia o loop
                
        return latest_node

