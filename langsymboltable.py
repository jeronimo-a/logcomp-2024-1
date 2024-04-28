class SymbolTable:

    def __init__(self):
        self.value_table = dict()
        self.type_table = dict()

    def get(self, key: str):
        return self.value_table[key], self.type_table[key]
    
    def set(self, key: str, value, type: str):
        _ = self.value_table[key]
        _ = self.type_table[key]
        self.value_table[key] = value
        self.type_table[key] = type

    def init(self, key: str):
        try: 
            self.get(key)
            raise ValueError('Variável "%s" já foi declarada.' % key)
        except KeyError: pass
        self.value_table[key] = None
        self.type_table[key] = None