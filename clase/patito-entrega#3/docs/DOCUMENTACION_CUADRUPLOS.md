# Generacion de Codigo Intermedio - Cuadruplos

---

## Introduccion

La generacion de codigo intermedio traduce el codigo fuente de Patito a una representacion de bajo nivel llamada cuadruplos. Los cuadruplos son instrucciones de tres direcciones que representan operaciones basicas y forman el puente entre el analisis semantico y la generacion de codigo objeto.

Este documento describe la implementacion de la traduccion a cuadruplos para expresiones aritmeticas, relacionales y estatutos lineales del lenguaje Patito.

---

## Estructuras de Datos

### Pilas (LIFO - Last In First Out)

El algoritmo de traduccion utiliza tres pilas principales que trabajan en conjunto durante el analisis sintactico:

#### Pila de Operandos

**Proposito:** Almacenar operandos durante la evaluacion de expresiones.

**Contenido:** Nombres de variables, constantes numericas y variables temporales.

**Operaciones:**
- `push_operand(operand)`: Agregar un operando al tope
- `pop_operand()`: Remover y retornar el operando del tope
- `peek_operand()`: Ver el operando del tope sin removerlo

**Ejemplo:**
```
Expresion: a + b * c

Estado de la pila durante el analisis:
1. [a]           <- se lee 'a'
2. [a, b]        <- se lee 'b'
3. [a, b, c]     <- se lee 'c'
4. [a, t1]       <- se genera t1 = b * c
5. [t2]          <- se genera t2 = a + t1
```

#### Pila de Operadores

**Proposito:** Almacenar operadores respetando precedencia durante evaluacion de expresiones.

**Contenido:** Operadores aritmeticos (+, -, *, /) y relacionales (>, <, !=)

**Precedencia:** Los operadores tienen niveles de precedencia que determinan el orden de ejecucion:
- Nivel 2: *, / (mas alta)
- Nivel 1: +, -
- Nivel 0: >, <, !=
- Nivel -1: = (mas baja)

**Operaciones:**
- `push_operator(op)`: Agregar operador al tope
- `pop_operator()`: Remover y retornar operador del tope
- `get_precedence(op)`: Obtener precedencia de un operador
- `should_reduce(op)`: Verificar si se debe generar cuadruplo

**Ejemplo:**
```
Expresion: a + b * c

Estado durante analisis:
1. []            <- inicio
2. [+]           <- se lee '+'
3. [+, *]        <- se lee '*' (mayor precedencia, no se reduce)
4. [+]           <- se procesa '*' primero
5. []            <- se procesa '+'
```

#### Pila de Tipos

**Proposito:** Mantener informacion de tipos correspondiente a los operandos.

**Contenido:** Tipos de datos ('int', 'float')

**Operaciones:**
- `push_type(type)`: Agregar tipo al tope
- `pop_type()`: Remover y retornar tipo del tope

**Sincronizacion:** Esta pila debe estar siempre sincronizada con la pila de operandos. Cada operando tiene su tipo correspondiente.

**Ejemplo:**
```
Expresion: x + y * 2.5
Tipos: x:int, y:int, 2.5:float

Pila de operandos: [x, y, 2.5]
Pila de tipos:     [int, int, float]
```

### Cola de Cuadruplos (FIFO - First In First Out)

**Proposito:** Almacenar la secuencia de cuadruplos generados en orden de ejecucion.

**Estructura:** Lista ordenada de cuadruplos donde cada cuadruplo tiene el formato:
```
(operador, operando1, operando2, resultado)
```

**Componentes de un Cuadruplo:**
- **Operador:** La operacion a realizar (+, -, *, /, >, <, !=, =, PRINT, etc.)
- **Operando1:** Primer operando (variable, constante, temporal)
- **Operando2:** Segundo operando (puede ser None para operaciones unarias)
- **Resultado:** Destino del resultado (variable o temporal)

**Operaciones:**
- `generate(op, op1, op2, result)`: Generar y agregar nuevo cuadruplo
- `get_quadruples()`: Obtener lista completa de cuadruplos
- `get_next_address()`: Obtener direccion del siguiente cuadruplo
- `fill_quad(index, value)`: Llenar cuadruplo pendiente (para saltos)

### Generador de Temporales

**Proposito:** Crear variables temporales unicas para almacenar resultados intermedios.

**Formato:** t1, t2, t3, ..., tn

**Operaciones:**
- `generate()`: Generar nueva variable temporal
- `reset()`: Reiniciar contador
- `get_count()`: Obtener numero de temporales generados

**Ejemplo:**
```
Expresion: a + b * c

Temporales generados:
t1 = b * c
t2 = a + t1
```

---

## Puntos Neuralgicos

Los puntos neuralgicos son ubicaciones estrategicas en la gramatica donde se ejecutan acciones para generar cuadruplos. Cada punto neuralgico corresponde a una construccion del lenguaje.

### PN_PUSH_OPERAND: Reconocimiento de Operandos

**Ubicacion:** Al reconocer un ID o constante en la regla de `factor`

**Accion:**
1. Obtener valor del operando (variable o constante)
2. Obtener tipo del operando del analizador semantico
3. Push operando a pila de operandos
4. Push tipo a pila de tipos

**Ejemplo:**
```
Regla: factor -> ID
Codigo: x + y

Al reconocer 'x':
  operand_stack.push('x')
  type_stack.push('int')

Al reconocer 'y':
  operand_stack.push('y')
  type_stack.push('int')
```

### PN_PUSH_OPERATOR: Reconocimiento de Operadores

**Ubicacion:** Al reconocer operadores en reglas de expresiones

**Accion:**
1. Push operador a pila de operadores

**Nota:** Este punto neuralgico es implicito en la gramatica. Los operadores se procesan cuando se completa la regla.

### PN_OPERATION: Generacion de Cuadruplos Aritmeticos

**Ubicacion:** Al completar reglas de `exp` (suma/resta) y `termino` (multiplicacion/division)

**Accion:**
1. Pop dos operandos de la pila
2. Pop dos tipos de la pila
3. Verificar operacion valida con cubo semantico
4. Generar variable temporal
5. Generar cuadruplo (operador, operando_izq, operando_der, temporal)
6. Push temporal a pila de operandos
7. Push tipo resultado a pila de tipos

**Diagrama:**
```
Regla: exp -> exp PLUS termino

Al completar la regla:

Pilas antes:                    Cuadruplo generado:
operand_stack: [a, b]           (+ a b t1)
type_stack: [int, int]

Pilas despues:
operand_stack: [t1]
type_stack: [int]
```

**Ejemplo Completo:**
```
Expresion: a + b * c

Paso 1: Leer 'a'
  operand_stack: [a]

Paso 2: Leer '+'
  (operador almacenado implicitamente)

Paso 3: Leer 'b'
  operand_stack: [a, b]

Paso 4: Leer '*'
  (operador almacenado implicitamente)

Paso 5: Leer 'c'
  operand_stack: [a, b, c]

Paso 6: Completar 'termino' (b * c)
  Pop: c, b
  Generar: (* b c t1)
  Push: t1
  operand_stack: [a, t1]

Paso 7: Completar 'exp' (a + t1)
  Pop: t1, a
  Generar: (+ a t1 t2)
  Push: t2
  operand_stack: [t2]
```

### PN_RELATIONAL: Operadores Relacionales

**Ubicacion:** Al completar regla de `expression` con operadores >, <, !=

**Accion:**
Similar a PN_OPERATION pero para operadores relacionales.

**Ejemplo:**
```
Expresion: a > b

Cuadruplo generado:
(> a b t1)
```

### PN_ASSIGNMENT: Asignaciones

**Ubicacion:** Al completar regla de `assign`

**Accion:**
1. Pop operando (resultado de expresion) de la pila
2. Pop tipo de la pila
3. Verificar compatibilidad de tipos
4. Generar cuadruplo (= operando _ variable)

**Diagrama:**
```
Regla: assign -> ID EQ expression SEMICOLON

Al completar:

Pilas antes:                    Cuadruplo generado:
operand_stack: [t2]             (= t2 _ x)
(donde t2 es resultado de la expresion)

Pilas despues:
operand_stack: []
```

**Ejemplo:**
```
Codigo: x = a + b;

Cuadruplos generados:
1. (+ a b t1)
2. (= t1 _ x)
```

### PN_PRINT: Estatutos Print

**Ubicacion:** Al completar regla de `print`

**Accion:**
Por cada elemento en print_list:
1. Si es string literal: generar (PRINT "string" _ _)
2. Si es expresion:
   - Pop operando de la pila
   - Generar (PRINT operando _ _)

**Ejemplo:**
```
Codigo: print("Valor:", x, y + z);

Cuadruplos generados:
1. (+ y z t1)
2. (PRINT "Valor:" _ _)
3. (PRINT x _ _)
4. (PRINT t1 _ _)
```

---

## Algoritmo de Traduccion

### Algoritmo para Expresiones Aritmeticas

```
function procesar_expresion(expr):
    for each token in expr:
        if token is operand:
            PN_PUSH_OPERAND(token)

        else if token is operator:
            while operator_stack not empty and
                  precedence(top_operator) >= precedence(token):
                PN_OPERATION()

            operator_stack.push(token)

    while operator_stack not empty:
        PN_OPERATION()
```

**Caracteristicas:**
- Respeta precedencia de operadores
- Evalua de izquierda a derecha
- Los parentesis se manejan naturalmente por la gramatica

### Algoritmo para Asignaciones

```
function procesar_asignacion(variable, expresion):
    procesar_expresion(expresion)
    resultado = operand_stack.pop()
    PN_ASSIGNMENT(variable, resultado)
```

### Algoritmo para Print

```
function procesar_print(print_list):
    for each item in print_list:
        if item is expression:
            procesar_expresion(item)
            operando = operand_stack.pop()
            generate_quad(PRINT, operando, _, _)
        else if item is string:
            generate_quad(PRINT, item, _, _)
```

---

## Ejemplos Completos

### Ejemplo 1: Expresion Simple

**Codigo:**
```
x = 5 + 3;
```

**Cuadruplos:**
```
0: (+ 5 3 t1)
1: (= t1 _ x)
```

### Ejemplo 2: Precedencia de Operadores

**Codigo:**
```
result = a + b * c;
```

**Cuadruplos:**
```
0: (* b c t1)
1: (+ a t1 t2)
2: (= t2 _ result)
```

**Explicacion:** La multiplicacion se evalua primero por tener mayor precedencia.

### Ejemplo 3: Parentesis

**Codigo:**
```
result = (a + b) * c;
```

**Cuadruplos:**
```
0: (+ a b t1)
1: (* t1 c t2)
2: (= t2 _ result)
```

**Explicacion:** Los parentesis fuerzan la evaluacion de la suma primero.

### Ejemplo 4: Expresion Compleja

**Codigo:**
```
result = a + b * c / d - e;
```

**Cuadruplos:**
```
0: (* b c t1)
1: (/ t1 d t2)
2: (+ a t2 t3)
3: (- t3 e t4)
4: (= t4 _ result)
```

**Explicacion:**
1. b * c (precedencia 2)
2. t1 / d (precedencia 2, misma que *)
3. a + t2 (precedencia 1)
4. t3 - e (precedencia 1, misma que +)
5. Asignacion final

### Ejemplo 5: Operadores Relacionales

**Codigo:**
```
c = a > b;
```

**Cuadruplos:**
```
0: (> a b t1)
1: (= t1 _ c)
```

### Ejemplo 6: Print con Expresiones

**Codigo:**
```
print("Resultado:", x + y);
```

**Cuadruplos:**
```
0: (+ x y t1)
1: (PRINT "Resultado:" _ _)
2: (PRINT t1 _ _)
```

### Ejemplo 7: Programa Completo

**Codigo:**
```
program test;
var x, y, z : int;
main() {
    x = 5;
    y = 10;
    z = x + y * 2;
    print("Resultado:", z);
}
end
```

**Cuadruplos:**
```
0: (= 5 _ x)
1: (= 10 _ y)
2: (* y 2 t1)
3: (+ x t1 t2)
4: (= t2 _ z)
5: (PRINT "Resultado:" _ _)
6: (PRINT z _ _)
```

---

## Diagrama de Sintaxis con Puntos Neuralgicos

```
programa
  |
  +-- vars
  +-- funcs
  +-- main
       |
       +-- body
            |
            +-- statement_list
                 |
                 +-- statement
                      |
                      +-- assign
                      |    |
                      |    +-- ID EQ expression SEMICOLON
                      |         |            |
                      |         |            +-- [PN_OPERATION]
                      |         +-- [PN_ASSIGNMENT]
                      |
                      +-- print
                           |
                           +-- PRINT LPAREN print_list RPAREN SEMICOLON
                                          |
                                          +-- [PN_PRINT]

expression
  |
  +-- exp [GT|LT|NEQ] exp
       |               |
       |               +-- [PN_RELATIONAL]
       |
       +-- termino [PLUS|MINUS] termino
            |                   |
            |                   +-- [PN_OPERATION]
            |
            +-- factor [MULT|DIV] factor
                 |                |
                 |                +-- [PN_OPERATION]
                 |
                 +-- ID | CTE
                      |
                      +-- [PN_PUSH_OPERAND]
```

---

## Validaciones

### Verificaciones Durante Generacion

1. **Verificacion de Tipos:** Cada operacion verifica compatibilidad de tipos usando el cubo semantico antes de generar el cuadruplo.

2. **Variables Declaradas:** Solo se pueden referenciar variables previamente declaradas.

3. **Precedencia Correcta:** El algoritmo garantiza que se respeta la precedencia de operadores.

4. **Variables Temporales Unicas:** Cada temporal tiene un identificador unico.

---

## Comandos de Desarrollo

### Compilar Archivo Patito

```bash
cd patito-entrega#3
python3 compile_patito.py <archivo.patito>
```

### Ejecutar Tests de Cuadruplos

```bash
cd patito-entrega#3
python3 tests/test_quadruples.py
```

### Probar Ejemplos

```bash
# Expresiones aritmeticas
python3 compile_patito.py tests/test_arithmetic.patito

# Expresiones relacionales
python3 compile_patito.py tests/test_relational.patito

# Expresiones complejas
python3 compile_patito.py tests/test_complex_expr.patito

# Print statements
python3 compile_patito.py tests/test_print_simple.patito
```

---

## Decisiones de Diseno

### Uso de Pilas vs Arbol

Se eligio un enfoque de traduccion dirigida por sintaxis (SDT) con pilas en lugar de construir un arbol sintactico abstracto (AST) completo por las siguientes razones:

1. **Eficiencia:** La generacion de cuadruplos ocurre durante el parsing, en un solo pase
2. **Simplicidad:** No requiere almacenar y recorrer una estructura de arbol completa
3. **Memoria:** Menor consumo de memoria al no mantener el arbol completo
4. **Alineacion con teoria:** Sigue el modelo clasico de compiladores de Dragon Book

### Formato de Cuadruplos

Se eligio el formato de cuatro componentes (operador, op1, op2, resultado) por:

1. **Estandar:** Es el formato clasico usado en teoria de compiladores
2. **Legibilidad:** Facil de entender y debuggear
3. **Flexibilidad:** Soporta tanto operaciones binarias como unarias
4. **Extension:** Facil de extender para nuevas operaciones

### Variables Temporales

Se decidio usar el prefijo 't' con numeracion secuencial (t1, t2, ...) por:

1. **Claridad:** Facil identificar variables temporales vs variables de usuario
2. **Simplicidad:** Generacion trivial de nombres unicos
3. **Debug:** Facil seguir el flujo de temporales en los cuadruplos

---

Fin de la Documentacion
