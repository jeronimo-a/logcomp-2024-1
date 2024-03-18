from langsymboltable import SymbolTable
from langtokenizer import Tokenizer
from langprepro import PrePro
from langnodes import *


class Parser:

    tokenizer    : Tokenizer   = None   # instância da classe Tokenizer que irá ler o código fonte e alimentar o Parser
    symbol_table : SymbolTable = None   # instância da classe SymbolTable que irá armazenar o valor das variáveis

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

        _ = Parser.inrun(source, filter=True)

        if (Parser.tokenizer.next.type != "EOF"):
            raise Exception("Erro de sintaxe")
    

    @staticmethod
    def testrun(source_file: str):
        with open(source_file) as file:
            source = file.read()
        return Parser.inrun(source, True)


    @staticmethod
    def inrun(source: str, filter: bool=False):
        if filter: source = PrePro.filter(source)
        Parser.tokenizer = Tokenizer(source)
        Parser.tokenizer.select_next()
        Parser.symbol_table = SymbolTable()
        root = Parser.parse_block()
        root.Evaluate()
        return root
    

    @staticmethod
    def parse_block():
        '''
        Implementação do block do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        root = Block()

        while Parser.tokenizer.next.type != "EOF":
            root.children.append(Parser.parse_statement())

        return root


    @staticmethod
    def parse_statement():
        '''
        Implementação do statement do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position = 0        # posição no diagrama sintático, vide diagrama_sintatico.png
        latest_node = None  # último node gerado
        
        # loop de percorrimento do diagrama sintático
        while True:

            token = Parser.tokenizer.next   # último token

            # comportamento da parte inicial do diagrama sintático na parte statement
            if position == 0:
                
                # se for token do tipo "IDENT"
                if token.type == "IDENT":
                    Parser.tokenizer.select_next()                          # consome o token
                    latest_node = Ident(token.value, Parser.symbol_table)   # cria o novo Node do tipo Ident
                    position = 2                                            # atualiza a posição no diagrama sintático
                    continue                                                # reinicia o loop

                # se for token do tipo "PRINT"
                if token.type == "PRINT":
                    Parser.tokenizer.select_next()  # consome o token
                    latest_node = Print()           # cria o novo Node do tipo Print
                    position = 1                    # atualiza a posição no diagrama sintático
                    continue                        # reinicia o loop

                # se for token do tipo "NEWLINE"
                if token.type == "NEWLINE" or token.type == "EOF":
                    Parser.tokenizer.select_next()  # consome o token
                    position = 7                    # atualiza a posição no diagrama sintático
                    continue                        # reinicia o loop

                raise Exception("Erro de sintaxe")

            # comportamento na posição 1 do diagrama sintático na parte statement
            if position == 1:
                if token.type != "OPENPAR":                                 # espera-se apenas abertura de parênteses
                    raise Exception("Print requer abertura de parênteses")  # gera erro caso não for abertura de parênteses
                Parser.tokenizer.select_next()                              # consome o token
                position = 3                                                # atualiza a posição no diagrama sintático
                continue                                                    # reinicia o loop

            # comportamento na posição 2 do diagrama sintático na parte statement
            if position == 2:
                if token.type != "ASSIGN":                          # espera-se apenas o operador de atribuição
                    raise Exception("Token de atribuição esperado") # gera erro caso não for abertura de parênteses
                Parser.tokenizer.select_next()                      # consome o token
                assign_node = Assign(Parser.symbol_table)           # cria o novo Node do tipo Assign
                assign_node.children.append(latest_node)            # inclui o Ident gerado na posição 2 nos filhos do Assign
                latest_node = assign_node                           # torna o Assign o latest_node
                position = 4                                        # atualiza a posição no diagrama sintático
                continue                                            # reinicia o loop

            # comportamento na posição 3 e 4 do diagrama sintático na parte statement
            if position == 3 or position == 4:
                subroutine_node = Parser.parse_expression()     # chama parse_expression
                latest_node.children.append(subroutine_node)    # adiciona o Node gerado por parse_expression aos filhos do Print/Assign
                position += 2                                   # atualiza a posição no diagrama sintático conforme a posição original
                continue                                        # reinicia o loop

            # comportamento na posição 5 do diagrama sintático na parte statement
            if position == 5:
                if token.type != "CLOSEPAR":                                        # espera-se apenas abertura de parênteses
                    raise Exception("Fechamento de parênteses do print faltando")   # gera erro caso não for abertura de parênteses
                Parser.tokenizer.select_next()                                      # consome o token
                position = 6                                                        # atualiza a posição no diagrama sintático
                continue                                                            # reinicia o loop
            
            # posição inútil, não tinha me tocado
            if position == 6:
                position = 0
                continue

            # comportamento na posição 7 (final) do diagrama sintático na parte statement
            if position == 7:
                break
        
        if latest_node is None: latest_node = NoOp()
        return latest_node


    @staticmethod
    def parse_expression():
        '''
        Implementação do expression do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position    = 0     # posição no diagrama sintático, vide diagrama_sintatico.png
        latest_node = None  # último node gerado
        term_node   = None  # node gerado pelo term

        # loop de percorrimento do diagrama sintático
        while True:

            token = Parser.tokenizer.next   # último token

            # comportamento na primeira parte do diagrama sintático na parte term
            if position == 0:
                term_node = Parser.parse_term()                 # chama parse_term
                try:
                    latest_node.children.append(term_node)      # se já existir o latest node, appenda o novo term aos filhos
                    term_node = latest_node                     # o latest node vira o term node
                except: latest_node = term_node
                position = 1                                    # vai para a segunda parte do diagrama
                continue                                        # reinicia o loop

            # comportamento na segunda parte do diagrama sintático na parte term
            if position == 1:

                # lida com os operadores binários
                if token.type == "PLUS" or token.type == "MINUS":
                    Parser.tokenizer.select_next()              # consome o token
                    latest_node = BinOp(token.value)            # cria o novo node do operador binário
                    latest_node.children.append(term_node)      # adiciona o resultado do parse term aos filhos do operador binário
                    position = 0                                # volta para a primeira parte do diagrama na parte term
                    continue                                    # reinicia o loop
                    
                # se chegou aqui, termina a função
                break
        
        return latest_node
    

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
                except: latest_node = factor_node
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

        position     = 0     # posição no diagrama sintático, vide diagrama_sintatico.png
        latest_node  = None  # último node gerado

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

                # lide com variáveis
                if token.type == "IDENT":
                    Parser.tokenizer.select_next()                          # consome o token
                    latest_node = Ident(token.value, Parser.symbol_table)   # cria o novo node
                    position = 1                                            # vai para a posição 1 do diagrama
                    continue                                                # reinicia o loop

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
                subroutine_node = Parser.parse_expression()             # chama parse_expression de novo
                try: latest_node.children.append(subroutine_node)       # adiciona o resultado da subrotina aos filhos do node desse escopo, se houver node desse escopo
                except AttributeError: latest_node = subroutine_node    # se não houver, torna o resultado da subrotina o latest node
                position = 4                                            # vai para a posição 4 do diagrama na parte factor
                continue                                                # reinicia o loop

            # comportamento da posição 4 do diagram na parte factor, vide diagrama_sintatico.png
            if position == 4:
                if token.type != "CLOSEPAR":                    # verifica se é fechamento de parênteses
                    raise Exception("Parênteses sem fechar")    # se não for, gera um erro
                Parser.tokenizer.select_next()                  # consome o token
                position = 1                                    # vai para a posição 1 do diagrama na parte factor
                continue                                        # reinicia o loop
                
        return latest_node
