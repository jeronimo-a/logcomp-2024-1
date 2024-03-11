class PrePro:

    @staticmethod
    def filter(text: str):

        try: i = str.index(text, "--")
        except ValueError: i = len(text)
        return text[:i].strip()