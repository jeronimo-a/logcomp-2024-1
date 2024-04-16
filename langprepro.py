class PrePro:

    @staticmethod
    def filter(text: str):

        # remove comentários
        while True:
            try: start = str.index(text, "--")
            except ValueError: break
            end = start
            try:
                while text[end] != "\n":
                    end += 1
            except IndexError:
                text = text[:start]
                break
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