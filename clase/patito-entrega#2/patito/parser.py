import ply.yacc as yacc
from patito.lexer import PatitoLexer
from patito.errors import SyntaxError as PatitoSyntaxError
from patito.semantic_analyzer import SemanticAnalyzer


class PatitoParser:
    def __init__(self):
        self.lexer = PatitoLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False)
        self.errors = []
        self.semantic = SemanticAnalyzer()

    def p_programa(self, p):
        '''programa : PROGRAM ID SEMICOLON vars funcs MAIN LPAREN RPAREN body END'''
        self.semantic.set_program_name(p[2], p.lineno(2))
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
        var_type = p[3]
        id_list = p[1]

        for var_name in id_list:
            self.semantic.declare_variable(var_name, var_type, p.lineno(2))

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

    def p_func_start(self, p):
        '''func_start : VOID ID LPAREN'''
        func_name = p[2]
        self.semantic.declare_function(func_name, 'void', p.lineno(2))
        self.semantic.enter_function(func_name)
        p[0] = func_name

    def p_func_with_start(self, p):
        '''func : func_start params RPAREN LBRACKET vars body RBRACKET SEMICOLON'''
        self.semantic.exit_function()
        p[0] = ('function', p[1], p[2])

    def p_params(self, p):
        '''params : param_list
                  | empty'''
        p[0] = p[1] if p[1] else []

    def p_param_list(self, p):
        '''param_list : ID COLON type COMMA param_list
                      | ID COLON type'''
        param_name = p[1]
        param_type = p[3]

        self.semantic.add_parameter(param_name, param_type, p.lineno(1))

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
        var_name = p[1]
        expr_info = p[3]
        expr_type = self._get_expr_type(expr_info)
        self.semantic.check_assignment(var_name, expr_type, p.lineno(1))
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
            left_type = self._get_expr_type(p[1])
            right_type = self._get_expr_type(p[3])
            operator = p[2]
            result_type = self.semantic.check_operation(left_type, operator, right_type, p.lineno(2))
            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

    def p_exp(self, p):
        '''exp : termino
               | exp PLUS termino
               | exp MINUS termino'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            left_type = self._get_expr_type(p[1])
            right_type = self._get_expr_type(p[3])
            operator = p[2]
            result_type = self.semantic.check_operation(left_type, operator, right_type, p.lineno(2))
            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

    def p_termino(self, p):
        '''termino : factor
                   | termino MULT factor
                   | termino DIV factor'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            left_type = self._get_expr_type(p[1])
            right_type = self._get_expr_type(p[3])
            operator = p[2]
            result_type = self.semantic.check_operation(left_type, operator, right_type, p.lineno(2))
            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

    def p_factor(self, p):
        '''factor : LPAREN expression RPAREN
                  | PLUS factor
                  | MINUS factor
                  | cte
                  | ID'''
        if len(p) == 4:
            p[0] = p[2]
        elif len(p) == 3:
            factor_type = self._get_expr_type(p[2])
            if p[1] == '-':
                p[0] = ('type_info', factor_type, ('unary', p[1], p[2]))
            else:
                p[0] = p[2]
        else:
            if isinstance(p[1], str) and not p[1].replace('.', '').replace('-', '').replace('+', '').isdigit():
                var_type = self.semantic.lookup_variable(p[1], p.lineno(1))
                p[0] = ('type_info', var_type, ('id', p[1]))
            else:
                p[0] = p[1]

    def p_cte(self, p):
        '''cte : CTE_INT
               | CTE_FLOAT'''
        value = p[1]
        if '.' in str(value):
            const_type = 'float'
        else:
            const_type = 'int'

        p[0] = ('type_info', const_type, ('const', value))

    def p_f_call(self, p):
        '''f_call : ID LPAREN expression_list RPAREN SEMICOLON
                  | ID LPAREN RPAREN SEMICOLON'''
        func_name = p[1]

        if len(p) == 6:
            arg_expressions = p[3]
            arg_types = [self._get_expr_type(expr) for expr in arg_expressions]
        else:
            arg_types = []

        self.semantic.validate_function_call(func_name, arg_types, p.lineno(1))

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

    def _get_expr_type(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'type_info':
                return expr[1]
            elif len(expr) == 3:
                return 'int'

        if isinstance(expr, str):
            if '.' in expr:
                return 'float'
            else:
                return 'int'

        return 'int'

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
        self.semantic.reset()

        try:
            result = self.parser.parse(data, lexer=self.lexer.lexer)
            return result
        except Exception as e:
            raise

    def print_semantic_info(self):
        self.semantic.print_semantic_info()


def build_parser():
    return PatitoParser()
