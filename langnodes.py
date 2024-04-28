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

        eval_l, type_l = self.children[0].Evaluate()
        eval_r, type_r = self.children[1].Evaluate()
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

    def Evaluate(self):
        child_eval, child_type = self.children[0].Evaluate()
        if child_type != "int": raise Exception("UnOp funciona apenas com int, não com %s, var: %s" % child_type. self.children[0].value)
        if self.value == "+"    : return child_eval, "int"
        if self.value == "-"    : return child_eval * -1, "int"
        if self.value == "not"  : return int(not bool(child_eval)), "int"
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