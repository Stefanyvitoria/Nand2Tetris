import sys 
from Parser import *

class main(parser):
    def __init__(self, name_arq):
        self.nome_arquivo = name_arq

        self.DadosAuxiliares = {'indLabel': 0, 'indFuncao' : 0, 'ListaFuncao' : []} #Dados que auxiliarão na escrita no código hack.

        self.traduz(self.nome_arquivo, self.DadosAuxiliares) #Inicia a tradução.


    def traduz(self, nome_entrada,D_AUX):
        """Faz a tradução."""
        super().__init__(nome_arquivo= nome_entrada) #inicia o construtor da classe parser
        
        while self.hasMoreCommands(): #Enquato tiver mais comandos.
            self.advance() #Carrega o próximo comando. 
            tipo_comando = self.commandType() #Obtem o tipo 

            #Escreve o código baseado no tipo e nos argumnetos.
            if tipo_comando == 'C_ARITHMETIC': 
                self.writeArithmetic(comando=self.linha_comando[0], ind= D_AUX['indLabel'])
                D_AUX['indLabel'] += 1

            elif (tipo_comando == 'C_POP') or (tipo_comando == 'C_PUSH'): 
                self.writePushPop(self.linha_comando[0], self.arg1(), self.arg2())

            elif tipo_comando == 'C_LABEL':
                self.writeLabel(self.arg1(), D_AUX['ListaFuncao'])
            
            elif tipo_comando == 'C_GOTO':
                self.writeGoto(self.arg1(), D_AUX['ListaFuncao'])

            elif tipo_comando == 'C_IFGOTO':
                self.writeIf(self.arg1(), D_AUX['ListaFuncao'])

            elif tipo_comando == 'C_FUNCTION':
                self.writeFunction(self.arg1(),self.arg2())
                D_AUX['ListaFuncao'].append(self.arg1())

            elif tipo_comando == 'C_CALL':
                self.writeCall(self.arg1(), self.arg2(), str(D_AUX['indFuncao']))
                D_AUX['indFuncao'] += 1
                
            elif tipo_comando == 'C_RETURN':
                self.writeReturn()

            else:
                continue
                
        self.close() #Fecha o arquivo asm.


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('use:python VMTranslator.py [nomearquivo].vm')
