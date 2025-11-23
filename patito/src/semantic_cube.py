'''
SemanticCube es una clase que representa el cubo semantico del lenguaje Patito.

Actua como un juez que decide si una operacion es valida o no

Es una tabla que contiene las operaciones validas entre los diferentes tipos de datos

Cada operacion es una tupla de la forma (tipo_izq, operador, tipo_der) -> tipo_resultante

Por ejemplo:
    ('int', '+', 'int') -> 'int'
    ('int', '+', 'float') -> 'float'
    ('float', '+', 'int') -> 'float'
    ('float', '+', 'float') -> 'float'
    ('int', '=', 'int') -> 'int'
    ('float', '=', 'float') -> 'float'
    ('float', '=', 'int') -> 'float'
'''


class SemanticCube:

    def __init__(self):
        self.cube = self._build_semantic_cube()

    def _build_semantic_cube(self):
        cube = {}
        self.arithmetic_operations = ['+', '-', '*', '/']
        self.comparison_operations = ['>', '<', '!=']

        for op in self.arithmetic_operations:
            cube[('int', op, 'int')] = 'int'

        for op in self.arithmetic_operations:
            cube[('int', op, 'float')] = 'float'

        for op in self.arithmetic_operations:
            cube[('float', op, 'int')] = 'float'

        for op in self.arithmetic_operations:
            cube[('float', op, 'float')] = 'float'

        for op in self.comparison_operations:
            cube[('int', op, 'int')] = 'int'

        for op in self.comparison_operations:
            cube[('int', op, 'float')] = 'int'

        for op in self.comparison_operations:
            cube[('float', op, 'int')] = 'int'

        for op in self.comparison_operations:
            cube[('float', op, 'float')] = 'int'

        cube[('int', '=', 'int')] = 'int'
        cube[('float', '=', 'float')] = 'float'
        cube[('float', '=', 'int')] = 'float'

        return cube

    def get_result_type(self, left_type, operator, right_type):
        return self.cube.get((left_type, operator, right_type))

    def is_valid_operation(self, left_type, operator, right_type):
        return (left_type, operator, right_type) in self.cube

    def print_cube(self):
        print("\n" + "="*70)
        print("CUBO SEMANTICO DEL LENGUAJE PATITO")
        print("="*70)

        operators = {}
        for (left, op, right), result in sorted(self.cube.items()):
            if op not in operators:
                operators[op] = []
            operators[op].append((left, right, result))

        for op in self.arithmetic_operations + self.comparison_operations + ['=']:
            if op in operators:
                print(f"\n{self._get_operator_name(op)}:")
                print("-" * 50)
                for left, right, result in operators[op]:
                    print(f"  {left:6} {op:2} {right:6} -> {result}")

        print("\n" + "="*70 + "\n")

    def _get_operator_name(self, op):
        names = {
            '+': 'SUMA',
            '-': 'RESTA',
            '*': 'MULTIPLICACION',
            '/': 'DIVISION',
            '>': 'MAYOR QUE',
            '<': 'MENOR QUE',
            '!=': 'DIFERENTE DE',
            '=': 'ASIGNACION'
        }
        return names.get(op, op)


semantic_cube = SemanticCube()


def check_operation(left_type, operator, right_type):
    return semantic_cube.get_result_type(left_type, operator, right_type)


if __name__ == '__main__':
    cube = SemanticCube()
    cube.print_cube()

    print("\nEJEMPLOS DE USO:")
    print("-" * 50)

    test_cases = [
        ('int', '+', 'int'),
        ('int', '+', 'float'),
        ('float', '/', 'int'),
        ('int', '>', 'float'),
        ('float', '=', 'int'),
        ('int', '=', 'float'),
    ]

    for left, op, right in test_cases:
        result = cube.get_result_type(left, op, right)
        status = "VALIDO" if result else "INVALIDO"
        print(f"{status:12} | {left:6} {op:2} {right:6} -> {result if result else 'ERROR'}")
