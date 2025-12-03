
class VariableInfo:
    def __init__(self, name, var_type, scope, line, address=None):
        self.name = name
        self.var_type = var_type
        self.scope = scope
        self.line = line
        self.address = address

    def __repr__(self):
        return f"VariableInfo({self.name}, {self.var_type}, {self.scope}, line={self.line}, addr={self.address})"

    def __str__(self):
        return f"{self.name}:{self.var_type} ({self.scope}) @{self.address}"


class VariableTable:
    def __init__(self, scope_name='global'):
        self.scope_name = scope_name
        self.variables = {}

    def add_variable(self, name, var_type, scope, line, address=None):
        if name in self.variables:
            existing = self.variables[name]
            raise Exception(f"Error: Variable '{name}' ya fue declarada en linea {existing.line} (redefinicion en linea {line})")

        var_info = VariableInfo(name, var_type, scope, line, address)
        self.variables[name] = var_info
        return var_info

    def lookup(self, name):
        return self.variables.get(name)

    def exists(self, name):
        return name in self.variables

    def get_type(self, name):
        var_info = self.variables.get(name)
        return var_info.var_type if var_info else None
    
    def get_address(self, name):
        var_info = self.variables.get(name)
        return var_info.address if var_info else None

    def get_all_variables(self):
        return list(self.variables.values())

    def count(self):
        return len(self.variables)

    def clear(self):
        self.variables.clear()

    def print_table(self):
        print(f"\n{'='*70}")
        print(f"TABLA DE VARIABLES - Scope: {self.scope_name}")
        print(f"{'='*70}")

        if not self.variables:
            print("  (vacia)")
        else:
            print(f"{'Nombre':<15} {'Tipo':<10} {'Scope':<10} {'Linea':<10} {'Direccion':<10}")
            print("-" * 70)
            for var in self.variables.values():
                print(f"{var.name:<15} {var.var_type:<10} {var.scope:<10} {var.line:<10} {str(var.address):<10}")

        print(f"{'='*70}\n")

    def __repr__(self):
        return f"VariableTable({self.scope_name}, {len(self.variables)} vars)"

    def __str__(self):
        return f"VariableTable[{self.scope_name}]: {', '.join(self.variables.keys())}"


class ScopedVariableTable:
    def __init__(self):
        self.global_table = VariableTable('global')
        self.local_table = None
        self.current_scope = 'global'

    def enter_function(self, function_name):
        self.local_table = VariableTable(function_name)
        self.current_scope = function_name

    def exit_function(self):
        self.local_table = None
        self.current_scope = 'global'

    def add_variable(self, name, var_type, line, address=None):
        scope = self.current_scope
        table = self.local_table if self.local_table else self.global_table
        scope_type = 'local' if self.local_table else 'global'

        return table.add_variable(name, var_type, scope_type, line, address)

    def add_parameter(self, name, var_type, line, address=None):
        if not self.local_table:
            raise Exception("No se puede agregar parametro fuera de una funcion")

        return self.local_table.add_variable(name, var_type, 'param', line, address)

    def lookup(self, name, line=None):
        if self.local_table:
            var_info = self.local_table.lookup(name)
            if var_info:
                return var_info

        var_info = self.global_table.lookup(name)
        if var_info:
            return var_info

        if line is not None:
            raise Exception(f"Error: Variable '{name}' no ha sido declarada en linea {line}")

        return None

    def get_type(self, name, line=None):
        var_info = self.lookup(name, line)
        return var_info.var_type if var_info else None

    def print_all_tables(self):
        self.global_table.print_table()
        if self.local_table:
            self.local_table.print_table()


# if __name__ == '__main__':
#     print("DEMO: Tabla de Variables\n")

#     table = VariableTable('global')
#     table.add_variable('x', 'int', 'global', 1)
#     table.add_variable('y', 'float', 'global', 2)
#     table.print_table()

#     scoped = ScopedVariableTable()
#     scoped.add_variable('global_x', 'int', 1)
#     scoped.add_variable('global_y', 'float', 2)

#     scoped.enter_function('foo')
#     scoped.add_parameter('param_a', 'int', 5)
#     scoped.add_variable('local_z', 'float', 6)

#     scoped.print_all_tables()

#     print("\nPRUEBAS DE BUSQUEDA:")
#     print(f"local_z: {scoped.lookup('local_z')}")
#     print(f"global_x: {scoped.lookup('global_x')}")
#     print(f"param_a: {scoped.lookup('param_a')}")

#     try:
#         scoped.lookup('undefined', line=10)
#     except Exception as e:
#         print(f"\nError capturado: {e}")
