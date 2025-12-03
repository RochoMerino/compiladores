"""
Para probar el parser
<pythonversion> test_parser.py
"""

import sys
sys.path.insert(0, '..')

from patito.parser import PatitoParser
from patito.errors import SyntaxError as PatitoSyntaxError


def test_simple_program():
    """Test parsing a minimal valid program"""
    parser = PatitoParser()
    
    code = """
    program test;
    main() {
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Simple program test passed")


def test_variable_declarations():
    """Test parsing variable declarations"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x, y : int;
        z : float;
    main() {
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Variable declarations test passed")


def test_assignment():
    """Test parsing assignment statements"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int;
    main() {
        x = 5;
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Assignment test passed")


def test_arithmetic_expressions():
    """Test parsing arithmetic expressions"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x, y, z : int;
    main() {
        x = 5 + 3;
        y = 10 - 2;
        z = x * y / 2;
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Arithmetic expressions test passed")


def test_comparison_expressions():
    """Test parsing comparison expressions"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x, y : int;
    main() {
        x = 5 > 3;
        y = 10 < 20;
        x = y != x;
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Comparison expressions test passed")


def test_if_statement():
    """Test parsing if statements"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int;
    main() {
        if (x > 5) {
            x = 10;
        };
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ If statement test passed")


def test_if_else_statement():
    """Test parsing if-else statements"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int;
    main() {
        if (x > 5) {
            x = 10;
        } else {
            x = 0;
        };
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ If-else statement test passed")


def test_while_loop():
    """Test parsing while loops"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int;
    main() {
        while (x < 10) do {
            x = x + 1;
        };
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ While loop test passed")


def test_print_statement():
    """Test parsing print statements"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int;
    main() {
        print("Hello", x, "World");
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Print statement test passed")


def test_function_declaration():
    """Test parsing function declarations"""
    parser = PatitoParser()
    
    code = """
    program test;
    
    void myFunc(x : int, y : float) [
        var z : int;
    {
        z = x + 1;
    }
    ];
    
    main() {
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Function declaration test passed")


def test_function_call():
    """Test parsing function calls"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int;
    main() {
        myFunc(x, 5);
        otherFunc();
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Function call test passed")


def test_complex_expression():
    """Test parsing complex expressions with precedence"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x, y : int;
    main() {
        x = 5 + 3 * 2 - 1;
        y = (5 + 3) * 2;
        x = -5 + +3;
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Complex expression test passed")


def test_syntax_error_missing_semicolon():
    """Test that syntax errors are detected"""
    parser = PatitoParser()
    
    code = """
    program test;
    var x : int
    main() {
    }
    end
    """
    
    try:
        result = parser.parse(code)
        assert False, "Should have raised a syntax error"
    except PatitoSyntaxError:
        print("✓ Syntax error detection test passed")


def test_complete_program():
    """Test a complete program with multiple features"""
    parser = PatitoParser()
    
    code = """
    program calculator;
    var a, b : int;
        result : float;
    
    void sum(x : int, y : int) [
        var temp : int;
    {
        temp = x + y;
        print("Sum:", temp);
    }
    ];
    
    main() {
        a = 10;
        b = 5;
        result = a + b * 2.5;
        
        if (result > 15) {
            print("Result is large:", result);
        } else {
            print("Result is small:", result);
        };
        
        while (a < 20) do {
            a = a + 1;
        };
        
        sum(a, b);
    }
    end
    """
    
    result = parser.parse(code)
    assert result is not None
    print("✓ Complete program test passed")


def run_all_tests():
    """Run all parser tests"""
    print("\n========== PARSER TESTS ==========")
    test_simple_program()
    test_variable_declarations()
    test_assignment()
    test_arithmetic_expressions()
    test_comparison_expressions()
    test_if_statement()
    test_if_else_statement()
    test_while_loop()
    test_print_statement()
    test_function_declaration()
    test_function_call()
    test_complex_expression()
    test_syntax_error_missing_semicolon()
    test_complete_program()
    print("==================================")
    print("All parser tests passed! ✓\n")


if __name__ == '__main__':
    run_all_tests()

