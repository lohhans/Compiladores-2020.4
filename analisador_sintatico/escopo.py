class Escopo():
    def __init__(self, index, escopoAtual):
        self.index = index
        self.escopoAtual = escopoAtual
        self.escopoAberto = True

    def fechar(self):
        self.escopoAberto = False

    def __str__(self):
        return "Index: %s\n Escopo atual: %s\n Está aberto?:%s\n" % (str(self.index), str(self.escopoAtual), str(self.escopoAberto))
