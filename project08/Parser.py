import os
import re
from CodeWriter import *

class parser(codewriter):
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.nome_arquivo_saida = nome_arquivo[:-3] if (nome_arquivo.endswith('.vm')) else nome_arquivo+'/'+nome_arquivo    #Determina o nome do arquivo asm.
        self.arquivo = self.Trata_Arquivos(nome_arquivo)  #lista de comando do arquivo VM.

        self.linha_comando = ''
        self.linha_atual = 0
        self.comentario = re.compile(r'//.*$')
        
    
    def Trata_Arquivos(self,nome_arquivo):
        """Obtem o código VM do arquivo ou do diretório."""

        super().__init__(self.nome_arquivo_saida) #inicia construtor da classe codewriter.

        comandos = [] #Variável a ser retornada com os comandos.

        if nome_arquivo.endswith('.vm'):
            arq = open(file=nome_arquivo, mode='r')
            comandos = arq.readlines()
            arq.close()
            return comandos

        else:
            self.writeInit() #Escreve o código Bootstrap.

            for arquivovm in os.listdir(nome_arquivo):
                if arquivovm.endswith('.vm'):
                    arq = open(nome_arquivo + '/'+arquivovm, 'r')
                    linhas = arq.readlines()
                    self.nome_arquivosVM.append(arquivovm[:-3]) #Guarda o nome para ser usado na escrita de labels.
                    arq.close()
                    comandos.extend(linhas)
                    comandos.append('fim') #Marca o fim dos comandos de um arquivo.
            
            self.nome_arquivo_saida = nome_arquivo
            comandos.pop() #retira o ultimo 'fim'.
            
            return comandos


    def hasMoreCommands(self):
        """Retorna False quando chegar ao fim do arquivo, enquanto não, retorna True."""
        if (self.linha_atual+1) <= len(self.arquivo): return True
        else : return False

    def advance(self):
        """Obtem o próximo comando do arquivo e armazena em 'self.linha_comando'."""
        linha = self.arquivo[self.linha_atual]
        self.linha_atual += 1
        linha = self.comentario.sub('', linha)

        if linha == '\n': #Ignora linhas em branco
            self.advance()

        elif linha == 'fim': 
            self.nome_arquivosVM.pop(0) #retira o nome do arquivo da lista que auxilia na escrita de labels.
            self.advance() 

        else :
            if '//' in linha:
                linha = linha.split('//')[0].strip() #Retira comentarios na linha com comandos.
            self.linha_comando = linha.split() #Guarda o comando.

    def commandType(self):
        """Retorna o tipo de comando."""

        Tipos = {'add': 'C_ARITHMETIC', 'sub':'C_ARITHMETIC', 'neg': 'C_ARITHMETIC', 'eq':'C_ARITHMETIC',
        'gt': 'C_ARITHMETIC', 'lt': 'C_ARITHMETIC', 'and': 'C_ARITHMETIC', 'or': 'C_ARITHMETIC',
        'not': 'C_ARITHMETIC', 'pop': 'C_POP', 'push': 'C_PUSH', 'label' : 'C_LABEL', 'goto': 'C_GOTO', 'if-goto': 'C_IFGOTO',
        'function' : 'C_FUNCTION', 'call' : 'C_CALL', 'return' : 'C_RETURN'}
        comando = self.linha_comando[0]

        return(Tipos[comando]) 

    def arg1(self):
        """retorna o argumento 1 caso houver."""
        if self.commandType() not in  ['C_ARITHMETIC', 'C_RETURN']:
            return self.linha_comando[1]
        else: return None

    def arg2(self):
        """retorna o argumento 2 caso houver."""
        if self.commandType() in ['C_POP', 'C_PUSH', 'C_FUNCTION', 'C_CALL']:
            return int(self.linha_comando[2])
        else : return None
