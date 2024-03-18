import sys
from langparser import Parser

def main():
    source = sys.argv[1]
    with open(source, "r") as file:
        result = Parser.run(file.read())

if __name__ == "__main__":
    main()