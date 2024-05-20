from langsymboltable import SymbolTable
from langtokenizer import Tokenizer
from langprepro import PrePro
from langnodes import *


class Parser:

    tokenizer       : Tokenizer   = None    # instância da classe Tokenizer que irá ler o código fonte e alimentar o Parser
    symbol_table    : SymbolTable = None    # instância da classe SymbolTable que irá armazenar o valor das variáveis
    function_table  : SymbolTable = None    # instância da classe SymbolTable que irá armazenar o Node FuncDec das funções

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

        root = Parser._run(source)
        root.Evaluate()

        if (Parser.tokenizer.next.type != "EOF"):
            raise Exception("Erro de sintaxe")
    

    @staticmethod
    def testrun(source_file: str):
        with open(source_file) as file:
            source = file.read()
        return Parser._run(source)


    @staticmethod
    def _run(source: str):
        source = PrePro.filter(source)
        Parser.tokenizer = Tokenizer(source)
        Parser.tokenizer.select_next()
        Parser.symbol_table = SymbolTable()
        root = Parser.parse_block()
        return root
    

    @staticmethod
    def parse_block():
        '''
        Implementação do block do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        root = Block()

        while Parser.tokenizer.next.type != "EOF":
            statement_root_node = Parser.parse_statement()
            if statement_root_node is not None:
                root.children.append(statement_root_node)

        return root


    @staticmethod
    def parse_statement():
        '''
        Implementação do statement do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        # se o primeiro token da linha for um IDENT
        if Parser.tokenizer.next.type == "IDENT":

            # lembra do token IDENT
            ident_token = Parser.tokenizer.next
            Parser.tokenizer.select_next()

            # verifica se é ASSIGN
            if Parser.tokenizer.next.type == "ASSIGN":

                # cria o Node Ident a partir do valor do token passado
                ident_node = Ident(ident_token.value, Parser.symbol_table)

                # cria o Node Assign
                assign_node = Assign(Parser.symbol_table)
                Parser.tokenizer.select_next()

                # chama o parse_boolean_expression
                b_exp_root_node = Parser.parse_boolean_expression()

                # linka o IDENT e o node raiz de parse_boolean_expression ao ASSIGN
                assign_node.children.append(ident_node)
                assign_node.children.append(b_exp_root_node)

                # verifica sem tem NEWLINE
                Parser.expect("NEWLINE", "depois de uma atribuição")
                Parser.tokenizer.select_next()

                return assign_node

            # verifica se é OPENPAR
            if Parser.tokenizer.next.type == "OPENPAR":

                # cria o Node FuncCall a partir do token anterior, faz o parsing dos argumentos e consome o OPENPAR
                funccall_node = FuncCall(ident_token.value, Parser.function_table)
                Parser.parse_function_args(funccall_node)
                Parser.tokenizer.select_next()

                # verifica se tem fechamento de parênteses
                Parser.expect("CLOSEPAR", "para uma chamada de função")
                Parser.tokenizer.select_next()

                # verifica se tem quebra de linha
                Parser.expect("NEWLINE", "depois de uma chamada de função")
                Parser.tokenizer.select_next()

                return funccall_node
            
        # se o primeiro token da linha for um FUNCDEC
        if Parser.tokenizer.next.type == "FUNCDEC":

            # consome o token FUNCDEC e espera um token IDENT
            Parser.tokenizer.select_next()
            Parser.expect("IDENT", "ao declarar uma nova função")

            # cria o Node FuncDec e consome o token IDENT
            funcdec_node = FuncDec(Parser.tokenizer.next.value, Parser.function_table)
            funcdec_node.children.append(list())
            Parser.tokenizer.select_next()

            # espera-se um OPENPAR
            Parser.expect("OPENPAR", "para declarar uma nova função")
            Parser.tokenizer.select_next()

            # loop de coleta dos parâmetros
            if Parser.tokenizer.next.type == "IDENT":

                # cria os Nodes Vardec e Ident dos parâmetros ainda sem symbol table
                vardec_node = Vardec(None)
                ident_node = Ident(Parser.tokenizer.next.value, None)
                Parser.tokenizer.select_next()

                # cria as relações entre os Nodes
                vardec_node.children.append(ident_node)
                funcdec_node.children[0].append(vardec_node)

                # loop de coleta
                while Parser.tokenizer.next.type == "COMMA":
                    
                    # consome o token COMMA e espera um identifier
                    Parser.tokenizer.select_next()
                    Parser.expect("IDENT", "na declaração dos parâmetros de uma função")

                    # cria os Nodes Vardec e Ident dos parâmetros ainda sem symbol table
                    vardec_node = Vardec(None)
                    ident_node = Ident(Parser.tokenizer.next.value, None)
                    Parser.tokenizer.select_next()

                    # cria as relações entre os Nodes
                    vardec_node.children.append(ident_node)
                    funcdec_node.children[0].append(vardec_node)

                # espera-se um CLOSEPAR seguido de NEWLINE
                Parser.expect("CLOSEPAR", "ao declarar uma função")
                Parser.tokenizer.select_next()
                Parser.expect("NEWLINE", "ao declarar uma função")
                Parser.tokenizer.select_next()

                # loop de coleta dos statements
                statement_block = Block()
                FuncDec.children.append(statement_block)
                while Parser.tokenizer.next.type != "END":
                    statement_block.append(Parser.parse_statement())
                
                # consome o END e espera um NEWLINE
                Parser.tokenizer.select_next()
                Parser.expect("NEWLINE", "ao final de uma declaração de função")
                Parser.tokenizer.select_next()

                return FuncDec


        # se o primeiro token da linha for um PRINT
        if Parser.tokenizer.next.type == "PRINT":

            # gera o node PRINT
            print_node = Print()
            Parser.tokenizer.select_next()

            # verifica se abre parênteses
            Parser.expect("OPENPAR", "para chamar a função")
            Parser.tokenizer.select_next()

            # chama o parse_boolean_expression
            b_exp_root_node = Parser.parse_boolean_expression()
            
            # verifica se tem fechamento de parênteses
            Parser.expect("CLOSEPAR", "ao chamar a função print")
            Parser.tokenizer.select_next()

            # linka o node raiz de parse_boolean_expression ao PRINT
            print_node.children.append(b_exp_root_node)
            
            # verifica sem tem NEWLINE
            Parser.expect("NEWLINE", "depois de uma chamada da função print")
            Parser.tokenizer.select_next()

            return print_node
        
        # se o primeiro token da linha for um WHILE
        if Parser.tokenizer.next.type == "WHILE":

            # gera o node WHILE
            while_node = While()
            Parser.tokenizer.select_next()

            # chama o parse_boolean_expression
            condition_node = Parser.parse_boolean_expression()

            # linka o a raiz do boolean expression ao while como a condição de loop
            while_node.children.append(condition_node)

            # verifica se tem DO seguido de NEWLINE
            Parser.expect("DO", "depois da condição de loop while")
            Parser.tokenizer.select_next()
            Parser.expect("NEWLINE", "depois do uma linha de loop while")
            Parser.tokenizer.select_next()

            # loop de coleta dos statements dentro do while usando um node block
            block_node = Block()
            while Parser.tokenizer.next.type != "END":
                statement_node = Parser.parse_statement()
                block_node.children.append(statement_node)

            # linka o node block ao node while e consome o token END
            while_node.children.append(block_node)
            Parser.tokenizer.select_next()

            # verifica se tem NEWLINE
            Parser.expect("NEWLINE", 'depois do "end" que fecha o while')
            Parser.tokenizer.select_next()

            return while_node
        
        # se o primeiro token da linha for um IF
        if Parser.tokenizer.next.type == "IF":
            
            # gera o node IF
            if_node = If()
            Parser.tokenizer.select_next()

            # chama o parse_boolean_expression
            b_exp_root_node = Parser.parse_boolean_expression()

            # linka a raiz do node da boolean expression ao node if
            if_node.children.append(b_exp_root_node)

            # verifica se tem THEN seguido de NEWLINE
            Parser.expect("THEN", "depois da condição de if")
            Parser.tokenizer.select_next()
            Parser.expect("NEWLINE", "depois do uma linha de if")
            Parser.tokenizer.select_next()

            # gera os node blocks do if e do else e linka ao node do if
            block_node_true = Block()
            block_node_false = Block()
            if_node.children.append(block_node_true)
            if_node.children.append(block_node_false)

            # loop de coleta dos statements dentro do if usando o block node do if
            while Parser.tokenizer.next.type not in ["END", "ELSE"]:
                statement_node = Parser.parse_statement()
                block_node_true.children.append(statement_node)

            # se o próximo token for ELSE
            if Parser.tokenizer.next.type == "ELSE":

                # consome o else
                Parser.tokenizer.select_next()
                
                # verifica se tem NEWLINE
                Parser.expect("NEWLINE", "depois de else")
                Parser.tokenizer.select_next()

                # loop de coleta dos statements dentro do else usando o block node do else
                while Parser.tokenizer.next.type != "END":
                    statement_node = Parser.parse_statement()
                    block_node_false.children.append(statement_node)

            # se chegou aqui, o próximo token é um END
            Parser.tokenizer.select_next()

            # verifica se é NEWLINE
            Parser.expect("NEWLINE", "depois do end de um bloco if else")
            Parser.tokenizer.select_next()

            return if_node
        
        # se o primeiro token da linha for um VARDEC
        if Parser.tokenizer.next.type == "VARDEC":

            # gera o node VARDEC
            vardec_node = Vardec(Parser.symbol_table)
            Parser.tokenizer.select_next()

            # espera um IDENT
            Parser.expect("IDENT", "um identificador depois de uma declaração de variável.")

            # gera o node IDENT que vem em seguida
            ident_node = Ident(Parser.tokenizer.next.value, Parser.symbol_table)
            Parser.tokenizer.select_next()

            # adiciona a variável aos filhos de vardec
            vardec_node.children.append(ident_node)

            # se o próximo for ASSIGN
            if Parser.tokenizer.next.type == "ASSIGN":

                # gera o node ASSIGN, adicona o IDENT ao seus filhos e o adiciona aos filhos de VARDEC
                assign_node = Assign(Parser.symbol_table)
                vardec_node.children.append(assign_node)
                assign_node.children.append(ident_node)
                Parser.tokenizer.select_next()

                # chama boolean expression e adiciona o root aos filhos de ASSIGN
                b_exp_root_node = Parser.parse_boolean_expression()
                assign_node.children.append(b_exp_root_node)
            
            # se o próximo não for ASSIGN, espera um newline
            Parser.expect("NEWLINE", "uma quebra de linha depois de declarar uma variável.")
            Parser.tokenizer.select_next()

            return vardec_node
        
        # gera erro caso chegar aqui
        print(Parser.tokenizer.next.type)
        raise Exception("Erro de sintaxe")


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
                if token.type == "DIV" or token.type == "MULT" or token.type == "CAT":
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
                
        # lida com números
        if Parser.tokenizer.next.type == "NUM":
            latest_node = IntVal(int(Parser.tokenizer.next.value))
            Parser.tokenizer.select_next()
            return latest_node
        
        # lida com strings
        if Parser.tokenizer.next.type == "STR":
            latest_node = StrVal(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return latest_node

        # lida com operadores unários
        if Parser.tokenizer.next.type in ["PLUS", "MINUS", "NOT"]:
            latest_node = UnOp(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            subroutine_node = Parser.parse_factor()
            latest_node.children.append(subroutine_node)
            return latest_node

        # lida com parênteses
        if Parser.tokenizer.next.type == "OPENPAR":
            Parser.tokenizer.select_next()
            latest_node = Parser.parse_boolean_expression()
            Parser.expect("CLOSEPAR")
            Parser.tokenizer.select_next()
            return latest_node

        # lida com variáveis e chamadas de função
        if Parser.tokenizer.next.type == "IDENT":

            # lembra do token IDENT
            ident_token = Parser.tokenizer.next
            Parser.tokenizer.select_next()

            # se for OPENPAR, é chamada de função
            if Parser.tokenizer.next.type == "OPENPAR":

                # cria o Node FuncCall da chamada de função, faz o parsing dos argumentos e consome o OPENPAR
                funccall_node = FuncCall(ident_token.value, Parser.function_table)
                Parser.parse_function_args(funccall_node)
                Parser.tokenizer.select_next()

                # verifica se tem fechamento de parênteses
                Parser.expect("CLOSEPAR", "em uma chamada de função")
                Parser.tokenizer.select_next()

                return funccall_node

            # não for OPENPAR, é "chamada" de variável
            else:
                ident_node = Ident(ident_token.value, Parser.symbol_table)
                Parser.tokenizer.select_next()
                return ident_node

        # lida com read
        if Parser.tokenizer.next.type == "READ":
            latest_node = Read()
            Parser.tokenizer.select_next()
            Parser.expect("OPENPAR", "para chamar a função read") 
            Parser.tokenizer.select_next()
            Parser.expect("CLOSEPAR", "para chamar a função read") 
            Parser.tokenizer.select_next()
            return latest_node
            
        # gera erro caso chegar aqui
        raise Exception("Erro de sintaxe")
    

    @staticmethod
    def parse_boolean_expression():
        '''
        Implementação do boolean expression do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position = 0    # posição no diagrama sintático, 0 para esquerda, 1 para direita
        or_node = None

        while True:

            if position == 0:
                b_term_root_node = Parser.parse_boolean_term()
                position = 1

            if position == 1:

                if Parser.tokenizer.next.type == "OR" and or_node is None:
                    or_node = BinOp("or")
                    Parser.tokenizer.select_next()
                    or_node.children.append(b_term_root_node)
                    position = 0
                    continue

                if or_node is not None:
                    or_node.children.append(b_term_root_node)
                    break

                break
        
        if or_node is None: root_node = b_term_root_node
        else: root_node = or_node
        return root_node
    

    @staticmethod
    def parse_boolean_term():
        '''
        Implementação do boolean term do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position = 0    # posição no diagrama sintático, 0 para esquerda, 1 para direita
        and_node = None

        while True:

            if position == 0:
                r_exp_root_node = Parser.parse_rel_expression()
                position = 1

            if position == 1:

                if Parser.tokenizer.next.type == "AND" and and_node is None:
                    and_node = BinOp("and")
                    Parser.tokenizer.select_next()
                    and_node.children.append(r_exp_root_node)
                    position = 0
                    continue

                if and_node is not None:
                    and_node.children.append(r_exp_root_node)
                    break

                break
        
        if and_node is None: root_node = r_exp_root_node
        else: root_node = and_node
        return root_node
    

    @staticmethod
    def parse_rel_expression():
        '''
        Implementação do rel expression do diagrama sintático
        Vide diagrama_sintatico.png
        '''

        position = 0    # posição no diagrama sintático, 0 para esquerda, 1 para direita
        relational_node = None

        while True:

            if position == 0:
                exp_root_node = Parser.parse_expression()
                position = 1

            if position == 1:

                if Parser.tokenizer.next.type in ["EQUAL", "GREATER", "LESS"] and relational_node is None:
                    relational_node = BinOp(Parser.tokenizer.next.value)
                    Parser.tokenizer.select_next()
                    relational_node.children.append(exp_root_node)
                    position = 0
                    continue

                if relational_node is not None:
                    relational_node.children.append(exp_root_node)
                    break

                break
        
        if relational_node is None: root_node = exp_root_node
        else: root_node = relational_node
        return root_node
    

    @staticmethod
    def parse_function_args(funccall_node: FuncCall):
        ''' Faz o parsing dos argumentos de função em uma chamada '''

        # loop de coleta dos argumentos
        while Parser.tokenizer.next.type == "COMMA":
            
            # chama parse_boolean_expression para extrair o argumento e adiciona aos filhos de FuncCall
            b_exp_root_node = Parser.parse_boolean_expression()
            funccall_node.children.append(b_exp_root_node)


    @staticmethod
    def expect(token_type, extra_context=None):
        ''' Verifica se o próximo token é de um determinado tipo '''

        error_message = 'Erro de sintaxe, espera-se "%s"' % token_type
        if extra_context is not None:
            error_message += " " + extra_context
        error_message += '\nNão "%s".' % Parser.tokenizer.next.type

        if Parser.tokenizer.next.type != token_type:
            raise Exception(error_message)