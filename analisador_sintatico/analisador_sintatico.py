class AnalisadorSintatico:
    def __init__(self, tabelaDeTokens):
        self.tabelaDeTokens = tabelaDeTokens
        self.indexDaTabelaDeTokens = 0
        self.erro = False

    def statement_list(self):
        if(self.tokenAtual().tipo == "END"):
            self.listaEscopos[0].fechar()
            return

        elif(self.tokenAtual().tipo == "PROGRAM"):
            self.indexToken +=1
            if(self.tokenAtual().tipo == "CLEFT"):
                self.indexToken += 1
                if(block() == True):    # tem algo no block para rodar
                    self.statement()
                self.statement_list()
                return
                else:                   # bloco vazio
                    if(self.tokenAtual().tipo == "CRIGHT"):
                        self.indexToken += 1
                        if(self.tokenAtual().tipo == "END"):
                            self.listaEscopos[0].fechar()
                            # Deu certo
                        # else falta o end
                    #else falta fechar CRIGHT
            return   

        else:
            # Tratar erro
            self.listaEscopos[0].fechar()
            return
            
    # <declaration_var>
    def declaration_var_statement(self):
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):
            temp = []
            temp.append('VAR')
            temp.append(self.tokenAtual().tipo)
            self.indexToken +=1
            if(self.tokenAtual().tipo == 'ID'):
                temp.append(self.tokenAtual().lexema)
                self.indexToken +=1
                if(self.tokenAtual().tipo == 'ATTR'):   #atribuicao
                    self.indexToken +=1
                    # aqui vem o end_var

    # <declaration_func>
    def declaration_func_statement(self):
        if(self.tokenAtual().tipo == 'FUNC'):
            temp = []
            temp.append('FUNC')
            escopoDaFuncao = self.indexEscopoAtual
            escopoForaDaFunc = self.indexEscopoAtual
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'BOOL'):#tipo
                temp.append(self.tokenAtual().tipo)
                self.indexToken += 1
                if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'func'):#identificador
                    temp.append(self.tokenAtual().lexema)
                    self.indexToken += 1                  
                    #(params)

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
                #<identifier> (<params_call>)

    # <declaration_proc>
    def declaration_proc_statement(self):
        if(self.tokenAtual().tipo == 'PROC'):
            temp = []
            temp.append('PROC')
            escopoDoProcecimento = self.indexEscopoAtual
            escopoForaDoProc = self.indexEscopoAtual
            self.indexToken += 1
            #<identifier> (<params>) { <block> }
    
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
                #<identifier> (<params_call>)

    # def block
    # def params
    # <params_call>
    # def end_var
    # def <return_statement>
    # <identifier> (variavel)
    # <program> ::= program { <block> } end
    # <expression> 
    # <if_statement> 
    # <else_part> 
    # <unconditional_branch>
    # <print_statement>


