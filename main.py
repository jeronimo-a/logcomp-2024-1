import sys
from langparser import Parser

def main():
    source = sys.argv[1]
    result = Parser.run(source)
    print(result)

if __name__ == "__main__":
    main()