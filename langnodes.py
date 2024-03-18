class Node:

    def __init__(self, value):
        self.value    = value
        self.children = list()

    def Evaluate(self):
        return self.value
    
    def View(self, counter: int=0, margin: str="  "):
        print(counter * margin, self.value, sep="")
        for child in self.children:
            child.View(counter + 1, margin)


class BinOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self):

        evaluation_l = self.children[0].Evaluate()
        evaluation_r = self.children[1].Evaluate()

        if self.value == "+": return evaluation_l + evaluation_r
        if self.value == "-": return evaluation_l - evaluation_r
        if self.value == "*": return evaluation_l * evaluation_r
        if self.value == "/": return evaluation_l // evaluation_r

        raise Exception("BinOp Node com valor desconhecido")


class UnOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self):
        child_evaluation = self.children[0].Evaluate()
        if self.value == "+": return child_evaluation
        if self.value == "-": return child_evaluation * -1
        raise Exception("UnOp Node com valor desconhecido")


class IntVal(Node):

    def __init__(self, value: int):
        super().__init__(value)

    def Evaluate(self):
        return int(self.value)


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
        print(self.children[0].Evaluate())


class Assign(Node):

    def __init__(self, table):
        super().__init__("=")
        self.table = table
    
    def Evaluate(self):
        variable = self.children[0].value
        value = self.children[1].Evaluate()
        self.table.set(variable, value)


class Block(Node):

    def __init__(self):
        super().__init__("block")
    
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()