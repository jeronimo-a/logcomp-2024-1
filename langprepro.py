class PrePro:

    @staticmethod
    def filter(text: str):

        # remove linhas vazias
        new_text = text.replace("\n\n", "\n")
        while new_text != text:
            text = new_text
            new_text = text.replace("\n\n", "\n")

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

        if text[-1] != "\n": text += "\n"

        return text