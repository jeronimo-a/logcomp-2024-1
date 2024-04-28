class Node:

    def __init__(self, value):
        self.value    = value
        self.children = list()

    def Evaluate(self):
        return self.value, None
    
    def View(self, counter: int=0, margin: str="  "):
        print(counter * margin, self.value, sep="")
        for child in self.children:
            child.View(counter + 1, margin)


class BinOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self):

        value_l, type_l = self.children[0].Evaluate()
        value_r, type_r = self.children[1].Evaluate()
        mixed = type_l != type_r

        if self.value == ".."   : return str(value_l) + str(value_r)         , "str"
        if self.value == "or"   : return int(bool(value_l) or bool(value_r)) , "int"
        if self.value == "and"  : return int(bool(value_l) and bool(value_r)), "int"
        
        if not mixed:
            if self.value == "=="   : return int(value_l == value_r), type_l
            if self.value == "<"    : return int(value_l < value_r) , type_l
            if self.value == ">"    : return int(value_l > value_r) , type_l

        if not mixed and type_l == "int":
            if self.value == "+"    : return value_l + value_r , "int"
            if self.value == "-"    : return value_l - value_r , "int"
            if self.value == "*"    : return value_l * value_r , "int"
            if self.value == "/"    : return value_l // value_r, "int"

        raise Exception("Tipos errados para %s, %s e %s" % (self.value, type_l, type_r))


class UnOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self):
        child_value, child_type = self.children[0].Evaluate()
        if child_type != "int": raise Exception("UnOp funciona apenas com int, não com %s" % child_type)
        if self.value == "+"    : return child_value, "int"
        if self.value == "-"    : return child_value * -1, "int"
        if self.value == "not"  : return int(not bool(child_value)), "int"
        raise Exception('UnOp Node com valor desconhecido: "%s"' % self.value)


class IntVal(Node):

    def __init__(self, value: int):
        super().__init__(value)

    def Evaluate(self):
        return int(self.value), "int"
    

class StrVal(Node):

    def __init__(self, value: int):
        super().__init__(value)
    
    def Evaluate(self):
        return str(self.value), "str"


class NoOp(Node):

    def __init__(self):
        super().__init__(None)


class Ident(Node):

    def __init__(self, value: str, table):
        super().__init__(value)
        self.table = table

    def Evaluate(self):
        try: result = self.table.get(self.value)
        except KeyError: raise Exception('Variável "%s" não existe' % self.value)
        return result
    

class Print(Node):

    def __init__(self):
        super().__init__("print")

    def Evaluate(self):
        print(self.children[0].Evaluate()[0])


class Read(Node):

    def __init__(self):
        super().__init__("read")

    def Evaluate(self):
        return input(), "str"


class Assign(Node):

    def __init__(self, table):
        super().__init__("=")
        self.table = table
    
    def Evaluate(self):
        variable = self.children[0].value
        value, type = self.children[1].Evaluate()
        try: self.table.set(variable, value, type)
        except KeyError: raise Exception('Variável "%s" não existe' % self.value)


class Block(Node):

    def __init__(self):
        super().__init__("%BLOCK%")
    
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()


class While(Node):

    def __init__(self):
        super().__init__("while")

    def Evaluate(self):
        while self.children[0].Evaluate():
            self.children[1].Evaluate()     # Block


class If(Node):

    def __init__(self):
        super().__init__("if")

    def Evaluate(self):
        if self.children[0]: self.children[1].Evaluate()    # Block
        else: self.children[2].Evaluate()                   # Block


class Vardec(Node):

    def __init__(self, table):
        super().__init__("local")
        self.table = table

    def Evaluate(self):
        variable = self.children[0].value
        self.table.init(variable)
        try: self.children[1].Evaluate()
        except IndexError: pass