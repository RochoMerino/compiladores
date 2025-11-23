import sys
import os

# ---------------------------------------------------------
# CONFIGURACION DE IMPORTACIONES
# ---------------------------------------------------------
# Agregamos el directorio 'src' al path para poder importar los modulos directamente
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

from parser import PatitoParser

def demo_parser():
    print("="*60)
    print("DEMOSTRACION: ANALISIS SINTACTICO (PARSER)")
    print("="*60)
    
    # 1. Codigo Fuente
    codigo = """
    program test;
    var x, y : int;
    main() {
        x = 5;
        y = 10;
        x = x + y;
        print(x);
    }
    end
    """
    print("CODIGO DE ENTRADA:")
    print("-" * 60)
    print(codigo.strip())
    print("-" * 60)
    
    # 2. Inicializar Parser
    print("\nIniciando Parser...")
    parser = PatitoParser()
    
    # 3. Parsear
    try:
        print("Analizando estructura gramatical...")
        parser.parse(codigo)
        print("\n¡ANALISIS EXITOSO! El codigo respeta la gramatica.")
        
        # 4. Ver el resultado (Cuadruplos)
        print("\nRESULTADO: Cuadruplos Generados")
        parser.print_quadruples()
        
    except Exception as e:
        print(f"\nERROR DE SINTAXIS: {e}")

if __name__ == "__main__":
    demo_parser()
