class SymbolTable:

    def __init__(self):
        self.table = dict()

    def get(self, key: str):
        return self.table[key]
    
    def set(self, key: str, value):
        current_value = self.table[key]
        self.table[key] = value

    def init(self, key: str):
        self.table[key] = None