import sys
import os.path
import string

class AnalisadorLexico():

# Metodo construtor da classe
def __init__(self):
    self.arquivo_e = "programa.txt"
    self.arquivo_s = "resp-lex.txt"

# Metodo para mudar arquivo de entrada
def mudaEntrada(self, string):
    self.arquivo_e = string

def getEntrada(self):
    return self.arquivo_e

def getSaida(self):
    return self.arquivo_s

# Metodo que verifica se a entrada eh um delimitador
# O metodo find() retorna a posicao do caractere na string de 
# entrada caso o mesmo seja encontrado
def ehDelimitador(self, caracter):
    # String com os delimitadores componentes da linguagem
    delimitadores = ";,(){}"
    if caracter in delimitadores:
        return True
    return False

# Metodo que verifica se a entrada eh uma letra
def ehLetra (self, caracter):
    # String com as letras componentes da linguagem (a..z|A..Z)
    letra = string.ascii_letters
    if caracter in letra:
        return True
    return False

# Metodo que verifica se a entrada eh um digito
def ehDigito (self, caracter):
    # String com os digitos componentes da linguagem
    digito = '0123456789'
    if caracter in digito:
        return True
    return False

# Metodo que verifica se a entrada eh um operador
def ehOperador(self, entrada):
    # Listas com os operadores componentes da linguagem
    operadores = '+ - * / == != > >= < <= ='.split()
    if entrada in operadores:
        return True
    return False
