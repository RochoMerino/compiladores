# Patito Compiler - Entrega #3: Generacion de Cuadruplos

## Descripcion

Esta entrega implementa la generacion de codigo intermedio (cuadruplos) para el compilador Patito. Los cuadruplos son instrucciones de tres direcciones que representan expresiones aritmeticas, relacionales y estatutos lineales.

## Que se Implemento

### Estructuras de Datos

1. **Stack (stack.py)** - Pila generica LIFO reutilizada de tarea1
2. **TempManager (temp_manager.py)** - Generador de variables temporales (t1, t2, ...)
3. **QuadrupleGenerator (quadruple_generator.py)** - Cola FIFO de cuadruplos
4. **OperandStack (operand_stack.py)** - Pila de operandos
5. **OperatorStack (operator_stack.py)** - Pila de operadores con precedencia
6. **TypeStack (type_stack.py)** - Pila de tipos sincronizada con operandos

### Puntos Neuralgicos

- **PN_PUSH_OPERAND**: Push de variables y constantes a pilas
- **PN_OPERATION**: Generacion de cuadruplos para operaciones aritmeticas
- **PN_RELATIONAL**: Generacion de cuadruplos para operadores relacionales
- **PN_ASSIGNMENT**: Generacion de cuadruplos de asignacion
- **PN_PRINT**: Generacion de cuadruplos para print statements

### Caracteristicas

- Respeta precedencia de operadores (*, / > +, - > comparaciones)
- Genera variables temporales unicas para resultados intermedios
- Maneja parentesis correctamente
- Soporta expresiones complejas y anidadas
- Genera cuadruplos para print con strings y expresiones

## Estructura del Proyecto

```
patito-entrega#3/
├── patito/
│   ├── lexer.py                  # Analizador lexico
│   ├── parser.py                 # Parser con generacion de cuadruplos
│   ├── semantic_analyzer.py      # Analisis semantico
│   ├── semantic_cube.py          # Cubo semantico
│   ├── variable_table.py         # Tabla de variables
│   ├── function_directory.py     # Directorio de funciones
│   ├── stack.py                  # Pila generica (NEW)
│   ├── temp_manager.py           # Variables temporales (NEW)
│   ├── quadruple_generator.py    # Generador de cuadruplos (NEW)
│   ├── operand_stack.py          # Pila de operandos (NEW)
│   ├── operator_stack.py         # Pila de operadores (NEW)
│   ├── type_stack.py             # Pila de tipos (NEW)
│   └── errors.py                 # Excepciones personalizadas
├── tests/
│   ├── test_arithmetic.patito    # Test: expresiones aritmeticas
│   ├── test_complex_expr.patito  # Test: precedencia de operadores
│   ├── test_relational.patito    # Test: operadores relacionales
│   ├── test_print_simple.patito  # Test: print statements
│   └── test_quadruples.py        # Tests automatizados (NEW)
├── docs/
│   └── DOCUMENTACION_CUADRUPLOS.md  # Documentacion completa (NEW)
└── compile_patito.py             # Script principal (NEW)
```

## Como Usar

### Compilar un Programa

```bash
python3 compile_patito.py tests/test_arithmetic.patito
```

Esto mostrara:
1. Codigo fuente
2. Informacion semantica (variables, funciones)
3. Cuadruplos generados en formato tabla

### Ejecutar Tests

```bash
python3 tests/test_quadruples.py
```

Tests incluyen:
- Asignaciones simples
- Expresiones aritmeticas
- Precedencia de operadores
- Parentesis
- Operadores relacionales
- Multiples operaciones
- Print statements
- Numeracion de temporales

### Ejemplos de Salida

**Entrada:**
```patito
program test;
var x, y, z : int;
main() {
    x = 5;
    y = 10;
    z = x + y * 2;
}
end
```

**Cuadruplos Generados:**
```
#     Operator   Operand1        Operand2        Result
--------------------------------------------------------------
0     =          5               _               x
1     =          10              _               y
2     *          y               2               t1
3     +          x               t1              t2
4     =          t2              _               z
```

## Archivos de Prueba

### test_arithmetic.patito
Expresiones aritmeticas basicas (suma, multiplicacion)

### test_complex_expr.patito
Expresiones complejas con multiples operadores y parentesis
Demuestra precedencia correcta

### test_relational.patito
Operadores relacionales (>, <, !=)

### test_print_simple.patito
Print con strings literales y expresiones

## Formato de Cuadruplos

Cada cuadruplo tiene el formato:
```
(operador, operando1, operando2, resultado)
```

**Operadores soportados:**
- Aritmeticos: +, -, *, /
- Relacionales: >, <, !=
- Asignacion: =
- Salida: PRINT
- Unarios: unary-

**Operandos:**
- Variables de usuario: x, y, result
- Constantes: 5, 10, 3.14
- Temporales: t1, t2, t3, ...
- Strings: "mensaje"

## Precedencia de Operadores

1. `*`, `/` (Nivel 2 - mas alta)
2. `+`, `-` (Nivel 1)
3. `>`, `<`, `!=` (Nivel 0)
4. `=` (Nivel -1 - mas baja)

## Decisiones de Diseno

### SDT vs AST
Se usa Syntax-Directed Translation (SDT) en lugar de construir un AST completo:
- Generacion durante el parsing (un solo pase)
- Menor uso de memoria
- Mas eficiente
- Alineado con teoria clasica de compiladores

### Variables Temporales
Formato: t1, t2, t3, ...
- Claramente distinguibles de variables de usuario
- Facil de generar
- Simple de debuggear

### Pilas Especializadas
Tres pilas separadas (operandos, operadores, tipos):
- Clara separacion de responsabilidades
- Facil de entender y mantener
- Sincronizacion explicita entre operandos y tipos

## Validaciones

El sistema mantiene todas las validaciones semanticas de entrega#2:
- Variables declaradas
- Compatibilidad de tipos
- Operaciones validas
- Scope de variables

Mas nuevas validaciones:
- Precedencia correcta de operadores
- Generacion de temporales unicos
- Sincronizacion de pilas

## Documentacion

Ver `docs/DOCUMENTACION_CUADRUPLOS.md` para:
- Descripcion detallada de pilas y cola
- Algoritmos de traduccion
- Diagramas de sintaxis con puntos neuralgicos
- Ejemplos paso a paso
- Explicacion de cada punto neuralgico

## Dependencias

- Python 3.x
- PLY (Python Lex-Yacc)
- Modulos estandar de Python

## Autor

Implementacion para el curso de Compiladores
