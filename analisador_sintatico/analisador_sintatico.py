class AnalisadorSintatico:
    def __init__(self, tabelaDeTokens):
        self.tabelaDeTokens = tabelaDeTokens
        self.indexDaTabelaDeTokens = 0
        self.erro = False

    def statement_list(self):
        if(self.tokenAtual().tipo == "END"):
            self.listaEscopos[0].fechar()
            return
        else:
            self.statement()
            self.statement_list()
            return