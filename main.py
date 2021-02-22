from lexer.scanner import Scanner
from parser_compiler.parser import Parser
from pprint import pprint

import sys

if __name__ == "__main__":
    caminho = sys.argv[1]

    try:
        arquivo = open(caminho, "r")
        programa = "".join(arquivo.readlines())
        arquivo.close()
    except Exception:
        print("Error: caminho não informado")
        sys.exit(1)

    lexer = Scanner(programa)

    tabelaDeTokens = lexer.scan()

    parser = Parser(tabelaDeTokens)

    # print("\nTABELA DE TOKENS:\n")
    # for i in tabelaDeTokens:
    #     print(i)

    try:
        parser.start()
        print("\nTABELA DE SÍMBOLOS:")
        pprint(parser.tabelaDeSimbolos)
    except Exception as e:
        print(e)

else:
    print("me executou como um módulo")
