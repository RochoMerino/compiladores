import sys
import os

# ---------------------------------------------------------
# CONFIGURACION DE IMPORTACIONES
# ---------------------------------------------------------
# Agregamos el directorio 'src' al path para poder importar los modulos directamente
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

from semantic_cube import SemanticCube
from variable_table import VariableTable

def demo_semantics():
    print("="*60)
    print("DEMOSTRACION: SEMANTICA (EL CEREBRO)")
    print("="*60)
    
    # PARTE 1: EL CUBO SEMANTICO
    # Es el juez que decide que operaciones son validas.
    print("\n1. EL CUBO SEMANTICO (Reglas de Tipos)")
    print("-" * 60)
    cube = SemanticCube()
    
    casos_prueba = [
        ('int', '+', 'int'),      # 5 + 10
        ('int', '+', 'float'),    # 5 + 10.5
        ('int', '=', 'float'),    # x = 10.5 (donde x es int)
        ('int', '>', 'int'),      # 5 > 10
        ('int', '+', 'string')    # 5 + "hola" (Deberia fallar)
    ]
    
    for t1, op, t2 in casos_prueba:
        resultado = cube.get_result_type(t1, op, t2)
        status = "VALIDO" if resultado else "INVALIDO"
        res_str = resultado if resultado else "ERROR"
        print(f"Operacion: {t1:6} {op:2} {t2:6} -> Resultado: {res_str} ({status})")

    # PARTE 2: LA TABLA DE VARIABLES
    # Es la memoria del compilador.
    print("\n2. LA TABLA DE VARIABLES (Memoria)")
    print("-" * 60)
    tabla = VariableTable('main')
    
    print("Declarando variables...")
    tabla.add_variable('x', 'int', 'local', 1)
    tabla.add_variable('y', 'float', 'local', 2)
    print(f"Variables en memoria: {tabla.count()}")
    
    print("\nConsultando variables:")
    vars_a_buscar = ['x', 'y', 'z']
    for var in vars_a_buscar:
        info = tabla.lookup(var)
        if info:
            print(f"  Variable '{var}': Encontrada! Tipo: {info.var_type}")
        else:
            print(f"  Variable '{var}': NO EXISTE (Error Semantico)")

if __name__ == "__main__":
    demo_semantics()
