#!/usr/bin/env python3
"""
Patito Compiler - Main compilation script
Compiles .patito files and displays generated quadruples.
"""

import sys
import os

# Add patito module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patito.parser import PatitoParser


def compile_file(filename):
    """Compile a Patito source file and display quadruples."""
    print("="*70)
    print(f"COMPILING: {filename}")
    print("="*70)

    try:
        with open(filename, 'r') as f:
            code = f.read()

        print("\nSOURCE CODE:")
        print("-"*70)
        print(code)
        print("-"*70)

        parser = PatitoParser()
        result = parser.parse(code)

        print("\nCOMPILATION SUCCESSFUL")
        print()

        parser.print_semantic_info()
        parser.print_quadruples()

        return True

    except FileNotFoundError:
        print(f"\nERROR: File '{filename}' not found")
        return False

    except Exception as e:
        print(f"\nCOMPILATION ERROR:")
        print(f"  {type(e).__name__}: {e}")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 compile_patito.py <file.patito>")
        print("\nExample test files:")
        print("  python3 compile_patito.py tests/test_arithmetic.patito")
        print("  python3 compile_patito.py tests/test_relational.patito")
        print("  python3 compile_patito.py tests/test_complex_expr.patito")
        print("  python3 compile_patito.py tests/test_print_simple.patito")
        sys.exit(1)

    filename = sys.argv[1]
    success = compile_file(filename)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
