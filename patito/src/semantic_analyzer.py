from semantic_cube import SemanticCube
from variable_table import VariableTable
from function_directory import FunctionDirectory
from errors import (
    SemanticError,
    TypeError as PatitoTypeError,
    UndefinedVariableError,
    RedefinitionError
)


class SemanticAnalyzer:

    def __init__(self):
        self.semantic_cube = SemanticCube()
        self.global_vars = VariableTable('global')
        self.function_directory = FunctionDirectory()
        self.current_function = None
        self.program_name = None

    def set_program_name(self, name, line):
        self.program_name = name

    def declare_variable(self, name, var_type, line):
        if self.current_function is None:
            self.global_vars.add_variable(name, var_type, 'global', line)
        else:
            func_info = self.function_directory.get_function(self.current_function)
            func_info.var_table.add_variable(name, var_type, 'local', line)

    def lookup_variable(self, name, line):
        if self.current_function:
            func_info = self.function_directory.get_function(self.current_function)
            var_info = func_info.var_table.lookup(name)
            if var_info:
                return var_info.var_type

        var_info = self.global_vars.lookup(name)
        if var_info:
            return var_info.var_type

        raise UndefinedVariableError(
            f"Variable '{name}' no ha sido declarada",
            line=line,
            identifier=name
        )

    def variable_exists(self, name):
        if self.current_function:
            func_info = self.function_directory.get_function(self.current_function)
            if func_info.var_table.exists(name):
                return True

        return self.global_vars.exists(name)

    def declare_function(self, name, return_type, line):
        self.function_directory.add_function(name, return_type, line)

    def enter_function(self, name):
        self.current_function = name
        self.function_directory.start_function(name)

    def exit_function(self):
        self.current_function = None
        self.function_directory.end_function()

    def add_parameter(self, name, param_type, line):
        self.function_directory.add_parameter(name, param_type, line)

    def validate_function_call(self, func_name, arg_types, line):
        self.function_directory.validate_call(func_name, arg_types, line)

    def check_operation(self, left_type, operator, right_type, line):
        result_type = self.semantic_cube.get_result_type(left_type, operator, right_type)

        if result_type is None:
            raise PatitoTypeError(
                f"Operacion invalida: '{left_type}' {operator} '{right_type}'",
                line=line
            )

        return result_type

    def check_assignment(self, var_name, expr_type, line):
        var_type = self.lookup_variable(var_name, line)

        result_type = self.semantic_cube.get_result_type(var_type, '=', expr_type)

        if result_type is None:
            raise PatitoTypeError(
                f"No se puede asignar tipo '{expr_type}' a variable '{var_name}' de tipo '{var_type}'",
                line=line
            )

        return var_type

    def is_in_function(self):
        return self.current_function is not None

    def get_current_scope(self):
        return self.current_function if self.current_function else 'global'

    def print_semantic_info(self):
        print("\n" + "="*70)
        print(f"INFORMACION SEMANTICA - Programa: {self.program_name}")
        print("="*70)

        self.global_vars.print_table()
        self.function_directory.print_directory()

        print(f"Cubo Semantico: {len(self.semantic_cube.cube)} reglas definidas\n")

    def reset(self):
        self.global_vars = VariableTable('global')
        self.function_directory = FunctionDirectory()
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


if __name__ == '__main__':
    print("DEMO: Analizador Semantico\n")

    analyzer = SemanticAnalyzer()

    analyzer.set_program_name('test', 1)

    analyzer.declare_variable('x', 'int', 2)
    analyzer.declare_variable('y', 'float', 3)

    analyzer.declare_function('suma', 'void', 5)
    analyzer.enter_function('suma')
    analyzer.add_parameter('a', 'int', 5)
    analyzer.add_parameter('b', 'int', 5)
    analyzer.declare_variable('temp', 'int', 6)
    analyzer.exit_function()

    analyzer.print_semantic_info()

    print("PRUEBAS DE VALIDACION:")
    print("-" * 70)

    try:
        var_type = analyzer.lookup_variable('x', 10)
        print(f"Variable 'x' tiene tipo: {var_type}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        var_type = analyzer.lookup_variable('z', 11)
        print(f"Variable 'z' tiene tipo: {var_type}")
    except UndefinedVariableError as e:
        print(f"Error capturado: {e}")

    try:
        result = analyzer.check_operation('int', '+', 'float', 12)
        print(f"int + float = {result}")
    except Exception as e:
        print(f"Error: {e}")

    try:
        analyzer.check_assignment('x', 'float', 13)
        print(f"Asignacion x = float es valida")
    except PatitoTypeError as e:
        print(f"Error capturado: {e}")

    try:
        analyzer.validate_function_call('suma', ['int', 'int'], 14)
        print(f"Llamada suma(int, int) es valida")
    except Exception as e:
        print(f"Error: {e}")

    try:
        analyzer.validate_function_call('suma', ['float', 'int'], 15)
        print(f"Llamada suma(float, int) es valida")
    except PatitoTypeError as e:
        print(f"Error capturado: {e}")

    print("\n" + "="*70)
