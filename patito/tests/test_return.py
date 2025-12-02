import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.append(src_path)

from parser import PatitoParser
from virtual_machine import VirtualMachine

def test_return():
    print("="*60)
    print("TEST: FUNCTION RETURN VALUES")
    print("="*60)
    
    codigo = """
    program test_return;
    var x, y, z : int;
    
    int suma(a: int, b: int) [
        {
            return a + b;
        }
    ];
    
    int factorial(n: int) [
        {
            if (n < 2) {
                return 1;
            }
            return n * factorial(n - 1);
        }
    ];
    
    
    main() {
        x = 5;
        /* print("Probando suma..."); */
        /* x = suma(5, 10); */
        print("Resultado suma (5+10):", x);
        
        print("Probando expresion con llamada...");
        y = suma(2, 3) * 2;
        print("Resultado (2+3)*2:", y);
        
        print("Probando factorial (recursivo)...");
        z = factorial(5);
        print("Factorial de 5:", z);
    }
    end
    """
    
    print("CODIGO:")
    print(codigo)
    print("-" * 60)
    
    # 1. Compile
    print("\n1. COMPILANDO...")
    parser = PatitoParser()
    try:
        parser.parse(codigo)
        print("Compilacion Exitosa!")
        
        quads = parser.get_quadruples()
        print(f"Generados {len(quads)} cuadruplos.")
        # parser.print_quadruples()
        
    except Exception as e:
        print(f"Error de Compilacion: {e}")
        import traceback
        traceback.print_exc()
        return

    # 2. Execute
    print("\n2. EJECUTANDO EN MAQUINA VIRTUAL...")
    vm = VirtualMachine()
    vm.load_quadruples(quads)
    
    # Load constants
    constants = parser.semantic.memory_manager.get_constants()
    vm.set_constants(constants)
    
    vm.execute()

if __name__ == "__main__":
    test_return()
