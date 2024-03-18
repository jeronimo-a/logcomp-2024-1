class SymbolTable:

    def __init__(self):
        self.table = dict()

    def get(self, key: str):
        return self.table[key]
    
    def set(self, key: str, value: int):
        self.table[key] = value