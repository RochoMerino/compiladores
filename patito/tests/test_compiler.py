import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.append(src_path)

from parser import PatitoParser
from virtual_machine import VirtualMachine

def test_compiler():
    print("="*60)
    print("TEST: COMPILER & VIRTUAL MACHINE")
    print("="*60)
    
    codigo = """
    program test;
    var x, y : int;
    
    void suma(a: int, b: int) [
        var t : int;
        {
            t = a + b;
            print("Suma:", t);
        }
    ];
    
    main() {
        x = 5;
        y = 10;
        
        print("Iniciando...");
        
        if (x < y) {
            print("x es menor que y");
        } else {
            print("x es mayor o igual que y");
        }
        
        while (x < 8) do {
            print("x vale:", x);
            x = x + 1;
        }
        
        suma(x, y);
        
        print("Fin");
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
        parser.print_quadruples()
        
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
    print(f"Cargando {len(constants)} constantes.")
    vm.set_constants(constants)
    
    vm.execute()

if __name__ == "__main__":
    test_compiler()
