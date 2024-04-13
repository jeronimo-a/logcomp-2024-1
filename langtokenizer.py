from langtoken import Token

class Tokenizer:

    letters        = "abcdefghijklmnopqrstuvwxyz"
    letters       += letters.upper()
    allowed_chars  = letters + "0123456789_"
    reserved_words = {
        "print" : "PRINT",
        "and"   : "AND",
        "or"    : "OR",
        "if"    : "IF",
        "while" : "WHILE",
        "end"   : "END",
        "do"    : "DO",
        "then"  : "THEN",
        "else"  : "ELSE",
        "read"  : "READ",
        "not"   : "NOT"
    }

    def __init__(self, source: str):
        self.source     : str   = source    # o código fonte
        self.position   : int   = 0         # posição atual que está sendo separada
        self.next       : Token = None      # o último token separado

    def test(self):
        if self.position != 0: raise Exception("select_next já chamado")
        self.select_next()
        while self.next.type != "EOF":
            print(self.next.type, self.next.value)
            self.select_next()
        print(self.next.type, self.next.value)

    def over(self):
        return self.position == len(self.source)
    
    def select_next(self):
        self._select_next()
        print("next token: ", self.next.type, self.next.value)

    def _select_next(self):

        token_value = str()
        token_type  = str()

        if self.over():
            self.next = Token("EOF", "")
            return

        # se for espaço ou tab, pula
        while self.source[self.position] in [" ", "\t"]:
            self.position += 1
            if self.over():
                self.next = Token("EOF", "")
                return
        
        # se o caractere atual for um caractere numérico, concatena todos ao token_value até que não seja mais numérico
        while self.source[self.position].isnumeric():
            token_type       = "NUM" 
            token_value     += self.source[self.position]
            self.position   += 1
            if self.over(): break

        # se o caractere atual não for numérico nem + - / * () ou \n
        if not self.over() and token_type != "NUM":
            if self.source[self.position] in Tokenizer.letters:
                identifier = ""
                while self.source[self.position] in Tokenizer.allowed_chars:
                    identifier    += self.source[self.position]
                    self.position += 1
                    if self.over(): break
                if identifier in Tokenizer.reserved_words.keys():
                    self.next = Token(Tokenizer.reserved_words[identifier], identifier)
                    return
                else:
                    self.next = Token("IDENT", identifier)
                    return
        
        # se o token já tiver sido definido como inteiro, cria o token e termina a função
        if token_type == "NUM":
            if not self.over():
                if self.source[self.position] in Tokenizer.allowed_chars:
                    raise Exception("Nome de variável não pode começar com número")
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
        
        # se for =
        if self.source[self.position] == "=":

            # se for relacional de igualdade, cria o token e termina a função
            try:
                if self.source[self.position + 1] == "=":
                    self.next       = Token("EQUAL", "==")
                    self.position  += 2
                    return
            except IndexError:
                pass

            # se não for relaciona de igualdade, cria o token de ASSIGN e termina a função
            self.next       = Token("ASSIGN", "=")
            self.position  += 1
            return
        
        # se for newline, cria o token e termina a função
        if self.source[self.position] == "\n":
            self.next       = Token("NEWLINE", "\n")
            self.position  += 1
            return
        
        # se for "maior que", cria o token e termina a função
        if self.source[self.position] == ">":
            self.next       = Token("GREATER", ">")
            self.position  += 1
            return
        
        # se for "menor que", cria o token e termina a função
        if self.source[self.position] == "<":
            self.next       = Token("LESS", "<")
            self.position  += 1
            return

        # se chegou até aqui, o caractere não pertence ao alfabeto
        raise Exception("Erro léxico")