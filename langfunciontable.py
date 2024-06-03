class FuncTable:

    def __init__(self):
        self.node_table = dict()

    def get(self, key: str):
        return self.node_table[key]
    
    def set(self, key: str, value):
        _ = self.node_table[key]
        self.node_table[key] = value

    def init(self, key: str):
        try: 
            self.get(key)
            raise ValueError('Função "%s" já foi declarada.' % key)
        except KeyError: pass
        self.node_table[key] = None