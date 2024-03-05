from langtoken import Token

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