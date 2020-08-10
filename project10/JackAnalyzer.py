import sys
import os
from JackTokenizer import JackTokenizer

class Main(JackTokenizer):
    def __init__(self, entrada_arquivosjack):
        self.nome_entrada = entrada_arquivosjack

        self.principal()
    
    def principal(self):
        if self.nome_entrada.endswith('.jack'): self.Routine(self.nome_entrada)

        else:
            for ele in os.listdir(self.nome_entrada):
                if ele.endswith('.jack'): self.Routine(self.nome_entrada+'/'+ele)

    def Routine(self, entrada):
        super().__init__(entrada)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        Main(sys.argv[-1])

    else:
        print('Use: JackTokenizer.py [NomeArquivo].jack ou JackTokenizer.py [NomeDiretório]')
