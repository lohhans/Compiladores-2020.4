class AnalisadorSintatico:
    def __init__(self, tabelaDeTokens):
        self.tabelaDeTokens = tabelaDeTokens
        self.indexDaTabelaDeTokens = 0

    def tokenAtual(self):
        return self.tabelaDeTokens[self.indexDaTabelaDeTokens]

    def start(self):
        self.statement_list()
        return

    def statement_list(self):
        if(self.tokenAtual().tipo == "PROGRAM"):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == "CLEFT"):
                self.indexDaTabelaDeTokens += 1

                while(self.tokenAtual().tipo != 'CRIGHT'):
                    self.block_statement()

                if(self.tokenAtual().tipo == "CRIGHT"):
                    self.indexDaTabelaDeTokens += 1

                    if(self.tokenAtual().tipo == "END"):
                        print('FIM DO PROGRAMA - DEU CERTO :)')
                        # Deu certo
                    else:
                        raise Exception(
                            'Erro sintatico: falta do END na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do CLEFT na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: Código fora do padrão na linha ' + str(self.tokenAtual().linha))
            self.listaEscopos[0].fechar()
            return

    # TODO: Falta - <call_op>
    # <block>
    def block_statement(self):
        # <declaration_var>
        if (self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            self.declaration_var_statement()

        # <declaration_func>
        elif (self.tokenAtual().tipo == 'FUNC'):
            self.declaration_func_statement()

        # <declaration_proc>
        elif (self.tokenAtual().tipo == 'PROC'):
            self.declaration_proc_statement()

        # Chamadas de função e procedimentos
        elif (self.tokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                self.call_func_statement()
            # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                self.call_proc_statement()
            else:
                raise Exception(
                    'Erro sintatico: falta de PROC ou FUNC' + str(self.tokenAtual().linha))

        # <print_statement>
        elif (self.tokenAtual().tipo == 'PRINT'):
            self.print_statement()

        # <if_statement>
        elif (self.tokenAtual().tipo == 'IF'):
            self.if_statement()

        # <while_statement>
        elif (self.tokenAtual().tipo == 'WHILE'):
            self.while_statement(self)

        # <identifier>
        elif (self.tokenAtual().tipo == 'ID'):
            self.call_var_statement()

        # <call_op>
        # elif (self.tokenAtual())

        else:
            return

    # <declaration_var> OK
    def declaration_var_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ATB'):  # atribuicao
                self.indexDaTabelaDeTokens += 1
                self.end_var_statement()        # o que tem dentro da variavel
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta da atribuição na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # <end_var> OK
    def end_var_statement(self):
        #  <call_func> | <call_op>
        if (self.tokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                self.call_func_statement()
                self.indexDaTabelaDeTokens += 1
            # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                self.call_proc_statement()
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: chamada de função ou procedimento erroneamente na linha ' + str(self.tokenAtual().linha))

        # <boolean>
        if (self.tokenAtual().tipo == 'BOOLEAN'):
            if (self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
                self.indexDaTabelaDeTokens += 1
                return
            else:
                raise Exception(
                    'Erro sintatico: boolean atribuido erroneamente na linha ' + str(self.tokenAtual().linha))
        # <num>
        if (self.tokenAtual().tipo == 'NUM'):
            if (self.tokenAtual().lexema >= '0' and self.tokenAtual().lexema <= '9'):
                self.indexDaTabelaDeTokens += 1
                return
            else:
                raise Exception(
                    'Erro sintatico: int atribuido erroneamente na linha ' + str(self.tokenAtual().linha))

         # <identifier>
        if (self.tokenAtual().tipo == 'ID'):
            self.indexDaTabelaDeTokens += 1

        else:
            raise Exception(
                'Erro sintatico: atribuição de variavel erroneamente na linha ' + str(self.tokenAtual().linha))

    # Chamada de variavel OK
    def call_var_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ATB'):  # atribuicao
            self.indexDaTabelaDeTokens += 1
            if ((self.tokenAtual().tipo == 'NUM') or (self.tokenAtual().tipo == 'BOOLEAN') or (self.tokenAtual().tipo == 'ID')):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: variável não atribuída na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: símbolo de atribuição não encontrado na linha ' + str(self.tokenAtual().linha))

    # TODO: Falta - params, colocar bloco
    # <declaration_func>
    def declaration_func_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):  # tipo
            self.indexDaTabelaDeTokens += 1
            # identificador
            if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'func'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'PLEFT'):
                    self.indexDaTabelaDeTokens += 1
                    # (params) TODO: criar metodo

                    if(self.tokenAtual().tipo == 'CLEFT'):
                        self.indexDaTabelaDeTokens += 1
                        # <block>  TODO: colocar block

                        if(self.tokenAtual().tipo == 'RETURN'):
                            self.return_statement()
                            self.indexDaTabelaDeTokens += 1

                        else:
                            raise Exception(
                                'Erro sintatico: falta do retorno na linha ' + str(self.tokenAtual().linha))

                    else:
                        raise Exception(
                            'Erro sintatico: falta do chave esquerda na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do type na linha ' + str(self.tokenAtual().linha))

    # <return_statement> OK
    def return_statement(self):
        self.indexDaTabelaDeTokens += 1

        # Se for chamada de função
        if (self.TokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            if(self.TokenAtual().tipo == 'FUNC'):
                self.call_func_statement()
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: Erro de chamada, só é permitido chamada de funções na linha ' + str(self.tokenAtual().linha))

        # Se for chamada de variavel/num/bool
        if ((self.tokenAtual().tipo == 'NUM') or (self.tokenAtual().tipo == 'BOOLEAN') or (self.tokenAtual().tipo == 'ID')):
            self.indexDaTabelaDeTokens += 1
            if(self.TokenAtual().tipo == 'SEMICOLON'):
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: Retorno errado na linha ' + str(self.tokenAtual().linha))

    # TODO: Falta - params_call, colocar bloco
    # <call_func>
    def call_func_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'func'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexDaTabelaDeTokens += 1
                # (params_call) TODO: criar metodo
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # TODO: Falta - params, colocar bloco
    # <declaration_proc>
    def declaration_proc_statement(self):
        # <declaration_proc> ::= proc <identifier> (<params>) { <block> }
        self.indexDaTabelaDeTokens += 1
        # identificador
        if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'proc'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexDaTabelaDeTokens += 1
                # (params) TODO: criar metodo

                if(self.tokenAtual().tipo == 'CLEFT'):
                    self.indexDaTabelaDeTokens += 1
                    # <block> TODO: colocar o bloco

                else:
                    raise Exception(
                        'Erro sintatico: falta do chave esquerda na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # TODO: Falta - params_call
    # <call_proc>
    def call_proc_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'proc'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexDaTabelaDeTokens += 1
                # (params_call) TODO: criar metodo
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # TODO: Falta - params_print_statement()
    # <print_statement>
    def print_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == ''):  # <params_print>
                self.indexDaTabelaDeTokens += 1
                # params_print_statement()  # TODO: Criação do método
                if(self.tokenAtual().tipo == 'PRIGHT'):
                    self.indexDaTabelaDeTokens += 1
                    if(self.tokenAtual().tipo == 'SEMICOLON'):
                        self.indexDaTabelaDeTokens += 1
                    else:
                        raise Exception(
                            'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do Parentese direito na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: sem argumento no Print na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do Parentese esquerdo na linha  ' + str(self.tokenAtual().linha))

        # <print_statement> ::= print (<params_print>) ; <block>

    # TODO: Falta - <expression>, <block2>
    # <if_statement>
    def if_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.indexDaTabelaDeTokens += 1
            # <expression> TODO: criar metodo
            if(self.tokenAtual().tipo == 'PRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'CLEFT'):
                    self.indexDaTabelaDeTokens += 1
                    # <block2> TODO: criar metodo
                    if(self.tokenAtual().tipo == 'CRIGHT'):
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'ELSE'):
                            self.indexDaTabelaDeTokens += 1
                            else_part_statement(self)   # Block do ELSE
                            if(self.tokenAtual().tipo == 'ENDIF'):
                                self.indexDaTabelaDeTokens += 1
                            else:
                                raise Exception(
                                    'Erro sintatico: falta de ENDIF ' + str(self.tokenAtual().linha))
                        elif(self.tokenAtual().tipo == 'ENDIF'):
                            self.indexDaTabelaDeTokens += 1
                        else:
                            raise Exception(
                                'Erro sintatico: falta de ENDIF ' + str(self.tokenAtual().linha))
                    else:
                        raise Exception(
                            'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do CLEFT na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do Parentese direito na linha  ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do Parentese esquerdo na linha  ' + str(self.tokenAtual().linha))

    # TODO: Falta - colocar block2
    # <else_part>
    def else_part_statement(self):
        if(self.tokenAtual().tipo == 'CLEFT'):
            self.indexDaTabelaDeTokens += 1
            # <block2> TODO: criar metodo
            if(self.tokenAtual().tipo == 'CRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'ENDELSE'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta de ENDIF na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do CLEFT na linha ' + str(self.tokenAtual().linha))

    # TODO: <expression>, <block2>
    # <while_statement> ::= while(<expression>){<block2>}endwhile
    def while_statement(self):
        def while_statement(self):
        self.indexDaTabelaDeTokens += 1
        self.indexDaTabelaDeTokens += 1
        self.indexDaTabelaDeTokens += 1
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.indexDaTabelaDeTokens += 1
            # <expression> TODO: fazer método
            if(self.tokenAtual().tipo == 'PRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'CLEFT'):
                    self.indexDaTabelaDeTokens += 1

                    # Block while TODO: criar metodo com break e continue
                    if (self.tokenAtual().tipo == 'ENDWHILE'):
                        self.indexDaTabelaDeTokens += 1

                    else:
                        raise Exception(
                            'Erro sintatico: falta de ENDWHILE na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do PRIGHT na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do PLEFT na linha ' + str(self.tokenAtual().linha))

    # TODO: funções que faltam
    # def params
    # <params_call>
    # <expression>
    # <call_op>
    # <unconditional_branch>
