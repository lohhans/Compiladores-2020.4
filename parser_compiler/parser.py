import re
from pprint import pprint

# print('Entrou... Tipo: %s, lexema: %s, na linha: %s' % (self.tokenAtual().tipo, self.tokenAtual().lexema, self.tokenAtual().linha))


class Parser:
    def __init__(self, tabelaDeTokens):
        self.tabelaDeTokens = tabelaDeTokens
        self.indexDaTabelaDeTokens = 0
        self.indexLookAhead = 0
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
        escopoPai = self.indexEscopoAtual  # (-1 -> início)
        self.indexEscopoAtual += 1
        self.statement_list()  # Análise Sintática
        # Temporário \/
        self.checkSemantica()
        return

    def statement_list(self):
        if self.tokenAtual().tipo == "END":
            return
        else:
            self.statement()
            self.statement_list()
            return

    def statement(self):
        if self.tokenAtual().tipo == "PROGRAM":
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "CLEFT":
                self.indexDaTabelaDeTokens += 1

                while self.tokenAtual().tipo != "CRIGHT":
                    self.block_statement()

                if self.tokenAtual().tipo == "CRIGHT":
                    self.indexDaTabelaDeTokens += 1

                    if self.tokenAtual().tipo == "END":
                        print("\nFIM DA ANÁLISE SINTÁTICA - DEU CERTO :)\n")
                        # Deu certo
                    else:
                        raise Exception(
                            "Erro sintatico: falta do END na linha "
                            + str(self.tokenAtual().linha)
                        )
                else:
                    raise Exception(
                        "Erro sintatico: falta do CRIGHT na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do CLEFT na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: Código fora do padrão na linha "
                + str(self.tokenAtual().linha)
            )

    # <block>
    def block_statement(self):
        # ESCOPO OK
        # <declaration_var>
        if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.declaration_var_statement(temp)
            return temp

        # ESCOPO OK
        # <declaration_func>
        if self.tokenAtual().tipo == "FUNC":
            # Ordem: [escopo, tipo, tipoDoRetorno, id, [[params], [params], [params]]]
            # Obs: Params pode ser >= 0
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            # temp.append('FUNC')
            temp.append(self.tokenAtual().tipo)
            self.declaration_func_statement(temp)
            return temp

        # ESCOPO OK
        # <declaration_proc>
        if self.tokenAtual().tipo == "PROC":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            # temp.append('PROC')
            temp.append(self.tokenAtual().tipo)
            temp = self.declaration_proc_statement(temp)
            self.tabelaDeSimbolos.append(temp)
            return temp

        # ESCOPO OK
        # Chamadas de função e procedimentos
        if self.tokenAtual().tipo == "CALL":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if self.tokenAtual().tipo == "FUNC":
                temp.append(self.tokenAtual().tipo)
                temp = self.call_func_statement(temp)
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                    return temp
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            # <call_proc>
            elif self.tokenAtual().tipo == "PROC":
                temp.append(self.tokenAtual().tipo)
                temp = self.call_proc_statement(temp)
                # self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                    return temp
                else:
                    raise Exception(
                        "aErro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )

            else:
                raise Exception(
                    "Erro sintatico: falta de PROC ou FUNC"
                    + str(self.tokenAtual().linha)
                )

        # ESCOPO OK
        # <print_statement>
        if self.tokenAtual().tipo == "PRINT":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.print_statement(temp)
            return temp

        # ESCOPO ok
        # <if_statement>
        if self.tokenAtual().tipo == "IF":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.if_statement(temp)
            return temp

        # ESCOPO ok
        # <while_statement>
        if self.tokenAtual().tipo == "WHILE":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.while_statement(temp)
            return temp

        # ESCOPO OK
        # <identifier>
        if self.tokenAtual().tipo == "ID":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            temp.append(self.tokenAtual().lexema)
            self.call_var_statement(temp)
            return temp

        else:
            return

    # block2 é o bloco que contém break/continue que só pode ser chamado dentro de um while
    def block2_statement(self):
        # ESCOPO OK
        # <declaration_var>
        if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.declaration_var_statement(temp)
            return temp

        # ESCOPO OK
        # Chamadas de função e procedimentos
        if self.tokenAtual().tipo == "CALL":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if self.tokenAtual().tipo == "FUNC":
                temp.append(self.tokenAtual().tipo)
                temp = self.call_func_statement(temp)
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                    return temp
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            # <call_proc>
            elif self.tokenAtual().tipo == "PROC":
                temp.append(self.tokenAtual().tipo)
                temp = self.call_proc_statement(temp)
                # self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                    return temp
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta de PROC ou FUNC"
                    + str(self.tokenAtual().linha)
                )

        # ESCOPO OK
        # <print_statement>
        if self.tokenAtual().tipo == "PRINT":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.print_statement(temp)
            return temp

        # ESCOPO OK
        # <if_statement>
        if self.tokenAtual().tipo == "IF":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.if_statement2(temp)
            return temp

        # Tratamento de erro ELSE
        if self.tokenAtual().tipo == "ELSE":
            raise Exception(
                "Erro sintatico: ELSE adicionado de maneira incorreta "
                + str(self.tokenAtual().linha)
            )

        # ESCOPO OK
        # <while_statement>
        if self.tokenAtual().tipo == "WHILE":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.while_statement(temp)
            return temp

        # ESCOPO OK
        # <identifier>
        if self.tokenAtual().tipo == "ID":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            temp.append(self.tokenAtual().lexema)
            self.call_var_statement(temp)
            return temp

        # ESCOPO OK
        # <unconditional_branch>
        if self.tokenAtual().tipo == "BREAK" or self.tokenAtual().tipo == "CONTINUE":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.unconditional_branch_statement()
            return temp

        else:
            raise Exception(
                "Erro sintatico: bloco vazio na linha " +
                str(self.tokenAtual().linha)
            )

    # block3 é o bloco do if/else, que não pode declarar função e procedimento dentro
    def block3_statement(self):
        # ESCOPO OK
        # <declaration_var>
        if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.declaration_var_statement(temp)
            return temp

        # ESCOPO OK
        # Chamadas de função e procedimentos
        if self.tokenAtual().tipo == "CALL":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if self.tokenAtual().tipo == "FUNC":
                temp.append(self.tokenAtual().tipo)
                temp = self.call_func_statement(temp)
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                    return temp
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            # <call_proc>
            elif self.tokenAtual().tipo == "PROC":
                temp.append(self.tokenAtual().tipo)
                temp = self.call_proc_statement(temp)
                # self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                    return temp
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta de PROC ou FUNC"
                    + str(self.tokenAtual().linha)
                )

        # ESCOPO OK
        # <print_statement>
        if self.tokenAtual().tipo == "PRINT":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.print_statement(temp)
            return temp

        # ESCOPO Ok
        # <if_statement>
        if self.tokenAtual().tipo == "IF":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.if_statement(temp)
            return temp

        # Tratamento de erro ELSE
        if self.tokenAtual().tipo == "ELSE":
            raise Exception(
                "Erro sintatico: ELSE adicionado de maneira incorreta "
                + str(self.tokenAtual().linha)
            )

        # ESCOPO OK
        # <while_statement>
        if self.tokenAtual().tipo == "WHILE":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            self.while_statement(temp)
            return temp

        # ESCOPO OK
        # <identifier>
        if self.tokenAtual().tipo == "ID":
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.tokenAtual().linha)
            temp.append(self.tokenAtual().tipo)
            temp.append(self.tokenAtual().lexema)
            self.call_var_statement(temp)
            return temp

        else:
            raise Exception(
                "Erro sintatico: bloco vazio na linha " +
                str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <declaration_var> OK
    def declaration_var_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "ID":
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "ATB":  # atribuicao
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                tempEndVar = []
                # o que tem dentro da variavel
                self.end_var_statement(tempEndVar)
                temp.append(tempEndVar)
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta da atribuição na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do ID na linha " +
                str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <end_var> OK
    def end_var_statement(self, tempEndVar):
        #  <call_func>
        if self.tokenAtual().tipo == "CALL":
            tempEndVar.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # <call_func>
            if self.tokenAtual().tipo == "FUNC":
                tempEndVar.append(self.tokenAtual().tipo)
                self.call_func_statement(tempEndVar)
                return
            else:
                raise Exception(
                    "Erro sintatico: chamada de função erroneamente na linha "
                    + str(self.tokenAtual().linha)
                )

        # <boolean>
        if self.tokenAtual().tipo == "BOOLEAN":

            if (
                self.tokenAtual().lexema == "True"
                or self.tokenAtual().lexema == "False"
            ):
                tempEndVar.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                return
            else:
                raise Exception(
                    "Erro sintatico: boolean atribuido erroneamente na linha "
                    + str(self.tokenAtual().linha)
                )
        # <num>
        if self.tokenAtual().tipo == "NUM":
            tempEndVar.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if (
                self.tokenAtual().tipo == "ADD"
                or self.tokenAtual().tipo == "SUB"
                or self.tokenAtual().tipo == "MULT"
                or self.tokenAtual().tipo == "DIV"
            ):
                tempEndVar.append(self.tokenAtual().lexema)
                self.call_op_statement(tempEndVar)
                return
            else:
                return

        # <identifier>
        if self.tokenAtual().tipo == "ID":
            tempEndVar.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            # <call_op>
            if (
                self.tokenAtual().tipo == "ADD"
                or self.tokenAtual().tipo == "SUB"
                or self.tokenAtual().tipo == "MULT"
                or self.tokenAtual().tipo == "DIV"
            ):
                tempEndVar.append(self.tokenAtual().lexema)
                self.call_op_statement(tempEndVar)
                return
            else:
                return
        else:
            raise Exception(
                "Erro sintatico: atribuição de variavel erroneamente na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # Chamada de variavel OK
    def call_var_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "ATB":  # atribuicao
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if (
                (self.tokenAtual().tipo == "NUM")
                or (self.tokenAtual().tipo == "BOOLEAN")
                or (self.tokenAtual().tipo == "ID")
            ):
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.indexDaTabelaDeTokens += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(
                        "Erro sintatico: falta do ponto e vírgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: variável não atribuída na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: símbolo de atribuição não encontrado na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <declaration_func> OK
    def declaration_func_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL":  # tipo
            # Salvando o tipo do retorno
            temp.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            # identificador
            if self.tokenAtual().tipo == "ID":
                # Salvando o id
                temp.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "PLEFT":
                    # (int a, bool b)
                    # [[params], [params]]
                    # [] -> lista do que tem dewntro dos parenteses do parametro
                    # [[escopo, int, a], [escopo, bool, var]]

                    tempParenteses = []
                    self.indexDaTabelaDeTokens += 1
                    if (
                        self.tokenAtual().tipo == "INT"
                        or self.tokenAtual().tipo == "BOOL"
                    ):
                        tempParentesesParamAtual = []
                        # Ordem dos params: [[escopo, tipo, id], [escopo, tipo, id]]
                        # Fazendo com que o escopo fique correto
                        tempParentesesParamAtual.append(
                            self.indexEscopoAtual + 1)

                        # Salvando o tipo do parametro atual
                        tempParentesesParamAtual.append(self.tokenAtual().tipo)

                        self.indexDaTabelaDeTokens += 1
                        if self.tokenAtual().tipo == "ID":
                            # Salvando o tipo do parametro atual
                            tempParentesesParamAtual.append(
                                self.tokenAtual().lexema)
                            # [escopo, int, a] -> antes
                            tempParenteses.append(tempParentesesParamAtual)
                            # [[escopo, int, a]] -> depois
                            self.indexDaTabelaDeTokens += 1
                            if self.tokenAtual().tipo == "COMMA":
                                # [[escopo, int, a]] -> antes
                                tempParenteses.append(
                                    self.params_statement(tempParenteses)
                                )
                                tempParenteses.pop()  # Remoção do None que fica ao fim
                                # [[escopo, int, a], i1, i2, i3 ... in]
                                temp.append(tempParenteses)
                                if self.tokenAtual().tipo == "PRIGHT":
                                    self.indexDaTabelaDeTokens += 1
                                    if self.tokenAtual().tipo == "CLEFT":
                                        # Armazendando o escopo antes de entrar na função
                                        self.indexEscopoAntesDaFuncao = (
                                            self.indexEscopoAtual
                                        )
                                        self.indexEscopoAtual += 1
                                        self.indexDaTabelaDeTokens += 1

                                        tempBlock = []
                                        # BLOCK
                                        while self.tokenAtual().tipo != "RETURN":
                                            tempBlock.append(
                                                self.block_statement())

                                        temp.append(tempBlock)
                                        tempReturn = []
                                        if self.tokenAtual().tipo == "RETURN":
                                            tempReturn.append(
                                                self.indexEscopoAtual)
                                            tempReturn.append(
                                                self.tokenAtual().tipo)
                                            # RETURN
                                            tempReturnParams = []
                                            tempReturnParams = self.return_statement(
                                                tempReturnParams
                                            )
                                            tempReturn.append(tempReturnParams)
                                            temp.append(tempReturn)
                                            if self.tokenAtual().tipo == "CRIGHT":
                                                # Retornando o valor do escopo antes de entrar na função
                                                self.indexEscopoAtual = (
                                                    self.indexEscopoAntesDaFuncao
                                                )
                                                self.indexDaTabelaDeTokens += 1

                                                if (
                                                    self.tokenAtual().tipo
                                                    == "SEMICOLON"
                                                ):
                                                    self.indexDaTabelaDeTokens += 1
                                                    # Adiciona na tabela de símbolos
                                                    self.tabelaDeSimbolos.append(
                                                        temp)
                                                else:
                                                    raise Exception(
                                                        "Erro sintatico: falta do ponto e vírgula na linha "
                                                        + str(self.tokenAtual().linha)
                                                    )
                                            else:
                                                raise Exception(
                                                    "Erro sintatico: falta da chave direita na linha "
                                                    + str(self.tokenAtual().linha)
                                                )
                                        else:
                                            raise Exception(
                                                "Erro sintatico: falta do retorno na linha "
                                                + str(self.tokenAtual().linha)
                                            )

                                    else:
                                        raise Exception(
                                            "Erro sintatico: falta da chave esquerda na linha "
                                            + str(self.tokenAtual().linha)
                                        )
                                else:
                                    raise Exception(
                                        "Erro sintatico: falta do parentese direito na linha "
                                        + str(self.tokenAtual().linha)
                                    )

                            elif self.tokenAtual().tipo == "PRIGHT":

                                temp.append(tempParenteses)
                                if self.tokenAtual().tipo == "PRIGHT":
                                    self.indexDaTabelaDeTokens += 1
                                    if self.tokenAtual().tipo == "CLEFT":
                                        self.indexEscopoAntesDaFuncao = (
                                            self.indexEscopoAtual
                                        )
                                        self.indexEscopoAtual += 1
                                        self.indexDaTabelaDeTokens += 1
                                        tempBlock = []
                                        # BLOCK
                                        while self.tokenAtual().tipo != "RETURN":
                                            tempBlock.append(
                                                self.block_statement())

                                        temp.append(tempBlock)
                                        tempReturn = []
                                        # RETURN
                                        if self.tokenAtual().tipo == "RETURN":
                                            tempReturn.append(
                                                self.indexEscopoAtual)
                                            tempReturn.append(
                                                self.tokenAtual().tipo)
                                            # RETURN
                                            tempReturnParms = []
                                            tempReturnParms = self.return_statement(
                                                tempReturnParms
                                            )
                                            tempReturn.append(tempReturnParms)
                                            temp.append(tempReturn)
                                            if self.tokenAtual().tipo == "CRIGHT":
                                                self.indexEscopoAtual = (
                                                    self.indexEscopoAntesDaFuncao
                                                )
                                                self.indexDaTabelaDeTokens += 1
                                                if (
                                                    self.tokenAtual().tipo
                                                    == "SEMICOLON"
                                                ):
                                                    self.indexDaTabelaDeTokens += 1
                                                    # Adiciona na tabela de símbolos
                                                    self.tabelaDeSimbolos.append(
                                                        temp)
                                                else:
                                                    raise Exception(
                                                        "Erro sintatico: falta do ponto e vírgula na linha "
                                                        + str(self.tokenAtual().linha)
                                                    )
                                            else:
                                                raise Exception(
                                                    "Erro sintatico: falta da chave direita na linha "
                                                    + str(self.tokenAtual().linha)
                                                )
                                        else:
                                            raise Exception(
                                                "Erro sintatico: falta do retorno na linha "
                                                + str(self.tokenAtual().linha)
                                            )
                                    else:
                                        raise Exception(
                                            "Erro sintatico: falta da chave esquerda na linha "
                                            + str(self.tokenAtual().linha)
                                        )
                                else:
                                    raise Exception(
                                        "Erro sintatico: falta do parentese direito na linha "
                                        + str(self.tokenAtual().linha)
                                    )
                            else:
                                # TODO: (5 - falta descobrir) resolver exceção
                                raise Exception(
                                    "Erro sintatico: falta da virgula na linha "
                                    + str(self.tokenAtual().linha)
                                )
                        else:
                            raise Exception(
                                "Erro sintatico: falta o ID na linha "
                                + str(self.tokenAtual().linha)
                            )

                    else:
                        if self.tokenAtual().tipo == "PRIGHT":
                            temp.append(tempParenteses)
                            self.indexDaTabelaDeTokens += 1
                            if self.tokenAtual().tipo == "CLEFT":
                                self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                                self.indexEscopoAtual += 1
                                self.indexDaTabelaDeTokens += 1

                                tempBlock = []
                                # BLOCK
                                while self.tokenAtual().tipo != "RETURN":
                                    tempBlock.append(self.block_statement())

                                temp.append(tempBlock)

                                tempReturn = []
                                # RETURN
                                if self.tokenAtual().tipo == "RETURN":
                                    tempReturn.append(self.indexEscopoAtual)
                                    tempReturn.append(self.tokenAtual().tipo)
                                    # RETURN
                                    tempReturnParms = []
                                    tempReturnParms = self.return_statement(
                                        tempReturnParms
                                    )

                                    tempReturn.append(tempReturnParms)
                                    temp.append(tempReturn)
                                    if self.tokenAtual().tipo == "CRIGHT":
                                        self.indexEscopoAtual = (
                                            self.indexEscopoAntesDaFuncao
                                        )
                                        self.indexDaTabelaDeTokens += 1
                                        if self.tokenAtual().tipo == "SEMICOLON":
                                            self.indexDaTabelaDeTokens += 1
                                            # Adiciona na tabela de símbolos
                                            self.tabelaDeSimbolos.append(temp)
                                        else:
                                            raise Exception(
                                                "Erro sintatico: falta do ponto e vírgula na linha "
                                                + str(self.tokenAtual().linha)
                                            )
                                    else:
                                        raise Exception(
                                            "Erro sintatico: falta da chave direita na linha "
                                            + str(self.tokenAtual().linha)
                                        )
                                else:
                                    raise Exception(
                                        "Erro sintatico: falta do retorno na linha "
                                        + str(self.tokenAtual().linha)
                                    )

                            else:
                                raise Exception(
                                    "Erro sintatico: falta da chave esquerda na linha "
                                    + str(self.tokenAtual().linha)
                                )
                        else:
                            raise Exception(
                                "Erro sintatico: falta do parentese direito na linha "
                                + str(self.tokenAtual().linha)
                            )
                else:
                    raise Exception(
                        "Erro sintatico: falta do parentese esquerdo na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do ID na linha "
                    + str(self.tokenAtual().linha)
                )

    # ESCOPO OK
    # <return_statement> OK
    def return_statement(self, tempReturnParams):
        self.indexDaTabelaDeTokens += 1

        # Se for chamada de função
        if self.tokenAtual().tipo == "CALL":
            tempReturnParams.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "FUNC":
                tempReturnParams.append(self.tokenAtual().tipo)
                self.call_func_statement(tempReturnParams)
                self.indexDaTabelaDeTokens += 1
                return tempReturnParams
            else:
                raise Exception(
                    "Erro sintatico: Erro de chamada, só é permitido chamada de funções na linha "
                    + str(self.tokenAtual().linha)
                )

        # Se for chamada de variavel/num/bool
        if (
            (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "BOOLEAN")
            or (self.tokenAtual().tipo == "ID")
        ):
            tempReturnParams.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "SEMICOLON":
                self.indexDaTabelaDeTokens += 1
                return tempReturnParams
            else:
                raise Exception(
                    "Erro sintatico: falta do ponto e virgula na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: Retorno errado na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <params> OK
    def params_statement(self, tempParenteses):
        # [[escopo, int, a], adsfasd, asdasd]
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL":
            tempParentesesParamAtual = []
            tempParentesesParamAtual.append(self.indexEscopoAtual + 1)
            tempParentesesParamAtual.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "ID":
                tempParentesesParamAtual.append(self.tokenAtual().lexema)
                tempParenteses.append(tempParentesesParamAtual)
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "COMMA":
                    self.params_statement(tempParenteses)
                elif (
                    self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL"
                ):
                    raise Exception(
                        "Erro sintatico: falta vírgula na linha "
                        + str(self.tokenAtual().linha)
                    )
                else:
                    return tempParenteses
            else:
                raise Exception(
                    "Erro sintatico: é necessário informar alguma váriavel na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: é necessário informar um tipo na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <declaration_proc> OK
    def declaration_proc_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        # identificador
        if self.tokenAtual().tipo == "ID":
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "PLEFT":
                tempParenteses = []
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOL":
                    tempParentesesParamAtual = []
                    tempParentesesParamAtual.append(self.indexEscopoAtual + 1)
                    tempParentesesParamAtual.append(self.tokenAtual().tipo)
                    self.indexDaTabelaDeTokens += 1
                    if self.tokenAtual().tipo == "ID":
                        tempParentesesParamAtual.append(
                            self.tokenAtual().lexema)
                        tempParenteses.append(tempParentesesParamAtual)
                        self.indexDaTabelaDeTokens += 1
                        if self.tokenAtual().tipo == "COMMA":
                            tempParenteses.append(
                                self.params_statement(tempParenteses))
                            tempParenteses.pop()
                            temp.append(tempParenteses)
                            if self.tokenAtual().tipo == "PRIGHT":
                                self.indexDaTabelaDeTokens += 1
                                if self.tokenAtual().tipo == "CLEFT":

                                    self.indexEscopoAntesDaFuncao = (
                                        self.indexEscopoAtual
                                    )

                                    self.indexEscopoAtual += 1
                                    self.indexDaTabelaDeTokens += 1

                                    tempBlock = []
                                    # BLOCK # TODO: Verificar
                                    while (
                                        self.tokenAtual().tipo != "CRIGHT"
                                        and self.tokenLookAhead().tipo != "SEMICOLON"
                                    ):
                                        tempBlock.append(
                                            self.block_statement())

                                    temp.append(tempBlock)

                                    if self.tokenAtual().tipo == "CRIGHT":
                                        self.indexEscopoAtual = (
                                            self.indexEscopoAntesDaFuncao
                                        )
                                        self.indexDaTabelaDeTokens += 1
                                        if self.tokenAtual().tipo == "SEMICOLON":
                                            self.indexDaTabelaDeTokens += 1
                                            return temp
                                        else:
                                            raise Exception(
                                                "Erro sintatico: falta do ponto e vírgula na linha "
                                                + str(self.tokenAtual().linha)
                                            )
                                    else:
                                        raise Exception(
                                            "Erro sintatico: falta da chave direito na linha "
                                            + str(self.tokenAtual().linha)
                                        )
                                else:
                                    raise Exception(
                                        "Erro sintatico: falta da chave esquerda na linha "
                                        + str(self.tokenAtual().linha)
                                    )
                            else:
                                raise Exception(
                                    "Erro sintatico: falta do parentese direito na linha "
                                    + str(self.tokenAtual().linha)
                                )

                        elif self.tokenAtual().tipo == "PRIGHT":
                            temp.append(tempParenteses)
                            if self.tokenAtual().tipo == "PRIGHT":
                                self.indexDaTabelaDeTokens += 1
                                if self.tokenAtual().tipo == "CLEFT":

                                    self.indexEscopoAntesDaFuncao = (
                                        self.indexEscopoAtual
                                    )
                                    self.indexEscopoAtual += 1
                                    self.indexDaTabelaDeTokens += 1
                                    tempBlock = []
                                    # BLOCK # TODO: Verificar
                                    while (
                                        self.tokenAtual().tipo != "CRIGHT"
                                        and self.tokenLookAhead().tipo != "SEMICOLON"
                                    ):
                                        tempBlock.append(
                                            self.block_statement())

                                    temp.append(tempBlock)
                                    if self.tokenAtual().tipo == "CRIGHT":
                                        self.indexEscopoAtual = (
                                            self.indexEscopoAntesDaFuncao
                                        )
                                        self.indexDaTabelaDeTokens += 1
                                        if self.tokenAtual().tipo == "SEMICOLON":
                                            self.indexDaTabelaDeTokens += 1
                                            return temp
                                        else:
                                            raise Exception(
                                                "Erro sintatico: falta do ponto e vírgula na linha "
                                                + str(self.tokenAtual().linha)
                                            )
                                    else:
                                        raise Exception(
                                            "Erro sintatico: falta da chave direito na linha "
                                            + str(self.tokenAtual().linha)
                                        )
                                else:
                                    raise Exception(
                                        "Erro sintatico: falta da chave esquerda na linha "
                                        + str(self.tokenAtual().linha)
                                    )
                            else:
                                raise Exception(
                                    "Erro sintatico: falta do parentese direito na linha "
                                    + str(self.tokenAtual().linha)
                                )
                        else:
                            # TODO: (5 - falta descobrir) resolver exceção
                            raise Exception(
                                "Erro sintatico: falta da virgula na linha "
                                + str(self.tokenAtual().linha)
                            )
                    else:
                        raise Exception(
                            "Erro sintatico: falta o ID na linha "
                            + str(self.tokenAtual().linha)
                        )
                else:
                    if self.tokenAtual().tipo == "PRIGHT":
                        temp.append(tempParenteses)
                        self.indexDaTabelaDeTokens += 1
                        if self.tokenAtual().tipo == "CLEFT":
                            self.indexEscopoAntesDaFuncao = self.indexEscopoAtual
                            self.indexEscopoAtual += 1
                            self.indexDaTabelaDeTokens += 1
                            tempBlock = []
                            # BLOCK # TODO: Verificar
                            while (
                                self.tokenAtual().tipo != "CRIGHT"
                                and self.tokenLookAhead().tipo != "SEMICOLON"
                            ):
                                tempBlock.append(self.block_statement())

                            temp.append(tempBlock)
                            if self.tokenAtual().tipo == "CRIGHT":
                                self.indexEscopoAtual = self.indexEscopoAntesDaFuncao
                                self.indexDaTabelaDeTokens += 1
                                if self.tokenAtual().tipo == "SEMICOLON":
                                    self.indexDaTabelaDeTokens += 1
                                    return temp
                                else:
                                    raise Exception(
                                        "Erro sintatico: falta do ponto e vírgula na linha "
                                        + str(self.tokenAtual().linha)
                                    )
                            else:
                                raise Exception(
                                    "Erro sintatico: falta da chave direito na linha "
                                    + str(self.tokenAtual().linha)
                                )

                        else:
                            raise Exception(
                                "Erro sintatico: falta da chave esquerda na linha "
                                + str(self.tokenAtual().linha)
                            )
                    else:
                        raise Exception(
                            "Erro sintatico: falta do parentese direito na linha "
                            + str(self.tokenAtual().linha)
                        )
            else:
                raise Exception(
                    "Erro sintatico: falta do parentese esquerdo na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do ID na linha " +
                str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <call_proc>
    def call_proc_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "ID":
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "PLEFT":
                self.indexDaTabelaDeTokens += 1
                tempParams = []
                if (
                    self.tokenAtual().tipo == "ID"
                    or self.tokenAtual().lexema == "True"
                    or self.tokenAtual().lexema == "False"
                ):
                    tempParams.append(self.tokenAtual().lexema)
                    self.indexDaTabelaDeTokens += 1
                    if self.tokenAtual().tipo == "COMMA":
                        tempParams.append(
                            self.params_call_statement(tempParams))
                        tempParams.pop()
                        temp.append(tempParams)
                        #  [0, 'CALL', 'PROC', 'proc1', ['a', 'b', 'c']],
                        #  [0, 'CALL', 'PROC', 'proc1', [['a'], ['b'], ['c']]],
                        if self.tokenAtual().tipo == "PRIGHT":
                            self.indexDaTabelaDeTokens += 1
                            temp.append(tempParams)
                            return temp

                    elif self.tokenAtual().tipo == "PRIGHT":
                        self.indexDaTabelaDeTokens += 1
                        temp.append(tempParams)
                        return temp
                    else:
                        raise Exception(
                            "Erro sintatico: falta da virgula na linha "
                            + str(self.tokenAtual().linha)
                        )
                else:
                    temp.append(tempParams)
                    if self.tokenAtual().tipo == "PRIGHT":

                        self.indexDaTabelaDeTokens += 1
                        return temp
                    else:
                        raise Exception(
                            "Erro sintatico: falta do parentese direito na linha "
                            + str(self.tokenAtual().linha)
                        )
            else:
                raise Exception(
                    "Erro sintatico: falta do parentese esquerdo na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do ID na linha " +
                str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <call_func>
    def call_func_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "ID":
            temp.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "PLEFT":
                self.indexDaTabelaDeTokens += 1
                tempParams = []
                if (
                    self.tokenAtual().tipo == "ID"
                    or self.tokenAtual().lexema == "True"
                    or self.tokenAtual().lexema == "False"
                ):
                    tempParams.append(self.tokenAtual().lexema)
                    self.indexDaTabelaDeTokens += 1
                    if self.tokenAtual().tipo == "COMMA":
                        tempParams.append(
                            self.params_call_statement(tempParams))
                        tempParams.pop()
                        if self.tokenAtual().tipo == "PRIGHT":
                            self.indexDaTabelaDeTokens += 1
                            temp.append(tempParams)
                            return temp
                        else:
                            raise Exception(
                                "Erro sintatico: falta do parentese direito na linha "
                                + str(self.tokenAtual().linha)
                            )
                    elif self.tokenAtual().tipo == "PRIGHT":
                        self.indexDaTabelaDeTokens += 1
                        temp.append(tempParams)
                        return temp
                    else:
                        raise Exception(
                            "Erro sintatico: falta do parentese direito na linha "
                            + str(self.tokenAtual().linha)
                        )

                else:
                    temp.append(tempParams)
                    if self.tokenAtual().tipo == "PRIGHT":
                        self.indexDaTabelaDeTokens += 1

                        return temp
                    else:
                        raise Exception(
                            "Erro sintatico: falta do parentese direito na linha "
                            + str(self.tokenAtual().linha)
                        )
            else:
                raise Exception(
                    "Erro sintatico: falta do parentese esquerdo na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do ID na linha " +
                str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <params_call>
    def params_call_statement(self, tempParams):
        self.indexDaTabelaDeTokens += 1
        if (
            self.tokenAtual().tipo == "ID"
            or self.tokenAtual().lexema == "True"
            or self.tokenAtual().lexema == "False"
        ):
            tempParams.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "COMMA":
                self.params_call_statement(tempParams)
            elif (
                self.tokenAtual().tipo == "ID"
                or self.tokenAtual().lexema == "True"
                or self.tokenAtual().lexema == "False"
            ):
                raise Exception(
                    "Erro sintatico: falta vírgula na linha "
                    + str(self.tokenAtual().linha)
                )
            else:
                # Removido p/ correção
                # self.indexDaTabelaDeTokens += 1
                return tempParams
        else:
            raise Exception(
                "Erro sintatico: é necessário informar alguma váriavel na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <print_statement> OK
    def print_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "PLEFT":
            tempParams = []
            temp.append(self.params_print_statement(tempParams))
            if self.tokenAtual().tipo == "PRIGHT":
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "SEMICOLON":
                    self.tabelaDeSimbolos.append(temp)
                    self.indexDaTabelaDeTokens += 1
                    return
                else:
                    # TODO: (4) SOLVE BUG DE CONTAGEM DE LINHAS
                    raise Exception(
                        "Erro sintatico: falta do ponto e virgula na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do Parentese direito na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do Parentese esquerdo na linha  "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <params_print_statement> OK
    def params_print_statement(self, tempParams):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "CALL":
            tempParams.append(self.tokenAtual().tipo)
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "FUNC":
                tempParams.append(self.tokenAtual().tipo)
                tempParams = self.call_func_statement(tempParams)
                return tempParams
            elif self.tokenAtual().tipo == "PROC":
                raise Exception(
                    "Erro sintatico: Procedimento não tem retorno na linha "
                    + str(self.tokenAtual().linha)
                )
            else:
                raise Exception(
                    "Erro sintatico: chamada incorreta de função na linha "
                    + str(self.tokenAtual().linha)
                )

        elif (
            (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "BOOLEAN")
            or (self.tokenAtual().tipo == "ID")
        ):
            tempParams.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if (
                self.tokenAtual().tipo == "ADD"
                or self.tokenAtual().tipo == "SUB"
                or self.tokenAtual().tipo == "MULT"
                or self.tokenAtual().tipo == "DIV"
            ):
                tempParams.append(self.tokenAtual().lexema)
                self.call_op_statement(tempParams)
                return tempParams
            else:
                return tempParams
        else:
            raise Exception(
                "Erro sintatico: uso incorreto dos parametros na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <if_statement>
    def if_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "PLEFT":
            self.indexDaTabelaDeTokens += 1
            tempExpression = []
            # Expression
            tempExpression = self.expression_statement(tempExpression)
            temp.append(tempExpression)

            if self.tokenAtual().tipo == "PRIGHT":
                olhaAfrente = self.tokenLookAhead()
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "CLEFT" and olhaAfrente.tipo != "CRIGHT":
                    self.indexDaTabelaDeTokens += 1
                    self.indexEscopoAtual += 1
                    tempBlock = []
                    while (
                        self.tokenAtual().tipo != "CRIGHT"
                        and self.tokenLookAhead().tipo != "ENDIF"
                    ):
                        tempBlock.append(self.block3_statement())

                    temp.append(tempBlock)
                    if self.tokenAtual().tipo == "CRIGHT":
                        self.indexDaTabelaDeTokens += 1
                        if self.tokenAtual().tipo == "ENDIF":
                            temp.append(self.tokenAtual().tipo)
                            self.indexDaTabelaDeTokens += 1

                            tempElse = []
                            if self.tokenAtual().tipo == "ELSE":
                                tempElse.append(self.indexEscopoAtual)
                                tempElse.append(self.tokenAtual().tipo)
                                tempElse = self.else_part_statement(
                                    tempElse)  # ELSE

                                temp.append(tempElse)
                                self.tabelaDeSimbolos.append(temp)
                                self.indexEscopoAtual -= 1
                            else:
                                temp.append(tempElse)
                                self.tabelaDeSimbolos.append(temp)
                                self.indexEscopoAtual -= 1
                                return
                        else:
                            raise Exception(
                                "Erro sintatico: falta de ENDIF "
                                + str(self.tokenAtual().linha)
                            )
                    else:
                        raise Exception(
                            "Erro sintatico: falta do CRIGHT na linha "
                            + str(self.tokenAtual().linha)
                        )
                else:
                    raise Exception(
                        "Erro sintatico: falta do CLEFT ou bloco vazio na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do Parentese direito na linha  "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do Parentese esquerdo na linha  "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <else_part>
    def else_part_statement(self, tempElse):
        olhaAfrente = self.tokenLookAhead()
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "CLEFT" and olhaAfrente.tipo != "CRIGHT":
            self.indexDaTabelaDeTokens += 1
            tempBlock = []
            while (
                self.tokenAtual().tipo != "CRIGHT"
                and self.tokenLookAhead().tipo != "ENDELSE"
            ):
                # Block
                tempBlock.append(self.block3_statement())
            tempElse.append(tempBlock)
            if self.tokenAtual().tipo == "CRIGHT":
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "ENDELSE":
                    tempElse.append(self.tokenAtual().tipo)
                    self.indexDaTabelaDeTokens += 1
                    return tempElse
                else:
                    raise Exception(
                        "Erro sintatico: falta de ENDELSE na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do CRIGHT na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do CLEFT ou bloco vazio na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <if_statement2>
    # IF chamado somente dentro do while, pois dentro dele pode ter BREAK E CONTINUE (block2)
    def if_statement2(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "PLEFT":
            self.indexDaTabelaDeTokens += 1
            tempExpression = []
            # Expression
            tempExpression = self.expression_statement(tempExpression)
            temp.append(tempExpression)
            if self.tokenAtual().tipo == "PRIGHT":
                olhaAfrente = self.tokenLookAhead()
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "CLEFT" and olhaAfrente.tipo != "CRIGHT":
                    self.indexDaTabelaDeTokens += 1
                    self.indexEscopoAtual += 1
                    tempBlock = []
                    while (
                        self.tokenAtual().tipo != "CRIGHT"
                        and self.tokenLookAhead().tipo != "ENDIF"
                    ):
                        tempBlock.append(self.block2_statement())
                    temp.append(tempBlock)
                    if self.tokenAtual().tipo == "CRIGHT":
                        self.indexDaTabelaDeTokens += 1
                        if self.tokenAtual().tipo == "ENDIF":
                            temp.append(self.tokenAtual().tipo)
                            self.indexDaTabelaDeTokens += 1
                            tempElse = []
                            if self.tokenAtual().tipo == "ELSE":
                                tempElse.append(self.indexEscopoAtual)
                                tempElse.append(self.tokenAtual().tipo)
                                tempElse = self.else_part_statement2(
                                    tempElse)  # ELSE

                                temp.append(tempElse)
                                self.tabelaDeSimbolos.append(temp)
                                self.indexEscopoAtual -= 1
                            else:
                                temp.append(tempElse)
                                self.tabelaDeSimbolos.append(temp)
                                self.indexEscopoAtual -= 1
                                return
                        else:
                            raise Exception(
                                "Erro sintatico: falta de ENDIF "
                                + str(self.tokenAtual().linha)
                            )
                    else:
                        raise Exception(
                            "Erro sintatico: falta do CRIGHT na linha "
                            + str(self.tokenAtual().linha)
                        )
                else:
                    raise Exception(
                        "Erro sintatico: falta do CLEFT ou Bloco vazio na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do Parentese direito na linha  "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do Parentese esquerdo na linha  "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # ELSE chamado somente dentro do while, pois dentro dele pode ter BREAK E CONTINUE (block2)
    # <else_part2>
    def else_part_statement2(self, tempElse):
        olhaAfrente = self.tokenLookAhead()
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "CLEFT" and olhaAfrente.tipo != "CRIGHT":
            self.indexDaTabelaDeTokens += 1
            # Block
            tempBlock = []
            while (
                self.tokenAtual().tipo != "CRIGHT"
                and self.tokenLookAhead().tipo != "ENDELSE"
            ):
                tempBlock.append(self.block2_statement())
            tempElse.append(tempBlock)
            if self.tokenAtual().tipo == "CRIGHT":
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "ENDELSE":
                    tempElse.append(self.tokenAtual().tipo)
                    self.indexDaTabelaDeTokens += 1
                    return tempElse
                else:
                    raise Exception(
                        "Erro sintatico: falta de ENDELSE na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do CRIGHT na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do CLEFT ou bloco vazio na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <while_statement>
    def while_statement(self, temp):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "PLEFT":
            self.indexDaTabelaDeTokens += 1
            tempExpression = []
            # Expression
            tempExpression = self.expression_statement(tempExpression)
            temp.append(tempExpression)
            if self.tokenAtual().tipo == "PRIGHT":
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "CLEFT":
                    self.indexDaTabelaDeTokens += 1
                    self.indexEscopoAtual += 1
                    tempBlock = []
                    # BLOCK
                    while (
                        self.tokenAtual().tipo != "CRIGHT"
                        and self.tokenLookAhead().tipo != "ENDWHILE"
                    ):
                        tempBlock.append(self.block2_statement())

                    temp.append(tempBlock)

                    if self.tokenAtual().tipo == "CRIGHT":
                        self.indexDaTabelaDeTokens += 1
                        if self.tokenAtual().tipo == "ENDWHILE":
                            temp.append(self.tokenAtual().tipo)
                            self.indexDaTabelaDeTokens += 1
                            self.tabelaDeSimbolos.append(temp)
                            self.indexEscopoAtual -= 1
                        else:
                            raise Exception(
                                "Erro sintatico: falta de ENDWHILE na linha "
                                + str(self.tokenAtual().linha)
                            )
                    else:
                        raise Exception(
                            "Erro sintatico: falta do CRIGHT na linha "
                            + str(self.tokenAtual().linha)
                        )
                else:
                    raise Exception(
                        "Erro sintatico: falta do CLEFT na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do PRIGHT na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do PLEFT na linha "
                + str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <unconditional_branch>
    def unconditional_branch_statement(self):
        if self.tokenAtual().tipo == "CONTINUE":
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "SEMICOLON":
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    "Erro sintatico: falta do ponto e virgula na linha "
                    + str(self.tokenAtual().linha)
                )

        if self.tokenAtual().tipo == "BREAK":
            self.indexDaTabelaDeTokens += 1
            if self.tokenAtual().tipo == "SEMICOLON":
                self.indexDaTabelaDeTokens += 1
            else:
                raise Exception(
                    "Erro sintatico: falta do ponto e virgula na linha "
                    + str(self.tokenAtual().linha)
                )

    # ESCOPO OK
    # <expression>
    def expression_statement(self, tempExpression):
        if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
            tempExpression.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if (
                self.tokenAtual().tipo == "EQUAL"
                or self.tokenAtual().tipo == "DIFF"
                or self.tokenAtual().tipo == "LESSEQUAL"
                or self.tokenAtual().tipo == "LESS"
                or self.tokenAtual().tipo == "GREATEREQUAL"
                or self.tokenAtual().tipo == "GREATER"
            ):
                tempExpression.append(self.tokenAtual().lexema)
                self.indexDaTabelaDeTokens += 1
                if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
                    tempExpression.append(self.tokenAtual().lexema)
                    self.indexDaTabelaDeTokens += 1
                    return tempExpression
                else:
                    raise Exception(
                        "Erro sintatico: falta do ID na linha "
                        + str(self.tokenAtual().linha)
                    )
            else:
                raise Exception(
                    "Erro sintatico: falta do operador booleano na linha "
                    + str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintatico: falta do ID na linha " +
                str(self.tokenAtual().linha)
            )

    # ESCOPO OK
    # <call_op> ok - Operações aritméticas
    def call_op_statement(self, tempEndVar):
        self.indexDaTabelaDeTokens += 1
        if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
            tempEndVar.append(self.tokenAtual().lexema)
            self.indexDaTabelaDeTokens += 1
            if (
                self.tokenAtual().tipo == "ADD"
                or self.tokenAtual().tipo == "SUB"
                or self.tokenAtual().tipo == "MULT"
                or self.tokenAtual().tipo == "DIV"
            ):
                tempEndVar.append(self.tokenAtual().lexema)
                self.call_op_statement(tempEndVar)
            else:
                return
        else:
            raise Exception(
                "Erro sintatico: falta do ID na linha " +
                str(self.tokenAtual().linha)
            )

    """

    \/ Análise Semântica \/

    """

    # Não finalizado
    # Checa semantica, se tiver tudo OK return True
    def checkSemantica(self):
        for k in range(len(self.tabelaDeSimbolos)):
            simbolo = self.tabelaDeSimbolos[k][2]
            if simbolo == "FUNC":
                self.declaration_func_semantico(self.tabelaDeSimbolos[k])

            if simbolo == "PROC":
                self.declaration_proc_semantico(self.tabelaDeSimbolos[k])

            if simbolo == "CALL":
                if self.tabelaDeSimbolos[k][3] == "FUNC":
                    self.call_func_semantico(
                        self.tabelaDeSimbolos[k],
                        4,
                        self.tabelaDeSimbolos[k][0],
                        5,
                        self.tabelaDeSimbolos[k][1],
                    )
                if self.tabelaDeSimbolos[k][3] == "PROC":
                    self.call_proc_semantico(
                        self.tabelaDeSimbolos[k], 5, self.tabelaDeSimbolos[k][1]
                    )
            # Se for declaração de variável
            if simbolo == "INT" or simbolo == "BOOL":
                # print("Análise da declaração", k + 1, " -> ", self.tabelaDeSimbolos[k])
                self.declaration_var_semantico(self.tabelaDeSimbolos[k])

            if simbolo == "IF":
                # print("Análise da declaração", k + 1, " -> ", self.tabelaDeSimbolos[k])
                self.expression_semantico(self.tabelaDeSimbolos[k])

            if simbolo == "WHILE":
                # print("Análise da declaração", k + 1, " -> ", self.tabelaDeSimbolos[k])
                self.expression_semantico(self.tabelaDeSimbolos[k])

            # Se for chamada/atribuição de variável
            if simbolo == "ID":
                # print("Análise da declaração", k + 1, " -> ", self.tabelaDeSimbolos[k])
                self.call_var_semantico(self.tabelaDeSimbolos[k])
                # Outras condições

        print("FIM DA ANÁLISE SEMÂNTICA - DEU CERTO :)\n")

    def buscarNaTabelaDeSimbolos(self, simbolo, indice):
        for k in range(len(self.tabelaDeSimbolos)):
            if self.tabelaDeSimbolos[k][indice] == simbolo:
                return self.tabelaDeSimbolos[k]

    # TODO: Não finalizado (faltam expressões e funções)
    def declaration_var_semantico(self, tabelaNoIndiceAtual):
        # Se var for int
        if tabelaNoIndiceAtual[2] == "INT":
            simbolo = tabelaNoIndiceAtual[5][0]
            # Exemplo: Caso se 'int b = 1';
            #  <num>
            if simbolo.isnumeric():
                return True

            # TODO: Caso se 'int b = call func a();' se o return de func for int
            # <call_func>
            if simbolo == "CALL":
                if tabelaNoIndiceAtual[5][1] == "FUNC":
                    for k in range(len(self.tabelaDeSimbolos)):
                        # Procura na tabela de simbolos alguma declaração de Função
                        if self.tabelaDeSimbolos[k][2] == "FUNC":
                            # Vê se alguma função declarada tem o mesmo nome da função da variável
                            if self.tabelaDeSimbolos[k][4] == tabelaNoIndiceAtual[5][2]:
                                # Conferir se a função está declarada no escopo/linha menor ou igual
                                if (
                                    self.tabelaDeSimbolos[k][0]
                                    <= tabelaNoIndiceAtual[0]
                                ) and (
                                    self.tabelaDeSimbolos[k][1]
                                    <= tabelaNoIndiceAtual[1]
                                ):
                                    # Verificar a quantidade de parametros da função declarada com a função passada
                                    if len(self.tabelaDeSimbolos[k][5]) == len(
                                        tabelaNoIndiceAtual[5][3]
                                    ):
                                        # TODO: Verificar se as variáveis passadas na chamada, já foram declaradas
                                        for n in range(len(tabelaNoIndiceAtual[5][3])):
                                            # Procura tem alguma variável declarada na tabela com o nome da var passada na chamada
                                            varDeclaradaNaTabela = self.buscarNaTabelaDeSimbolos(
                                                tabelaNoIndiceAtual[5][3][n], 3)
                                            if(varDeclaradaNaTabela != None):
                                                # Conferir se a variavel está declarada no escopo/linha menor ou igual
                                                if (varDeclaradaNaTabela[0] <= tabelaNoIndiceAtual[0]
                                                    ) and (varDeclaradaNaTabela[1] <= tabelaNoIndiceAtual[1]):
                                                    # Verifica qual o tipo de retorno da função declarada
                                                    if self.tabelaDeSimbolos[k][3] == "INT":
                                                        return True
                                                    else:
                                                        raise Exception(
                                                            "Erro Semântico: int não recebe int na linha: "
                                                            + str(tabelaNoIndiceAtual[1])
                                                        )
                                                else:
                                                    raise Exception(
                                                        "Erro Semântico: variável não declarada nos parametros na linha: "
                                                        + str(tabelaNoIndiceAtual[1])
                                                    )
                                            else:
                                                raise Exception(
                                                    "Erro Semântico: variável não declarada nos parametros na linha: "
                                                    + str(tabelaNoIndiceAtual[1])
                                                )
                                    else:
                                        raise Exception(
                                            "Erro Semântico: quantidade de parametros inválida na linha: "
                                            + str(tabelaNoIndiceAtual[1])
                                        )
                                else:
                                    raise Exception(
                                        "Erro Semântico: função não declarada na linha: "
                                        + str(tabelaNoIndiceAtual[1])
                                    )

                            else:
                                raise Exception(
                                    "Erro Semântico: função não declarada na linha: "
                                    + str(tabelaNoIndiceAtual[1])
                                )
                else:
                    raise Exception(
                        "Erro Semântico: variável não pode receber procedimento na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
            # TODO: Fazer semantico caso 'int e = a + d;' 'int f = 1 + 2;' (Expressão aritmética)
            # <call_op>

            # Caso 'int b = a'; se 'int a' for declarado já
            # <identifier>
            if simbolo.isalpha():
                # Buscar se o 'a' foi declarado
                varDeclarada = self.buscarNaTabelaDeSimbolos(
                    tabelaNoIndiceAtual[5][0], 3
                )
                # Se foi a varDeclarada não é none
                if varDeclarada != None:
                    # Verifica se 'a' foi declarada em um escopo visivel e linhas anteriores
                    if (
                        varDeclarada[0] <= tabelaNoIndiceAtual[0]
                        and varDeclarada[1] <= tabelaNoIndiceAtual[1]
                    ):
                        # Verificar se 'a' é int
                        if varDeclarada[2] == "INT":
                            return True
                        # Se não, 'int b', não pode receber 'a'
                        else:
                            raise Exception(
                                "Erro Semântico: variável do tipo int não recebe int na linha: "
                                + str(tabelaNoIndiceAtual[1])
                            )
                    # Se não está em um escopo visivel, é considerada como não declarada
                    else:
                        raise Exception(
                            "Erro Semântico: variavel não declarada na linha: "
                            + str(tabelaNoIndiceAtual[1])
                        )
                # Se varDeclarada == None, então 'a' nunca foi declarada
                else:
                    raise Exception(
                        "Erro Semântico: variavel não declarada na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
            else:
                raise Exception(
                    "Erro Semântico: variável do tipo inteiro não recebe inteiro na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

        if tabelaNoIndiceAtual[1] == "BOOL":
            # Exemplo: Caso se 'int b = True';
            #  <boolean>
            simbolo = tabelaNoIndiceAtual[4][0]
            if simbolo == "True" or simbolo == "False":
                return True

            # <call_func>
            if simbolo == "CALL":
                return True

            # TODO: Fazer semantico caso 'int e = a + d;' 'int f = 1 + 2;' (Expressão aritmética)
            # <call_op>

            # Caso 'bool b = a'; se 'bool a' for declarado já
            # <identifier>
            if simbolo.isalpha():
                # Buscar se o 'a' foi declarado
                varDeclarada = self.buscarNaTabelaDeSimbolos(
                    tabelaNoIndiceAtual[5][0], 3
                )
                # Se foi a varDeclarada não é none
                if varDeclarada != None:
                    # Verifica se 'a' foi declarada em um escopo visivel e linhas anteriores
                    if (
                        varDeclarada[0] <= tabelaNoIndiceAtual[0]
                        and varDeclarada[1] <= tabelaNoIndiceAtual[1]
                    ):
                        # Verificar se 'a' é bool
                        if varDeclarada[2] == "BOOL":
                            return True
                        # Se não, 'bool b', não pode receber 'a'
                        else:
                            raise Exception(
                                "Erro Semântico: variável do tipo boolean não recebe boolean na linha: "
                                + str(tabelaNoIndiceAtual[1])
                            )
                    # Se não está em um escopo visivel, é considerada como não declarada
                    else:
                        raise Exception(
                            "Erro Semântico: variavel não declarada na linha: "
                            + str(tabelaNoIndiceAtual[1])
                        )
                # Se varDeclarada == None, então 'a' nunca foi declarada
                else:
                    raise Exception(
                        "Erro Semântico: variavel não declarada na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )

            else:
                raise Exception(
                    "Erro Semântico: variável do tipo boolean não recebe boolean na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

    # TODO: Não finalizado (faltam expressões e funções)
    # TODO: Resolver problema de escopo antigo sendo visivel
    def call_var_semantico(self, simbolo):
        flag = False
        for k in range(len(self.tabelaDeSimbolos)):
            if (
                self.tabelaDeSimbolos[k][2] == "INT"
                or self.tabelaDeSimbolos[k][2] == "BOOL"
            ):
                print
                # Verificando se há duas var. com msm nome
                if self.tabelaDeSimbolos[k][3] == simbolo[3]:
                    # Se houver, verifica se a variavel está visivel no
                    # escopo da qual foi chamada
                    if self.tabelaDeSimbolos[k][0] <= simbolo[0]:
                        if self.tabelaDeSimbolos[k][1] <= simbolo[1]:
                            flag = True  # Flag para verificar se a chamada tá ok
                            # Chamada de método para verificar o tipo da variavel
                            # que está sendo atribuída
                            self.verificarTipoCallVar(
                                self.tabelaDeSimbolos[k], simbolo)
                            break

            # Buscar em parametros de PROC
            elif self.buscarParamsProc(simbolo) == True:
                flag = True
                break

            # Buscar em parametros de FUNC
            elif self.buscarParamsFunc(simbolo, 3) == True:
                flag = True
                break

        # Se der errado a declaração:
        if flag == False:
            raise Exception(
                "Erro Semântico: variável não declarada na linha: " +
                str(simbolo[1])
            )

    def buscarParamsProc(self, simbolo):
        paramsProc = self.buscarNaTabelaDeSimbolos("PROC", 2)
        if paramsProc != None:
            paramsProc = paramsProc[4]
            for k in range(len(paramsProc)):
                if simbolo[3] == paramsProc[k][2]:
                    if paramsProc[k][1] == "INT":
                        if simbolo[5].isnumeric():
                            return True
                        if not simbolo[5].isnumeric():
                            raise Exception(
                                "Erro Semântico: variável do tipo int não recebe int na linha: "
                                + str(simbolo[1])
                            )
                    if paramsProc[k][1] == "BOOL":
                        # TODO: verificar posteriormente
                        if simbolo[5] == "True" or simbolo[5] == "False":
                            return True
                        else:
                            raise Exception(
                                "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                                + str(simbolo[1])
                            )
                    break
        else:
            return False

    def buscarParamsFunc(self, simbolo, n):
        paramsFunc = self.buscarNaTabelaDeSimbolos("FUNC", 2)
        if paramsFunc != None:
            paramsFunc = paramsFunc[5]
            for k in range(len(paramsFunc)):
                if simbolo[n] == paramsFunc[k][2]:
                    if paramsFunc[k][1] == "INT":
                        if simbolo[5].isnumeric():
                            return True
                        if not simbolo[5].isnumeric():
                            raise Exception(
                                "Erro Semântico: variável do tipo int não recebe int na linha: "
                                + str(simbolo[1])
                            )
                    if paramsFunc[k][1] == "BOOL":
                        # TODO: verificar posteriormente
                        if simbolo[5] == "True" or simbolo[5] == "False":
                            return True
                        else:
                            raise Exception(
                                "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                                + str(simbolo[1])
                            )
                    break
        else:
            return False

    # TODO: Faltam expressões e funções
    def verificarTipoCallVar(self, simboloDeclaradoNaTabela, simbolo):
        if simboloDeclaradoNaTabela[2] == "INT":
            if not simbolo[5].isnumeric():
                raise Exception(
                    "Erro Semântico: variável do tipo int não recebe int na linha: "
                    + str(simbolo[1])
                )
        if simboloDeclaradoNaTabela[2] == "BOOL":
            if simbolo[5] == "True" or simbolo[5] == "False":
                return True
            else:
                raise Exception(
                    "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                    + str(simbolo[1])
                )

    # TODO:  Faltam variaveis e funções
    def declaration_func_semantico(self, tabelaNoIndiceAtual):
        # print(tabelaNoIndiceAtual)
        if tabelaNoIndiceAtual[3] == "INT":
            if not tabelaNoIndiceAtual[7][2][0].isnumeric():
                raise Exception(
                    "Erro Semântico: O retorno espera um inteiro na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

        if tabelaNoIndiceAtual[3] == "BOOL":
            if (
                tabelaNoIndiceAtual[7][2][0] == "True"
                or tabelaNoIndiceAtual[7][2][0] == "False"
            ) is False:
                raise Exception(
                    "Erro Semântico: O retorno espera um boolean na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

    def call_func_semantico(self, tabelaNoIndiceAtual, n, escopo, m, linha):
        # print(tabelaNoIndiceAtual)
        flag = False
        for k in range(len(self.tabelaDeSimbolos)):
            if self.tabelaDeSimbolos[k][2] == "FUNC":
                if self.tabelaDeSimbolos[k][4] == tabelaNoIndiceAtual[n]:
                    if self.tabelaDeSimbolos[k][0] <= escopo:
                        flag = True
                        self.verificarParams(
                            self.tabelaDeSimbolos[k],
                            tabelaNoIndiceAtual,
                            5,
                            "FUNC",
                            m,
                            linha,
                            escopo,
                        )
                        return True
                        break

        # Se der errado a declaração:
        if flag == False:
            raise Exception(
                "Erro Semântico: função não declarada na linha: "
                + str(tabelaNoIndiceAtual[1])
            )

    def verificarParams(
        self, simboloDeclaradoNaTabela, simbolo, n, tipo, m, linha, escopo
    ):
        # PASSO A PASSO:
        # 1º -> Verificar quantidade de parametros de acordo com a declaração
        # 2º -> Se for > 0
        # Devemos percorrer cada variavel dos parametros, então verificar em cada um o seguinte:
        # 1º -> Verificar se já foi declarada no escopo visível ok
        # 2º -> Verificar se o tipo na chamada é o mesmo da declaração ok
        # 3º -> Se for sem params, prosseguir

        flag = 0
        # Verifica se a quantidade de parametros da chamada corresponde com a declaração
        if len(simboloDeclaradoNaTabela[n]) == len(simbolo[m]):
            # Se os parâmetros não for vazio:
            if len(simbolo[m]) > 0:
                # P/ cada parâmetro
                for k in range(len(simbolo[m])):
                    # Leitura da declaração do parametro atual
                    for i in range(len(self.tabelaDeSimbolos)):
                        # Busca na tabela de simbolos a variavel passada na chamada da função
                        if self.tabelaDeSimbolos[i][3] == simbolo[m][k]:
                            # Verifica se foi declarado em escopo/linhas anteriores
                            if (self.tabelaDeSimbolos[i][0] <= escopo) and (
                                self.tabelaDeSimbolos[i][1] <= linha
                            ):
                                # Só incrementa quando acha declaração de váriavel
                                if (
                                    self.tabelaDeSimbolos[i][2] == "INT"
                                    or self.tabelaDeSimbolos[i][2] == "BOOL"
                                ):
                                    flag += 1
                                    self.comparaTipoChamadaComDeclaracao(
                                        self.tabelaDeSimbolos[i], simbolo, tipo, n
                                    )
                                break

            # Se não tiver params
            else:
                return True
        else:
            raise Exception(
                "Erro Semântico: quantidade de parâmetros inválido na linha: "
                + str(linha)
            )

        if flag != len(simboloDeclaradoNaTabela[n]):
            raise Exception(
                "Erro Semântico: variável do parâmetro não declarada na linha: "
                + str(linha)
            )
        else:
            return True

    def comparaTipoChamadaComDeclaracao(
        self, declaracaoVarNaTabela, callFuncTabela, tipo, n
    ):
        declaracaoFuncNaTabela = self.buscarNaTabelaDeSimbolos(tipo, 2)
        flag = False
        for k in range(len(declaracaoFuncNaTabela[n])):
            if declaracaoFuncNaTabela[n][k][1] == declaracaoVarNaTabela[2]:
                flag = True
                break

            # Caso ele encontre um ID ao inves da declaração direta,
            # deve buscar pra saber se o tipo corresponde
            elif declaracaoVarNaTabela[2] == "ID":
                tipoDeclaracaoDoID = self.buscarNaTabelaDeSimbolos("ID", 2)
                varDeclarada = self.buscarNaTabelaDeSimbolos(
                    tipoDeclaracaoDoID[3], 3)
                if declaracaoFuncNaTabela[n][k][1] == varDeclarada[2]:
                    flag = True
                    break

        if flag == False:
            raise Exception(
                "Erro Semântico: tipo do parâmetro inválido na linha: "
                + str(callFuncTabela[1])
            )

    def declaration_proc_semantico(self, tabelaNoIndiceAtual):
        # Analisar se variaveis e funções usados dentro do procedimento são passados no parametro ou se são declarados antes
        # print(tabelaNoIndiceAtual)
        # Quebrando no BOOL quando atualzia a variavel com outro valor

        flag = False
        cont = 0
        for k in range(len(self.tabelaDeSimbolos)):
            # Percorre lista de Block do PROC
            for i in range(len(tabelaNoIndiceAtual[5])):
                # Pega as variaveis declaradas da tabela de simbolo
                if (
                    self.tabelaDeSimbolos[k][2] == "BOOL"
                    or self.tabelaDeSimbolos[k][2] == "INT"
                ):
                    if tabelaNoIndiceAtual[5][i] == self.tabelaDeSimbolos[k][3]:
                        # Verificar se a variável encontrada está no escopo/linha menor ou igual
                        if (
                            self.tabelaDeSimbolos[k][0] <= tabelaNoIndiceAtual[0]
                            and self.tabelaDeSimbolos[k][1] <= tabelaNoIndiceAtual[1]
                        ):
                            # Chamada de método para verificar o tipo da variavel
                            # que está sendo atribuída
                            if self.tabelaDeSimbolos[k][2] == "INT":
                                if not tabelaNoIndiceAtual[5][i][5].isnumeric():
                                    raise Exception(
                                        "Erro Semântico: variável do tipo int não recebe int na linha: "
                                        + str(tabelaNoIndiceAtual[1])
                                    )
                                else:
                                    cont += 1
                                    flag = True
                                    break
                                    return True

                            elif self.tabelaDeSimbolos[k][2] == "BOOL":
                                if (
                                    tabelaNoIndiceAtual[5][i][5] == "True"
                                    or tabelaNoIndiceAtual[5][i][5] == "False"
                                ):
                                    cont += 1
                                    flag = True
                                    break
                                    return True
                                else:
                                    raise Exception(
                                        "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                                        + str(tabelaNoIndiceAtual[1])
                                    )

                    else:
                        for m in range(len(tabelaNoIndiceAtual[5])):
                            for n in range(len(tabelaNoIndiceAtual[4])):
                                if (
                                    tabelaNoIndiceAtual[5][m][3]
                                    == tabelaNoIndiceAtual[4][n][2]
                                ):
                                    if tabelaNoIndiceAtual[4][n][1] == "INT":
                                        if not tabelaNoIndiceAtual[5][m][5].isnumeric():
                                            raise Exception(
                                                "Erro Semântico: variável do tipo int não recebe int na linha: "
                                                + str(tabelaNoIndiceAtual[1])
                                            )
                                        else:
                                            cont += 1
                                            flag = True
                                            break
                                            return True

                                    if tabelaNoIndiceAtual[4][n][1] == "BOOL":
                                        if (
                                            tabelaNoIndiceAtual[5][i][5] == "True"
                                            or tabelaNoIndiceAtual[5][i][5] == "False"
                                        ):
                                            cont += 1
                                            flag = True
                                            break
                                            return True
                                        else:
                                            raise Exception(
                                                "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                                                + str(tabelaNoIndiceAtual[1])
                                            )
                else:
                    for m in range(len(tabelaNoIndiceAtual[5])):
                        for n in range(len(tabelaNoIndiceAtual[4])):
                            if (
                                tabelaNoIndiceAtual[5][m][3]
                                == tabelaNoIndiceAtual[4][n][2]
                            ):
                                if tabelaNoIndiceAtual[4][n][1] == "INT":
                                    if not tabelaNoIndiceAtual[5][m][5].isnumeric():
                                        raise Exception(
                                            "Erro Semântico: variável do tipo int não recebe int na linha: "
                                            + str(tabelaNoIndiceAtual[1])
                                        )
                                    else:
                                        cont += 1
                                        flag = True
                                        break
                                        return True

                                if tabelaNoIndiceAtual[4][n][1] == "BOOL":
                                    if (
                                        tabelaNoIndiceAtual[5][i][5] == "True"
                                        or tabelaNoIndiceAtual[5][i][5] == "False"
                                    ):
                                        cont += 1
                                        flag = True
                                        break
                                        return True
                                    else:
                                        raise Exception(
                                            "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                                            + str(tabelaNoIndiceAtual[1])
                                        )

        # Se der errado a declaração:
        if flag == False and (cont != len(tabelaNoIndiceAtual[4])):
            raise Exception(
                "Erro Semântico: variável não declarada na linha: "
                + str(tabelaNoIndiceAtual[1])
            )

    def call_proc_semantico(self, tabelaNoIndiceAtual, m, linha):
        # Analisar se o procedimento chamado já foi declarado ok
        # Analisar se os parâmetros da chamada foram declarados antes ok
        # Analisar se o tipo dos parâmetros da chamada são os mesmos da declaração ok
        # Analisar se a quantidade dos parâmetros da chamada é a mesma da declaração ok
        # print(tabelaNoIndiceAtual)
        flag = False
        for k in range(len(self.tabelaDeSimbolos)):
            if self.tabelaDeSimbolos[k][2] == "PROC":
                if self.tabelaDeSimbolos[k][3] == tabelaNoIndiceAtual[4]:
                    if self.tabelaDeSimbolos[k][0] <= tabelaNoIndiceAtual[0]:
                        flag = True
                        self.verificarParams(
                            self.tabelaDeSimbolos[k],
                            tabelaNoIndiceAtual,
                            4,
                            "PROC",
                            m,
                            linha,
                            tabelaNoIndiceAtual[0],
                        )
                        break

        # Se der errado a declaração:
        if flag == False:
            raise Exception(
                "Erro Semântico: procedimento não declarado na linha: "
                + str(tabelaNoIndiceAtual[1])
            )

    def expression_semantico(self, tabelaNoIndiceAtual):
        buscaParam1 = self.buscarNaTabelaDeSimbolos(
            tabelaNoIndiceAtual[3][0], 3)
        buscaParam2 = self.buscarNaTabelaDeSimbolos(
            tabelaNoIndiceAtual[3][2], 3)

        if (tabelaNoIndiceAtual[3][0]).isnumeric() and (
            tabelaNoIndiceAtual[3][2]
        ).isnumeric():
            return True

        elif (
            tabelaNoIndiceAtual[3][0].isalpha(
            ) and tabelaNoIndiceAtual[3][2].isalpha()
        ):
            if buscaParam1 != None and buscaParam2 != None:
                if buscaParam1[2] == "INT" and buscaParam2[2] != "INT":
                    raise Exception(
                        "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
                if buscaParam2[2] == "INT" and buscaParam1[2] != "INT":
                    raise Exception(
                        "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )

                if buscaParam2[2] == "INT" and buscaParam1[2] == "INT":
                    if (buscaParam1[0] <= tabelaNoIndiceAtual[0]) and (
                        buscaParam2[0] <= tabelaNoIndiceAtual[0]
                    ):
                        return True
                    else:
                        raise Exception(
                            "Erro Semântico: Variável não declarada na linha: "
                            + str(tabelaNoIndiceAtual[1])
                        )
                if buscaParam2[2] == "BOOL" and buscaParam1[2] == "BOOL":
                    if (buscaParam1[0] <= tabelaNoIndiceAtual[0]) and (
                        buscaParam2[0] <= tabelaNoIndiceAtual[0]
                    ):
                        if (
                            tabelaNoIndiceAtual[3][1] == "=="
                            or tabelaNoIndiceAtual[3][1] == "!="
                        ):
                            return True
                        else:
                            raise Exception(
                                "Erro Semântico: Não é possível fazer este tipo de comparação com Boolean na linha: "
                                + str(tabelaNoIndiceAtual[1])
                            )
                    else:
                        raise Exception(
                            "Erro Semântico: Variável não declarada na linha: "
                            + str(tabelaNoIndiceAtual[1])
                        )

                if buscaParam2[2] == "INT" and buscaParam1[2] != "BOOL":
                    raise Exception(
                        "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
                if buscaParam2[2] == "BOOL" and buscaParam1[2] != "INT":
                    raise Exception(
                        "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
            else:
                raise Exception(
                    "Erro Semântico: variavel não declarada na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

        elif (
            tabelaNoIndiceAtual[3][0].isalpha()
            and (tabelaNoIndiceAtual[3][2]).isnumeric()
        ):
            if buscaParam1 != None:
                if buscaParam1[2] != "INT":
                    raise Exception(
                        "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
                else:
                    if buscaParam1[0] <= tabelaNoIndiceAtual[0]:
                        return True
                    else:
                        raise Exception(
                            "Erro Semântico: Variável não declarada na linha: "
                            + str(tabelaNoIndiceAtual[1])
                        )
            else:
                raise Exception(
                    "Erro Semântico: variavel não declarada na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

        elif (tabelaNoIndiceAtual[3][0]).isnumeric() and tabelaNoIndiceAtual[3][
            2
        ].isalpha():
            if buscaParam2 != None:
                if buscaParam2[2] != "INT":
                    raise Exception(
                        "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
                        + str(tabelaNoIndiceAtual[1])
                    )
                else:
                    if buscaParam2[0] <= tabelaNoIndiceAtual[0]:
                        return True
                    else:
                        raise Exception(
                            "Erro Semântico: Variável não declarada na linha: "
                            + str(tabelaNoIndiceAtual[1])
                        )
            else:
                raise Exception(
                    "Erro Semântico: variavel não declarada na linha: "
                    + str(tabelaNoIndiceAtual[1])
                )

        else:
            raise Exception(
                "Erro Semântico: parametros inválidos na linha: "
                + str(tabelaNoIndiceAtual[1])
            )
