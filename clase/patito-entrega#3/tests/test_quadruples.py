"""
Tests for quadruple generation in the Patito compiler.

Tests verify:
1. Arithmetic expression quadruples
2. Relational expression quadruples
3. Assignment quadruples
4. Print statement quadruples
5. Correct operator precedence
6. Temporary variable generation
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patito.parser import PatitoParser


class TestQuadrupleGeneration(unittest.TestCase):
    """Test suite for quadruple generation."""

    def setUp(self):
        """Initialize parser before each test."""
        self.parser = PatitoParser()

    def test_simple_assignment(self):
        """Test: Simple assignment generates correct quadruple."""
        code = """
        program test;
        var x : int;
        main() {
            x = 5;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 1)
        self.assertEqual(quads[0].operator, '=')
        self.assertEqual(quads[0].operand1, '5')
        self.assertIsNone(quads[0].operand2)
        self.assertEqual(quads[0].result, 'x')

    def test_arithmetic_addition(self):
        """Test: Addition expression generates correct quadruples."""
        code = """
        program test;
        var x, y, z : int;
        main() {
            z = x + y;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 2)
        # First quadruple: addition
        self.assertEqual(quads[0].operator, '+')
        self.assertEqual(quads[0].operand1, 'x')
        self.assertEqual(quads[0].operand2, 'y')
        self.assertEqual(quads[0].result, 't1')
        # Second quadruple: assignment
        self.assertEqual(quads[1].operator, '=')
        self.assertEqual(quads[1].operand1, 't1')
        self.assertEqual(quads[1].result, 'z')

    def test_arithmetic_precedence(self):
        """Test: Operator precedence (* before +)."""
        code = """
        program test;
        var a, b, c, result : int;
        main() {
            result = a + b * c;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 3)
        # First: b * c (higher precedence)
        self.assertEqual(quads[0].operator, '*')
        self.assertEqual(quads[0].operand1, 'b')
        self.assertEqual(quads[0].operand2, 'c')
        # Second: a + t1
        self.assertEqual(quads[1].operator, '+')
        self.assertEqual(quads[1].operand1, 'a')
        self.assertEqual(quads[1].operand2, 't1')
        # Third: assignment
        self.assertEqual(quads[2].operator, '=')

    def test_parenthesized_expression(self):
        """Test: Parentheses override precedence."""
        code = """
        program test;
        var a, b, c, result : int;
        main() {
            result = (a + b) * c;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 3)
        # First: a + b (due to parentheses)
        self.assertEqual(quads[0].operator, '+')
        self.assertEqual(quads[0].operand1, 'a')
        self.assertEqual(quads[0].operand2, 'b')
        # Second: t1 * c
        self.assertEqual(quads[1].operator, '*')
        self.assertEqual(quads[1].operand1, 't1')
        self.assertEqual(quads[1].operand2, 'c')

    def test_relational_operators(self):
        """Test: Relational operators generate correct quadruples."""
        code = """
        program test;
        var a, b, c : int;
        main() {
            c = a > b;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 2)
        # First: relational operation
        self.assertEqual(quads[0].operator, '>')
        self.assertEqual(quads[0].operand1, 'a')
        self.assertEqual(quads[0].operand2, 'b')
        # Second: assignment
        self.assertEqual(quads[1].operator, '=')

    def test_multiple_operations(self):
        """Test: Multiple operations generate correct sequence."""
        code = """
        program test;
        var x, y : int;
        main() {
            x = 5;
            y = 10;
            x = x + y;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 4)
        self.assertEqual(quads[0].operator, '=')
        self.assertEqual(quads[0].result, 'x')
        self.assertEqual(quads[1].operator, '=')
        self.assertEqual(quads[1].result, 'y')
        self.assertEqual(quads[2].operator, '+')
        self.assertEqual(quads[3].operator, '=')

    def test_print_variables(self):
        """Test: Print generates PRINT quadruples."""
        code = """
        program test;
        var x : int;
        main() {
            x = 5;
            print(x);
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        # Find PRINT quadruple
        print_quads = [q for q in quads if q.operator == 'PRINT']
        self.assertEqual(len(print_quads), 1)
        self.assertEqual(print_quads[0].operand1, 'x')

    def test_print_strings(self):
        """Test: Print with strings generates correct quadruples."""
        code = """
        program test;
        var x : int;
        main() {
            x = 5;
            print("Value:", x);
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        # Find PRINT quadruples
        print_quads = [q for q in quads if q.operator == 'PRINT']
        self.assertEqual(len(print_quads), 2)
        self.assertEqual(print_quads[0].operand1, '"Value:"')
        self.assertEqual(print_quads[1].operand1, 'x')

    def test_complex_expression(self):
        """Test: Complex expression with multiple operators."""
        code = """
        program test;
        var a, b, c, d, result : int;
        main() {
            result = a + b * c - d;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        self.assertEqual(len(quads), 4)
        # b * c
        self.assertEqual(quads[0].operator, '*')
        # a + t1
        self.assertEqual(quads[1].operator, '+')
        # t2 - d
        self.assertEqual(quads[2].operator, '-')
        # assignment
        self.assertEqual(quads[3].operator, '=')

    def test_temp_variable_numbering(self):
        """Test: Temporary variables are numbered correctly."""
        code = """
        program test;
        var a, b, c, d, result : int;
        main() {
            result = a + b;
            result = c + d;
        }
        end
        """
        self.parser.parse(code)
        quads = self.parser.get_quadruples()

        # Check that temps are numbered sequentially
        temps = set()
        for quad in quads:
            if quad.result and quad.result.startswith('t'):
                temps.add(quad.result)

        self.assertEqual(temps, {'t1', 't2'})


def run_tests():
    """Run all tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuadrupleGeneration)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == '__main__':
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
