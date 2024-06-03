from langsymboltable import SymbolTable
from langfunciontable import FuncTable

class Node:

    BASE_ID = 0

    def __init__(self, value):
        self.id = Node.BASE_ID
        self.value    = value
        self.children = list()
        Node.BASE_ID += 1

    def Evaluate(self, symbol_table: SymbolTable):
        return self.value, None
    
    def View(self, counter: int=0, margin: str="  "):
        print(counter * margin, self.value, sep="")
        for child in self.children:
            child.View(counter + 1, margin)


class BinOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self, symbol_table: SymbolTable):

        eval_l, type_l = self.children[0].Evaluate(symbol_table)
        eval_r, type_r = self.children[1].Evaluate(symbol_table)
        mixed = type_l != type_r

        if self.value == ".."   : return str(eval_l) + str(eval_r)         , "str"
        if self.value == "or"   : return int(bool(eval_l) or bool(eval_r)) , "int"
        if self.value == "and"  : return int(bool(eval_l) and bool(eval_r)), "int"
        
        if not mixed:
            if self.value == "=="   : return int(eval_l == eval_r), type_l
            if self.value == "<"    : return int(eval_l < eval_r) , type_l
            if self.value == ">"    : return int(eval_l > eval_r) , type_l

        if not mixed and type_l == "int":
            if self.value == "+"    : return eval_l + eval_r , "int"
            if self.value == "-"    : return eval_l - eval_r , "int"
            if self.value == "*"    : return eval_l * eval_r , "int"
            if self.value == "/"    : return eval_l // eval_r, "int"

        variables = (self.value, self.children[0].value, type_l, self.children[1].value, type_r)
        raise Exception('Tipos errados para %s, "%s":%s e "%s":%s' % variables)


class UnOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self, symbol_table: SymbolTable):
        child_eval, child_type = self.children[0].Evaluate(symbol_table)
        if child_type != "int": raise Exception("UnOp funciona apenas com int, não com %s, var: %s" % child_type. self.children[0].value)
        if self.value == "+"    : return child_eval, "int"
        if self.value == "-"    : return child_eval * -1, "int"
        if self.value == "not"  : return int(not bool(child_eval)), "int"
        raise Exception('UnOp Node com valor desconhecido: "%s"' % self.value)


class IntVal(Node):

    def __init__(self, value: int):
        super().__init__(value)

    def Evaluate(self, symbol_table: SymbolTable):
        return int(self.value), "int"
    

class StrVal(Node):

    def __init__(self, value: int):
        super().__init__(value)
    
    def Evaluate(self, symbol_table: SymbolTable):
        return str(self.value), "str"


class NoOp(Node):

    def __init__(self, symbol_table: SymbolTable):
        super().__init__(None)


class Ident(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self, symbol_table: SymbolTable):
        try: result = symbol_table.get(self.value)
        except KeyError: raise Exception('Variável "%s" não existe' % self.value)
        return result
    

class Print(Node):

    def __init__(self):
        super().__init__("print")

    def Evaluate(self, symbol_table: SymbolTable):
        print(self.children[0].Evaluate(symbol_table)[0])


class Read(Node):

    def __init__(self):
        super().__init__("read")

    def Evaluate(self, symbol_table: SymbolTable):
        return int(input()), "int"


class Assign(Node):

    def __init__(self):
        super().__init__("=")
    
    def Evaluate(self, symbol_table: SymbolTable):
        variable = self.children[0].value
        value, type = self.children[1].Evaluate(symbol_table)
        try: symbol_table.set(variable, value, type)
        except KeyError: raise Exception('Variável "%s" não existe' % self.value)


class Block(Node):

    def __init__(self):
        super().__init__("%BLOCK%")
    
    def Evaluate(self, symbol_table: SymbolTable):
        for child in self.children:
            value = child.Evaluate(symbol_table)
            if value is not None and isinstance(child, Return):
                return value


class While(Node):

    def __init__(self):
        super().__init__("while")

    def Evaluate(self, symbol_table: SymbolTable):
        while self.children[0].Evaluate(symbol_table)[0]:
            return self.children[1].Evaluate(symbol_table)     # Block


class If(Node):

    def __init__(self):
        super().__init__("if")

    def Evaluate(self, symbol_table: SymbolTable):
        if self.children[0].Evaluate(symbol_table)[0]: return self.children[1].Evaluate(symbol_table)    # Block
        else: return self.children[2].Evaluate(symbol_table)                   # Block


class Vardec(Node):

    def __init__(self):
        super().__init__("local")

    def Evaluate(self, symbol_table: SymbolTable):
        identifier = self.children[0].value
        symbol_table.init(identifier)
        try: self.children[1].Evaluate(symbol_table)
        except IndexError: pass


class FuncDec(Node):
    '''
    Possui n filhos no total, divididos em 3 pedaços
    Filho i: i-ésimo Vardec Node (i-ésimo parâmetro)
    Filho n: Block Node com o corpo da função
    '''

    def __init__(self, name: str, function_table: FuncTable):
        super().__init__(name)
        self.function_table = function_table
    
    def Evaluate(self, symbol_table: SymbolTable):

        # inicializa o nome na function table, define o valor como a instância de FuncDec em si
        self.function_table.init(self.value)
        self.function_table.set(self.value, self)


class FuncCall(Node):
    '''
    Possui n filhos
    Filho i: argumento para o i-ésimo parâmetro da função
    '''

    def __init__(self, name, function_table: FuncTable):
        super().__init__(name)
        self.function_table = function_table

    def Evaluate(self, symbol_table: SymbolTable):
        
        # pega a referência do node de definição da função
        funcdec_node = self.function_table.get(self.value)

        # conta o número de parâmetros da função e de argumentos da chamada
        n_params = len(funcdec_node.children) - 1
        n_args = len(self.children)
        if n_params != n_args:
            raise Exception('Quantidade inválida de parâmetros na chamada da função %s' % funcdec_node.value)

        # cria a symbol table local e define os parâmetros
        local_symbol_table = SymbolTable(self.value + str(self.id))
        for i in range(n_args):
            param = funcdec_node.children[i]
            arg_value, arg_type = self.children[i].Evaluate(symbol_table)
            param.Evaluate(local_symbol_table)
            local_symbol_table.set(param.children[0].value, arg_value, arg_type)

        # faz o evaluate do block da função com a symbol table local
        return funcdec_node.children[-1].Evaluate(local_symbol_table)


class Return(Node):

    def __init__(self):
        super().__init__("return")
    
    def Evaluate(self, symbol_table: SymbolTable):
        return self.children[0].Evaluate(symbol_table)