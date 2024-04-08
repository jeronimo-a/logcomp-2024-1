def remove_all_empty_str(iterable):
    result = iterable.copy()
    while True:
        try: result.remove('')
        except ValueError: break
    return result


def read_alphabet_file(filename):

    with open(filename) as file:
        contents = file.read().split("#")
        
    types = contents[1].split("\n")[1:]
    words = contents[2].split("\n")[1:]
    types = remove_all_empty_str(types)
    words = remove_all_empty_str(words)

    return types, words