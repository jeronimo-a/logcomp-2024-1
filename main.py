import sys
from langparser import Parser

header_file = "assembly_header.asm"
footer_file = "assembly_footer.asm"

def main():
    source = sys.argv[1]
    destination = source.split(".")[0] + ".asm"
    
    with open(header_file) as file:
        header = file.read()
    with open(footer_file) as file:
        footer = file.read()
    with open(source, "r") as file:
        source = file.read()
        try: assembly_code = Parser.run(source)
        except: raise Exception(source)
    
    assembly_code = "\n" + "\n".join(assembly_code) + "\n"
    
    with open(destination, "w+") as file:
        file.write(header)
        file.write(assembly_code)
        file.write(footer)



if __name__ == "__main__":
    main()