"""
Script para probar archivos .patito y verificar análisis semántico.
"""

import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patito.parser import PatitoParser
from patito.errors import PatitoError


def test_file(filename):
    """
    Prueba un archivo .patito.

    Args:
        filename (str): Nombre del archivo a probar
    """
    filepath = os.path.join(os.path.dirname(__file__), filename)

    print(f"\n{'='*70}")
    print(f"PROBANDO: {filename}")
    print(f"{'='*70}\n")

    # Leer archivo
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"ERROR: Archivo '{filename}' no encontrado")
        return

    print("Código fuente:")
    print("-" * 70)
    print(code)
    print("-" * 70)

    # Parsear y analizar semánticamente
    parser = PatitoParser()

    try:
        result = parser.parse(code)
        print("\n✓ COMPILACIÓN EXITOSA")
        print("\nInformación semántica:")
        parser.print_semantic_info()

    except PatitoError as e:
        print(f"\n✗ ERROR DETECTADO:")
        print(f"   {e}")
        print(f"\n   Tipo: {type(e).__name__}")

    except Exception as e:
        print(f"\n✗ ERROR INESPERADO:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Probar archivo especificado
        test_file(sys.argv[1])
    else:
        # Probar varios archivos
        test_files = [
            'valid_program.patito',
            'error_duplicate_var.patito',
            'error_undefined_var.patito',
            'error_type_mismatch.patito',
        ]

        for filename in test_files:
            test_file(filename)
            print("\n")
