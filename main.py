import sys
from langparser import Parser

def main():
    source = sys.argv[1]
    with open(source, "r") as file:
        result = Parser.run(file.read())
    print(result)

if __name__ == "__main__":
    main()