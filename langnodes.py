class Node:

    id = 0

    def __init__(self, value):
        self.value    = value
        self.children = list()
        self.id = Node.id
        Node.id += 1

    def Evaluate(self):
        return list()
    
    def View(self, counter: int=0, margin: str="  "):
        print(counter * margin, self.value, sep="")
        for child in self.children:
            child.View(counter + 1, margin)


class BinOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self):

        code = list()
        code += self.children[1].Evaluate()
        code += ["PUSH EAX"]
        code += self.children[0].Evaluate()
        code += ["POP EBX"]

        if self.value == "or" : code += ["OR EAX, EBX"]
        if self.value == "and": code += ["AND EAX, EBX"]
        if self.value == "==" : code += ["CMP EBX, EAX", "SETE AL", "MOVZX EAX, AL"]
        if self.value == "<"  : code += ["CMP EBX, EAX", "SETG AL", "MOVZX EAX, AL"]
        if self.value == ">"  : code += ["CMP EBX, EAX", "SETL AL", "MOVZX EAX, AL"]
        if self.value == "+"  : code += ["ADD EAX, EBX"]
        if self.value == "-"  : code += ["SUB EAX, EBX"]
        if self.value == "*"  : code += ["IMUL EAX, EBX"]
        if self.value == "/"  : code += ["MOV EDX, 0", "IDIV EBX"]

        return code

class UnOp(Node):

    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self):

        code = list()
        code += self.children[0].Evaluate()

        if self.value == "-"  : code += ["NEG EAX"]
        if self.value == "not": code += ["CMP EAX, 0", "SETNE AL", "MOVZX EAX, AL"]

        return code


class IntVal(Node):

    def __init__(self, value: int):
        super().__init__(value)

    def Evaluate(self): 
        return ["MOV EAX, %d" % int(self.value)]
    

class StrVal(Node):

    def __init__(self, value: int):
        super().__init__(value)
    
    def Evaluate(self):
        return "str", str(self.value), 0


class NoOp(Node):

    def __init__(self):
        super().__init__(None)


class Ident(Node):

    def __init__(self, value: str, table):
        super().__init__(value)
        self.table = table

    def Evaluate(self):
        try: _, _, shift = self.table.get(self.value)
        except KeyError: raise Exception('Variável "%s" não existe' % self.value)
        return ["MOV EAX, [EBP - %d]" % shift]
    

class Print(Node):

    def __init__(self):
        super().__init__("print")

    def Evaluate(self):
        code = list()
        code += self.children[0].Evaluate()
        code += ["PUSH EAX"]
        code += ["PUSH formatout"]
        code += ["CALL printf"]
        code += ["ADD ESP, 8"]
        return code


class Read(Node):

    def __init__(self):
        super().__init__("read")

    def Evaluate(self):
        code = list()
        code += ["PUSH scanint"]
        code += ["PUSH formatin"]
        code += ["CALL scanf"]
        code += ["ADD ESP, 8"]
        code += ["MOV EAX, DWORD [scanint]"]
        return code


class Assign(Node):

    def __init__(self, table):
        super().__init__("=")
        self.table = table
    
    def Evaluate(self):
        variable = self.children[0].value
        _, _, shift = self.table.get(variable)
        code = list()
        code += self.children[1].Evaluate()
        code += ["MOV [EBP - %d], EAX" % shift]
        return code


class Block(Node):

    def __init__(self):
        super().__init__("%BLOCK%")
    
    def Evaluate(self):
        code = list()
        for child in self.children:
            code += child.Evaluate()
        return code


class While(Node):

    def __init__(self):
        super().__init__("while")

    def Evaluate(self):
        code = list()
        code += ["LOOP_%d:" % self.id]
        code += self.children[0].Evaluate()
        code += ["CMP EAX, False"]
        code += ["JE EXIT_%d" % self.id]
        code += self.children[1].Evaluate()
        code += ["JMP LOOP_%d" % self.id]
        code += ["EXIT_%d:" % self.id]
        return code


class If(Node):

    def __init__(self):
        super().__init__("if")

    def Evaluate(self):
        if self.children[0].Evaluate()[0]: self.children[1].Evaluate()    # Block
        else: self.children[2].Evaluate()                   # Block


class Vardec(Node):

    def __init__(self, table):
        super().__init__("local")
        self.table = table

    def Evaluate(self):
        self.table.init(self.children[0].value)
        code = ["PUSH DWORD 0"]
        try: code += self.children[1].Evaluate()
        except IndexError: pass
        return code