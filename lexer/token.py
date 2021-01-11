class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha

    def __str__(self):
        return "Tipo: %s\n Lexema: %s\n Linha: %s\n" % (str(self.tipo), str(self.lexema), str(self.linha))