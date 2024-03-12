class Node:

    def __init__(self, value):
        self.value    = value
        self.children = list()

    def Evaluate(self):
        return self.value
    
    def View(self, counter: int=0, margin: str="  "):
        print(counter * margin, self.value, sep="")
        try: self.children[0].View(counter + 1, margin)
        except Exception: return
        try: self.children[1].View(counter + 1, margin)
        except Exception: return


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
        super().__init__(None, [])
