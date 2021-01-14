class AnalisadorSintatico:
    def __init__(self, tabelaDeTokens):
        self.tabelaDeTokens = tabelaDeTokens
        self.indexDaTabelaDeTokens = 0

    def statement_list(self):
        if(self.tokenAtual().tipo == "PROGRAM"):
            self.indexToken += 1
            if(self.tokenAtual().tipo == "CLEFT"):
                self.indexToken += 1
                if(block() == True):    # tem algo no block para rodar
                    self.statement()
                    self.statement_list()

                else:                   # bloco vazio
                    if(self.tokenAtual().tipo == "CRIGHT"):
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == "END"):
                            self.listaEscopos[0].fechar()
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
            # TODO: Tratar erro
            self.listaEscopos[0].fechar()
            return

    # <declaration_var>
    def declaration_var_statement(self):
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            temp = []
            temp.append('VAR')
            temp.append(self.tokenAtual().tipo)
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'ID'):
                temp.append(self.tokenAtual().lexema)
                self.indexToken += 1
                if(self.tokenAtual().tipo == 'ATTR'):  # atribuicao
                    self.indexToken += 1
                    # TODO: aqui vem o end_var
                else:
                    raise Exception(
                        'Erro sintatico: falta da atribuição na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))
        else:
            return

    # <declaration_func>
    def declaration_func_statement(self):
        if(self.tokenAtual().tipo == 'FUNC'):
            temp = []
            temp.append('FUNC')
            escopoDaFuncao = self.indexEscopoAtual
            escopoForaDaFunc = self.indexEscopoAtual
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):  # tipo
                temp.append(self.tokenAtual().tipo)
                self.indexToken += 1
                # identificador
                if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'func'):
                    temp.append(self.tokenAtual().lexema)
                    self.indexToken += 1
                    # (params) TODO: criar metodo
                else:
                    raise Exception(
                        'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do type na linha ' + str(self.tokenAtual().linha))
        else:
            return

    # <call_func>
    def call_func_statement(self):
        if(self.tokenAtual().tipo == 'CALL'):
            temp = []
            temp.append('CALL')
            escopoDaFuncao = self.indexEscopoAtual
            escopoForaDaFunc = self.indexEscopoAtual
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'FUNC'):
                temp.append('FUNC')
                escopoDaFuncao = self.indexEscopoAtual
                escopoForaDaFunc = self.indexEscopoAtual
                self.indexToken += 1
                # <identifier> (<params_call>)   TODO: fazer metodo
            else:
                raise Exception(
                    'Erro sintatico: falta do FUNC na linha ' + str(self.tokenAtual().linha))
        else:
            return

    # <declaration_proc>
    def declaration_proc_statement(self):
        if(self.tokenAtual().tipo == 'PROC'):
            temp = []
            temp.append('PROC')
            escopoDoProcecimento = self.indexEscopoAtual
            escopoForaDoProc = self.indexEscopoAtual
            self.indexToken += 1
            # <identifier> (<params>) { <block> } TODO: fazer método
        else:
            return

    # <call_proc>
    def call_proc_statement(self):
        if(self.tokenAtual().tipo == 'CALL'):
            temp = []
            temp.append('CALL')
            escopoDaFuncao = self.indexEscopoAtual
            escopoForaDaFunc = self.indexEscopoAtual
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'PROC'):
                temp.append('PROC')
                escopoDaFuncao = self.indexEscopoAtual
                escopoForaDaFunc = self.indexEscopoAtual
                self.indexToken += 1
                # <identifier> (<params_call>) TODO: Fazer método
            else:
                raise Exception(
                    'Erro sintatico: falta do PROC na linha ' + str(self.tokenAtual().linha))
        else:
            return

    # <print_statement>
    def print_statement(self):
        if(self.tokenAtual().tipo == 'PRINT'):
            temp = []
            temp.append('PRINT')
            escopoDaFuncao = self.indexEscopoAtual
            escopoForaDaFunc = self.indexEscopoAtual
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                temp.append('PLEFT')
                self.indexToken += 1
                if(self.tokenAtual().tipo == ''):  # <params_print>
                    temp.append('')  # <params_print>
                    self.indexToken += 1
                    params_print_statement()  # TODO: Criação do método

                    if(self.tokenAtual().tipo == 'PRIGHT'):
                        temp.append('PRIGHT')
                        self.indexToken += 1
                        if(self.tokenAtual().tipo == 'SEMICOLON'):
                            temp.append('SEMICOLON')
                            self.indexToken += 1
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
        else:
            return

            # <print_statement> ::= print (<params_print>) ; <block>
            # <params_print> ::= <identifier> | <call_func> | <call_op> | <boolean> | <num>

    # <if_statement>
    def if_statement(self):
        if(self.tokenAtual().tipo == 'IF'):
            temp = []
            temp.append('IF')
            self.indexToken += 1

            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexToken += 1
                # <expression> TODO: criar metodo

                if(self.tokenAtual().tipo == 'PRIGHT'):
                    self.indexToken += 1
                    if(self.tokenAtual().tipo == 'CLEFT'):
                        self.indexToken += 1

                        # <block2> TODO: criar metodo

                        if(self.tokenAtual().tipo == 'CRIGHT'):
                            self.indexToken += 1

                            if(self.tokenAtual().tipo == 'ELSE'):
                                self.indexToken += 1

                                else_part_statement(self)   # Block do ELSE

                                if(self.tokenAtual().tipo == 'ENDIF'):
                                    self.indexToken += 1

                                else:
                                    raise Exception(
                                        'Erro sintatico: falta de ENDIF ' + str(self.tokenAtual().linha))

                            elif(self.tokenAtual().tipo == 'ENDIF'):
                                self.indexToken += 1

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
        else:
            return

    # <else_part>
    def else_part_statement(self):
        if(self.tokenAtual().tipo == 'ELSE'):
            self.indexToken += 1

        # TODO: funções que faltam

        # def block
        # def params
        # <params_call>
        # def end_var
        # def <return_statement>
        # <identifier> (variavel)
        # <program> ::= program { <block> } end
        # <expression>
        # <unconditional_branch>
