import re
from CodeWriter import *

class parser(codewriter):
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.nome_arquivo_saida = nome_arquivo[:-2]+'asm'
        
        self.arquivo = open(self.nome_arquivo, 'r', encoding='UTF-8')
        self.linhas = self.arquivo.readlines()
        self.arquivo.close()      

        self.linha_comando = ''
        self.linha_atual = 0
        self.comentario = re.compile(r'//.*$')

        super().__init__(self.nome_arquivo_saida) #inicia construtor da classe  codewriter
    

    def hasMoreCommands(self):
        """Retorna False quando chegar ao fim do arquivo, enquanto não, retorna True."""
        if (self.linha_atual+1) <= len(self.linhas): return True
        else : return False

    def advance(self):
        """Obtem o próximo comando do arquivo e armazena em 'self.linha_comando'."""
        linha = self.linhas[self.linha_atual]
        self.linha_atual += 1
        linha = self.comentario.sub('', linha)

        if linha == '\n':
            self.advance()
        else :
            self.linha_comando = linha.split() 

    def commandType(self):
        """Retorna o tipo de comando."""
        comandos_arit_log = {'add': 'C_ARITHMETIC', 'sub':'C_ARITHMETIC', 'neg': 'C_ARITHMETIC', 'eq':'C_ARITHMETIC', 'gt': 'C_ARITHMETIC', 'lt': 'C_ARITHMETIC', 'and': 'C_ARITHMETIC', 'or': 'C_ARITHMETIC', 'not': 'C_ARITHMETIC', 'pop': 'C_POP', 'push': 'C_PUSH'}
        comando = self.linha_comando[0]
        return(comandos_arit_log[comando]) 

    def arg1(self):
        """retorna o argumento 1 caso houver."""
        if self.commandType() != 'C_ARITHMETIC':
            return self.linha_comando[1]
        else: return None

    def arg2(self):
        """retorna o argumento 2 caso houver."""
        tipo_comando = self.commandType()
        if (tipo_comando == 'C_POP') or (tipo_comando == 'C_PUSH'):
            return int(self.linha_comando[2])
        else : return None
