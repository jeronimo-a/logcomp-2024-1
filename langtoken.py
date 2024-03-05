class Token:

    def __init__(self, token_type: str, value: str):
        self.type   : str = token_type  # tipo do Token, tal como inteiro, sinal de mais, etc.
        self.value  : str = value       # valor do Token, para inteiros, o número em si
    
