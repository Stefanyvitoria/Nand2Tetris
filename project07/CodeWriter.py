import Constantes

class codewriter():
    def __init__(self, nome_saida):
        self.codigo = Constantes.CODIGO
        self.tabela_simbolos = Constantes.TABELA_SIMBOLOS

        self.nome_saida = nome_saida
        self.arquivo_saida = open(self.nome_saida, 'a', encoding='UTF-8')


    def writeArithmetic(self, comando, ind):
        """Escreve os comandos aritméticos no arquivo de saída."""

        if comando in ['eq','lt','gt']:
            code = self.codigo[comando].format(ind, ind, ind, ind)
        else:
            code= self.codigo[comando]
        self.arquivo_saida.write(code)


    def writePushPop(self, comando, segmento, indice):
        """Escreve os comandos POP/PUSH no arquivo de saída."""

        if comando == 'push':
            if segmento in ['local', 'argument', 'this', 'that']:
                code = self.codigo['push_basico'].format(segmento, indice, indice, self.tabela_simbolos[segmento])
                self.arquivo_saida.write(code)
        
            elif segmento == 'constant':
                code = self.codigo['push_const'].format(indice, indice)
                self.arquivo_saida.write(code)

            elif segmento == 'static':
                code = self.codigo['push_static'].format(indice, indice)
                self.arquivo_saida.write(code)
            
            elif segmento == 'temp':
                code = self.codigo['push_temp'].format(indice, indice)
                self.arquivo_saida.write(code)

            elif segmento == 'pointer':
                code = self.codigo['push_pointer'].format(indice, self.tabela_simbolos[str(indice)])
                self.arquivo_saida.write(code)


        elif comando == 'pop':
            if segmento in ['local', 'argument', 'this', 'that']:
                code = self.codigo['pop_basico'].format(segmento, indice, indice, self.tabela_simbolos[segmento])
                self.arquivo_saida.write(code)

            elif segmento == 'static':
                code = self.codigo['pop_static'].format(indice, indice)
                self.arquivo_saida.write(code)

            elif segmento == 'temp':
                code = self.codigo['pop_temp'].format(indice, indice)
                self.arquivo_saida.write(code)

            elif segmento == 'pointer':
                code = self.codigo['pop_pointer'].format(indice, self.tabela_simbolos[str(indice)])
                self.arquivo_saida.write(code)


    def close(self):
        """Fecha o arquivo de saída."""
        self.arquivo_saida.close()