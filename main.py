from lexer.scanner import Scanner
from analisador_sintatico.analisador_sintatico import AnalisadorSintatico

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

    # for i in tabelaDeTokens:
    #     print(i.lexema)

    for i in tabelaDeTokens:
        print(i)
    
    AnalisadorSintatico(tabelaDeTokens)

else:
    print('me executou como um módulo')