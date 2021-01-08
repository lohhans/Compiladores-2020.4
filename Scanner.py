
def scanReserved(self):
    for i in self.tokens:
        if(i.tipo == 'ID'):
            if(i.lexema == 'func'):
                i.tipo = "FUNC"
            
            elif(i.lexema == 'proc'):
                i.tipo = "PROC"
                
            elif(i.lexema == 'var'):
                i.tipo = "VAR"
            
            elif(i.lexema == 'int'):
                i.tipo = 'INT'
            
            elif(i.lexema == 'bool'):
                i.tipo = 'BOOLEAN'          #Tipo Booleano
            
            elif(i.lexema == 'True'):
                i.tipo = 'BOOLEAN'          #Booleano
            
            elif(i.lexema == 'False'):
                i.tipo = 'BOOLEAN'          #Booleano
            
            elif(i.lexema == 'return'):
                i.tipo = 'RETURN'
            
            elif(i.lexema == 'if'):
                i.tipo = 'IF'
            
            elif(i.lexema == 'else'):
                i.tipo = 'ELSE'
                
            elif(i.lexema == 'while'):
                i.tipo = 'WHILE'
            
            elif(i.lexema == 'print'):
                i.tipo = 'PRINT'
            
            elif(i.lexema == 'break'):
                i.tipo = 'BREAK'
            
            elif(i.lexema == 'continue'):
                i.tipo = 'CONTINUE'
                
            elif(i.lexema == 'return'):
                i.tipo = 'RETURN'