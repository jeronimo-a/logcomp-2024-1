def remove_all_empty_str(iterable):
    result = iterable.copy()
    while True:
        try: result.remove('')
        except ValueError: break
    return result


def read_token_types_file(filename):

    try:
        with open(filename) as file:
            contents = file.read().split("#")
            
        types = contents[1].split("\n")[1:]
        words = contents[2].split("\n")[1:]
        types = remove_all_empty_str(types)
        words = remove_all_empty_str(words)

        words_dict = dict()
        for word in words:
            word = word.replace("\t", " ")
            values = word.split(" ")
            values = remove_all_empty_str(values)
            if values[1] not in types:
                raise Exception('Tipo "%s" para a palavra reservada "%s" não existe' % (values[1], values[0]))
            words_dict[values[0]] = values[1]

        return types, words_dict
    
    except:
        raise Exception("Formatação inválida de tokentypes.txt")