import ply.lex as lex

class PatitoLexer:
    reserved = {
        'program': 'PROGRAM',
        'var': 'VAR',
        'int': 'INT',
        'float': 'FLOAT',
        'void': 'VOID',
        'main': 'MAIN',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'do': 'DO',
        'print': 'PRINT',
        'end': 'END',
    }
    
    tokens = [
        'ID',
        'CTE_INT',
        'CTE_FLOAT',
        'CTE_STRING', 
        'PLUS',
        'MINUS',
        'MULT',
        'DIV',
        'GT',
        'LT',
        'NEQ',
        'EQ', 
        'LPAREN', 
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET', 
        'RBRACKET', 
        'COMMA', 
        'SEMICOLON', 
        'COLON',  
    ] + list(reserved.values())
    
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_GT = r'>'
    t_LT = r'<'
    t_NEQ = r'!='
    t_EQ = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_COLON = r':'
    
    t_ignore = ' \t'
    
    def t_CTE_STRING(self, t):
        r'"(?:\\.|[^"\\])*"'
        raw = t.value[1:-1]
        t.value = bytes(raw, 'utf-8').decode('unicode_escape')
        return t
    
    def t_CTE_FLOAT(self, t):
        r'[+-]?\d+\.\d+'
        t.value = float(t.value)
        return t
    
    def t_CTE_INT(self, t):
        r'[+-]?\d+'
        t.value = int(t.value)
        return t
    
    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t
    
    def t_COMMENT_LINE(self, t):
        r'//[^\n]*'
        pass 
    
    def t_COMMENT_BLOCK(self, t):
        r'/\*([^*]|\*+[^*/])*\*+/'
        t.lexer.lineno += t.value.count('\n')
        pass  
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
    
    def tokenize(self, data):
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens

def build_lexer():
    lexer = PatitoLexer()
    return lexer.build()