from analisador_sintatico.escopo import Escopo
import re

#print('Entrou... Tipo: %s, lexema: %s, na linha: %s' % (self.tokenAtual().tipo, self.tokenAtual().lexema, self.tokenAtual().linha))


class AnalisadorSintatico:
    def __init__(self, tabelaDeTokens, programa):
        self.tabelaDeTokens = tabelaDeTokens
        self.indexDaTabelaDeTokens = 0
        self.indexLookAhead = 0
        self.programa = programa
        # self.listaEscopos = []
        self.indexEscopoAtual = -1
        self.tabelaDeSimbolos = []
        # Pra saber na semantica qual declaracao de variavel no codigo tá sendo checada
        self.indexDaDeclaracaoDaVariavelAtual = -1
        self.indexEscopoAntesDaFuncao = 0

    def tokenAtual(self):
        return self.tabelaDeTokens[self.indexDaTabelaDeTokens]

    def tokenLookAhead(self):
        self.indexLookAhead = self.indexDaTabelaDeTokens + 1
        return self.tabelaDeTokens[self.indexLookAhead]

    def start(self):
        self.indexEscopoAtual += 1
        # escopoInicial = Escopo(self.indexEscopoAtual+1, self.indexEscopoAtual)
        # self.listaEscopos.append(escopoInicial)
        self.statement_list()
        return

    def statement_list(self):
        if(self.tokenAtual().tipo == "END"):
            # self.listaEscopos[0].fechar()
            return
        else:
            self.statement()
            self.statement_list()
            return

    def statement(self):
        if(self.tokenAtual().tipo == "PROGRAM"):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == "CLEFT"):
                self.indexDaTabelaDeTokens += 1

                while(self.tokenAtual().tipo != 'CRIGHT'):
                    self.block_statement()

                if(self.tokenAtual().tipo == "CRIGHT"):
                    self.indexDaTabelaDeTokens += 1

                    if(self.tokenAtual().tipo == "END"):
                        print('FIM DA ANÁLISE SINTÁTICA - DEU CERTO :)')
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

    # <block>
    def block_statement(self):
        # ESCOPO OK
        # <declaration_var>
        if (self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.declaration_var_statement(temp)

        # ESCOPO OK
        # <declaration_func>
        if (self.tokenAtual().tipo == 'FUNC'):
            # Ordem: [escopo, tipo, tipoDoRetorno, id, [[params], [params], [params]]]
            # Obs: Params pode ser >= 0
            temp = []
            temp.append(self.indexEscopoAtual)
            # temp.append('FUNC')
            temp.append(self.tokenAtual().tipo)

            self.declaration_func_statement(temp)

        # ESCOPO OK
        # <declaration_proc>
        if (self.tokenAtual().tipo == 'PROC'):
            temp = []
            temp.append(self.indexEscopoAtual)
            # temp.append('PROC')
            temp.append(self.tokenAtual().tipo)
            self.declaration_proc_statement(temp)

        # ESCOPO OK
        # Chamadas de função e procedimentos
        if (self.tokenAtual().tipo == 'CALL'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                temp.append(self.tokenAtual().tipo)
                temp = self.call_func_statement(temp)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                temp.append(self.tokenAtual().tipo)
                temp = self.call_proc_statement(temp)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta de PROC ou FUNC' + str(self.tokenAtual().linha))

        # TODO: ESCOPO DO PRINT BLOCK 1
        # <print_statement>
        if (self.tokenAtual().tipo == 'PRINT'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.print_statement(temp)

        # TODO: ESCOPO DO IF BLOCK 1
        # <if_statement>
        if (self.tokenAtual().tipo == 'IF'):
            self.if_statement()

        # TODO: ESCOPO DO WHILE BLOCK 1
        # <while_statement>
        if (self.tokenAtual().tipo == 'WHILE'):
            self.while_statement()

        # ESCOPO OK
        # <identifier>
        if (self.tokenAtual().tipo == 'ID'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().lexema)
            self.call_var_statement(temp)

        else:
            return

    # block2 é o bloco que contém break/continue que só pode ser chamado dentro de um while
    def block2_statement(self):
        # ESCOPO OK
        # <declaration_var>
        if (self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.declaration_var_statement(temp)
            return

        # ESCOPO OK
        # Chamadas de função e procedimentos
        if (self.tokenAtual().tipo == 'CALL'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                temp.append(self.tokenAtual().tipo)
                temp = self.call_func_statement(temp)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                temp.append(self.tokenAtual().tipo)
                temp = self.call_proc_statement(temp)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta de PROC ou FUNC' + str(self.tokenAtual().linha))

        # TODO: ESCOPO DO PRINT DO BLOCK 2
        # <print_statement>
        if (self.tokenAtual().tipo == 'PRINT'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.print_statement(temp)
            return

        # TODO: ESCOPO IF DO BLOCK 2
        # <if_statement>
        if (self.tokenAtual().tipo == 'IF'):
            self.if_statement2()
            return

        # TODO: ESCOPO DO ELSE DO BLOCK 2
        # Tratamento de erro ELSE
        if (self.tokenAtual().tipo == 'ELSE'):
            raise Exception(
                'Erro sintatico: ELSE adicionado de maneira incorreta ' + str(self.tokenAtual().linha))

        # TODO: ESCOPO DO WHILE DO BLOCK 2
        # <while_statement>
        if (self.tokenAtual().tipo == 'WHILE'):
            self.while_statement()
            return

        # ESCOPO OK
        # <identifier>
        if (self.tokenAtual().tipo == 'ID'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().lexema)
            self.call_var_statement(temp)
            return

        # TODO: ESCOPO DO UNCONDITIONAL BRANCH DO BLOCK 2
        # <unconditional_branch>
        if (self.tokenAtual().tipo == 'BREAK' or self.tokenAtual().tipo == 'CONTINUE'):
            self.unconditional_branch_statement()
            return

        else:
            raise Exception(
                'Erro sintatico: bloco vazio na linha ' + str(self.tokenAtual().linha))

    # block3 é o bloco do if/else, que não pode declarar função e procedimento dentro
    def block3_statement(self):
        # ESCOPO OK
        # <declaration_var>
        if (self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.declaration_var_statement(temp)
            return

        # ESCOPO OK
        # Chamadas de função e procedimentos
        if (self.tokenAtual().tipo == 'CALL'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                temp.append(self.tokenAtual().tipo)
                temp = self.call_func_statement(temp)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            # <call_proc>
            elif (self.tokenAtual().tipo == 'PROC'):
                temp.append(self.tokenAtual().tipo)
                temp = self.call_proc_statement(temp)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta de PROC ou FUNC' + str(self.tokenAtual().linha))

        # TODO: ESCOPO DO PRINT BLOCK 3
        # <print_statement>
        if (self.tokenAtual().tipo == 'PRINT'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().tipo)
            self.print_statement(temp)
            return

        # TODO: ESCOPO DO IF BLOCK 3
        # <if_statement>
        if (self.tokenAtual().tipo == 'IF'):
            self.if_statement()
            return

        # TODO: ESCOPO DO ELSE BLOCK 3
        # Tratamento de erro ELSE
        if (self.tokenAtual().tipo == 'ELSE'):
            raise Exception(
                'Erro sintatico: ELSE adicionado de maneira incorreta ' + str(self.tokenAtual().linha))

        # TODO: ESCOPO DO WHILE BLOCK 3
        # <while_statement>
        if (self.tokenAtual().tipo == 'WHILE'):
            self.while_statement()
            return

        # ESCOPO OK
        # <identifier>
        if (self.tokenAtual().tipo == 'ID'):
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().lexema)
            self.call_var_statement(temp)
            return

        else:
            raise Exception(
                'Erro sintatico: bloco vazio na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO DECLARATION VAR
    # <declaration_var> OK
    def declaration_var_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID'):
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ATB'):  # atribuicao
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                tempEndVar = []
                # o que tem dentro da variavel
                self.end_var_statement(tempEndVar)
                temp.append(tempEndVar)
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta da atribuição na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO END VAR
    # <end_var> OK
    def end_var_statement(self, tempEndVar):
        #  <call_func> | <call_op>
        if (self.tokenAtual().tipo == 'CALL'):
            tempEndVar.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if (self.tokenAtual().tipo == 'FUNC'):
                tempEndVar.append(self.tokenAtual().tipo)
                self.call_func_statement(tempEndVar)
                return
            else:
                raise Exception(
                    'Erro sintatico: chamada de função erroneamente na linha ' + str(self.tokenAtual().linha))

        # <boolean>
        if (self.tokenAtual().tipo == 'BOOLEAN'):

            if (self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
                tempEndVar.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                return
            else:
                raise Exception(
                    'Erro sintatico: boolean atribuido erroneamente na linha ' + str(self.tokenAtual().linha))
        # <num>
        if (self.tokenAtual().tipo == 'NUM'):
            tempEndVar.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ADD' or self.tokenAtual().tipo == 'SUB' or self.tokenAtual().tipo == 'MULT' or self.tokenAtual().tipo == 'DIV'):
                tempEndVar.append(self.tokenAtual().lexema)
                self.call_op_statement(tempEndVar)
                return
            else:
                return

         # <identifier>
        if (self.tokenAtual().tipo == 'ID'):
            tempEndVar.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            # <call_op>
            if(self.tokenAtual().tipo == 'ADD' or self.tokenAtual().tipo == 'SUB' or self.tokenAtual().tipo == 'MULT' or self.tokenAtual().tipo == 'DIV'):
                tempEndVar.append(self.tokenAtual().lexema)
                self.call_op_statement(tempEndVar)
                return
            else:
                return
        else:
            raise Exception(
                'Erro sintatico: atribuição de variavel erroneamente na linha ' + str(self.tokenAtual().linha))

    # ESCOPO OK
    # Chamada de variavel OK
    def call_var_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ATB'):  # atribuicao
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if ((self.tokenAtual().tipo == 'NUM') or (self.tokenAtual().tipo == 'BOOLEAN') or (self.tokenAtual().tipo == 'ID')):
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(
                        'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: variável não atribuída na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: símbolo de atribuição não encontrado na linha ' + str(self.tokenAtual().linha))

    # ESCOPO OK
    # <declaration_func> OK
    def declaration_func_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):  # tipo
            # Salvando o tipo do retorno
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # identificador
            if(self.tokenAtual().tipo == 'ID'):
                # Salvando o id
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'PLEFT'):
                    # (int a, bool b)
                    # [[params], [params]]
                    # [] -> lista do que tem dewntro dos parenteses do parametro
                    # [[escopo, int, a], [escopo, bool, var]]

                    tempParenteses = []
                    self.indexDaTabelaDeTokens += 1
                    if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
                        tempParentesesParamAtual = []
                        # Ordem dos params: [[escopo, tipo, id], [escopo, tipo, id]]
                        # Fazendo com que o escopo fique correto
                        tempParentesesParamAtual.append(
                            self.indexEscopoAtual + 1)

                        # Salvando o tipo do parametro atual
                        tempParentesesParamAtual.append(self.tokenAtual().tipo)

                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'ID'):
                            # Salvando o tipo do parametro atual
                            tempParentesesParamAtual.append(
                                self.tokenAtual().lexema)

                            # [escopo, int, a] -> antes

                            tempParenteses.append(tempParentesesParamAtual)

                            # [[escopo, int, a]] -> depois

                            self.indexDaTabelaDeTokens += 1
                            if(self.tokenAtual().tipo == 'COMMA'):

                                # [[escopo, int, a]] -> antes
                                tempParenteses.append(
                                    self.params_statement(tempParenteses))
                                tempParenteses.pop()  # Remoção do None que fica ao fim
                                # [[escopo, int, a], i1, i2, i3 ... in]

                                temp.append(tempParenteses)

                                if(self.tokenAtual().tipo == 'PRIGHT'):
                                    self.indexDaTabelaDeTokens += 1
                                    if(self.tokenAtual().tipo == 'CLEFT'):
                                        # Armazendando o escopo antes de entrar na função
                                        self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                                        self.indexEscopoAtual += 1
                                        self.indexDaTabelaDeTokens += 1
                                        # BLOCK
                                        self.block_statement()

                                        if(self.tokenAtual().tipo == 'RETURN'):

                                            # RETURN
                                            self.return_statement(temp)

                                            if(self.tokenAtual().tipo == 'CRIGHT'):
                                                # Retornando o valor do escopo antes de entrar na função
                                                self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                                self.indexDaTabelaDeTokens += 1

                                                if(self.tokenAtual().tipo == 'SEMICOLON'):
                                                    self.indexDaTabelaDeTokens += 1
                                                    # Adiciona na tabela de símbolos
                                                    self.tabelaDeSimbolos.append(
                                                        temp)
                                                else:
                                                    raise Exception(
                                                        'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
                                            else:
                                                raise Exception(
                                                    'Erro sintatico: falta da chave direita na linha ' + str(self.tokenAtual().linha))
                                        else:
                                            raise Exception(
                                                'Erro sintatico: falta do retorno na linha ' + str(self.tokenAtual().linha))

                                    else:
                                        raise Exception(
                                            'Erro sintatico: falta da chave esquerda na linha ' + str(self.tokenAtual().linha))
                                else:
                                    raise Exception(
                                        'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))

                            elif(self.tokenAtual().tipo == 'PRIGHT'):

                                temp.append(tempParenteses)
                                if(self.tokenAtual().tipo == 'PRIGHT'):
                                    self.indexDaTabelaDeTokens += 1
                                    if(self.tokenAtual().tipo == 'CLEFT'):
                                        self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                                        self.indexEscopoAtual += 1
                                        self.indexDaTabelaDeTokens += 1
                                        # BLOCK
                                        self.block_statement()
                                        # RETURN
                                        if(self.tokenAtual().tipo == 'RETURN'):
                                            self.return_statement(temp)
                                            if(self.tokenAtual().tipo == 'CRIGHT'):
                                                self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                                self.indexDaTabelaDeTokens += 1
                                                if(self.tokenAtual().tipo == 'SEMICOLON'):
                                                    self.indexDaTabelaDeTokens += 1
                                                    # Adiciona na tabela de símbolos
                                                    self.tabelaDeSimbolos.append(
                                                        temp)
                                                else:
                                                    raise Exception(
                                                        'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
                                            else:
                                                raise Exception(
                                                    'Erro sintatico: falta da chave direita na linha ' + str(self.tokenAtual().linha))
                                        else:
                                            raise Exception(
                                                'Erro sintatico: falta do retorno na linha ' + str(self.tokenAtual().linha))
                                    else:
                                        raise Exception(
                                            'Erro sintatico: falta da chave esquerda na linha ' + str(self.tokenAtual().linha))
                                else:
                                    raise Exception(
                                        'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))
                            else:
                                # TODO: resolver exceção
                                raise Exception(
                                    'Erro sintatico: falta da virgula linha ' + str(self.tokenAtual().linha))
                        else:
                            raise Exception(
                                'Erro sintatico: falta o ID na linha ' + str(self.tokenAtual().linha))

                    else:
                        if(self.tokenAtual().tipo == 'PRIGHT'):
                            temp.append(tempParenteses)
                            self.indexDaTabelaDeTokens += 1
                            if(self.tokenAtual().tipo == 'CLEFT'):
                                self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                                self.indexEscopoAtual += 1
                                self.indexDaTabelaDeTokens += 1

                                # BLOCK
                                self.block_statement()

                                # RETURN
                                if(self.tokenAtual().tipo == 'RETURN'):
                                    self.return_statement(temp)

                                    if(self.tokenAtual().tipo == 'CRIGHT'):
                                        self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                        self.indexDaTabelaDeTokens += 1
                                        if(self.tokenAtual().tipo == 'SEMICOLON'):
                                            self.indexDaTabelaDeTokens += 1
                                            # Adiciona na tabela de símbolos
                                            self.tabelaDeSimbolos.append(temp)
                                        else:
                                            raise Exception(
                                                'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
                                    else:
                                        raise Exception(
                                            'Erro sintatico: falta da chave direita na linha ' + str(self.tokenAtual().linha))
                                else:
                                    raise Exception(
                                        'Erro sintatico: falta do retorno na linha ' + str(self.tokenAtual().linha))

                            else:
                                raise Exception(
                                    'Erro sintatico: falta da chave esquerda na linha ' + str(self.tokenAtual().linha))
                        else:
                            raise Exception(
                                'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO RETURN
    # <return_statement> OK
    def return_statement(self, temp):
        self.indexDaTabelaDeTokens += 1

        # Se for chamada de função
        if (self.tokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'FUNC'):
                self.call_func_statement(temp)
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: Erro de chamada, só é permitido chamada de funções na linha ' + str(self.tokenAtual().linha))

        # Se for chamada de variavel/num/bool
        if ((self.tokenAtual().tipo == 'NUM') or (self.tokenAtual().tipo == 'BOOLEAN') or (self.tokenAtual().tipo == 'ID')):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'SEMICOLON'):
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: Retorno errado na linha ' + str(self.tokenAtual().linha))

    # ESCOPO OK
    # <params> OK
    def params_statement(self, tempParenteses):
        # [[escopo, int, a], adsfasd, asdasd]
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            tempParentesesParamAtual = []
            tempParentesesParamAtual.append(self.indexEscopoAtual + 1)
            tempParentesesParamAtual.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ID'):
                tempParentesesParamAtual.append(
                    self.tokenAtual().lexema)
                tempParenteses.append(tempParentesesParamAtual)
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'COMMA'):
                    self.params_statement(tempParenteses)
                elif(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
                    raise Exception(
                        'Erro sintatico: falta vírgula na linha ' + str(self.tokenAtual().linha))
                else:
                    return tempParenteses
            else:
                raise Exception('Erro sintatico: é necessário informar alguma váriavel na linha ' +
                                str(self.tokenAtual().linha))
        else:
            raise Exception('Erro sintatico: é necessário informar um tipo na linha ' +
                            str(self.tokenAtual().linha))

    # ESCOPO OK
    # <declaration_proc> OK
    def declaration_proc_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        # identificador
        if(self.tokenAtual().tipo == 'ID'):
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                tempParenteses = []
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
                    tempParentesesParamAtual = []
                    tempParentesesParamAtual.append(self.indexEscopoAtual + 1)
                    tempParentesesParamAtual.append(self.tokenAtual().tipo)
                    self.indexDaTabelaDeTokens += 1
                    if(self.tokenAtual().tipo == 'ID'):
                        tempParentesesParamAtual.append(
                            self.tokenAtual().lexema)
                        tempParenteses.append(tempParentesesParamAtual)
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'COMMA'):
                            tempParenteses.append(
                                self.params_statement(tempParenteses))
                            tempParenteses.pop()
                            temp.append(tempParenteses)
                            if(self.tokenAtual().tipo == 'PRIGHT'):
                                self.indexDaTabelaDeTokens += 1
                                if(self.tokenAtual().tipo == 'CLEFT'):

                                    self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                                    self.indexEscopoAtual += 1
                                    self.indexDaTabelaDeTokens += 1
                                    # <block>
                                    self.block_statement()
                                    if(self.tokenAtual().tipo == 'CRIGHT'):
                                        self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                        self.indexDaTabelaDeTokens += 1
                                        if(self.tokenAtual().tipo == 'SEMICOLON'):
                                            self.indexDaTabelaDeTokens += 1
                                            self.tabelaDeSimbolos.append(temp)
                                        else:
                                            raise Exception(
                                                'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
                                    else:
                                        raise Exception(
                                            'Erro sintatico: falta da chave direito na linha ' + str(self.tokenAtual().linha))
                                else:
                                    raise Exception(
                                        'Erro sintatico: falta da chave esquerda na linha ' + str(self.tokenAtual().linha))
                            else:
                                raise Exception(
                                    'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))

                        elif(self.tokenAtual().tipo == 'PRIGHT'):
                            temp.append(tempParenteses)
                            if(self.tokenAtual().tipo == 'PRIGHT'):
                                self.indexDaTabelaDeTokens += 1
                                if(self.tokenAtual().tipo == 'CLEFT'):

                                    self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                                    self.indexEscopoAtual += 1
                                    self.indexDaTabelaDeTokens += 1
                                    # <block>
                                    self.block_statement()
                                    if(self.tokenAtual().tipo == 'CRIGHT'):
                                        self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                        self.indexDaTabelaDeTokens += 1
                                        if(self.tokenAtual().tipo == 'SEMICOLON'):
                                            self.indexDaTabelaDeTokens += 1
                                            self.tabelaDeSimbolos.append(temp)
                                        else:
                                            raise Exception(
                                                'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
                                    else:
                                        raise Exception(
                                            'Erro sintatico: falta da chave direito na linha ' + str(self.tokenAtual().linha))
                                else:
                                    raise Exception(
                                        'Erro sintatico: falta da chave esquerda na linha ' + str(self.tokenAtual().linha))
                            else:
                                raise Exception(
                                    'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))
                        else:
                            # TODO: resolver exceção
                            raise Exception(
                                'Erro sintatico: falta da virgula linha ' + str(self.tokenAtual().linha))
                    else:
                        raise Exception(
                            'Erro sintatico: falta o ID na linha ' + str(self.tokenAtual().linha))
                else:
                    if(self.tokenAtual().tipo == 'PRIGHT'):
                        temp.append(tempParenteses)
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'CLEFT'):
                            self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                            self.indexEscopoAtual += 1
                            self.indexDaTabelaDeTokens += 1
                            self.block_statement()
                            if(self.tokenAtual().tipo == 'CRIGHT'):
                                self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                self.indexDaTabelaDeTokens += 1
                                if(self.tokenAtual().tipo == 'SEMICOLON'):
                                    self.indexDaTabelaDeTokens += 1
                                    self.tabelaDeSimbolos.append(temp)
                                else:
                                    raise Exception(
                                        'Erro sintatico: falta do ponto e vírgula na linha ' + str(self.tokenAtual().linha))
                            else:
                                raise Exception(
                                    'Erro sintatico: falta da chave direito na linha ' + str(self.tokenAtual().linha))

                        else:
                            raise Exception(
                                'Erro sintatico: falta da chave esquerda na linha ' + str(self.tokenAtual().linha))
                    else:
                        raise Exception(
                            'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # ESCOPO OK
    # <call_proc>
    def call_proc_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID'):
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexDaTabelaDeTokens += 1
                tempParams = []
                if(self.tokenAtual().tipo == 'ID' or self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
                    tempParams.append(self.tokenAtual().lexema)
                    self.indexDaTabelaDeTokens += 1
                    if(self.tokenAtual().tipo == 'COMMA'):
                        tempParams.append(
                            self.params_call_statement(tempParams))
                        tempParams.pop()
                        temp.append(tempParams)
                        #  [0, 'CALL', 'PROC', 'proc1', ['a', 'b', 'c']],
                        #  [0, 'CALL', 'PROC', 'proc1', [['a'], ['b'], ['c']]],
                        return temp
                    elif(self.tokenAtual().tipo == 'PRIGHT'):
                        self.indexDaTabelaDeTokens += 1
                        temp.append(tempParams)
                        return temp
                    else:
                        raise Exception(
                            'Erro sintatico: falta da virgula na linha ' + str(self.tokenAtual().linha))
                else:
                    temp.append(tempParams)
                    if(self.tokenAtual().tipo == 'PRIGHT'):

                        self.indexDaTabelaDeTokens += 1
                        return temp
                    else:
                        raise Exception(
                            'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # ESCOPO OK
    # <call_func>
    def call_func_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID'):
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'PLEFT'):
                self.indexDaTabelaDeTokens += 1
                tempParams = []
                if(self.tokenAtual().tipo == 'ID' or self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
                    tempParams.append(self.tokenAtual().lexema)
                    self.indexDaTabelaDeTokens += 1
                    if(self.tokenAtual().tipo == 'COMMA'):
                        tempParams.append(
                            self.params_call_statement(tempParams))
                        tempParams.pop()
                        temp.append(tempParams)
                        return temp
                    elif(self.tokenAtual().tipo == 'PRIGHT'):
                        self.indexDaTabelaDeTokens += 1
                        temp.append(tempParams)
                        return temp
                    else:
                        raise Exception(
                            'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))

                else:
                    temp.append(tempParams)
                    if(self.tokenAtual().tipo == 'PRIGHT'):
                        self.indexDaTabelaDeTokens += 1

                        return temp
                    else:
                        raise Exception(
                            'Erro sintatico: falta do parentese direito na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do parentese esquerdo na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # ESCOPO OK
    # <params_call>
    def params_call_statement(self, tempParams):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID' or self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
            tempParams.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'COMMA'):
                self.params_call_statement(tempParams)
            elif(self.tokenAtual().tipo == 'ID' or self.tokenAtual().lexema == 'True' or self.tokenAtual().lexema == 'False'):
                raise Exception(
                    'Erro sintatico: falta vírgula na linha ' + str(self.tokenAtual().linha))
            else:
                self.indexDaTabelaDeTokens += 1
                return tempParams
        else:
            raise Exception('Erro sintatico: é necessário informar alguma váriavel na linha ' +
                            str(self.tokenAtual().linha))

    # TODO: ESCOPO DO PRINT
    # <print_statement>
    def print_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.params_print_statement(temp)
            if(self.tokenAtual().tipo == 'PRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'SEMICOLON'):
                    self.indexDaTabelaDeTokens += 1
                    return
                else:
                    # TODO: SOLVE BUG DE CONTAGEM DE LINHAS
                    raise Exception(
                        'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do Parentese direito na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do Parentese esquerdo na linha  ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO PARAMS PRINT
    # <params_print_statement>
    def params_print_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'CALL'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'FUNC'):
                self.call_func_statement(temp)
            elif(self.tokenAtual().tipo == 'PROC'):
                # TODO: Verificar atribuição do ;
                # (decidir se deixa ou se tira, ou se resolve o bug [-- print(call func soma()); --])
                self.call_proc_statement(temp)
            else:
                raise Exception(
                    'Erro sintatico: chamada incorreta de função ou procedimento na linha ' + str(self.tokenAtual().linha))

        elif((self.tokenAtual().tipo == 'NUM') or (self.tokenAtual().tipo == 'BOOLEAN') or (self.tokenAtual().tipo == 'ID')):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ADD' or self.tokenAtual().tipo == 'SUB' or self.tokenAtual().tipo == 'MULT' or self.tokenAtual().tipo == 'DIV'):
                self.call_op_statement(temp)
                return
            else:
                return
        else:
            raise Exception(
                'Erro sintatico: uso incorreto dos parametros na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO IF
    # <if_statement>
    def if_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.indexDaTabelaDeTokens += 1
            # Expression
            self.expression_statement()
            if(self.tokenAtual().tipo == 'PRIGHT'):
                olhaAfrente = self.tokenLookAhead()
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'CLEFT' and olhaAfrente.tipo != 'CRIGHT'):
                    self.indexDaTabelaDeTokens += 1
                    while(self.tokenAtual().tipo != 'CRIGHT' and self.tokenLookAhead().tipo != 'ENDIF'):
                        self.block3_statement()
                    if(self.tokenAtual().tipo == 'CRIGHT'):
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'ENDIF'):
                            self.indexDaTabelaDeTokens += 1
                            if(self.tokenAtual().tipo == 'ELSE'):

                                self.else_part_statement()   # ELSE
                            else:
                                return
                        else:
                            raise Exception(
                                'Erro sintatico: falta de ENDIF ' + str(self.tokenAtual().linha))
                    else:
                        raise Exception(
                            'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do CLEFT ou bloco vazio na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do Parentese direito na linha  ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do Parentese esquerdo na linha  ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO ELSE
    # <else_part>
    def else_part_statement(self):
        olhaAfrente = self.tokenLookAhead()
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'CLEFT' and olhaAfrente.tipo != 'CRIGHT'):
            self.indexDaTabelaDeTokens += 1
            while(self.tokenAtual().tipo != 'CRIGHT' and self.tokenLookAhead().tipo != 'ENDELSE'):
                # Block
                self.block3_statement()
            if(self.tokenAtual().tipo == 'CRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'ENDELSE'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta de ENDELSE na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do CLEFT ou bloco vazio na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO IF 2
    # <if_statement2>
    # IF chamado somente dentro do while, pois dentro dele pode ter BREAK E CONTINUE (block2)
    def if_statement2(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.indexDaTabelaDeTokens += 1
            # Expression
            self.expression_statement()
            if(self.tokenAtual().tipo == 'PRIGHT'):
                olhaAfrente = self.tokenLookAhead()
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'CLEFT' and olhaAfrente.tipo != 'CRIGHT'):
                    self.indexDaTabelaDeTokens += 1
                    while(self.tokenAtual().tipo != 'CRIGHT' and self.tokenLookAhead().tipo != 'ENDIF'):
                        self.block2_statement()

                    if(self.tokenAtual().tipo == 'CRIGHT'):
                        self.indexDaTabelaDeTokens += 1
                        if(self.tokenAtual().tipo == 'ENDIF'):
                            self.indexDaTabelaDeTokens += 1
                            if(self.tokenAtual().tipo == 'ELSE'):
                                self.else_part_statement2()   # ELSE
                            else:
                                return
                        else:
                            raise Exception(
                                'Erro sintatico: falta de ENDIF ' + str(self.tokenAtual().linha))
                    else:
                        raise Exception(
                            'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
                else:
                    raise Exception(
                        'Erro sintatico: falta do CLEFT ou Bloco vazio na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do Parentese direito na linha  ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do Parentese esquerdo na linha  ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO ELSE 2
    # ELSE chamado somente dentro do while, pois dentro dele pode ter BREAK E CONTINUE (block2)
    # <else_part2>
    def else_part_statement2(self):
        olhaAfrente = self.tokenLookAhead()
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'CLEFT' and olhaAfrente.tipo != 'CRIGHT'):
            self.indexDaTabelaDeTokens += 1
            # Block
            while(self.tokenAtual().tipo != 'CRIGHT' and self.tokenLookAhead().tipo != 'ENDELSE'):
                self.block2_statement()

            if(self.tokenAtual().tipo == 'CRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'ENDELSE'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta de ENDELSE na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do CRIGHT na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do CLEFT ou bloco vazio na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO WHILE
    # <while_statement>
    def while_statement(self):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'PLEFT'):
            self.indexDaTabelaDeTokens += 1
            # Expression
            self.expression_statement()
            if(self.tokenAtual().tipo == 'PRIGHT'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'CLEFT'):
                    self.indexDaTabelaDeTokens += 1

                    # BLOCK
                    while(self.tokenAtual().tipo != 'CRIGHT' and self.tokenLookAhead().tipo != 'ENDWHILE'):
                        self.block2_statement()

                    if(self.tokenAtual().tipo == 'CRIGHT'):
                        self.indexDaTabelaDeTokens += 1
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
                        'Erro sintatico: falta do CLEFT na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do PRIGHT na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do PLEFT na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO UNCONDITIONAL BRANCH
    # <unconditional_branch>
    def unconditional_branch_statement(self):
        if(self.tokenAtual().tipo == 'CONTINUE'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'SEMICOLON'):
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))

        if(self.tokenAtual().tipo == 'BREAK'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'SEMICOLON'):
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    'Erro sintatico: falta do ponto e virgula na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO EXPRESSION STATEMENT
    # <expression>
    def expression_statement(self):
        if(self.tokenAtual().tipo == 'ID' or self.tokenAtual().tipo == 'NUM'):
            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'EQUAL' or self.tokenAtual().tipo == 'DIFF' or self.tokenAtual().tipo == 'LESSEQUAL' or self.tokenAtual().tipo == 'LESS' or self.tokenAtual().tipo == 'GREATEREQUAL' or self.tokenAtual().tipo == 'GREATER'):
                self.indexDaTabelaDeTokens += 1
                if(self.tokenAtual().tipo == 'ID' or self.tokenAtual().tipo == 'NUM'):
                    self.indexDaTabelaDeTokens += 1
                else:
                    raise Exception(
                        'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))
            else:
                raise Exception(
                    'Erro sintatico: falta do operador booleano na linha ' + str(self.tokenAtual().linha))
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    # TODO: ESCOPO DO CALL OP
    # <call_op> ok - Operações aritméticas
    def call_op_statement(self, tempEndVar):
        self.indexDaTabelaDeTokens += 1
        if(self.tokenAtual().tipo == 'ID' or self.tokenAtual().tipo == 'NUM'):
            tempEndVar.append(self.tokenAtual().lexema)

            self.indexDaTabelaDeTokens += 1
            if(self.tokenAtual().tipo == 'ADD' or self.tokenAtual().tipo == 'SUB' or self.tokenAtual().tipo == 'MULT' or self.tokenAtual().tipo == 'DIV'):
                tempEndVar.append(self.tokenAtual().lexema)
                self.call_op_statement(tempEndVar)
            else:
                return
        else:
            raise Exception(
                'Erro sintatico: falta do ID na linha ' + str(self.tokenAtual().linha))

    '''
    
    \/ Análise Semântica \/
    
    '''

    # TODO: CORRIGIR
    # checa semantica, se tiver tudo OK return True
    def checkSemantica(self, tipo, index):
        if(tipo == 'VARDEC'):  # checa semantica de declaração de Variável
            simbAtual = self.tabSimbolos[index]
            if(simbAtual[1] == 'INT'):
                if(simbAtual[3].isnumeric() or bool(re.match("[0-9A-Za-a]*( ){0,}([+-/*]( ){0,}[0-9A-Za-a]*( ){0,})*", simbAtual[3]))):
                    return True
                else:
                    # linha do ponto e virgula que é a mesma
                    raise Exception(
                        "Erro Semântico, variavel do tipo inteiro nao recebe inteiro na linha: "+str(self.tokenAtual().linha))
            if(simbAtual[1] == 'TBOOLEAN'):
                if(simbAtual[3] == 'true' or simbAtual[3] == 'false'):
                    return True
                else:
                    # linha do ponto e virgula que é a mesma
                    raise Exception(
                        "Erro Semântico, variavel do tipo boolean nao recebe boolean na linha: "+str(self.tokenAtual().linha))
        self.indexDecVarAtual += 1
        # elif(outros tipos)
