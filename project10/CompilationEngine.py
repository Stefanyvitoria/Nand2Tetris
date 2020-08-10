

class CompilationEngine():

    def __init__(self, nome_arquivoXML, Lista_tokens):
        self.nome_arquivoXML = nome_arquivoXML
        self.lista_tokens = Lista_tokens
        self.identacao = ''
        self.rotinas_abertas = []

        self.arquivo_xml = open(self.nome_arquivoXML, 'w', encoding='UTF-8')

        print(self.tokens)

        self.CompileClass()

        self.arquivo_xml.close()
        self.arquivo_entrada.close()
        

    def CompileClass(self):
        
        self.writeTag('class') 
        self.identacao+='  '

        while self.hasMoreTokens(): 
            self.advance() 

            if self.token_atual == 'class': 
                self.writeTokens(self.token_atual)
                self.advance()

                if self.tokenType() == 'IDENTIFIER': 
                    self.writeTokens(self.token_atual)
                    self.advance()

                    if self.token_atual == '{': 
                        self.writeTokens(self.token_atual)
                        self.advance()

                        self.CompileClassVarDec()
                        

                        self.CompileSubroutineDec()
                                                

        if self.token_atual == '}':
            self.writeTokens(self.token_atual)

            self.identacao = self.identacao[:-2]
            self.writeTag(self.rotinas_abertas[-1])
            print('fim')


    def CompileClassVarDec(self):

        while self.token_atual in ['static', 'field']:
            vazio = False
            while True:
                self.writeTag('classVarDec')
                self.identacao+='  '

                self.writeTokens(self.token_atual) 
                self.advance()

                if (self.token_atual in ['int', 'char','boolean']) or (self.tokenType() == 'IDENTIFIER'): #tipo da variável
                    self.writeTokens(self.token_atual)
                    self.advance()

                    while self.token_atual != ';':
                        self.writeTokens(self.token_atual)
                        self.advance()

                    self.writeTokens(self.token_atual)
                    self.advance()

                    self.identacao = self.identacao[:-2]
                    self.writeTag(self.rotinas_abertas[-1])
                    break
                    

    def CompileSubroutineDec(self):

        while self.token_atual in ['constructor','function','method']:
            vazio = False

            self.writeTag('subroutineDec')
            self.identacao += '  '

            self.writeTokens(self.token_atual)
            self.advance()

            if (self.token_atual in ['void', 'int', 'char','boolean']) or (self.tokenType() == 'IDENTIFIER'):
                self.writeTokens(self.token_atual)
                self.advance()
              
                if self.tokenType() == 'IDENTIFIER':
                    self.writeTokens(self.token_atual)
                    self.advance()

                    if self.token_atual == '(':
                        self.writeTokens(self.token_atual)
                        self.advance()

                        self.CompileParameterList() 
                        

                        self.CompileSubroutineBody()

            self.identacao = self.identacao[:-2]
            self.writeTag(self.rotinas_abertas[-1])
          

    def CompileParameterList(self):
        self.writeTag('parameterList')
        self.identacao += '  ' 

        while self.token_atual != ')':
                self.writeTokens(self.token_atual)
                self.advance()

        if self.token_atual == ')':
            self.identacao = self.identacao[:-2]
            self.writeTag(self.rotinas_abertas[-1])
            
            self.writeTokens(self.token_atual)
            self.advance()
        

    def CompileSubroutineBody(self):
        #SubroutineBody
        if self.token_atual == '{':
            self.writeTag('subroutineBody')
            self.identacao += '  '

            self.writeTokens(self.token_atual)
            self.advance()

            self.CompileVarDec()

            self.CompileStatements()

            self.identacao = self.identacao[:-2]
            self.writeTag(self.rotinas_abertas[-1])
            

    def CompileVarDec(self):
        while self.token_atual == 'var':
                self.writeTag('varDec')
                self.identacao += '  '

                while self.token_atual != ';':
                    self.writeTokens(self.token_atual)
                    self.advance()
                   
                self.writeTokens(self.token_atual)
                self.advance()

                self.identacao = self.identacao[:-2]
                self.writeTag(self.rotinas_abertas[-1])
            

    def CompileStatements(self):
        self.writeTag('statements')
        self.identacao += '  '  

        while self.token_atual in ['let','do','if','while','return']:
                        
            if self.token_atual == 'let':
                self.CompileLet()
                
            elif self.token_atual == 'if':
                self.CompileIf()

            elif self.token_atual == 'while':
                self.CompileWhile()

            elif self.token_atual == 'do':
                self.CompileDo()

            elif self.token_atual == 'return':
                self.CompileReturn()
            
        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])

        self.writeTokens(self.token_atual)
        self.advance()


    def CompileLet(self):
        self.writeTag('letStatement')
        self.identacao += '  '

        self.writeTokens(self.token_atual) 
        self.advance()

        if self.tokenType() == 'IDENTIFIER':
            self.writeTokens(self.token_atual) 
            self.advance()

        while self.token_atual != ';': 

            if self.token_atual == '=': 
                self.writeTokens(self.token_atual)
                self.advance()

                self.CompileExpression() 
            
            elif self.token_atual == '[':
                self.writeTokens(self.token_atual)
                self.advance()

                self.CompileExpression()

                self.writeTokens(self.token_atual)
                self.advance()
            
        self.writeTokens(self.token_atual) 
        self.advance() 

        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])


    def CompileIf(self):
        self.writeTag('ifStatement')
        self.identacao += '  '
        
        self.writeTokens(self.token_atual)
        self.advance()

        if self.token_atual == '(':
            self.writeTokens(self.token_atual)
            self.advance()

            self.CompileExpression()

            self.writeTokens(self.token_atual)
            self.advance()
            
            if self.token_atual == '{':
                self.writeTokens(self.token_atual)
                self.advance()
                
                self.CompileStatements()

                if self.token_atual == 'else':
                    self.writeTokens(self.token_atual)
                    self.advance()

                    self.writeTokens(self.token_atual)
                    self.advance()

                    self.CompileStatements()
                
        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])


    def CompileWhile(self):
        self.writeTag('whileStatement')
        self.identacao += '  '

        self.writeTokens(self.token_atual)
        self.advance()

        if self.token_atual == '(':
            self.writeTokens(self.token_atual)
            self.advance()

            self.CompileExpression()

            self.writeTokens(self.token_atual)
            self.advance()
            
            if self.token_atual == '{':
                self.writeTokens(self.token_atual)
                self.advance()
                
                self.CompileStatements()

        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])


    def CompileDo(self):
        self.writeTag('doStatement')
        self.identacao += '  '

        self.writeTokens(self.token_atual)
        self.advance()

        #SubroutineCall
        if self.tokenType() == 'IDENTIFIER':
            self.writeTokens(self.token_atual)
            self.advance()

            if self.token_atual == '(':
                    self.writeTokens(self.token_atual)
                    self.advance()
                    self.CompileExpressionList()#Expression list
                    
                
            elif self.token_atual == '.':
                self.writeTokens(self.token_atual)
                self.advance()

                self.writeTokens(self.token_atual)
                self.advance()

                if self.token_atual == '(':
                    self.writeTokens(self.token_atual)
                    self.advance()

                    self.CompileExpressionList() 

        self.writeTokens(self.token_atual)
        self.advance()

        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])


    def CompileReturn(self):
        self.writeTag('returnStatement')
        self.identacao += '  '

        self.writeTokens(self.token_atual)
        self.advance()

        self.CompileExpression()

        self.writeTokens(self.token_atual)
        self.advance()

        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])



    def CompileExpression(self):
        if self.token_atual != ';':
            self.writeTag('expression')
            self.identacao += '  '

            op = ['+','-','/','*','|','&gt;','&lt;','=','&amp;']
            tem_termo = True
            
            while tem_termo:
                tem_termo = self.CompileTerm()
                
                if self.token_atual in op:
                    
                    self.writeTokens(self.token_atual)
                    self.advance()

                    tem_termo = True

            self.identacao = self.identacao[:-2]
            self.writeTag(self.rotinas_abertas[-1])
        

    def CompileTerm(self):
        
        self.writeTag('term')
        self.identacao += '  '

        condicao1 = self.tokenType() in ['IDENTIFIER', 'INT_CONST', 'STRING_CONST']
        condicao2 = self.token_atual in ['(','-','~','true', 'false', 'null', 'this']

        if condicao1 or condicao2:

            if self.tokenType() == 'IDENTIFIER':
                self.writeTokens(self.token_atual)
                self.advance()

                if self.token_atual == '[':
                    self.writeTokens(self.token_atual)
                    self.advance()
                    
                    self.CompileExpression()

                    self.writeTokens(self.token_atual) 
                    self.advance()
                
                elif self.token_atual == '(':
                    self.writeTokens(self.token_atual)
                    self.advance()
                    self.CompileExpressionList()
                    
                
                elif self.token_atual == '.':
                    self.writeTokens(self.token_atual)
                    self.advance()

                    self.writeTokens(self.token_atual)
                    self.advance()

                    if self.token_atual == '(':
                        self.writeTokens(self.token_atual)
                        self.advance()

                        self.CompileExpressionList()

            
            elif self.token_atual in ['true', 'false', 'null', 'this']:
                self.writeTokens(self.token_atual)
                self.advance()
            
            elif self.tokenType() in ['INT_CONST', 'STRING_CONST']:
                self.writeTokens(self.token_atual)
                self.advance()
            
            elif self.token_atual == '(':
                self.writeTokens(self.token_atual)
                self.advance()
                
                self.CompileExpression()

                self.writeTokens(self.token_atual)
                self.advance()
            
            elif self.token_atual in ['-', '~']:
                self.writeTokens(self.token_atual)
                self.advance()

                self.CompileTerm()

        self.identacao= self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])
        return False


    def CompileExpressionList(self):
        self.writeTag('expressionList')
        self.identacao += '  '
        while self.token_atual != ')':
            
            if self.token_atual == ',':
                self.writeTokens(self.token_atual)
                self.advance()
            
            self.CompileExpression()

        self.identacao = self.identacao[:-2]
        self.writeTag(self.rotinas_abertas[-1])
    
        self.writeTokens(self.token_atual)
        self.advance()

    def writeTag(self, tag):
        self.arquivo_xml.write(f'{self.identacao}<{tag}>\n')

        if len(self.rotinas_abertas) > 0 and tag == self.rotinas_abertas[-1]:
            self.rotinas_abertas.pop(-1)
        else: 
            self.rotinas_abertas.append(f'/{tag}')

    def writeTokens(self, token):
        tipo = self.tokenType().lower()

        if tipo == 'int_const': tipo = 'integerConstant'
        elif tipo == 'string_const': 
            tipo = 'stringConstant'
            token = token[1:-1]
        
        self.arquivo_xml.write('{}<{}> {} <{}>\n'.format(self.identacao,tipo, token, '/'+tipo))
