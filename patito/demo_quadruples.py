import sys
import os

# ---------------------------------------------------------
# CONFIGURACION DE IMPORTACIONES
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.append(src_path)

from quadruple_generator import QuadrupleGenerator
from operand_stack import OperandStack
from operator_stack import OperatorStack
from temp_manager import TempManager

def print_state(step_name, op_stack, oper_stack, quads):
    print(f"\n--- {step_name} ---")
    print(f"Pila Operandos:  {op_stack.stack}")
    print(f"Pila Operadores: {oper_stack.stack}")
    if quads.quadruples:
        print(f"Ultimo Cuadruplo: {quads.quadruples[-1]}")
    else:
        print(f"Ultimo Cuadruplo: (Ninguno)")

def demo_quadruples():
    print("="*60)
    print("DEMOSTRACION: GENERACION DE CUADRUPLOS (EL GRAN FINAL)")
    print("="*60)
    print("Vamos a simular paso a paso la expresion: x = a + b * c")
    print("Objetivo: Respetar la precedencia (* va antes que +)")
    
    # Inicializar componentes
    quad_gen = QuadrupleGenerator()
    op_stack = OperandStack()
    oper_stack = OperatorStack()
    temp_mgr = TempManager()
    
    # 1. x = ...
    print("\n1. Leyendo 'x ='")
    op_stack.push_operand('x')
    oper_stack.push('=')
    print_state("Estado Inicial", op_stack, oper_stack, quad_gen)
    
    # 2. ... a + ...
    print("\n2. Leyendo 'a +'")
    op_stack.push_operand('a')
    oper_stack.push('+')
    print_state("Push a, +", op_stack, oper_stack, quad_gen)
    
    # 3. ... b * ...
    print("\n3. Leyendo 'b *'")
    op_stack.push_operand('b')
    oper_stack.push('*')
    print_state("Push b, *", op_stack, oper_stack, quad_gen)
    
    # 4. ... c
    print("\n4. Leyendo 'c'")
    op_stack.push_operand('c')
    print_state("Push c", op_stack, oper_stack, quad_gen)
    
    # 5. Resolver Multiplicacion (*)
    # El parser detecta que * tiene mayor precedencia que lo que sigue (o fin de linea)
    print("\n5. Resolviendo Multiplicacion (*)")
    print("   -> Sacamos c, b y *")
    right = op_stack.pop_operand()
    left = op_stack.pop_operand()
    operator = oper_stack.pop()
    
    # Generamos temporal
    temp = temp_mgr.generate()
    print(f"   -> Generamos temporal {temp}")
    
    quad_gen.generate(operator, left, right, temp)
    op_stack.push_operand(temp)
    
    print_state("Despues de Multiplicar", op_stack, oper_stack, quad_gen)
    
    # 6. Resolver Suma (+)
    print("\n6. Resolviendo Suma (+)")
    print("   -> Sacamos t1, a y +")
    right = op_stack.pop_operand()
    left = op_stack.pop_operand()
    operator = oper_stack.pop()
    
    temp = temp_mgr.generate()
    print(f"   -> Generamos temporal {temp}")
    
    quad_gen.generate(operator, left, right, temp)
    op_stack.push_operand(temp)
    
    print_state("Despues de Sumar", op_stack, oper_stack, quad_gen)
    
    # 7. Resolver Asignacion (=)
    print("\n7. Resolviendo Asignacion (=)")
    print("   -> Sacamos t2, x y =")
    res = op_stack.pop_operand()
    target = op_stack.pop_operand() 
    operator = oper_stack.pop()
    
    quad_gen.generate(operator, res, None, target)
    
    print_state("Despues de Asignar", op_stack, oper_stack, quad_gen)
    
    print("\n" + "="*60)
    print("RESULTADO FINAL: TABLA DE CUADRUPLOS")
    quad_gen.print_quadruples()

if __name__ == "__main__":
    demo_quadruples()
