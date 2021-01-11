from lexer.scanner import Scanner

import sys

if __name__ == '__main__':
    caminho = sys.argv[1]

    try:
        arquivo = open(caminho, 'r')
        programa = ''.join(arquivo.readlines())
        arquivo.close()
    except Exception:
        print("Error: caminho não informado")
        sys.exit(1)

    lexer = Scanner(programa)

    tabelaDeTokens = lexer.scan()

    for i in tabelaDeTokens:
        print(i.lexema)

    # for i in tabelaDeTokens:
    #     print(i)

else:
    print('me executou como um módulo')