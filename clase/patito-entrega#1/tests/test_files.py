#!/usr/bin/env python3
import sys
from patito import PatitoParser

if len(sys.argv) < 2:
    print("Usage: python3 test_file.py <file.patito>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    code = f.read()

parser = PatitoParser()
try:
    result = parser.parse(code)
    print(f'✓ {filename} is syntactically correct!')
    print(f'Program name: {result[1]}')
except Exception as e:
    print(f'✗ Syntax error in {filename}:')
    print(f'   {e}')