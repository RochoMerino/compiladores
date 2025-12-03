import ply.yacc as yacc
from .lexer import PatitoLexer
from .errors import SyntaxError as PatitoSyntaxError

class PatitoParser:    
    def __init__(self):
        self.lexer = PatitoLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False)
        self.errors = []
    
    def p_programa(self, p):
        '''programa : PROGRAM ID SEMICOLON vars funcs MAIN LPAREN RPAREN body END'''
        p[0] = ('program', p[2])
    
    def p_vars(self, p):
        '''vars : VAR var_decl_list
                | empty'''
        p[0] = p[2] if len(p) == 3 else []
    
    def p_var_decl_list(self, p):
        '''var_decl_list : var_decl var_decl_list
                         | var_decl'''
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]
    
    def p_var_decl(self, p):
        '''var_decl : id_list COLON type SEMICOLON'''
        p[0] = ('var_decl', p[1], p[3])
    
    def p_id_list(self, p):
        '''id_list : ID COMMA id_list
                   | ID'''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]
    
    def p_type(self, p):
        '''type : INT
                | FLOAT'''
        p[0] = p[1]
    
    def p_funcs(self, p):
        '''funcs : func funcs
                 | empty'''
        if len(p) == 3 and p[1]:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = []
    
    def p_func(self, p):
        '''func : VOID ID LPAREN params RPAREN LBRACKET vars body RBRACKET SEMICOLON'''
        p[0] = ('function', p[2], p[4])
    
    def p_params(self, p):
        '''params : param_list
                  | empty'''
        p[0] = p[1] if p[1] else []
    
    def p_param_list(self, p):
        '''param_list : ID COLON type COMMA param_list
                      | ID COLON type'''
        if len(p) == 6:
            p[0] = [(p[1], p[3])] + p[5]
        else:
            p[0] = [(p[1], p[3])]
    
    def p_body(self, p):
        '''body : LBRACE statement_list RBRACE'''
        p[0] = ('body', p[2])
    
    def p_statement_list(self, p):
        '''statement_list : statement statement_list
                          | empty'''
        if len(p) == 3 and p[1]:
            p[0] = [p[1]] + (p[2] if p[2] else [])
        else:
            p[0] = []
    
    def p_statement(self, p):
        '''statement : assign
                     | condition
                     | cycle
                     | f_call
                     | print'''
        p[0] = p[1]
    
    def p_assign(self, p):
        '''assign : ID EQ expression SEMICOLON'''
        p[0] = ('assign', p[1], p[3])
    
    def p_condition(self, p):
        '''condition : IF LPAREN expression RPAREN body ELSE body SEMICOLON
                     | IF LPAREN expression RPAREN body SEMICOLON'''
        if len(p) == 9:
            p[0] = ('if', p[3], p[5], p[7])
        else:
            p[0] = ('if', p[3], p[5])
    
    def p_cycle(self, p):
        '''cycle : WHILE LPAREN expression RPAREN DO body SEMICOLON'''
        p[0] = ('while', p[3], p[6])
    
    def p_print(self, p):
        '''print : PRINT LPAREN print_list RPAREN SEMICOLON'''
        p[0] = ('print', p[3])
    
    def p_print_list(self, p):
        '''print_list : print_item COMMA print_list
                      | print_item'''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]
    
    def p_print_item(self, p):
        '''print_item : expression
                      | CTE_STRING'''
        p[0] = p[1]
    
    def p_expression(self, p):
        '''expression : exp
                      | exp GT exp
                      | exp LT exp
                      | exp NEQ exp'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[1], p[3])
    
    def p_exp(self, p):
        '''exp : termino
               | exp PLUS termino
               | exp MINUS termino'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[1], p[3])
    
    def p_termino(self, p):
        '''termino : factor
                   | termino MULT factor
                   | termino DIV factor'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[2], p[1], p[3])
    
    def p_factor(self, p):
        '''factor : LPAREN expression RPAREN
                  | PLUS factor
                  | MINUS factor
                  | cte
                  | ID'''
        if len(p) == 4:
            p[0] = p[2]
        elif len(p) == 3:
            if p[1] == '-':
                p[0] = ('unary', p[1], p[2])
            else:
                p[0] = p[2] 
        else:
            p[0] = p[1]
    
    def p_cte(self, p):
        '''cte : CTE_INT
               | CTE_FLOAT'''
        p[0] = p[1]
    
    def p_f_call(self, p):
        '''f_call : ID LPAREN expression_list RPAREN SEMICOLON
                  | ID LPAREN RPAREN SEMICOLON'''
        if len(p) == 6:
            p[0] = ('call', p[1], p[3])
        else:
            p[0] = ('call', p[1], [])
    
    def p_expression_list(self, p):
        '''expression_list : expression COMMA expression_list
                           | expression'''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]
    
    def p_empty(self, p):
        '''empty :'''
        pass
    
    def p_error(self, p):
        if p:
            error_msg = f"Unexpected token '{p.value}'"
            self.errors.append(error_msg)
            raise PatitoSyntaxError(error_msg, line=p.lineno, token=p.value)
        else:
            error_msg = "Unexpected end of input"
            self.errors.append(error_msg)
            raise PatitoSyntaxError(error_msg)
    
    def parse(self, data):
        self.errors = []
        try:
            result = self.parser.parse(data, lexer=self.lexer.lexer)
            return result
        except Exception as e:
            raise

def build_parser():
    return PatitoParser()

