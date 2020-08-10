import sys
from CompilationEngine import CompilationEngine
class JackTokenizer(CompilationEngine):
    
    def __init__(self, Nome_entrada):

        
    
        self.KEYWORDS = ['class','constructor','function',
            'method','field','static','var','int',
            'char','boolean','void','true','false',
            'null','this','let','do','if','else',
            'while','return']

        self.SYMBOL_CONVERSIONS = {'<': '&lt;','>': '&gt;','\"': '&quot;','&': '&amp;'}

        self.SYMBOLOS = ["{", "}", "(", ")", "[", "]", ".", ",",
        ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

        self.nome_arquivo_entrada = Nome_entrada

        self.arquivo_entrada = open(self.nome_arquivo_entrada, 'r', encoding="UTF-8")
        #self.arquivoT = open(self.nome_arquivo_entrada[:-5]+'T.xml', 'w', encoding='UTF-8')
        
        self.linhas = []
        self.tokens = []
        self.token_atual = ""

        self.handleSpace()
        self.separateTokens()
        #self.writeFile()

        #self.arquivo_entrada.close()
        #self.arquivoT.close()

        super().__init__(Nome_entrada[:-4]+'xml', self.tokens)


    def handleSpace(self):
        linhas = self.arquivo_entrada.readlines()

        cont = 0
        while cont < len(linhas):

            if '//' in linhas[cont] and (not linhas[cont].strip().startswith('/*')):
                if linhas[cont].startswith('//'):
                    cont += 1
                
                elif linhas[cont].count('//') > 1:
                    linha = linhas[cont][:linhas[cont].find('//')]
                    self.linhas.append(linha)
                    cont+= 1

                else:
                    linha = linhas[cont][:linhas[cont].find('//')]
                    self.linhas.append(linha)
                    cont+= 1

            elif '/*' in linhas[cont]:
                while not linhas[cont].strip().endswith('*/')  :
                    cont += 1
                cont+= 1

            elif linhas[cont] == '\n':
                cont+=1
            
            else:
                self.linhas.append(linhas[cont])
                cont+= 1

    def separateTokens(self):
        for linha in self.linhas:
            token = ""
            ind = 0
            st = True
            while len(linha) > ind:
                caractere = (linha[ind])
                
                if caractere in self.SYMBOLOS and st:
                    if caractere in self.SYMBOL_CONVERSIONS:
                        if len(token) > 0 : self.tokens.append(token)
                        self.tokens.append(self.SYMBOL_CONVERSIONS[caractere])
                        token = ""
                    else:
                        if len(token) > 0 : self.tokens.append(token)
                        self.tokens.append(caractere)
                        token = ""
                
                elif caractere.isspace()  and st:
                    if len(token) > 0 : self.tokens.append(token)
                    token = ""
                
                elif caractere == '"': 
                    st = not st
                    token += caractere

                else : 
                    token += caractere

                ind += 1


    def hasMoreTokens(self):
        if len(self.tokens) > 0 : return True
        else : return False

    def advance(self):
        if len(self.tokens) > 0:
            self.token_atual = self.tokens.pop(0)

    def tokenType(self):
        if self.token_atual in self.KEYWORDS:
            return 'KEYWORD'
        elif self.token_atual in self.SYMBOLOS or self.token_atual in self.SYMBOL_CONVERSIONS.values():
            return 'SYMBOL'
        elif self.token_atual.startswith('"'):
            return 'STRING_CONST'
        elif self.token_atual.isnumeric():
            return 'INT_CONST'
        else: 
            return 'IDENTIFIER' 
        
    def keyWord(self):
        if self.tokenType == 'KEYWORD':
            return self.token_atual.upper()

    def symbol(self):
        if self.tokenType == 'SYMBOL':
            return self.token_atual


    def identifier(self):
        if self.tokenType == 'IDENTIFIER':
            return self.token_atual

    def intVal(self):
        if self.tokenType == 'INT_CONST':
            return self.token_atual

    def stringVal(self):
        if self.tokenType == 'STRING_CONST':
            return self.token_atual[1:-1]


    """def writeFile(self):
        self.arquivoT.write('<tokens>\n')
        while self.hasMoreTokens():
            
            self.advance()
            tipo = self.tokenType()

            if tipo == 'SYMBOL':
                self.arquivoT.write(f'<symbol> {self.token_atual} </symbol>\n')
            elif tipo == 'KEYWORD':
                self.arquivoT.write(f'<keyword> {self.token_atual} </keyword>\n')
            elif tipo == 'STRING_CONST':
                self.arquivoT.write(f'<stringConstant> {self.token_atual[1:-1]} </stringConstant>\n')
            elif tipo == 'INT_CONST':
                self.arquivoT.write(f'<integerConstant> {self.token_atual} </integerConstant>\n')
            elif tipo == 'IDENTIFIER':
                self.arquivoT.write(f'<identifier> {self.token_atual} </identifier>\n')


        self.arquivoT.write('</tokens>')
        return f'escreveu {self.nome_arquivo_entrada}'"""
        

"""if __name__ == '__main__':
    if len(sys.argv) == 2:
        JackTokenizer(sys.argv[1]) 
    else:
        print('Use: JackTokenizer [NomeArquivo].jack')
"""
    
    