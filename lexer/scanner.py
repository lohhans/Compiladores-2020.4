from token import Token

class Scanner:

    # Construtor da classe
    def __init__(self, programa):
        self.inicio = 0
        self.atual = 0
        self.linha = 1
        self.tokens = []
        self.programa = programa

    # Busca caracteres, passa para o próximo char (atual é o char a frente do que tá sendo lido)
    def nextChar(self):
        self.atual += 1
        return self.programa[self.atual - 1]  #

    # Chama o buscador de Tokens, adiciona o fim do arquivo (Token END),
    # chama o buscador de token de palavras reservadas
    def scan(self):
        self.scanTokens()
        self.tokens.append(Token("END", '', self.linha))
        self.scanReserved()
        return self.tokens

    # Procura tokens até chegar no Fim
    def scanTokens(self):
        while(self.atual < len(self.programa)):
            self.inicio = self.atual
            char = self.nextChar()

            if char == ' ' or char == '\t' or char == '\r':
                pass

            elif char == '\n':
                self.linha += 1

            # Delimitadores
            elif char == '(':  # Parentese esquerdo
                self.tokens.append(
                    Token("PLEFT", self.programa[self.inicio:self.atual], self.linha))

            elif char == ')':  # Parentese direito
                self.tokens.append(
                    Token("PRIGHT", self.programa[self.inicio:self.atual], self.linha))

            elif char == '{':  # Chaves esquerdo
                self.tokens.append(
                    Token("CLEFT", self.programa[self.inicio:self.atual], self.linha))

            elif char == '}':  # Chaves direito
                self.tokens.append(
                    Token("CRIGHT", self.programa[self.inicio:self.atual], self.linha))

            # Operações Aritméticas
            elif char == '+':  # Soma
                self.tokens.append(
                    Token("ADD", self.programa[self.inicio:self.atual], self.linha))

            elif char == '-':  # Subtração
                self.tokens.append(
                    Token("SUB", self.programa[self.inicio:self.atual], self.linha))

            elif char == '*':  # Multiplicação
                self.tokens.append(
                    Token("MULT", self.programa[self.inicio:self.atual], self.linha))

            elif char == '/':  # Divisão
                self.tokens.append(
                    Token("DIV", self.programa[self.inicio:self.atual], self.linha))

            # Operações Booleanas
            elif char == '=':  # Igual ou Atribuição
                if self.lookAhead() == '=':  # == (comparação)
                    self.atual += 1
                    self.tokens.append(
                        Token("EQUAL", self.programa[self.inicio:self.atual], self.linha))
                else:  # = (atribuição)
                    self.tokens.append(
                        Token("ATB", self.programa[self.inicio:self.atual], self.linha))

            elif char == '!':  # Diferente
                if self.lookAhead() == '=':
                    self.atual += 1
                    self.tokens.append(
                        Token("DIFF", self.programa[self.inicio:self.atual], self.linha))

            elif char == '<':  # Menor ou igual, menor
                if self.lookAhead() == '=':
                    self.atual += 1
                    self.tokens.append(
                        Token("LESSEQUAL", self.programa[self.inicio:self.atual], self.linha))
                else:
                    self.tokens.append(
                        Token("LESS", self.programa[self.inicio:self.atual], self.linha))

            elif char == '>':  # Maior ou igual, Maior
                if self.lookAhead() == '=':
                    self.atual += 1
                    self.tokens.append(
                        Token("GREATEREQUAL", self.programa[self.inicio:self.atual], self.linha))
                else:
                    self.tokens.append(
                        Token("GREATER", self.programa[self.inicio:self.atual], self.linha))

            # Separador
            elif char == ',':  # Virgula
                self.tokens.append(
                    Token("COMMA", self.programa[self.inicio:self.atual], self.linha))

            # Demarcador de fim de bloco / expressão
            elif char == ';':  # Ponto e virgula
                self.tokens.append(
                    Token("SEMICOLON", self.programa[self.inicio:self.atual], self.linha))

            # Números
            elif char >= '0' and char <= '9':
                while(self.lookAhead() >= '0' and self.lookAhead() <= '9'):
                    self.nextChar()
                self.tokens.append(
                    Token("NUM", self.programa[self.inicio:self.atual], self.linha))

            # Letras / Identificadores / Palavras Reservadas
            elif char.isalpha():
                while(self.lookAhead().isalnum()):
                    self.nextChar()
                self.tokens.append(
                    Token("ID", self.programa[self.inicio:self.atual], self.linha))

            # Outros/Error
            else:
                print('Invalid character in line:', self.linha)
                exit(2)

    def scanReserved(self):
        for i in self.tokens:
            if(i.tipo == 'ID'):

                # Inicio do programa
                if(i.lexema == 'program'):
                    i.tipo = "PROGRAM"

                # Fim do programa
                elif(i.lexema == 'end'):
                    i.tipo = "END"

                # Identificador de função
                elif(i.lexema == 'func'):
                    i.tipo = "FUNC"

                # Identificador de procedimento
                elif(i.lexema == 'proc'):
                    i.tipo = "PROC"

                # Identificador de inteiros
                elif(i.lexema == 'int'):
                    i.tipo = 'INT'

                # Tipo Booleano
                elif(i.lexema == 'bool'):
                    i.tipo = 'BOOL'

                # Booleano Verdadeiro
                elif(i.lexema == 'True'):
                    i.tipo = 'BOOLEAN'

                # Booleano Falso
                elif(i.lexema == 'False'):
                    i.tipo = 'BOOLEAN'

                # Retorno da função
                elif(i.lexema == 'return'):
                    i.tipo = 'RETURN'

                # Condicional IF
                elif(i.lexema == 'if'):
                    i.tipo = 'IF'

                # Condicional ELSE
                elif(i.lexema == 'else'):
                    i.tipo = 'ELSE'

                # Condicional WHILE
                elif(i.lexema == 'while'):
                    i.tipo = 'WHILE'

                 # Escrita na tela
                elif(i.lexema == 'print'):
                    i.tipo = 'PRINT'

                # Incondicional BREAK
                elif(i.lexema == 'break'):
                    i.tipo = 'BREAK'

                # Incondicional CONTINUE
                elif(i.lexema == 'continue'):
                    i.tipo = 'CONTINUE'

    # Verifica o simbolo a frente e se está no final do programa
    def lookAhead(self):
        if(self.atual < len(self.programa)):
            return self.programa[self.atual]  
        else:
            return '\0'