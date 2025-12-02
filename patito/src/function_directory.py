
from variable_table import VariableTable


class ParameterInfo:
    def __init__(self, name, param_type, position):
        self.name = name
        self.param_type = param_type
        self.position = position
        
    def __repr__(self):
        return f"ParameterInfo({self.name}, {self.param_type}, pos={self.position})"

    def __str__(self):
        return f"{self.name}:{self.param_type}"


class FunctionInfo:
    def __init__(self, name, return_type, line):
        self.name = name
        self.return_type = return_type
        self.params = []
        self.var_table = VariableTable(name)
        self.line = line
        self.start_quad = None
        self.return_address = None
        self.resource_needs = {}

    def add_parameter(self, name, param_type, line, address=None):
        if any(p.name == name for p in self.params):
            raise Exception(f"Error: Parametro '{name}' ya fue declarado en la funcion '{self.name}' en linea {line}")

        position = len(self.params)
        param_info = ParameterInfo(name, param_type, position)
        self.params.append(param_info)

        self.var_table.add_variable(name, param_type, 'param', line, address)

    def get_param_count(self):
        return len(self.params)

    def get_param_types(self):
        return [p.param_type for p in self.params]

    def validate_call(self, arg_types, line):
        expected_count = len(self.params)
        actual_count = len(arg_types)

        if actual_count != expected_count:
            raise Exception(f"Error: Funcion '{self.name}' espera {expected_count} argumentos, pero se pasaron {actual_count} en linea {line}")

        for i, (param, arg_type) in enumerate(zip(self.params, arg_types)):
            if param.param_type != arg_type:
                raise Exception(f"Error: Argumento {i+1} de funcion '{self.name}': se esperaba tipo '{param.param_type}', pero se recibio '{arg_type}' en linea {line}")

    def __repr__(self):
        params_str = ', '.join(str(p) for p in self.params)
        return f"FunctionInfo({self.name}, {self.return_type}, [{params_str}])"

    def __str__(self):
        params_str = ', '.join(str(p) for p in self.params)
        return f"{self.return_type} {self.name}({params_str})"


class FunctionDirectory:

    def __init__(self):
        self.functions = {}
        self.current_function = None

    def add_function(self, name, return_type, line):
        if name in self.functions:
            existing = self.functions[name]
            raise Exception(f"Error: Funcion '{name}' ya fue declarada en linea {existing.line} (redefinicion en linea {line})")

        if name == 'main':
            raise Exception(f"Error: No se puede declarar funcion con nombre 'main' (reservada) en linea {line}")

        func_info = FunctionInfo(name, return_type, line)
        self.functions[name] = func_info
        self.current_function = func_info

        return func_info

    def start_function(self, name):
        if name not in self.functions:
            raise Exception(f"Funcion '{name}' no existe en el directorio")

        self.current_function = self.functions[name]

    def end_function(self):
        self.current_function = None

    def set_start_quad(self, quad_idx):
        if self.current_function:
            self.current_function.start_quad = quad_idx

    def set_return_address(self, address):
        if self.current_function:
            self.current_function.return_address = address

    def add_parameter(self, param_name, param_type, line, address=None):
        if not self.current_function:
            raise Exception("No hay funcion activa para agregar parametros")

        self.current_function.add_parameter(param_name, param_type, line, address)

    def get_function(self, name):
        return self.functions.get(name)

    def function_exists(self, name):
        return name in self.functions

    def validate_call(self, func_name, arg_types, line):
        if not self.function_exists(func_name):
            raise Exception(f"Error: Funcion '{func_name}' no ha sido declarada en linea {line}")

        func_info = self.get_function(func_name)
        func_info.validate_call(arg_types, line)

    def get_function_table(self, func_name):
        func_info = self.get_function(func_name)
        return func_info.var_table if func_info else None

    def count(self):
        return len(self.functions)

    def get_all_functions(self):
        return list(self.functions.values())

    def print_directory(self):
        print(f"\n{'='*70}")
        print("DIRECTORIO DE FUNCIONES")
        print(f"{'='*70}")

        if not self.functions:
            print("  (vacio)")
        else:
            for func in self.functions.values():
                print(f"\n{func.return_type} {func.name}(", end="")
                params_str = ', '.join(str(p) for p in func.params)
                print(f"{params_str}) - Linea {func.line}")

                if func.var_table.count() > 0:
                    print(f"  Variables locales: {func.var_table.count()}")
                    for var in func.var_table.get_all_variables():
                        print(f"    - {var}")

        print(f"\n{'='*70}\n")

    def __repr__(self):
        return f"FunctionDirectory({len(self.functions)} functions)"

    def __str__(self):
        return f"FunctionDirectory: {', '.join(self.functions.keys())}"


if __name__ == '__main__':
    print("DEMO: Directorio de Funciones\n")

    directory = FunctionDirectory()

    directory.add_function('calculateSum', 'void', 5)
    directory.add_parameter('x', 'int', 5)
    directory.add_parameter('y', 'int', 5)
    directory.current_function.var_table.add_variable('temp', 'int', 'local', 7)
    directory.end_function()

    directory.add_function('printValue', 'void', 12)
    directory.add_parameter('value', 'float', 12)
    directory.end_function()

    directory.print_directory()

    print("\nPRUEBAS DE VALIDACION:")

    try:
        directory.validate_call('calculateSum', ['int', 'int'], 20)
        print("calculateSum(int, int) - VALIDO")
    except Exception as e:
        print(f"Error: {e}")

    try:
        directory.validate_call('calculateSum', ['float', 'int'], 21)
        print("calculateSum(float, int) - VALIDO")
    except Exception as e:
        print(f"Error: {e}")

    try:
        directory.validate_call('printValue', ['float', 'int'], 22)
        print("printValue(float, int) - VALIDO")
    except Exception as e:
        print(f"Error: {e}")

    try:
        directory.validate_call('undefined', [], 23)
        print("undefined() - VALIDO")
    except Exception as e:
        print(f"Error: {e}")
