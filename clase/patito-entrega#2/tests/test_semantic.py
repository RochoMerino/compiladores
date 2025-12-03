"""
Tests para el Análisis Semántico del compilador Patito.

Estos tests verifican:
1. Declaración de variables (duplicadas y válidas)
2. Uso de variables (no declaradas)
3. Verificación de tipos en operaciones
4. Verificación de tipos en asignaciones
5. Declaración de funciones (duplicadas y válidas)
6. Llamadas a funciones (validación de argumentos)
7. Scope de variables (globales vs locales)
"""

import unittest
import sys
import os

# Agregar el directorio padre al path para importar el módulo patito
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patito.parser import PatitoParser
from patito.errors import (
    RedefinitionError,
    UndefinedVariableError,
    TypeError as PatitoTypeError,
    SemanticError
)


class TestSemanticAnalysis(unittest.TestCase):
    """Suite de tests para análisis semántico."""

    def setUp(self):
        """Inicializar parser antes de cada test."""
        self.parser = PatitoParser()

    # ==================== TESTS DE VARIABLES ====================

    def test_valid_variable_declarations(self):
        """Test: Declaraciones de variables válidas."""
        code = """
        program test;
        var x, y : int;
            z : float;
        main() {
            x = 5;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_duplicate_global_variable(self):
        """Test: Variable global declarada dos veces (ERROR)."""
        code = """
        program test;
        var x : int;
            x : float;
        main() {
        }
        end
        """
        with self.assertRaises(RedefinitionError) as context:
            self.parser.parse(code)

        self.assertIn("'x'", str(context.exception))

    def test_undefined_variable_usage(self):
        """Test: Uso de variable no declarada (ERROR)."""
        code = """
        program test;
        main() {
            y = 10;
        }
        end
        """
        with self.assertRaises(UndefinedVariableError) as context:
            self.parser.parse(code)

        self.assertIn("'y'", str(context.exception))

    def test_variable_scope_global(self):
        """Test: Acceso a variable global desde main."""
        code = """
        program test;
        var globalVar : int;
        main() {
            globalVar = 42;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    # ==================== TESTS DE TIPOS EN OPERACIONES ====================

    def test_valid_int_operations(self):
        """Test: Operaciones aritméticas entre enteros."""
        code = """
        program test;
        var x, y, z : int;
        main() {
            x = 10;
            y = 20;
            z = x + y;
            z = x - y;
            z = x * y;
            z = x / y;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_valid_float_operations(self):
        """Test: Operaciones aritméticas entre floats."""
        code = """
        program test;
        var x, y, z : float;
        main() {
            x = 10.5;
            y = 20.3;
            z = x + y;
            z = x * y;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_valid_mixed_operations(self):
        """Test: Operaciones mixtas int + float (promoción de tipo)."""
        code = """
        program test;
        var x : int;
            y : float;
            z : float;
        main() {
            x = 10;
            y = 5.5;
            z = x + y;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_valid_comparison_operations(self):
        """Test: Operaciones de comparación."""
        code = """
        program test;
        var x, y : int;
            result : int;
        main() {
            x = 10;
            y = 20;
            if (x > y) {
                result = 1;
            };
            if (x < y) {
                result = 0;
            };
            if (x != y) {
                result = 1;
            };
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    # ==================== TESTS DE ASIGNACIONES ====================

    def test_valid_assignment_int_to_int(self):
        """Test: Asignación int = int (válido)."""
        code = """
        program test;
        var x : int;
        main() {
            x = 42;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_valid_assignment_float_to_float(self):
        """Test: Asignación float = float (válido)."""
        code = """
        program test;
        var x : float;
        main() {
            x = 3.14;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_valid_assignment_int_to_float(self):
        """Test: Asignación float = int (válido, con promoción)."""
        code = """
        program test;
        var x : float;
        main() {
            x = 42;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_invalid_assignment_float_to_int(self):
        """Test: Asignación int = float (ERROR, pérdida de precisión)."""
        code = """
        program test;
        var x : int;
        main() {
            x = 3.14;
        }
        end
        """
        with self.assertRaises(PatitoTypeError) as context:
            self.parser.parse(code)

        # Debe mencionar incompatibilidad de tipos
        self.assertTrue(
            'asignar' in str(context.exception).lower() or
            'tipo' in str(context.exception).lower()
        )

    # ==================== TESTS DE FUNCIONES ====================

    def test_valid_function_declaration(self):
        """Test: Declaración válida de función."""
        code = """
        program test;
        void myFunc(x : int, y : float) [
        {
        }
        ];
        main() {
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_duplicate_function_declaration(self):
        """Test: Función declarada dos veces (ERROR)."""
        code = """
        program test;
        void myFunc() [
        {
        }
        ];
        void myFunc() [
        {
        }
        ];
        main() {
        }
        end
        """
        with self.assertRaises(RedefinitionError) as context:
            self.parser.parse(code)

        self.assertIn("myFunc", str(context.exception))

    def test_function_call_valid(self):
        """Test: Llamada válida a función."""
        code = """
        program test;
        var x : int;
            y : float;

        void calculate(a : int, b : float) [
        {
        }
        ];

        main() {
            x = 10;
            y = 5.5;
            calculate(x, y);
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_function_call_undefined(self):
        """Test: Llamada a función no declarada (ERROR)."""
        code = """
        program test;
        main() {
            undefinedFunc();
        }
        end
        """
        with self.assertRaises(UndefinedVariableError) as context:
            self.parser.parse(code)

        self.assertIn("undefinedFunc", str(context.exception))

    def test_function_call_wrong_arg_count(self):
        """Test: Llamada con número incorrecto de argumentos (ERROR)."""
        code = """
        program test;
        void myFunc(x : int) [
        {
        }
        ];
        main() {
            myFunc(10, 20);
        }
        end
        """
        with self.assertRaises(PatitoTypeError) as context:
            self.parser.parse(code)

        # Debe mencionar número de argumentos
        self.assertTrue(
            'argumento' in str(context.exception).lower()
        )

    def test_function_call_wrong_arg_types(self):
        """Test: Llamada con tipos de argumentos incorrectos (ERROR)."""
        code = """
        program test;
        var x : float;

        void myFunc(a : int) [
        {
        }
        ];

        main() {
            x = 3.14;
            myFunc(x);
        }
        end
        """
        with self.assertRaises(PatitoTypeError) as context:
            self.parser.parse(code)

        # Debe mencionar tipo de argumento
        self.assertTrue(
            'argumento' in str(context.exception).lower() or
            'tipo' in str(context.exception).lower()
        )

    # ==================== TESTS DE SCOPE ====================

    def test_local_variable_in_function(self):
        """Test: Variables locales en función."""
        code = """
        program test;
        void myFunc() [
            var local : int;
        {
            local = 10;
        }
        ];
        main() {
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_duplicate_parameter_names(self):
        """Test: Parámetros con nombres duplicados (ERROR)."""
        code = """
        program test;
        void myFunc(x : int, x : float) [
        {
        }
        ];
        main() {
        }
        end
        """
        with self.assertRaises(RedefinitionError) as context:
            self.parser.parse(code)

        self.assertIn("'x'", str(context.exception))

    def test_parameter_as_local_variable(self):
        """Test: Los parámetros actúan como variables locales."""
        code = """
        program test;
        void myFunc(x : int) [
        {
            x = x + 1;
        }
        ];
        main() {
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    # ==================== TESTS COMPLEJOS ====================

    def test_complex_expression(self):
        """Test: Expresión compleja con múltiples operaciones."""
        code = """
        program test;
        var a, b, c : int;
            result : float;
        main() {
            a = 10;
            b = 20;
            c = 5;
            result = (a + b) * c - 3.14;
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")

    def test_complete_program(self):
        """Test: Programa completo con todas las características."""
        code = """
        program calculator;

        var globalX, globalY : int;
            globalResult : float;

        void add(a : int, b : int) [
            var temp : int;
        {
            temp = a + b;
            print("Sum:", temp);
        }
        ];

        void multiply(x : float, y : float) [
            var result : float;
        {
            result = x * y;
            print("Product:", result);
        }
        ];

        main() {
            globalX = 10;
            globalY = 5;
            globalResult = globalX + globalY * 2.5;

            if (globalX > globalY) {
                print("X is greater");
            } else {
                print("Y is greater or equal");
            };

            add(globalX, globalY);
            multiply(3.14, 2.0);
        }
        end
        """
        try:
            result = self.parser.parse(code)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"No debería haber error: {e}")


def run_tests():
    """Ejecuta todos los tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("="*70)
    print("TESTS DE ANÁLISIS SEMÁNTICO - COMPILADOR PATITO")
    print("="*70)
    print()
    run_tests()
