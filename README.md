# Documentación Técnica del Compilador "Patito"

## Libreria que se utilizo

Para este compilador se utilizo la libreria ply (Python Lex-Yacc) la cual nos permite crear un analizador lexico y sintactico para nuestro lenguaje.

## Arquitectura del Sistema

El sistema se divide en dos componentes principales que operan secuencialmente:

1.  **El Compilador (`PatitoParser` y módulos auxiliares):** Responsable de leer el código fuente, validar su corrección sintáctica y semántica, y generar el código objeto (cuádruplos).
2.  **La Máquina Virtual (`VirtualMachine`):** Responsable de cargar el código objeto y ejecutarlo, simulando un procesador con manejo de memoria segmentada.

### Flujo de Compilación

1.  **Entrada:** Un string que representa el código fuente por ahora, estos estan definidos en @test_normal.py para un ejemplo.
2.  **Lexer (`lexer.py`):** Transforma la secuencia de caracteres en una secuencia de *tokens* (palabras reservadas, identificadores, operadores, constantes).
3.  **Parser (`parser.py`):** Analiza la estructura gramatical de la secuencia de tokens basándose en una Gramática Libre de Contexto (GLC).
4.  **Análisis Semántico (`semantic_analyzer.py`):** Verifica reglas de tipo, existencia de variables y consistencia lógica (ej. no sumar un `int` con un `string`). Basicamente opera como el cerebro de nuestra operación.
5.  **Generación de Código (`quadruple_generator.py`):** Produce una lista de instrucciones de tres direcciones (cuádruplos).
6.  **Salida:** No hay salida, por ahora el pograma utiliza una Maquina Virtual la cual recibe en memoria los cuádruplos y las constantes para su ejecución y solamente imprime todo en la terminal. No se generan archivos de salida a menos que en parser modifiques el debug=False a debug=True para poder tener un archivo de salida de la libreria de ply.

---

## Estructuras de Datos Fundamentales

Una de las características más críticas del compilador "Patito" es la selección cuidadosa de estructuras de datos para manejar la complejidad del análisis semántico y la generación de código. A continuación, se detalla el uso de **Diccionarios**, **Pilas** y **Tablas de Variables**, justificando su elección técnica.

### 1.1. Diccionarios (Tablas Hash)

El uso de diccionarios de Python (que son implementaciones de tablas hash altamente optimizadas) es omnipresente en el compilador, principalmente para la implementación de la **Tabla de Símbolos**.

#### ¿Por qué Diccionarios?
En un compilador, la operación más frecuente es la *búsqueda* de identificadores. Cada vez que el programador usa una variable `x`, el compilador debe preguntar: "¿Existe `x`?", "¿Qué tipo de dato es?", "¿Cuál es su dirección de memoria?".

*   **Complejidad Temporal:** Los diccionarios ofrecen una complejidad promedio de **O(1)** para inserciones y búsquedas. Si utilizáramos listas, la complejidad sería O(n), lo cual degradaría el rendimiento exponencialmente con el tamaño del programa.
*   **Flexibilidad:** Permiten asociar una clave (nombre de la variable) con un objeto complejo (`VariableInfo` o `FunctionInfo`) que contiene múltiples atributos.

#### Implementación en `FunctionDirectory` y `VariableTable`
*   `self.functions = {}`: Un diccionario maestro donde las claves son los nombres de las funciones (ej. "main", "calcularSuma") y los valores son instancias de `FunctionInfo`.
*   `self.variables = {}`: Dentro de cada función, existe un diccionario local donde las claves son los nombres de las variables locales y los valores son instancias de `VariableInfo`.

**Ejemplo de Estructura en Memoria:**
```python
{
    "global": { ... variables globales ... },
    "main": {
        "return_type": "void",
        "vars": {
            "i": { "type": "int", "address": 1000 },
            "resultado": { "type": "float", "address": 1001 }
        }
    },
    "factorial": {
        "return_type": "int",
        "vars": {
            "n": { "type": "int", "address": 3000 }, # Parámetro
            "temp": { "type": "int", "address": 3001 } # Local
        }
    }
}
```

### Pilas (Stacks)

Las pilas (estructuras LIFO - Last In, First Out) son el corazón de la lógica de procesamiento de expresiones y control de flujo. Se utilizan múltiples pilas especializadas para mantener el estado durante el análisis sintáctico.

#### Pila de Operandos (`operand_stack`)
*   **Función:** Almacena las direcciones de memoria de los operandos (variables y constantes) que están esperando ser procesados.
*   **Justificación:** Las expresiones matemáticas tienen una naturaleza jerárquica. En `a + b * c`, `b` y `c` deben operarse antes que `a`. La pila permite "recordar" `a` mientras se resuelve `b * c`.

#### Pila de Tipos (`type_stack`)
*   **Función:** Almacena los tipos de datos (`int`, `float`, etc.) correspondientes a los operandos en `operand_stack`.
*   **Justificación:** Esencial para el **Cubo Semántico**. Antes de generar un cuádruplo para `+`, el compilador verifica los dos tipos superiores de esta pila para asegurar que la operación es válida y determinar el tipo del resultado.

#### Pila de Saltos (`jump_stack`)
*   **Función:** Almacena índices de cuádruplos (direcciones de instrucción) que están pendientes de ser "rellenados".
*   **Justificación:** Fundamental para estructuras de control no lineales (`IF`, `WHILE`).
    *   Cuando el compilador encuentra un `IF`, genera un `GOTOF` (Ir si Falso) pero *no sabe a dónde saltar* porque aún no ha leído el bloque `ELSE` o el final del `IF`.
    *   Guarda la posición de ese `GOTOF` incompleto en la pila.
    *   Cuando encuentra el final del bloque, hace `pop` de la pila y rellena el destino del salto.
    *   La naturaleza anidada de los `IF`s (un `IF` dentro de otro) se maneja naturalmente con la estructura LIFO de la pila.

### Doble Tabla de Variables (Scoping)

El compilador implementa un manejo de ámbito (scope) mediante la clase `ScopedVariableTable`, que administra dos tablas activas simultáneamente:

1.  **Tabla Global:** Contiene variables accesibles desde cualquier punto del programa.
2.  **Tabla Local:** Contiene variables y parámetros de la función que se está analizando actualmente.

#### ¿Por qué dos tablas?
Esta arquitectura permite implementar **ocultamiento de variables (shadowing)** y garantiza la integridad de los datos locales.
*   Cuando se busca una variable, el compilador busca primero en la `local_table`. Si la encuentra, usa esa (prioridad local).
*   Si no está en la local, busca en la `global_table`.
*   Si no está en ninguna, lanza un error de "Variable no declarada".

Al terminar de compilar una función, la `local_table` se destruye (o se reinicia), liberando el contexto para la siguiente función, mientras que la `global_table` persiste.

---

## Modelo de Memoria (Memory Manager)

El `MemoryManager` es el componente encargado de asignar direcciones virtuales a cada variable y constante. Para facilitar la ejecución y la depuración, se ha optado por un modelo de **Memoria Segmentada**.

La memoria virtual se divide en rangos lógicos fijos. Esto permite saber el tipo y el alcance de una variable simplemente mirando su dirección.

### Mapa de Memoria

| Segmento | Rango de Direcciones | Descripción |
| :--- | :--- | :--- |
| **Globales** | 1000 - 2999 | Variables que existen durante toda la ejecución. |
| **Locales** | 3000 - 4999 | Variables propias de una función. Se reinician en cada llamada. |
| **Temporales** | 5000 - 6999 | Valores intermedios generados por el compilador (ej. resultado de `a + b`). |
| **Constantes** | 7000 - 8999 | Números y cadenas literales escritas en el código. |

Dentro de cada segmento, se subdivide por tipo de dato (ej. 1000-1999 para `int`, 2000-2999 para `float`).

#### Justificación del Diseño
*   **Simplicidad en la Máquina Virtual:** La VM no necesita tablas de símbolos complejas. Si recibe la dirección `1005`, sabe inmediatamente que es una variable global entera.
*   **Eficiencia:** El acceso a arreglos directos en la VM es O(1).
*   **Manejo de Recursión:** Aunque este modelo es estático, la VM implementa la memoria local real usando un stack de memoria (Activation Records) que se mapea a estas direcciones virtuales.

---

## Análisis Semántico y Generación de Código

Esta fase ocurre concurrentemente con el análisis sintáctico (Syntax-Directed Translation). En puntos neurálgicos de la gramática, se invocan acciones semánticas.

### Puntos Neurálgicos (Neuralgic Points)
Son momentos específicos durante el parseo donde se tiene suficiente información para realizar una acción.

**Ejemplo: Asignación `A = B + C;`**

1.  El parser lee `A`. -> Busca `A` en la tabla de variables, obtiene su dirección y la mete a la `operand_stack`.
2.  Lee `=`. -> Mete el operador a una pila de operadores (si existiera) o espera.
3.  Lee `B`. -> Busca `B`, obtiene dirección, mete a `operand_stack`.
4.  Lee `+`. -> Mete `+` a la pila de operadores.
5.  Lee `C`. -> Busca `C`, obtiene dirección, mete a `operand_stack`.
6.  **Punto Neurálgico (Reducción de expresión):**
    *   Detecta que hay una suma pendiente.
    *   Saca `C` y `B` de la pila.
    *   Verifica `int + int = int` en el Cubo Semántico.
    *   Solicita una dirección temporal `T1` al `MemoryManager`.
    *   Genera cuádruplo: `(+, B_addr, C_addr, T1_addr)`.
    *   Mete `T1` a la `operand_stack`.
7.  **Punto Neurálgico (Asignación):**
    *   Saca `T1` y `A` de la pila.
    *   Verifica que `A` pueda recibir el tipo de `T1`.
    *   Genera cuádruplo: `(=, T1_addr, _, A_addr)`.

### El Cubo Semántico
Es una estructura tridimensional (lógicamente) que define las reglas de interacción entre tipos.
*   Entrada: `(TipoOperando1, TipoOperando2, Operador)`
*   Salida: `TipoResultado` o `Error`.

Ejemplo: `('int', 'float', '+')` -> `'float'`.
Ejemplo: `('int', 'string', '+')` -> `Error`.

---

## Generación de Cuádruplos (Intermediate Code)

Los cuádruplos son una representación intermedia de bajo nivel, similar al ensamblador pero agnóstica de la máquina real. Cada cuádruplo tiene la forma:

`[ Operador, OperandoIzquierdo, OperandoDerecho, Resultado ]`

### Tipos de Cuádruplos

1.  **Aritméticos:** `+, -, *, /`. Ej: `['+', 1001, 1002, 5001]`
2.  **Asignación:** `=`. Ej: `['=', 5001, None, 1001]`
3.  **Saltos (Control de Flujo):**
    *   `GOTO`: Salto incondicional.
    *   `GOTOF`: Salto si falso. Usado en `IF` y `WHILE`.
    *   `GOTOV`: Salto si verdadero (opcional).
4.  **Funciones:**
    *   `ERA`: Expande registro de activación (prepara memoria para función).
    *   `PARAM`: Pasa un valor a un parámetro.
    *   `GOSUB`: Salta a la subrutina y guarda la posición actual.
    *   `ENDFUNC`: Termina la función y libera memoria.
    *   `RETURN`: Retorna un valor.

---

## Ejemplo de Compilación (Traza)

Considere el siguiente código fuente:

```
program ejemplo;
var
    int i;
    float f;
main() {
    i = 10;
    if (i > 5) {
        f = i * 2.5;
    }
}
end
```

### Paso a Paso

1.  **Declaración:**
    *   `i` se asigna a dir `1000` (Global Int).
    *   `f` se asigna a dir `2000` (Global Float).
    *   Constantes detectadas: `10` (7000), `5` (7001), `2.5` (8000).

2.  **Análisis de `i = 10`:**
    *   Genera: `['=', 7000, None, 1000]` (Asigna 10 a i).

3.  **Análisis de `if (i > 5)`:**
    *   Genera comparación: `['>', 1000, 7001, 5000]` (Temp bool en 5000).
    *   Genera salto incompleto: `['GOTOF', 5000, None, ____]`.
    *   Push del índice de este cuádruplo (digamos, índice 1) al `jump_stack`.

4.  **Análisis de `f = i * 2.5`:**
    *   Genera mult: `['*', 1000, 8000, 5001]` (Temp float en 5001).
    *   Genera asignación: `['=', 5001, None, 2000]`.

5.  **Cierre del `IF`:**
    *   Encuentra `}`.
    *   Pop del `jump_stack` (índice 1).
    *   Rellena el cuádruplo 1 con la dirección actual (digamos, índice 4).
    *   Cuádruplo 1 queda: `['GOTOF', 5000, None, 4]`.

### Resultado Final (Lista de Cuádruplos)

| # | Operador | Op1 | Op2 | Res | Comentario |
|---|---|---|---|---|---|
| 0 | `=` | 7000 | - | 1000 | `i = 10` |
| 1 | `>` | 1000 | 7001 | 5000 | `i > 5`? |
| 2 | `GOTOF`| 5000 | - | 5 | Si falso, ir a fin |
| 3 | `*` | 1000 | 8000 | 5001 | `i * 2.5` |
| 4 | `=` | 5001 | - | 2000 | `f = ...` |
| 5 | `ENDFUNC`| - | - | - | Fin de main |

---
