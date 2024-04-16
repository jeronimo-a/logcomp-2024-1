class PrePro:

    @staticmethod
    def filter(text: str):

        # loop de remoção de comentários
        while True:

            try: start = str.index(text, "--")  # índice de início do primeiro comentário
            except ValueError: break            # se não achar, sai do loop de remoção

            # procura o final da linha, consequentemente, o final do comentário
            end = start
            try:
                while text[end] != "\n":
                    end += 1
            except IndexError: pass # passa porque nesse caso end = len(text), e text[end:] = ""

            # remove o comentário
            text = text[:start] + text[end:]

        # remove linhas vazias fora de strings
        in_str = False
        indexes = list()
        for i in range(len(text)):
            if text[i] == '"':
                in_str = not in_str
                continue
            if not in_str and text[i:i+2] == "\n\n":
                indexes.append(i)
        indexes.reverse()
        for i in indexes:
            text = text[:i] + text[i+1:]

        # acrescenta um newline no final, se não haver
        if text[-1] != "\n":
            text += "\n"

        # remove newline do começo
        if text[0] == "\n":
            text = text[1:]

        return text