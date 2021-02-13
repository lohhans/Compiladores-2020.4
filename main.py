from lexer.scanner import Scanner
from analisador_sintatico.analisador_sintatico import AnalisadorSintatico
from pprint import pprint

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
    # tabelaDeSimbolos = []

    # for i in tabelaDeTokens:
    #     print(i.lexema)

    print('Tabela de tokens:\n')
    for i in tabelaDeTokens:
        print(i)
        # tabelaDeSimbolos.append(i.lexema)

    # print('Tabela de símbolos:\n')
    # print(tabelaDeSimbolos)

    analisadorSintatico = AnalisadorSintatico(tabelaDeTokens, programa)

    try:
        analisadorSintatico.start()
        print('\n--- PÓS LEXER ---\n')
        pprint(analisadorSintatico.tabelaDeSimbolos)
    except Exception as e:
        print(e)

else:
    print('me executou como um módulo')
