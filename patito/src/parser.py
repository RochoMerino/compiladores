import ply.yacc as yacc
from lexer import PatitoLexer
from semantic_analyzer import SemanticAnalyzer
from quadruple_generator import QuadrupleGenerator



class PatitoParser:
    def __init__(self):
        # Constuir el lexer
        self.lexer = PatitoLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens

        # Construir el parser, debug=True para ver la tabla de producciones
        self.parser = yacc.yacc(module=self, debug=True)

        # Declarar arreglo de errores
        self.errors = []

        # Construir el analizador semantico
        self.semantic = SemanticAnalyzer()

        # Construir el generador de cuadruplos
        self.quad_gen = QuadrupleGenerator()

        # Declarar pila de operandos
        self.operand_stack = []
        
        # Declarar la pila de tipos
        self.type_stack = []

        # Declarar la pila de saltos
        self.jump_stack = []

    def p_programa(self, p):
        '''programa : PROGRAM ID SEMICOLON program_start vars funcs MAIN LPAREN RPAREN main_start body END'''
        self.semantic.set_program_name(p[2], p.lineno(2))
        # Declaramos el nombre del programa
        p[0] = ('program', p[2])

    def p_program_start(self, p):
        '''program_start :'''
        # Rellenar GOTO MAIN nuestro salto de inicio
        self.main_jump = self.quad_gen.generate('GOTO', 'MAIN', None, None)

    def p_main_start(self, p):
        '''main_start :'''
        # Regresa al cuadruplo del inicio para rellenar el salto porque ya sabemos donde empieza el programa
        self.quad_gen.fill_quad(self.main_jump, self.quad_gen.get_next_address())

    def p_vars(self, p):
        '''vars : VAR var_decl_list
                | empty'''
        # Puede que haya una seecion que empieze con var y tenga declaraciones, o puede que no tenga nada
        p[0] = p[2] if len(p) == 3 else []

    def p_var_decl_list(self, p):
        '''var_decl_list : var_decl var_decl_list
                         | var_decl'''
        # Si tienes var_decl var_decl_list entonces es una lista de declaraciones                 
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        # Si solo tienes var_decl entonces es una declaracion nadamas
        else:
            p[0] = [p[1]]

    def p_var_decl(self, p):
        '''var_decl : id_list COLON type SEMICOLON'''
        # Tipo de la variable
        var_type = p[3]
        # ID de la variable
        id_list = p[1]
        # Por ID declaramos la variable con su nombre, tipo y linea
        for var_name in id_list:
            self.semantic.declare_variable(var_name, var_type, p.lineno(2))
        # Devolvemos la declaracion de la variable
        p[0] = ('var_decl', p[1], p[3])

    def p_id_list(self, p):
        '''id_list : ID COMMA id_list
                   | ID'''
        # Si tienes ID COMMA id_list entonces es una lista de IDs
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        # Si solo tienes ID entonces es un ID
        else:
            p[0] = [p[1]]

    def p_type(self, p):
        '''type : INT
                | FLOAT'''
        # Tipo de dato INT o FLOAT
        p[0] = p[1]

    def p_funcs(self, p):
        '''funcs : func funcs
                 | empty'''
        # Si tienes func funcs entonces es una lista de funciones
        if len(p) == 3 and p[1]:
            p[0] = [p[1]] + p[2]
        # Si solo tienes func entonces es una funcion
        else:
            p[0] = []

    def p_func_start(self, p):
        '''func_start : VOID ID LPAREN
                      | type ID LPAREN'''
        # Tipo de la funcion
        func_type = p[1]
        # Nombre de la funcion
        func_name = p[2]
        # Declaramos la funcion con su nombre, tipo y linea
        self.semantic.declare_function(func_name, func_type, p.lineno(2))
        
        # "Devolvemos" nombre de la funcion
        p[0] = func_name

    def p_func_with_start(self, p):
        '''func : func_start params RPAREN LBRACE vars func_code_start body RBRACE SEMICOLON'''
        # Generamos el cuadruplo de ENDFUNC
        self.quad_gen.generate('ENDFUNC', None, None, None)
        # Sakimos de la funcion
        self.semantic.exit_function()
        # "Devolvemos" la 'funcion' con p1 que es func_start y p2 que es params
        p[0] = ('function', p[1], p[2])

    def p_func_code_start(self, p):
        '''func_code_start :'''
        # Marcamos donde empieza el codigo ejecutable de la funcion
        self.semantic.set_start_quad(self.quad_gen.get_next_address())

    def p_params(self, p):
        '''params : param_list
                  | empty'''
        # Si tienes param_list entonces lista de parametros, si no entonces no hay nada
        p[0] = p[1] if p[1] else []

    def p_param_list(self, p):
        '''param_list : ID COLON type COMMA param_list
                      | ID COLON type'''
        # Nombre del parametro
        param_name = p[1]
        # Tipo del parametro
        param_type = p[3]
        # Agregamos parametro con su nombre, su tipo y su linea
        self.semantic.add_parameter(param_name, param_type, p.lineno(1))

        # Si tienes hasta param_list entonces es una lista de parametros
        if len(p) == 6:
            p[0] = [(p[1], p[3])] + p[5]
        # Si no tienes hasta param_list entonces es un parametro
        else:
            p[0] = [(p[1], p[3])]

    def p_body(self, p):
        '''body : LBRACE statement_list RBRACE'''
        # "Devolvemos" el cuerpo con p2 statement_list
        p[0] = ('body', p[2])

    def p_statement_list(self, p):
        '''statement_list : statement statement_list
                          | empty'''
        # Si tienes hasta statement_list entonces es una lista de statements 
        if len(p) == 3 and p[1]:
            p[0] = [p[1]] + (p[2] if p[2] else [])
        # Si no tienes statement_list entonces esta vacia
        else:
            p[0] = []

    def p_statement(self, p):
        '''statement : assign
                     | condition
                     | cycle
                     | f_call SEMICOLON
                     | print
                     | return_stmt'''
        # "Devolvemos" lo que sea en p1 jajajaj
        p[0] = p[1]

    def p_return_stmt(self, p):
        '''return_stmt : RETURN expression SEMICOLON'''
        # Tipo de la expresion
        expr_type = self._get_expr_type(p[2])
        # Validamos el tipo de la expresion
        return_addr = self.semantic.validate_return(expr_type, p.lineno(1))
        # Operand resultante
        result_operand = self.operand_stack.pop()
        # Generamos el cuadruplo 
        self.quad_gen.generate('=', result_operand, None, return_addr)
        # Generamos el cuadruplo de ENDFUNC
        self.quad_gen.generate('ENDFUNC', None, None, None)
        # "Devolvemos" el return con p2 que es expression
        p[0] = ('return', p[2])

    def p_assign(self, p):
        '''assign : ID EQ expression SEMICOLON'''
        # var name es ID
        var_name = p[1]
        # expr_info es expression
        expr_info = p[3]
        # Tipo de la expresion
        expr_type = self._get_expr_type(expr_info)
        # Checamos la asignacion con la funcion check_assignment de semantic analyzer
        self.semantic.check_assignment(var_name, expr_type, p.lineno(1))

        # result_operand es el resultado de la expresion
        result_operand = self.operand_stack.pop()
        # var_address es la direccion de la variable
        var_address = self.semantic.get_variable_address(var_name, p.lineno(1))
        # Generamos el cuadruplo de asignacion
        self.quad_gen.generate('=', result_operand, None, var_address)

        # "Devolvemos" el assign con p1 que es ID y p3 que es expression
        p[0] = ('assign', p[1], p[3])

    def p_condition(self, p):
        '''condition : IF LPAREN expression RPAREN if_test body if_end
                     | IF LPAREN expression RPAREN if_test body ELSE else_start body if_end'''
        # "Devolvemos" if expression
        p[0] = ('if', p[3])

    def p_if_test(self, p):
        '''if_test :'''
        # Tipo de la condicion
        condition_type = self.type_stack.pop()
        # Resultado de la condicion
        result = self.operand_stack.pop()
        # Generamos el cuadruplo de GOTOF
        quad_idx = self.quad_gen.generate('GOTOF', result, None, None)
        # Guardamos nuestra semillita de salto porque aun no sabemos a donde tenemos que saltar
        self.jump_stack.append(quad_idx)

    def p_if_end(self, p):
        '''if_end :'''
        # Sacamos el valor de nuestro jump stack
        end = self.jump_stack.pop()
        # Regresamos a rellenar el GOTOF con el siguiente address
        self.quad_gen.fill_quad(end, self.quad_gen.get_next_address())

    def p_else_start(self, p):
        '''else_start :'''
        # Sacamos el valor de nuestro jump stack
        false_jump = self.jump_stack.pop()
        # Generamos el cuadruplo de GOTO
        goto_idx = self.quad_gen.generate('GOTO', None, None, None)
        # Guardamos nuestra semilla para rellenar el GOTO
        self.jump_stack.append(goto_idx)
        # Regresamos a rellenar el GOTOF con el siguiente address
        self.quad_gen.fill_quad(false_jump, self.quad_gen.get_next_address())

    def p_cycle(self, p):
        '''cycle : WHILE while_start LPAREN expression RPAREN while_test DO body while_end'''
        # "Devolvemos" while expression
        p[0] = ('while', p[4])

    def p_while_start(self, p):
        '''while_start :'''
        # Guardamos nuestra semilla en la pila de saltos para poder regresar cuando termine el while
        self.jump_stack.append(self.quad_gen.get_next_address())

    def p_while_test(self, p):
        '''while_test :'''
        # Tipo de la condicion
        condition_type = self.type_stack.pop()
        # Resultado de la condicion
        result = self.operand_stack.pop()
        # Generamos cuadruplo de GOTOF
        quad_idx = self.quad_gen.generate('GOTOF', result, None, None)
        # Guardamos nuestra semilla en la pila de saltos para poder regresar
        self.jump_stack.append(quad_idx)

    def p_while_end(self, p):
        '''while_end :'''
        # Sacamos el false jump de la pila de saltos
        false_jump = self.jump_stack.pop()
        # Sacamos el start address de la pila de saltos
        start_addr = self.jump_stack.pop()
        # Generamos el cuadruplo de goto para regresar al while
        self.quad_gen.generate('GOTO', None, None, start_addr)
        # Rellenamos el GOTOF con el siguiente address para saber que pasa si no se cumple la condicion
        self.quad_gen.fill_quad(false_jump, self.quad_gen.get_next_address())

    def p_print(self, p):
        '''print : PRINT LPAREN print_list RPAREN SEMICOLON'''
        # Guardamos la lista de items para imprimir
        print_items = p[3]
        # Contamos el numero de expresiones
        num_expressions = sum(1 for item in print_items if not (isinstance(item, tuple) and item[0] == 'string_literal'))
        # Creamos una lista para los operands
        operands = []
        # Dependiendo del numero de expresiones, agregamos los operands a la lista
        for _ in range(num_expressions):
            operands.insert(0, self.operand_stack.pop())

        operand_idx = 0
        for item in print_items:
            if isinstance(item, tuple) and item[0] == 'string_literal':
                self.quad_gen.generate('PRINT', item[1], None, None)
            else:
                self.quad_gen.generate('PRINT', operands[operand_idx], None, None)
                operand_idx += 1

        p[0] = ('print', p[3])

    def p_print_list(self, p):
        '''print_list : print_item COMMA print_list
                      | print_item'''
        # Si tienes print_list entonces es una lista de items
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        # Si no tienes un print_list entonces es un item
        else:
            p[0] = [p[1]]

    def p_print_item(self, p):
        '''print_item : expression
                      | CTE_STRING'''
        # Si tienes CTE_STRING entonces es una string constant
        if len(p) == 2 and self._is_from_rule(p.slice[1].type, 'CTE_STRING'):
            # Obtenemos la direccion de la string constant
            address = self.semantic.get_const_address('string', p[1])
            # "Devolvemos" la string constant con p1 que es CTE_STRING
            p[0] = ('string_literal', address)
        # "Devolvemos" el expresion
        else:
            p[0] = p[1]

    def _is_from_rule(self, token_type, expected_type):
        """Check if a token is of the expected type."""
        # Si el token es del tipo esperado entonces es verdadero
        return token_type == expected_type

# 4 lowest priority
    def p_expression(self, p):
        '''expression : exp
                      | exp GT exp
                      | exp LT exp
                      | exp NEQ exp'''
        # "Devolvemos" la expresion con p1 que es exp
        if len(p) == 2:
            p[0] = p[1]
        # Si no tienes una expresion
        else:
            # Tipo de la izquierda
            left_type = self._get_expr_type(p[1])
            # Tipo de la derecha
            right_type = self._get_expr_type(p[3])
            # Operador
            operator = p[2]
            # Checamos si la operacion es valida
            result_type = self.semantic.check_operation(left_type, operator, right_type, p.lineno(2))

            # Operand derecho
            right_operand = self.operand_stack.pop()
            # Operando izquierdo
            left_operand = self.operand_stack.pop()
            # Sacamos los tipos de la pila de tipos
            self.type_stack.pop()
            self.type_stack.pop()

            # Direccion temporal para el resultado de la operacion
            temp = self.semantic.get_temp_address(result_type)
            # Generamos el cuadruplo de la operacion
            self.quad_gen.generate(operator, left_operand, right_operand, temp)
            # Agregamos el resultado de la operacion a la pila de operands
            self.operand_stack.append(temp)
            # Agregamos el tipo de resultado a la pila de tipos
            self.type_stack.append(result_type)
            # "Devolvemos" el tipo de resultado, con el operador, con el operand izquierdo y el operand derecho
            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

# 3
    def p_exp(self, p):
        '''exp : termino
               | exp PLUS termino
               | exp MINUS termino'''
        # Si es termino entonces "devolvemos" el termino con p1 
        if len(p) == 2:
            p[0] = p[1]
        else:
            # Tipo de la izquierda
            left_type = self._get_expr_type(p[1])
            # Tipo de la derecha
            right_type = self._get_expr_type(p[3])
            # Operador
            operator = p[2]
            # Checamos si la operacion es valida
            result_type = self.semantic.check_operation(left_type, operator, right_type, p.lineno(2))

            # Operand derecho
            right_operand = self.operand_stack.pop()
            # Operando izquierdo
            left_operand = self.operand_stack.pop()
            # Sacamos los tipos de la pila de tipos
            self.type_stack.pop()
            # Sacamos los tipos de la pila de tipos
            self.type_stack.pop()

            # Direccion temporal para el resultado de la operacion
            temp = self.semantic.get_temp_address(result_type)
            # Generamos el cuadruplo de la operacion
            self.quad_gen.generate(operator, left_operand, right_operand, temp)
            # Agregamos el resultado a la pila de oerands
            self.operand_stack.append(temp)
            # Agregamos el tipo de resultado a la pila de tipos
            self.type_stack.append(result_type)

            # "Devolvemos" el tipo de resultado, con el operador, con el operand izquierdo y el operand derecho
            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

# 2
    def p_termino(self, p):
        '''termino : factor
                   | termino MULT factor
                   | termino DIV factor'''
        # Si es factor entonces "devolvemos" el factor con p1 
        if len(p) == 2:
            p[0] = p[1]
        else:
            # Tipo de la izquierda
            left_type = self._get_expr_type(p[1])
            # Tipo de la derecha
            right_type = self._get_expr_type(p[3])
            # Operador
            operator = p[2]
            # Checamos si la operacion es valida
            result_type = self.semantic.check_operation(left_type, operator, right_type, p.lineno(2))

            # Operand derecho
            right_operand = self.operand_stack.pop()
            # Operando izquierdo
            left_operand = self.operand_stack.pop()
            # Sacamos los tipos de la pila de tipos
            self.type_stack.pop()
            # Sacamos los tipos de la pila de tipos
            self.type_stack.pop()

            # Direccion temporal para el resultado de la operacion
            temp = self.semantic.get_temp_address(result_type)
            # Generamos el cuadruplo de la operacion
            self.quad_gen.generate(operator, left_operand, right_operand, temp)
            # Agregamos el resultado de la operacion a la pila de operands
            self.operand_stack.append(temp)
            # Agregamos el tipo de resultado a la pila de tipos
            self.type_stack.append(result_type)
            # Devolvemos el tipo de resultado, operador, op izquierdo y op derecho
            p[0] = ('type_info', result_type, (operator, p[1], p[3]))

# 1 highest priority
    def p_factor(self, p):
        '''factor : LPAREN expression RPAREN
                  | PLUS factor
                  | MINUS factor
                  | f_call
                  | cte
                  | ID'''
        # Si tienes una length de 2 y representa una llamada a una func
        if len(p) == 2 and isinstance(p[1], tuple) and p[1][0] == 'call':
             # "Devolvemos" la llamada a la func con p1
             p[0] = p[1]
             # Salimos porque ya procesamos el caso de llamada a func
             return
        # Si tienes len 4 entonces es una expresion entre parentesis
        elif len(p) == 4:
            # "Asignamos" la expresion
            p[0] = p[2]
        # Si tenemos un len de 3 entonces es un tipo de factor
        elif len(p) == 3:
            # Tipo de factor
            factor_type = self._get_expr_type(p[2])
            # Si es un factor negativo
            if p[1] == '-':
                # operand
                operand = self.operand_stack.pop()
                # tipo
                self.type_stack.pop()
                # Direccion temporal para el resultado de la operacion
                temp = self.semantic.get_temp_address(factor_type)
                # Generamos cuadruplo de unary- porque es un factor negativo como -5
                self.quad_gen.generate('unary-', operand, None, temp)
                # Agregamos el resultado de la operacion a la pila de operands
                self.operand_stack.append(temp)
                # Agregamos el tipo de resultado a la pila de tipos
                self.type_stack.append(factor_type)
                # "Devolvemos" el tipo de resultado, con el operador, con el operand izquierdo y el operand derecho
                p[0] = ('type_info', factor_type, ('unary', p[1], p[2]))
            else:
                # "Devolvemos" el factor con p2 porque es un factor positivo
                p[0] = p[2]
        else:
            # Si p1 es un string y no es un numero (id)
            if isinstance(p[1], str) and not p[1].replace('.', '').replace('-', '').replace('+', '').isdigit():
                # Buscamos tipo de la variable
                var_type = self.semantic.lookup_variable(p[1], p.lineno(1))
                # Obtenemos direccion de la variable
                address = self.semantic.get_variable_address(p[1], p.lineno(1))
                # Agregamos la direccion a la pila de operand
                self.operand_stack.append(address)
                # Agregamos tipo de la var a la pila de tipos
                self.type_stack.append(var_type)
                # "Devolvemos" el tipo de la variable, con el id
                p[0] = ('type_info', var_type, ('id', p[1]))
            # Si p1 es un numero entonces es constante
            else:
                # "Devolvemos" la constante tal cual 
                p[0] = p[1]

    def p_cte(self, p):
        '''cte : CTE_INT
               | CTE_FLOAT'''
        # Valor de la constante
        value = p[1]
        # Si el valor tiene un . entonces es un float
        if '.' in str(value):
            const_type = 'float'
        # Si no tiene un . entonces es un int
        else:
            const_type = 'int'

        # Obtenemos la direccion de la constante
        address = self.semantic.get_const_address(const_type, value)
        # Agregamos la direccion de la constante a la pila de operands
        self.operand_stack.append(address)
        # Agregamos el tipo de la constante a la pila de tipos
        self.type_stack.append(const_type)
        # "Devolvemos" el tipo de la constante, con el valor
        p[0] = ('type_info', const_type, ('const', value))

    def p_f_call(self, p):
        '''f_call : ID LPAREN expression_list RPAREN
                  | ID LPAREN RPAREN'''
        # Nombre de la funcion
        func_name = p[1]

        # Si tienes una lista de expresiones
        if len(p) == 5:
            # Argumentos de la lista de expresiones
            arg_expressions = p[3]
            # Tipos de los argumentos de la lista de expresiones
            arg_types = [self._get_expr_type(expr) for expr in arg_expressions]
        # Si no tienes una lista de expresiones entonces no hay argumentos 
        else:
            arg_types = []

        # Checamos con el cubo si la llamada a la funcion es valida
        self.semantic.validate_function_call(func_name, arg_types, p.lineno(1))

        # GENERAMOS cuadruplo de ERA con nombre de la funcion
        self.quad_gen.generate('ERA', func_name, None, None)

        # Numero de argumentos
        num_args = len(arg_types)
        # Direcciones de los argumentos
        argument_addresses = []
        # Por cada arugmento
        for _ in range(num_args):
            # Agregamos la direccion del argumento a la lista de direcciones de argumentos
            argument_addresses.insert(0, self.operand_stack.pop())
            # Sacamos el tipo de la pila de tipos
            self.type_stack.pop()
        
        # Por cada argumento
        for i, arg_addr in enumerate(argument_addresses):
            # Generamos el cuadruplo con PARAM, argumento y nombre de parametro
            self.quad_gen.generate('PARAM', arg_addr, None, f"param{i+1}")
        
        # Obtenemos el cuadruplo de inicio de la funcion
        start_quad = self.semantic.get_function_start_quad(func_name)
        # Si no hay cuadruplo de inicio
        if start_quad is None:
            pass
        # Cuadruplo de GOSUB con el cuadruplo de inicio de la funcion
        self.quad_gen.generate('GOSUB', start_quad, None, None)

        # Direccion de retorno de la funcion
        return_addr = self.semantic.get_function_return_address(func_name)
        # Si hay direccion de retorno
        if return_addr is not None:
            # Obtenemos informacion de la funcion
            func_info = self.semantic.function_directory.get_function(func_name)
            # Obtenemos el tipo de retorno de la funcion
            return_type = func_info.return_type
            # Direccion temporal para el resultado de la operacion
            temp_addr = self.semantic.get_temp_address(return_type)
            # Generamos el cuadruplo de asignacion para el valor que retorna la funcion
            self.quad_gen.generate('=', return_addr, None, temp_addr)
            # Agregamos la direccion temporal a la pila de operands
            self.operand_stack.append(temp_addr)
            # Agregamos el tipo de retorno a la pila de tipos
            self.type_stack.append(return_type)

        # Si tienes lista de expresiones
        if len(p) == 5:
            # "Devolvemos" el call con el nombre de la func y la lista de expresioens
            p[0] = ('call', p[1], p[3])
        # Si no tienes entonces nadamas call con el nombre de la func y la lista vacia
        else:
            p[0] = ('call', p[1], [])

    def p_expression_list(self, p):
        '''expression_list : expression COMMA expression_list
                           | expression'''
        # Si tienes lista de expresiones entonces devolvemos la lista de expresiones con p1 y p3
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        # Si no tienes lista de expresiones entonces devolvemos la lista de expresiones con p1
        else:
            p[0] = [p[1]]

    def _get_expr_type(self, expr):
        # Si la expresion es una tupla
        if isinstance(expr, tuple):
            # Si empieza con type_info ya fue procesada
            if expr[0] == 'type_info':
                # Regresamos el tipo de la expresion
                return expr[1]
            # Si tiene 3 elementos pero no empieza con type_info
            elif len(expr) == 3:
                # Regresamos un int por defecto...
                return 'int'

        # Si la expresion es un string
        if isinstance(expr, str):
            # Si tiene un . entonces float
            if '.' in expr:
                return 'float'
            # Si no tiene . entonces int
            else:
                return 'int'

        # Si no es tupla ni string entonces regreamos int por defecto
        return 'int'

    def p_empty(self, p):
        '''empty :'''
        pass

    def p_error(self, p):
        # Si hay un token entonces es un error de token
        if p:
            error_msg = f"Unexpected token '{p.value}'"
            self.errors.append(error_msg)
            raise Exception(error_msg)
        # Si no hay un token entonces es un error de fin de input
        else:
            error_msg = "Unexpected end of input"
            self.errors.append(error_msg)
            raise Exception(error_msg)

    def parse(self, data):
        # Limpiamos lista de errores
        self.errors = []
        # Reset semantica
        self.semantic.reset()
        # Limpiamos la pila de cuadruplos
        self.quad_gen.clear()
        # Limpiamos la pila de operands
        self.operand_stack.clear()
        # Limpiamos la pila de tipos
        self.type_stack.clear()

        # Parse codigo
        try:
            result = self.parser.parse(data, lexer=self.lexer.lexer)
            return result
        # Return error
        except Exception as e:
            raise

    def print_semantic_info(self):
        # Imprimimos la informacion semantica
        self.semantic.print_semantic_info()

    def print_quadruples(self):
        """Print the generated quadruples."""
        # Imprimimos los cuadruplos generados
        self.quad_gen.print_quadruples()

    def get_quadruples(self):
        """Get the list of generated quadruples."""
        # Obtenemos la lista de cuadruplos generados
        return self.quad_gen.get_quadruples()


def build_parser():
    # Devolvemos el objeto PatitoParser
    return PatitoParser()
