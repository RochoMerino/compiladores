'''
PatitoParser es el analizador sintactico

toma los tokens que dejo el lexer y verifica que sigan las reglas gramaticales del lenguaje
en el orden correcto

aqui es donde sucede la magia de la generacion de cuadruplos. PatitoParser tiene "puntos neuralgicos"
cuando detecta una operacion completa (a+b) llama a las rutinas para generar los cuadruplos inmediatamente

PatitoParser cordina a todos los demas componentes 
'''


import ply.yacc as yacc
from lexer import PatitoLexer

from semantic_analyzer import SemanticAnalyzer
from quadruple_generator import QuadrupleGenerator
from temp_manager import TempManager




class PatitoParser:
    def __init__(self):
        self.lexer = PatitoLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False)
        self.errors = []
        self.semantic = SemanticAnalyzer()

        # Quadruple generation components
        self.quad_gen = QuadrupleGenerator()
        self.temp_mgr = TempManager()
        self.operand_stack = []
        # self.operator_stack removed as it was unused
        self.type_stack = []
        self.jump_stack = [] # Using a simple list as stack

    def p_programa(self, p):
        '''programa : PROGRAM ID SEMICOLON program_start vars funcs MAIN LPAREN RPAREN main_start body END'''
        self.semantic.set_program_name(p[2], p.lineno(2))
        p[0] = ('program', p[2])

    def p_program_start(self, p):
        '''program_start :'''
        # Generate GOTO main (pending)
        self.main_jump = self.quad_gen.generate('GOTO', None, None, None)

    def p_main_start(self, p):
        '''main_start :'''
        # Fill GOTO main
        self.quad_gen.fill_quad(self.main_jump, self.quad_gen.get_next_address())

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
        '''func_start : VOID ID LPAREN
                      | type ID LPAREN'''
        func_type = p[1]
        func_name = p[2]
        self.semantic.declare_function(func_name, func_type, p.lineno(2))
        # enter_function is now called inside declare_function (or should be?)
        # Wait, I removed enter_function in semantic analyzer and moved logic to declare_function.
        # But I need to check if I removed it from parser call.
        # In my previous edit to semantic analyzer, I merged them.
        # So I don't need to call enter_function here.
        p[0] = func_name

    def p_func_with_start(self, p):
        '''func : func_start params RPAREN LBRACKET vars func_code_start body RBRACKET SEMICOLON'''
        self.quad_gen.generate('ENDFUNC', None, None, None)
        self.semantic.exit_function()
        p[0] = ('function', p[1], p[2])

    def p_func_code_start(self, p):
        '''func_code_start :'''
        self.semantic.set_start_quad(self.quad_gen.get_next_address())

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
        # print(f"DEBUG: statement_list len={len(p)}")
        if len(p) == 3 and p[1]:
            p[0] = [p[1]] + (p[2] if p[2] else [])
        else:
            p[0] = []

    def p_statement(self, p):
        '''statement : assign
                     | condition
                     | cycle
                     | f_call SEMICOLON
                     | print
                     | return_stmt'''
        # print(f"DEBUG: p_statement matched {p[1]}")
        p[0] = p[1]

    def p_return_stmt(self, p):
        '''return_stmt : RETURN expression SEMICOLON'''
        # Validate return type and get global address
        expr_type = self._get_expr_type(p[2])
        return_addr = self.semantic.validate_return(expr_type, p.lineno(1))
        
        # Generate assignment to global return address
        result_operand = self.operand_stack.pop()
        self.quad_gen.generate('=', result_operand, None, return_addr)
        
        # Generate ENDFUNC (or RET)
        self.quad_gen.generate('ENDFUNC', None, None, None)
        
        p[0] = ('return', p[2])

    def p_assign(self, p):
        '''assign : ID EQ expression SEMICOLON'''
        var_name = p[1]
        expr_info = p[3]
        expr_type = self._get_expr_type(expr_info)
        self.semantic.check_assignment(var_name, expr_type, p.lineno(1))

        # PN_ASSIGNMENT: Generate assignment quadruple
        result_operand = self.operand_stack.pop()
        var_address = self.semantic.get_variable_address(var_name, p.lineno(1))
        self.quad_gen.generate('=', result_operand, None, var_address)

        p[0] = ('assign', p[1], p[3])

    def p_condition(self, p):
        '''condition : IF LPAREN expression RPAREN if_test body if_end
                     | IF LPAREN expression RPAREN if_test body ELSE else_start body if_end'''
        p[0] = ('if', p[3])

    def p_if_test(self, p):
        '''if_test :'''
        # Generate GOTOF
        condition_type = self.type_stack.pop()
        result = self.operand_stack.pop()
        quad_idx = self.quad_gen.generate('GOTOF', result, None, None)
        self.jump_stack.append(quad_idx)

    def p_if_end(self, p):
        '''if_end :'''
        # Fill GOTOF
        end = self.jump_stack.pop()
        self.quad_gen.fill_quad(end, self.quad_gen.get_next_address())

    def p_else_start(self, p):
        '''else_start :'''
        # Generate GOTO (to skip else) and fill GOTOF
        false_jump = self.jump_stack.pop()
        
        # GOTO end of else
        goto_idx = self.quad_gen.generate('GOTO', None, None, None)
        self.jump_stack.append(goto_idx)
        
        # Fill GOTOF to go here (start of else)
        self.quad_gen.fill_quad(false_jump, self.quad_gen.get_next_address())

    def p_cycle(self, p):
        '''cycle : WHILE while_start LPAREN expression RPAREN while_test DO body while_end'''
        p[0] = ('while', p[4])

    def p_while_start(self, p):
        '''while_start :'''
        # PN_WHILE_1: Save start address to jump back
        self.jump_stack.append(self.quad_gen.get_next_address())

    def p_while_test(self, p):
        '''while_test :'''
        # PN_WHILE_2: Generate GOTOF
        condition_type = self.type_stack.pop()
        result = self.operand_stack.pop()
        quad_idx = self.quad_gen.generate('GOTOF', result, None, None)
        self.jump_stack.append(quad_idx)

    def p_while_end(self, p):
        '''while_end :'''
        # PN_WHILE_3: Generate GOTO back and fill GOTOF
        false_jump = self.jump_stack.pop()
        start_addr = self.jump_stack.pop()
        
        self.quad_gen.generate('GOTO', None, None, start_addr)
        self.quad_gen.fill_quad(false_jump, self.quad_gen.get_next_address())

    def p_print(self, p):
        '''print : PRINT LPAREN print_list RPAREN SEMICOLON'''
        # PN_PRINT: Generate PRINT quadruples for each item
        # Items are processed in reverse order from the stack
        print_items = p[3]
        num_expressions = sum(1 for item in print_items if not (isinstance(item, tuple) and item[0] == 'string_literal'))

        # Pop operands in reverse order
        operands = []
        for _ in range(num_expressions):
            operands.insert(0, self.operand_stack.pop())

        operand_idx = 0
        for item in print_items:
            if isinstance(item, tuple) and item[0] == 'string_literal':
                # String literal - print directly
                self.quad_gen.generate('PRINT', item[1], None, None)
            else:
                # Expression result
                self.quad_gen.generate('PRINT', operands[operand_idx], None, None)
                operand_idx += 1

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
        # CTE_STRING is identified by the grammar rule itself
        if len(p) == 2 and self._is_from_rule(p.slice[1].type, 'CTE_STRING'):
            # String constant
            address = self.semantic.get_const_address('string', p[1])
            p[0] = ('string_literal', address)
        else:
            p[0] = p[1]

    def _is_from_rule(self, token_type, expected_type):
        """Check if a token is of the expected type."""
        return token_type == expected_type

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

            # PN_RELATIONAL: Generate quadruple for relational operators
            right_operand = self.operand_stack.pop()
            left_operand = self.operand_stack.pop()
            self.type_stack.pop()
            self.type_stack.pop()

            temp = self.semantic.get_temp_address(result_type)
            self.quad_gen.generate(operator, left_operand, right_operand, temp)

            self.operand_stack.append(temp)
            self.type_stack.append(result_type)

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

            # PN_OPERATION: Generate quadruple for +/-
            right_operand = self.operand_stack.pop()
            left_operand = self.operand_stack.pop()
            self.type_stack.pop()
            self.type_stack.pop()

            temp = self.semantic.get_temp_address(result_type)
            self.quad_gen.generate(operator, left_operand, right_operand, temp)

            self.operand_stack.append(temp)
            self.type_stack.append(result_type)

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

            # PN_OPERATION: Generate quadruple for *//
            right_operand = self.operand_stack.pop()
            left_operand = self.operand_stack.pop()
            self.type_stack.pop()
            self.type_stack.pop()

            temp = self.semantic.get_temp_address(result_type)
            self.quad_gen.generate(operator, left_operand, right_operand, temp)

            self.operand_stack.append(temp)
            self.type_stack.append(result_type)

            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

    def p_factor(self, p):
        '''factor : LPAREN expression RPAREN
                  | PLUS factor
                  | MINUS factor
                  | f_call
                  | cte
                  | ID'''
        if len(p) == 2 and isinstance(p[1], tuple) and p[1][0] == 'call':
             # Function call result is already on stack (handled in f_call)
             p[0] = p[1]
             return
        elif len(p) == 4:
            # Parenthesized expression - operand already on stack
            p[0] = p[2]
        elif len(p) == 3:
            factor_type = self._get_expr_type(p[2])
            if p[1] == '-':
                # Unary minus - generate quadruple
                operand = self.operand_stack.pop()
                self.type_stack.pop()

                temp = self.temp_mgr.generate()
                self.quad_gen.generate('unary-', operand, None, temp)

                self.operand_stack.append(temp)
                self.type_stack.append(factor_type)

                p[0] = ('type_info', factor_type, ('unary', p[1], p[2]))
            else:
                # Unary plus - no operation needed
                p[0] = p[2]
        else:
            # ID or constant - already handled in p_cte and below
            if isinstance(p[1], str) and not p[1].replace('.', '').replace('-', '').replace('+', '').isdigit():
                # PN_PUSH_OPERAND: Variable reference
                var_type = self.semantic.lookup_variable(p[1], p.lineno(1))
                address = self.semantic.get_variable_address(p[1], p.lineno(1))
                self.operand_stack.append(address)
                self.type_stack.append(var_type)
                p[0] = ('type_info', var_type, ('id', p[1]))
            else:
                # Constant - handled in p_cte
                p[0] = p[1]

    def p_cte(self, p):
        '''cte : CTE_INT
               | CTE_FLOAT'''
        value = p[1]
        if '.' in str(value):
            const_type = 'float'
        else:
            const_type = 'int'

        # PN_PUSH_OPERAND: Constant
        address = self.semantic.get_const_address(const_type, value)
        self.operand_stack.append(address)
        self.type_stack.append(const_type)

        p[0] = ('type_info', const_type, ('const', value))

    def p_f_call(self, p):
        '''f_call : ID LPAREN expression_list RPAREN
                  | ID LPAREN RPAREN'''
        func_name = p[1]

        if len(p) == 5:
            arg_expressions = p[3]
            arg_types = [self._get_expr_type(expr) for expr in arg_expressions]
        else:
            arg_types = []

        self.semantic.validate_function_call(func_name, arg_types, p.lineno(1))

        # PN_CALL: Generate ERA, PARAMs, GOSUB
        self.quad_gen.generate('ERA', func_name, None, None)
        
        # Generate PARAM for each argument
        # Arguments are on the operand stack (addresses)
        # We need to pop them in reverse order (stack is LIFO)
        # But wait, p[3] (arg_expressions) has the list of expressions
        # And the operands are on the stack in the order they were evaluated
        # If we evaluate (a, b, c), stack has [addr_a, addr_b, addr_c] (top is c)
        
        num_args = len(arg_types)
        argument_addresses = []
        for _ in range(num_args):
            argument_addresses.insert(0, self.operand_stack.pop())
            self.type_stack.pop()
            
        for i, arg_addr in enumerate(argument_addresses):
            # param_name = f"param{i+1}" # Or get actual param name from directory if needed
            self.quad_gen.generate('PARAM', arg_addr, None, f"param{i+1}")
            
        # Get function start address (we need to lookup function info)
        # We don't have direct access to function info here via semantic analyzer easily without a new method
        # But GOSUB usually takes the function name or address. 
        # If we use name, the VM will look it up. If we use address, we need to resolve it now.
        # Let's use name for now, or add get_function_start_quad to semantic.
        # The VM usually handles 'GOSUB func_name' by looking up the IP.
        # Or we can resolve it here if we want.
        # Let's use the function name in the quad and let VM resolve, OR resolve it now.
        # Resolving now is better for "compilation".
        
        # Let's add get_function_start_quad to semantic analyzer
        # For now, I'll put the name and let the VM or a linker resolve it. 
        # Actually, since we are compiling to "quadruples" which is IR, names are fine if VM supports it.
        # But the user asked for "addresses".
        # Let's try to get the start quad.
        
        # self.quad_gen.generate('GOSUB', func_name, None, None) 
        
        # Wait, if I use start_quad, I need to know it. If the function is defined AFTER, I can't know it yet.
        # So I need to fill it later? Or does Patito require declaration before use?
        # The grammar allows functions anywhere?
        # "funcs" are before "MAIN". So functions are defined before main.
        # But functions can call each other?
        # If recursion or forward reference is allowed, we need backpatching or name-based lookup.
        # Given the grammar structure, functions are defined before main.
        # If a function calls another function defined later, we have a problem if we need address immediately.
        # Let's assume we can use the function name in GOSUB and the VM handles the lookup table.
        # OR, we can use a "Function Address" which is just the index in the directory?
        
        # Let's stick to using the function name in GOSUB for simplicity in this step, 
        # as implementing a full linker/backpatcher for functions might be overkill if not requested.
        # But wait, the user said "instead of names... use memory addresses".
        # This applies to variables. For functions, jumping to a quad index is standard.
        
        start_quad = self.semantic.get_function_start_quad(func_name)
        if start_quad is None:
            # If function is not defined yet (recursion or forward ref), we have a problem.
            # For now, let's assume it is defined.
            # Or we can leave it as name and let VM handle it if we passed directory.
            # But I want to be "compiled".
            # Let's use a placeholder and fill it later? No, complex.
            # Let's assume definition before use.
            pass
            
        self.quad_gen.generate('GOSUB', start_quad, None, None)

        # Handle return value if function is non-void
        return_addr = self.semantic.get_function_return_address(func_name)
        if return_addr is not None:
            # Assign return value to a temporary
            # We need to know the return type to allocate a temp
            # Semantic analyzer should provide it, or we can look it up
            # Let's assume we can get the type from the return address?
            # Or better, ask semantic for the type.
            # But wait, get_function_return_address only gives address.
            # Let's just use the address type if we can infer it, or ask semantic.
            # Actually, we can just ask for a temp of the return type.
            
            # We need the return type.
            func_info = self.semantic.function_directory.get_function(func_name)
            return_type = func_info.return_type
            
            temp_addr = self.semantic.get_temp_address(return_type)
            self.quad_gen.generate('=', return_addr, None, temp_addr)
            
            # Push temp to operand stack
            self.operand_stack.append(temp_addr)
            self.type_stack.append(return_type)

        if len(p) == 5:
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
            raise Exception(error_msg)
        else:
            error_msg = "Unexpected end of input"
            self.errors.append(error_msg)
            raise Exception(error_msg)

    def parse(self, data):
        self.errors = []
        self.semantic.reset()

        # Reset quadruple generation structures
        self.quad_gen.clear()
        self.temp_mgr.reset()
        self.operand_stack.clear()
        # self.operator_stack.clear() removed
        self.type_stack.clear()

        try:
            result = self.parser.parse(data, lexer=self.lexer.lexer)
            return result
        except Exception as e:
            raise

    def print_semantic_info(self):
        self.semantic.print_semantic_info()

    def print_quadruples(self):
        """Print the generated quadruples."""
        self.quad_gen.print_quadruples()

    def get_quadruples(self):
        """Get the list of generated quadruples."""
        return self.quad_gen.get_quadruples()


def build_parser():
    return PatitoParser()
