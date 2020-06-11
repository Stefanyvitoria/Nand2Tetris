import sys 
from Parser import *

class main(parser):
    def __init__(self, name_arq):
        self.nome_arquivo = name_arq
        
        self.indice_comando = 0

        self.traduz(self.nome_arquivo)

    def traduz(self, nome_entrada):
        """Faz a tradução e escreve o arquivo de saida."""
        super().__init__(nome_arquivo= nome_entrada) #inicia o construtor da classe parser
        
        while self.hasMoreCommands():
            self.indice_comando += 1
            self.advance()
            tipo_comando = self.commandType()
            if tipo_comando == 'C_ARITHMETIC': 
                self.writeArithmetic(comando=self.linha_comando[0], ind=self.indice_comando)

            elif (tipo_comando == 'C_POP') or (tipo_comando == 'C_PUSH'): 
                self.writePushPop(self.linha_comando[0], self.arg1(), self.arg2())
                
        self.close()
        return None


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('use:python VMTranslator.py nomearquivo.vm')
