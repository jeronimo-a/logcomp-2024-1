class SymbolTable:

    shift = 4

    def __init__(self):
        self.table = dict()

    def get(self, key: str):
        return self.table[key]
    
    def set(self, key: str, type: str, value):
        _ = self.table[key]
        self.table[key] = (type, value, self.table[key][2])

    def init(self, key: str):
        try: 
            self.get(key)
            raise ValueError('Variável "%s" já foi declarada.' % key)
        except KeyError: pass
        self.table[key] = (None, None, SymbolTable.shift)
        SymbolTable.shift += 4