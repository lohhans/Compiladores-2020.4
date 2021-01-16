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
            # TODO: Tratar erro
            self.listaEscopos[0].fechar()
            return

    # <block>
    def block_statement(self):
        # <declaration_var>
        if (self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            self.declaration_var_statement()
            return True
        # <declaration_func>
        elif (self.tokenAtual().tipo == 'FUNC'):
            self.declaration_func_statement()
            return True
        # <declaration_proc>
        elif (self.tokenAtual().tipo == 'PROC'):
            self.declaration_proc_statement()
            return True
        elif (self.tokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                self.call_func_statement()
                return True
            # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                self.call_proc_statement()
                return True
            else:
                raise Exception(
                    'Erro sintatico: falta de PROC ou FUNC' + str(self.tokenAtual().linha))

        # <print_statement>
        elif (self.tokenAtual().tipo == 'PRINT'):
            self.print_statement()
            return True

        # <if_statement>
        elif (self.tokenAtual().tipo == 'IF'):
            self.if_statement()
            return True
        
        # TODO: Colocar os outros métodos

    # <declaration_var>
    def declaration_var_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ATB'):  # atribuicao
                self.indexDaTabelaDeTokens += 1
                self.end_var_statement()        # o que tem dentro da variavel
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1

                    return
                else:
                    raise Exception('Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception('Erro sintatico: falta da atribuição na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception('Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))
    # <end_var> 
    def end_var_statement(self):
        #  <call_func> | <call_op>
        if (self.tokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                self.call_func_statement()
             # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                self.call_proc_statement()
            else:
                raise Exception('Erro sintatico: chamada de função ou procedimento erroneamente na linha ' + str(self.tokenAtual().linha))
        
        # <boolean>
        if (self.tokenAtual().tipo == "BOOLEAN"):
            if (self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
                self.indexDaTabelaDeTokens += 1
                return
            else:
                raise Exception('Erro sintatico: boolean atribuido erroneamente na linha ' + str(self.tokenAtual().linha))
        # <num>
        if (self.tokenAtual().tipo == "NUM"):
            if (self.tokenAtual().lexema >= '0' and self.tokenAtual().lexema <= '9'):
                self.indexDaTabelaDeTokens += 1
                return
            else:
                raise Exception('Erro sintatico: int atribuido erroneamente na linha ' + str(self.tokenAtual().linha))
        
    # <identifier>
    def identifier_statement(self):
        return
        #<identifier> ::= <letter> (<letter> | <num>)* 

    # <declaration_func>
    def declaration_func_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):  # tipo
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # identificador
            if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'func'):
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                # (params) TODO: criar metodo
            else:
                raise Exception(
                    'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do type na linha ' + str(self.tokenAtual().linha))

    # <call_func>
    def call_func_statement(self):
        if(self.tokenAtual().tipo == 'CALL'):
            temp = []
            temp.append('CALL')
            escopoDaFuncao = self.indexEscopoAtual
            escopoForaDaFunc = self.indexEscopoAtual
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'FUNC'):
                temp.append('FUNC')
                escopoDaFuncao = self.indexEscopoAtual
                escopoForaDaFunc = self.indexEscopoAtual
                self.indexDaTabelaDeTokens += 1
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
            self.indexDaTabelaDeTokens += 1
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
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PROC'):
                temp.append('PROC')
                escopoDaFuncao = self.indexEscopoAtual
                escopoForaDaFunc = self.indexEscopoAtual
                self.indexDaTabelaDeTokens += 1
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
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                temp.append('PLEFT')
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == ''):  # <params_print>
                    temp.append('')  # <params_print>
                    self.indexDaTabelaDeTokens += 1
                    params_print_statement()  # TODO: Criação do método

                    if(self.tokenAtual().tipo == 'PRIGHT'):
                        temp.append('PRIGHT')
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'SEMICOLON'):
                            temp.append('SEMICOLON')
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
        else:
            return

            # <print_statement> ::= print (<params_print>) ; <block>
            # <params_print> ::= <identifier> | <call_func> | <call_op> | <boolean> | <num>

    # <if_statement>
    def if_statement(self):
        if(self.tokenAtual().tipo == 'IF'):
            temp = []
            temp.append('IF')
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
        else:
            return

    # <else_part>
    def else_part_statement(self):
        if(self.tokenAtual().tipo == 'ELSE'):
            temp = []
            temp.append('ELSE')
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'CLEFT'):
                self.indexDaTabelaDeTokens += 1

                # <block2> TODO: criar metodo

                if(self.tokenAtual().tipo == 'CRIGHT'):
                    self.indexDaTabelaDeTokens += 1

                    if(self.tokenAtual().tipo == 'ENDELSE'):
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
            return

    # <while_statement> ::= while(<expression>){<block2>}endwhile
    def while_statement(self):
        if(self.tokenAtual().tipo == 'WHILE'):
            temp = []
            temp.append('WHILE')
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexDaTabelaDeTokens+=1
                # <expression> TODO: fazer método

                if(self.tokenAtual().tipo == 'PRIGHT'):
                    self.indexDaTabelaDeTokens+=1
                    if(self.tokenAtual().tipo == 'CLEFT'):
                        self.indexDaTabelaDeTokens += 1

                    # Block while TODO: criar metodo com break e continue

                        if (self.tokenAtual().tipo == 'ENDWHILE'):
                            temp = []
                            temp.append('WHILE')
                            self.indexDaTabelaDeTokens += 1
                        
                        else:
                            raise Exception(
                                'Erro sintatico: falta de ENDWHILE ' + str(self.tokenAtual().linha))
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
    # def end_var
    # def <return_statement>
    # <identifier> (variavel)
    # <program> ::= program { <block> } end
    # <expression>
    # <unconditional_branch>
    
