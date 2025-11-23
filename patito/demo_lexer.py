import sys
import os

# ---------------------------------------------------------
# CONFIGURACION DE IMPORTACIONES
# ---------------------------------------------------------
# Agregamos el directorio 'src' al path para poder importar los modulos directamente
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

from lexer import PatitoLexer

def demo_lexer():
    print("="*50)
    print("DEMOSTRACION: ANALISIS LEXICO (LEXER)")
    print("="*50)
    
    # 1. El Codigo Fuente (Texto plano)
    codigo = """
    program test;
    var x, y : int;
    main() {
        x = 5;
        y = 10;
        x = x + y;
        x = x + 2;
        print(x);
    }
    end
    """
    print(f"Entrada: '{codigo}'")
    print("-" * 50)
    
    # 2. El Lexer (La maquina de fichas)
    lexer = PatitoLexer()
    lexer.build()
    
    # 3. Tokenizacion (Convertir texto a fichas)
    print(f"{'TIPO':<15} {'VALOR':<10} {'LINEA':<5}")
    print("-" * 50)
    
    tokens = lexer.tokenize(codigo)
    
    for token in tokens:
        print(f"{token.type:<15} {str(token.value):<10} {token.lineno:<5}")
        
    print("-" * 50)
    print(f"Total tokens encontrados: {len(tokens)}")

if __name__ == "__main__":
    demo_lexer()
