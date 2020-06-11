import CONSTANTES 

class codewriter():
    def __init__(self, nome_saida):
        self.tabela_simbolos = CONSTANTES.TABELA_SIMBOLOS 
        self.nome_saida = nome_saida       #Nome do arquivo asm.
        self.arquivo_final = open(self.nome_saida + '.asm', 'a', encoding='UTF-8') 

        self.nome_arquivosVM = [] #Lista a ser preenchida pela classe filha, terá o(s) nome(s) do arquivo que os comandos pertencem, servirá na escrita de labels personalizadas.


    def writeArithmetic(self, comando, ind):
        """Escreve os comandos aritméticos no arquivo de saída."""
        comando = comando.upper()
        if comando == 'EQ':
            code = CONSTANTES.EQ.format(ind, ind, ind, ind)

        elif comando == 'LT':
            code = CONSTANTES.LT.format(ind, ind, ind, ind)
        
        elif comando == 'GT':
            code = CONSTANTES.GT.format(ind, ind, ind, ind)

        elif comando == 'ADD':
            code = CONSTANTES.ADD

        elif comando == 'SUB':
            code = CONSTANTES.SUB

        elif comando == 'NEG':
            code = CONSTANTES.NEG

        elif comando == 'AND':
            code = CONSTANTES.AND

        elif comando == 'OR':
            code = CONSTANTES.OR

        else:
            code = CONSTANTES.NOT

        self.arquivo_final.write(code)


    def writePushPop(self, comando, segmento, indice):
        """Escreve os comandos POP/PUSH no arquivo de saída."""

        if comando == 'push':
            if segmento in ['local', 'argument', 'this', 'that']:
                code = CONSTANTES.PUSH['basico'].format(indice, self.tabela_simbolos[segmento])
                self.arquivo_final.write(code)
        
            elif segmento == 'constant':
                code = CONSTANTES.PUSH[segmento].format(indice, indice)
                self.arquivo_final.write(code)

            elif segmento == 'static':
                if '/' in self.nome_saida:
                    nome_saida = self.nome_arquivosVM[0]
                else:
                    nome_saida = self.nome_saida
                code = CONSTANTES.PUSH[segmento].format(nome_saida, indice)
                self.arquivo_final.write(code)
            
            elif segmento == 'temp':
                code = CONSTANTES.PUSH[segmento].format(indice, indice)
                self.arquivo_final.write(code)

            elif segmento == 'pointer':
                code = CONSTANTES.PUSH[segmento].format(self.tabela_simbolos[str(indice)])
                self.arquivo_final.write(code)


        elif comando == 'pop':
            if segmento in ['local', 'argument', 'this', 'that']:
                code = CONSTANTES.POP['basico'].format(indice, self.tabela_simbolos[segmento])
                self.arquivo_final.write(code)

            elif segmento == 'static':
                if '/' in self.nome_saida:
                    nome_saida = self.nome_arquivosVM[0]
                else:
                    nome_saida = self.nome_saida
                code = CONSTANTES.POP[segmento].format(nome_saida, indice)
                self.arquivo_final.write(code)

            elif segmento == 'temp':
                code = CONSTANTES.POP[segmento].format(indice)
                self.arquivo_final.write(code)

            elif segmento == 'pointer':
                code = CONSTANTES.POP[segmento].format(self.tabela_simbolos[str(indice)])
                self.arquivo_final.write(code)

    def writeInit(self):
        """Escreve o código Bootstrap no arquivo de saída."""
        code = CONSTANTES.BOOTSTRAP
        self.arquivo_final.write(code)

    def writeLabel(self, nome_label, f_lista):
        """Escreve os comandos Labels no arquivo de saída."""
        if len(f_lista) > 0:
            code = CONSTANTES.LABEL.format(f_lista[-1]+'$'+nome_label)
        else:
            code = CONSTANTES.LABEL.format(nome_label)
        self.arquivo_final.write(code)

    def writeIf(self, nome_label, f_lista):
        """Escreve os comando IF_GOTO no arquivo de saída."""
        if len(f_lista) > 0:
            code = CONSTANTES.IFGOTO.format(f_lista[-1]+'$'+nome_label) 
        else:
            code = CONSTANTES.IFGOTO.format(nome_label)
        self.arquivo_final.write(code) 

    def writeGoto(self,nome_label, f_lista):
        """Escreve os comando GOTO no arquivo de saída."""
        if len(f_lista) > 0:
            code = CONSTANTES.GOTO.format(f_lista[-1]+'$'+nome_label) 
        else:
            code = CONSTANTES.GOTO.format(nome_label)
        self.arquivo_final.write(code) 
    

    def writeFunction(self, nome_funcao, n_var):
        """Escreve os comando de FUNÇõES no arquivo de saída."""
        self.arquivo_final.write(CONSTANTES.FUNCTION['parte1'].format(nome_funcao))
        code = CONSTANTES.FUNCTION['parte2']
        for _ in range(n_var):
            self.arquivo_final.write(code)


    def writeCall(self,nome_funcao, n_arg, ind_funcao):
        """Escreve os comando de chamada no arquivo de saída."""
        code = CONSTANTES.CALL.format(nome_funcao,ind_funcao,str(5+n_arg),nome_funcao, nome_funcao,ind_funcao)
        self.arquivo_final.write(code)

    def writeReturn(self):
        """Escreve os comandos de retorno no arquivo de saída."""
        code = CONSTANTES.RETURN
        self.arquivo_final.write(code)

    def close(self):
        """Fecha o arquivo de saída."""
        self.arquivo_final.close()
