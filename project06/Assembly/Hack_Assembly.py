#importações
from tkinter import *
import os.path
import L_Assembly

class Assembly():
    def __init__(self, janela):
        self.tela = janela
        self.tela.title("Hack Assembly.")
        
        #Atributos a serem modificados posteriormente.
        self.endereco = ''
        self.nome_arquivo = ''
        self.dados_arquivo = ''
        self.tabela_simbolos = ''
        self.linhas_binario = ''
        self.erro = False

        self.Empacota_tela()


    def Empacota_tela(self): 
        """Cria e empacota a primeira tela."""

        if self.erro: #Remove mensagem de erro.
            self.btn.grid_forget()
            self.msg.grid_forget()
            self.erro = False

        texto = r"""Insira o endereço onde se encontra o arquivo que deseja converter como no exemplo abaixo.
Ex: C:\Users\Usuario\Documents"""
        self.lbl = Label(self.tela, text=texto)
        self.entry = Entry(self.tela, width=50)
        self.btn = Button(self.tela, text= "Confirmar", width=20, command=self.Checa_diretorio)
        #Empacotamento
        self.lbl.grid(row=0, column=0, columnspan=2, ipadx=20)
        self.entry.grid(row=1, column=0, columnspan=2, pady=8)
        self.btn.grid(row=2, column=0, columnspan=2, pady=5)


    def Checa_diretorio(self): 
        """Verifica se o endereço passado é válido."""

        self.endereco = self.entry.get()

        if os.path.isdir(self.endereco):
            if self.erro: #Remove mensagem de erro.
                self.msg.destroy()
                self.erro = False
            self.tela_2()

        else: self.MSG("Endereço inválido!")


    def tela_2(self): 
        """Modifica a tela para a tela de obter o nome do arquivo."""

        self.lbl['text']= "Insira o nome do arquivo que deseja converter como no exemplo abaixo.\nEx: Add.asm"
        self.entry.delete(0,END)
        self.btn['text'] = 'Traduzir'
        self.btn['command'] = self.Checa_arquivo


    def Checa_arquivo(self): 
        """Verifica se o nome do arquivo passado é válido."""
        self.nome_arquivo = self.entry.get()

        arq = "{}\{}".format(self.endereco, self.nome_arquivo)
        if os.path.isfile(arq):
            if self.erro: #Remove mensagem de erro.
                self.msg.destroy()
                self.erro = False
            self.Desempacota_tela()
            self.Confirmando()
        
        else: self.MSG("Arquivo Inválido!")


    def Desempacota_tela(self): 
        """Desempacota a tela."""
        self.lbl.grid_forget()
        self.entry.grid_forget()
        self.btn.grid_forget()


    def MSG(self, texto): 
        """Exibe mensagem."""
        if not self.erro: #Exibi Uma mensagem por vez.
            self.erro = True
            self.msg = Label(self.tela, text=texto)
            self.msg.grid(column=0, columnspan=2, pady=10, padx=10)


    def Confirmando(self):
        """Confirma o arquivo a ser traduzido e inicializa tradução."""
        self.MSG("Traduzir o arquivo:\n\n{}\{}".format(self.endereco, self.nome_arquivo))
        self.btn['command'] = self.Traducao
        self.btn['text'] = 'Traduzir'
        self.btn.grid(column=0, columnspan=2)


    def Traducao(self):
        """Faz a tradução do arquivo."""
        self.dados_arquivo = self.Inicializa_Arquivo() # Contem um dicinário com: Nome, endereço e linhas do arquivo.
        self.tabela_simbolos = self.Inicializa_Tabela() # Contem os Simbolos pré definidos
        self.Primeira_leitura(arquivo=self.dados_arquivo['arquivo'], tabela=self.tabela_simbolos)
        self.linhas_binario = self.Segunda_leitura(arquivo=self.dados_arquivo['arquivo'], tabela=self.tabela_simbolos) # Contem as linhas do arquivo em linguagem hack.
        self.Escreve_arquivo(arquivo=self.linhas_binario,endereco=self.dados_arquivo['endereco'],nome=self.dados_arquivo['nome'])

        self.Concluido()


    def Inicializa_Arquivo(self):
        """Retorna um dicionário, que contém o Nome e Endereço do arquivo e as linhas em limguagem simbólica."""
        
        ex=[r'C:\Users\Documents\nand2tetris\projects\06\add', 'add.asm']
        end_arquivo = self.endereco 
        nome_arquivo = self.nome_arquivo 
        arq = open(end_arquivo+"\\"+nome_arquivo, "r", encoding='UTF-8')
        linhas_arq = arq.readlines()
        arq.close()

        return {'nome': nome_arquivo, 'endereco': end_arquivo, 'arquivo': linhas_arq}
    

    def Inicializa_Tabela(self):
        """Retorna um dicionário, que contém a tabela de simbolos pré definidos."""

        simbolos = {'pos': 16, 'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3,'R4': 4, 'R5': 5, 'R6': 6,\
        'R7': 7, 'R8': 8, 'R9': 9, 'R1O': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14,\
        'R15': 15, 'SCREEN': 16384, 'KBD': 24576, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
        
        return simbolos


    def Primeira_leitura(self, arquivo, tabela):
        """Adiciona os Labels e as variáveis na tabela de simbolos."""

        posf = 0 #Conta o indice das linhas de comando.
        for linha in arquivo:
            linha = linha.strip()

            if linha.startswith('('): # Labels
                tabela[linha[1:-1]] = posf

            elif linha.startswith('//') or len(linha) == 0: # Cometários e espaços em branco.
                continue

            elif (not linha.startswith('//')) and (len(linha) > 0): #Instruções
                posf +=1 # acrescenta no indice que o  label recebe 

        
        for linha in arquivo:
            linha = linha.strip()

            if (not linha.startswith('//')) and (len(linha) > 0) and (not linha.startswith('(')) and linha.startswith('@') and (not linha[1:].isdigit()) and (linha[1] != 'R'):# Variáveis
                if linha[1:] not in tabela:
                    post = tabela['pos']
                    tabela[linha[1:]] = post
                    tabela['pos'] = post+1


    def Segunda_leitura(self, arquivo, tabela):
        """Retorna uma lista, que contém as linhas do arquivo em linguagem Hack."""
        arquivo_meio = [] # Instuções em linguagem simbólica.
        arquivo_saida = [] # Instruções sem linguagem hack.

        for linha in arquivo:
        
            if '//' in linha:
                fim = linha.index('//')
                linha = linha[:fim] # Remove comentários que estão na mesma linha da instrução / transforma linha em '' se a linha for um comentário.  

            linha = linha.strip()

            if len(linha) != 0 : arquivo_meio.append(linha)
        

        for linha in arquivo_meio:

            if linha.startswith('@'): # Instrução A / Labels

                if linha[1:].isdigit(): # Ex: @21
                    arquivo_saida.append('0'+self.Instrucao_A(linha[1:]))

                elif linha[1].isalpha() and linha[2:].isdigit(): # Ex: @R21
                    arquivo_saida.append('0'+self.Instrucao_A(linha[2:]))
                
                else: # Ex: @variavel
                    arquivo_saida.append('0'+self.Instrucao_A(tabela[linha[1:]]))

            elif linha[0].isalnum(): # Ex: 0;JMP / D=M+D / M=M+D;JLE 
                arquivo_saida.append(self.Instrucao_C(linha, tabela))

        return arquivo_saida


    def Instrucao_A(self, instrucao):
        """Converte instrução A em linguagem hack."""

        binario = []
        instrucao = int(instrucao) # Instrução em Linguagem simbólica.

        if instrucao == 0: return '000000000000000'
        else:
            while True:
                binario.append(str(instrucao%2)) 
                instrucao = instrucao//2

                if instrucao == 0 : break    

        while len(binario) != 15:
            binario.append('0')

        binario.reverse()

        return ''.join(binario)


    def Instrucao_C(self, instrucao_c, tabela):
        """Converte instrução C em linguagem hack."""

        tabela_comp = {'0':{'a':'0', 'binario':'101010' }, '1':{'a':'0', 'binario':'111111' },\
        '-1':{'a':'0', 'binario':'111010'}, 'D':{'a':'0', 'binario': '001100'}, 'A':{'a':'0', 'binario':'110000'}, '!D':{'a':'0', 'binario':'001101'},\
        '!A':{'a':'0', 'binario':'110001'}, '-D':{'a':'0', 'binario':'001111'}, '-A':{'a':'0', 'binario':'110011'}, 'D+1':{'a':'0', 'binario':'011111'},\
        'A+1':{'a':'0', 'binario':'110111'}, 'D-1':{'a':'0', 'binario':'001110'}, 'A-1':{'a':'0', 'binario':'110010'}, 'D+A':{'a':'0', 'binario':'000010'},\
        'D-A':{'a':'0', 'binario':'010011'}, 'A-D':{'a':'0', 'binario':'000111'}, 'D&A':{'a':'0', 'binario':'000000'}, 'D|A':{'a':'0', 'binario':'010101'},\
        'M':{'a':'1', 'binario':'110000'}, '!M':{'a':'1', 'binario':'110001'}, '-M':{'a':'1', 'binario':'110011'}, 'M+1':{'a':'1', 'binario':'110111'},\
        'M-1':{'a':'1', 'binario':'110010'}, 'D+M':{'a':'1', 'binario':'000010'}, 'D-M':{'a':'1', 'binario':'010011'}, 'M-D':{'a':'1', 'binario':'000111'},\
        'D&M':{'a':'1', 'binario':'000000'}, 'D|M':{'a':'1', 'binario':'010101'}}
        tabela_dest = {'M':'001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111', 'null': '000'}
        tabela_jump = {'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111', 'null': '000'}
        
        dest = ''
        comp = ''
        jump = ''

        if ('=' in instrucao_c) and (';' in instrucao_c): # Ex: M=M+D;JLE
            fim_dest = instrucao_c.index('=')
            dest = instrucao_c[:fim_dest]
            
            fim_comp = instrucao_c.index(';')
            comp = instrucao_c[fim_dest+1:fim_comp]
            
            jump = instrucao_c[fim_comp+1:]
            
        elif ('=' in instrucao_c) and (';' not in instrucao_c): # M=D
            fim_dest = instrucao_c.index('=')
            dest = instrucao_c[:fim_dest]

            comp = instrucao_c[fim_dest+1:]

            jump = 'null'

        elif ('=' not in instrucao_c) and (';' in instrucao_c): # 0;JMP
            dest = 'null'

            fim_comp = instrucao_c.index(';')
            comp = instrucao_c[:fim_comp]

            jump = instrucao_c[fim_comp+1:]

        # 1 1 1 a c c c c c c d d d j j j 
        return '111'+tabela_comp[comp]['a']+tabela_comp[comp]['binario']+tabela_dest[dest]+tabela_jump[jump]


    def Escreve_arquivo(self, arquivo, endereco, nome):
        """Escreve o arquivo.hack"""
        
        arq_binario = open(endereco+'\\'+nome[:-3]+'hack', 'w')
        
        for linha in arquivo:
            arq_binario.write(linha+'\n')

        arq_binario.close()


    def Concluido(self): 
        """Exibe mensagem e retorna ao início."""
        self.msg['text'] = "Tradução concluída com sucesso!"
        self.btn['text']= 'Traduzir outro arquivo'
        self.btn['command'] = self.Empacota_tela
        self.btn.grid(column=0, columnspan=2)


        
if __name__ == '__main__':
    janela = Tk()
    Assembly(janela)
    janela.mainloop()
