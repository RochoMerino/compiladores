"""
Para probar el lexer
<pythonversion> test_lexer.py
"""

import sys
sys.path.insert(0, '..')

from patito.lexer import PatitoLexer


def test_keywords():
    """Test that keywords are recognized correctly"""
    lexer = PatitoLexer()
    lexer.build()
    
    code = "program var int float void main if else while do print end"
    tokens = lexer.tokenize(code)
    
    expected_types = ['PROGRAM', 'VAR', 'INT', 'FLOAT', 'VOID', 'MAIN', 
                     'IF', 'ELSE', 'WHILE', 'DO', 'PRINT', 'END']
    
    assert len(tokens) == len(expected_types)
    for token, expected in zip(tokens, expected_types):
        assert token.type == expected
    
    print("✓ Keywords test passed")


def test_identifiers():
    """Test identifier recognition"""
    lexer = PatitoLexer()
    lexer.build()
    
    code = "x y variable123 myVar test_var"
    tokens = lexer.tokenize(code)
    
    assert len(tokens) == 5
    for token in tokens:
        assert token.type == 'ID'
    
    print("✓ Identifiers test passed")


def test_numbers():
    """Test integer and float literals"""
    lexer = PatitoLexer()
    lexer.build()
    
    # Test integers
    code = "42 -10 +5"
    tokens = lexer.tokenize(code)
    assert tokens[0].type == 'CTE_INT'
    assert tokens[0].value == 42
    assert tokens[1].type == 'CTE_INT'
    assert tokens[1].value == -10
    assert tokens[2].type == 'CTE_INT'
    assert tokens[2].value == 5
    
    # Test floats
    code = "3.14 -2.5 +1.0"
    tokens = lexer.tokenize(code)
    assert tokens[0].type == 'CTE_FLOAT'
    assert tokens[0].value == 3.14
    assert tokens[1].type == 'CTE_FLOAT'
    assert tokens[1].value == -2.5
    
    print("✓ Numbers test passed")


def test_strings():
    """Test string literals"""
    lexer = PatitoLexer()
    lexer.build()
    
    code = '"hello" "world 123" "test"'
    tokens = lexer.tokenize(code)
    
    assert len(tokens) == 3
    assert tokens[0].type == 'CTE_STRING'
    assert tokens[0].value == 'hello'
    assert tokens[1].value == 'world 123'
    
    print("✓ Strings test passed")


def test_operators():
    """Test arithmetic and comparison operators"""
    lexer = PatitoLexer()
    lexer.build()
    
    code = "+ - * / > < != ="
    tokens = lexer.tokenize(code)
    
    expected_types = ['PLUS', 'MINUS', 'MULT', 'DIV', 'GT', 'LT', 'NEQ', 'EQ']
    
    assert len(tokens) == len(expected_types)
    for token, expected in zip(tokens, expected_types):
        assert token.type == expected
    
    print("✓ Operators test passed")


def test_delimiters():
    """Test delimiters and punctuation"""
    lexer = PatitoLexer()
    lexer.build()
    
    code = "( ) { } [ ] , ; :"
    tokens = lexer.tokenize(code)
    
    expected_types = ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 
                     'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON', 'COLON']
    
    assert len(tokens) == len(expected_types)
    for token, expected in zip(tokens, expected_types):
        assert token.type == expected
    
    print("✓ Delimiters test passed")


def test_comments():
    """Test that comments are ignored"""
    lexer = PatitoLexer()
    lexer.build()
    
    # Line comment
    code = "var x // this is a comment\n int"
    tokens = lexer.tokenize(code)
    assert len(tokens) == 3
    assert tokens[0].type == 'VAR'
    assert tokens[1].type == 'ID'
    assert tokens[2].type == 'INT'
    
    # Block comment
    code = "var /* comment */ int"
    tokens = lexer.tokenize(code)
    assert len(tokens) == 2
    assert tokens[0].type == 'VAR'
    assert tokens[1].type == 'INT'
    
    print("✓ Comments test passed")


def test_complete_statement():
    """Test a complete variable declaration statement"""
    lexer = PatitoLexer()
    lexer.build()
    
    code = "var x, y : int;"
    tokens = lexer.tokenize(code)
    
    expected = ['VAR', 'ID', 'COMMA', 'ID', 'COLON', 'INT', 'SEMICOLON']
    
    assert len(tokens) == len(expected)
    for token, expected_type in zip(tokens, expected):
        assert token.type == expected_type
    
    print("✓ Complete statement test passed")


def run_all_tests():
    """Run all lexer tests"""
    print("\n========== LEXER TESTS ==========")
    test_keywords()
    test_identifiers()
    test_numbers()
    test_strings()
    test_operators()
    test_delimiters()
    test_comments()
    test_complete_statement()
    print("=================================")
    print("All lexer tests passed! ✓\n")


if __name__ == '__main__':
    run_all_tests()

