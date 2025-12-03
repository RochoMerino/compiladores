from semantic_cube import SemanticCube
from variable_table import VariableTable
from function_directory import FunctionDirectory
from memory_manager import MemoryManager

class SemanticAnalyzer:
    def __init__(self):
        self.semantic_cube = SemanticCube()
        self.global_vars = VariableTable('global')
        self.function_directory = FunctionDirectory()
        self.memory_manager = MemoryManager()
        self.current_function = None
        self.program_name = None

    def set_program_name(self, name, line):
        '''Nombre del programa'''
        self.program_name = name

    def declare_variable(self, name, var_type, line):
        '''Declarar una variable en el scope global o local'''
        if self.current_function is None:
            address = self.memory_manager.get_global_address(var_type)
            self.global_vars.add_variable(name, var_type, 'global', line, address)
        else:
            address = self.memory_manager.get_local_address(var_type)
            func_info = self.function_directory.get_function(self.current_function)
            func_info.var_table.add_variable(name, var_type, 'local', line, address)

    def lookup_variable(self, name, line):
        '''Buscar una variable local o global'''
        if self.current_function:
            func_info = self.function_directory.get_function(self.current_function)
            var_info = func_info.var_table.lookup(name)
            if var_info:
                return var_info.var_type

        var_info = self.global_vars.lookup(name)
        if var_info:
            return var_info.var_type

        raise Exception(f"Error: Variable '{name}' no ha sido declarada en linea {line}")

    def variable_exists(self, name):
        '''Checar si una variable existe en el scope local o global'''
        if self.current_function:
            func_info = self.function_directory.get_function(self.current_function)
            if func_info.var_table.exists(name):
                return True

        return self.global_vars.exists(name)

    def declare_function(self, name, return_type, line):
        '''Declarar una funcion en el directorio de funciones'''
        self.function_directory.add_function(name, return_type, line)
        self.current_function = name
        self.memory_manager.reset_local_memory()
        self.function_directory.start_function(name) 
        
        if return_type != 'void':
            address = self.memory_manager.get_global_address(return_type)
            self.function_directory.set_return_address(address)

    def exit_function(self):
        '''Salir de una funcion'''
        self.current_function = None
        self.function_directory.end_function()

    def add_parameter(self, name, param_type, line):
        '''Agregar un parametro a la funcion'''
        address = self.memory_manager.get_local_address(param_type)
        self.function_directory.add_parameter(name, param_type, line, address)

    def set_start_quad(self, quad_idx):
        '''Establecer el cuadruplo de inici'''
        self.function_directory.set_start_quad(quad_idx)

    def get_function_start_quad(self, func_name):
        '''Obtener el cuadruplo de inicio de la funcion'''
        func = self.function_directory.get_function(func_name)
        if func:
            return func.start_quad
        return None

    def get_function_return_address(self, func_name):
        '''Obtener direccion de retorno de la funcion'''
        func = self.function_directory.get_function(func_name)
        if func:
            return func.return_address
        return None

    def validate_function_call(self, func_name, arg_types, line):
        '''Checar si la llamada a la funcion es valida'''
        self.function_directory.validate_call(func_name, arg_types, line)

    def check_operation(self, left_type, operator, right_type, line):
        result_type = self.semantic_cube.get_result_type(left_type, operator, right_type)

        if result_type is None:
            raise Exception(f"Error: Operacion invalida: '{left_type}' {operator} '{right_type}' en linea {line}")

        return result_type

    def check_assignment(self, var_name, expr_type, line):
        '''Checa si la asignacion es valida'''
        var_type = self.lookup_variable(var_name, line)
        result_type = self.semantic_cube.get_result_type(var_type, '=', expr_type)
        if result_type is None:
            raise Exception(f"Error: No se puede asignar tipo '{expr_type}' a variable '{var_name}' de tipo '{var_type}' en linea {line}")

        return var_type

    def validate_return(self, expr_type, line):
        '''Checa si el return es valido'''
        if not self.current_function:
            raise Exception(f"Error: Return statement outside of function en linea {line}")
            
        func_info = self.function_directory.get_function(self.current_function)
        if func_info.return_type == 'void':
             raise Exception(f"Error: Void function '{self.current_function}' cannot return a value en linea {line}")
             
        if func_info.return_type != expr_type:
             if not (func_info.return_type == 'float' and expr_type == 'int'):
                raise Exception(f"Error: Type mismatch in return: Expected {func_info.return_type}, got {expr_type} en linea {line}")
        
        return func_info.return_address

    def is_in_function(self):
        '''Checa si estamos en una funcioni'''
        return self.current_function is not None

    def get_current_scope(self):
        '''Obtener el scope actual'''
        return self.current_function if self.current_function else 'global'

    def print_semantic_info(self):
        print("\n" + "="*70)
        print(f"INFORMACION SEMANTICA - Programa: {self.program_name}")
        print("="*70)

        self.global_vars.print_table()
        self.function_directory.print_directory()

        print(f"Cubo Semantico: {len(self.semantic_cube.cube)} reglas definidas\n")

    def get_variable_address(self, name, line):
        '''Obtener direccion de una variable'''
        if self.current_function:
            func_info = self.function_directory.get_function(self.current_function)
            var_info = func_info.var_table.lookup(name)
            if var_info:
                return var_info.address

        var_info = self.global_vars.lookup(name)
        if var_info:
            return var_info.address

        raise Exception(f"Error: Variable '{name}' no ha sido declarada en linea {line}")

    def get_temp_address(self, type_):
        '''Obtener direccion de temporal'''
        return self.memory_manager.get_temp_address(type_)

    def get_const_address(self, type_, value):
        '''Obtener direccion de constante'''
        return self.memory_manager.get_const_address(type_, value)

    def reset(self):
        '''Reset semantica'''
        self.global_vars = VariableTable('global')
        self.function_directory = FunctionDirectory()
        self.memory_manager = MemoryManager()
        self.current_function = None
        self.program_name = None


class ExpressionInfo:
    def __init__(self, expr_type, value=None):
        self.expr_type = expr_type
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"ExpressionInfo({self.expr_type}, value={self.value})"
        return f"ExpressionInfo({self.expr_type})"





