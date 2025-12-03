# Analisis Semantico del Compilador Patito

---

## Introduccion

El analisis semantico valida la coherencia de tipos y uso correcto de variables y funciones durante el proceso de compilacion. Se integra directamente con el parser mediante puntos neuralgicos que ejecutan validaciones en tiempo real durante el analisis sintactico.

---

## Cubo Semantico

### Proposito

El cubo semantico determina que operaciones son validas entre tipos de datos y cual es el tipo resultante de cada operacion.

### Estructura

Se implementa como un diccionario de tres dimensiones donde cada entrada mapea una combinacion de tipo izquierdo, operador y tipo derecho a un tipo resultado. La estructura permite verificaciones en tiempo constante O(1).

### Operadores Aritmeticos

Los operadores de suma, resta, multiplicacion y division siguen las siguientes reglas:

- **int con int:** -> int
- **int con float:** -> float (promocion automatica)
- **float con int:** -> float (promocion automatica)
- **float con float:** -> float

Patito implementa promocion automatica de int a float en operaciones mixtas para preservar precision.

### Operadores Relacionales

Los operadores de comparacion (mayor que, menor que, diferente de) siempre retornan int, ya que Patito no tiene tipo boolean explicito. Se usan 0 para falso y 1 para verdadero.

Estos operadores aceptan cualquier combinacion de int y float como operandos, facilitando comparaciones numericas sin restricciones de tipo.

### Asignacion

La asignacion tiene reglas especiales para proteger contra perdida de precision:

- **int = int:** Valido
- **float = float:** Valido
- **float = int:** Valido (promocion segura)
- **int = float:** Invalido (perderia precision)

Esta restriccion previene errores comunes de truncamiento no intencional.

### Implementacion

Archivo `patito/semantic_cube.py` contiene la clase `SemanticCube` con metodos `get_result_type()` para obtener el tipo resultado y `is_valid_operation()` para verificar validez.

---

## Tabla de Variables

### Proposito

La tabla de variables almacena informacion sobre todas las variables declaradas, incluyendo nombre, tipo, scope y linea de declaracion.

### Estructura

Implementada como un diccionario simple que mapea nombres de variables a objetos `VariableInfo`. Esto permite busquedas e inserciones en tiempo constante O(1), asi como deteccion inmediata de declaraciones duplicadas.

### Informacion de Variables

Cada variable almacena cuatro atributos: nombre, tipo (int o float), scope (global, local o param) y numero de linea donde fue declarada.

### Scopes

El sistema maneja dos niveles de scope:

**Global:** Contiene variables declaradas fuera de funciones. Permanece activo durante toda la compilacion.

**Local:** Se crea al entrar a una funcion y se destruye al salir. Contiene parametros y variables locales de la funcion.

La busqueda de variables sigue una estrategia en cascada: primero busca en el scope local (si existe), luego en el scope global.

### Implementacion

Archivo `patito/variable_table.py` contiene tres clases:

**VariableInfo:** Almacena informacion de una sola variable.

**VariableTable:** Maneja una tabla para un scope especifico con operaciones de agregar, buscar y verificar existencia.

**ScopedVariableTable:** Coordina multiples niveles de scope, manejando la creacion y destruccion de scopes locales al entrar y salir de funciones.

---

## Directorio de Funciones

### Proposito

El directorio de funciones almacena informacion sobre todas las funciones declaradas, incluyendo tipo de retorno, parametros y variables locales.

### Estructura

Implementado como un diccionario anidado donde cada funcion mapea a un objeto `FunctionInfo` que contiene toda su metadata. Cada funcion tiene su propia tabla de variables para manejar variables locales.

### Informacion de Funciones

Cada funcion almacena: nombre, tipo de retorno (siempre void en Patito), lista de parametros con sus tipos y posiciones, tabla de variables locales y numero de linea de declaracion.

### Parametros

Los parametros se almacenan como objetos `ParameterInfo` que contienen nombre, tipo y posicion ordinal. Esto facilita la validacion de llamadas a funciones.

### Validacion de Llamadas

Cuando se invoca una funcion, el directorio valida tres aspectos:

1. Que la funcion exista en el directorio
2. Que el numero de argumentos coincida con el numero de parametros
3. Que el tipo de cada argumento coincida exactamente con el tipo del parametro correspondiente

A diferencia de las expresiones aritmeticas, las llamadas a funciones NO permiten promocion automatica de tipos. Los tipos deben coincidir exactamente.

### Restricciones

El nombre "main" esta reservado y no puede usarse para declarar funciones, evitando conflictos con el punto de entrada del programa.

### Implementacion

Archivo `patito/function_directory.py` contiene tres clases:

**ParameterInfo:** Almacena informacion de un parametro individual.

**FunctionInfo:** Almacena informacion completa de una funcion, incluyendo metodos para agregar parametros y validar llamadas.

**FunctionDirectory:** Coordina todas las funciones del programa con operaciones para declarar, buscar y validar.

---

## Analizador Semantico

### Proposito

El analizador semantico coordina todas las estructuras de datos semanticas y proporciona una interfaz unificada para que el parser ejecute validaciones.

### Componentes

El analizador integra cuatro estructuras principales: el cubo semantico, la tabla de variables globales, el directorio de funciones y un registro del contexto actual (funcion activa y nombre del programa).

### Responsabilidades

**Gestion de Variables:** Declarar variables en el scope apropiado, buscar variables siguiendo las reglas de scope y verificar que las variables existan antes de usarse.

**Gestion de Funciones:** Declarar funciones, entrar y salir de scopes de funciones, agregar parametros y validar llamadas a funciones.

**Verificacion de Tipos:** Validar operaciones usando el cubo semantico y verificar compatibilidad de tipos en asignaciones.

### Contexto

El analizador mantiene un registro de la funcion actual para saber si esta en scope global o local. Esto determina donde se declaran variables y donde se buscan.

### Implementacion

Archivo `patito/semantic_analyzer.py` contiene la clase `SemanticAnalyzer` que actua como fachada para todas las operaciones semanticas. Proporciona metodos de alto nivel como `declare_variable()`, `lookup_variable()`, `check_operation()` y `validate_function_call()`.

---

## Puntos Neuralgicos

### Concepto

Los puntos neuralgicos son ubicaciones estrategicas en las reglas del parser donde se ejecutan validaciones semanticas. Cada punto neuralgico corresponde a una construccion del lenguaje que requiere verificacion.

### Ubicacion

Todos los puntos neuralgicos estan implementados en `patito/parser.py` dentro de las funciones de reglas gramaticales.

### PN1: Declaracion del Programa

Al reconocer la regla de programa, se registra el nombre del programa en el analizador semantico.

### PN2: Declaracion de Variables

Al reconocer una declaracion de variables, se agregan todas las variables de la lista a la tabla del scope actual. Se valida que ninguna variable este duplicada.

### PN3: Declaracion de Funciones

Al iniciar el reconocimiento de una funcion, se declara en el directorio y se entra a su scope. Al terminar, se sale del scope. Se valida que la funcion no este duplicada y que no use el nombre reservado "main".

### PN4: Parametros

Al reconocer cada parametro, se agrega a la funcion actual. Los parametros tambien se agregan a la tabla de variables locales de la funcion. Se valida que no haya parametros duplicados.

### PN5: Asignaciones

Al reconocer una asignacion, se valida que la variable exista y que el tipo de la expresion sea compatible con el tipo de la variable segun las reglas del cubo semantico.

### PN6: Expresiones

Al reconocer operaciones aritmeticas y relacionales, se valida que la operacion sea valida segun el cubo semantico. El resultado incluye el tipo resultante para propagarlo hacia arriba en el arbol de expresiones.

### PN7: Llamadas a Funciones

Al reconocer una llamada a funcion, se valida que la funcion exista, que el numero de argumentos coincida y que el tipo de cada argumento coincida exactamente con su parametro correspondiente.

### PN8: Uso de Variables

Al reconocer el uso de una variable en una expresion, se valida que la variable exista y se obtiene su tipo para la propagacion de tipos.

### Propagacion de Tipos

Las expresiones retornan tuplas con formato `('type_info', tipo, ast)` que contienen el tipo resultado y la estructura del AST. Esto permite verificar tipos durante la construccion del arbol sintactico y facilita la futura generacion de codigo.

---

## Validaciones Implementadas

El sistema implementa nueve validaciones semanticas completas:

**1. Variable Duplicada:** Se detecta cuando se intenta declarar una variable que ya existe en el mismo scope.

**2. Variable No Declarada:** Se detecta cuando se usa una variable que no ha sido declarada en ningun scope accesible.

**3. Funcion Duplicada:** Se detecta cuando se intenta declarar una funcion que ya existe.

**4. Funcion No Declarada:** Se detecta cuando se llama a una funcion que no ha sido declarada.

**5. Operacion Invalida:** Se detecta cuando se intenta una operacion entre tipos incompatibles segun el cubo semantico.

**6. Asignacion Incompatible:** Se detecta cuando se intenta asignar un valor de un tipo a una variable de tipo incompatible.

**7. Numero Incorrecto de Argumentos:** Se detecta cuando una llamada a funcion no proporciona el numero correcto de argumentos.

**8. Tipos Incorrectos de Argumentos:** Se detecta cuando los tipos de los argumentos no coinciden con los tipos esperados por los parametros.

**9. Parametro Duplicado:** Se detecta cuando una funcion tiene dos parametros con el mismo nombre.

### Manejo de Errores

Todos los errores semanticos incluyen el numero de linea donde ocurrieron y un mensaje descriptivo. Se usan tres tipos de excepciones: `RedefinitionError` para duplicados, `UndefinedVariableError` para elementos no declarados y `TypeError` para incompatibilidades de tipos.

---

## Pruebas

### Suite de Tests

El archivo `tests/test_semantic.py` contiene 22 tests automatizados que verifican todas las validaciones semanticas. Los tests estan organizados en seis categorias: variables, operaciones, asignaciones, funciones, scope y casos complejos.

### Archivos de Ejemplo

Se incluyen nueve archivos `.patito` de ejemplo que demuestran tanto programas validos como cada tipo de error semantico posible.

---

## Decisiones de Diseño

### Estructuras de Datos

Se eligieron diccionarios para todas las estructuras principales porque proporcionan acceso en tiempo constante, son simples de implementar y faciles de extender. Esta decision prioriza eficiencia sobre complejidad.

### Integracion con Parser

Se eligio integrar las validaciones directamente en el parser mediante puntos neuralgicos en lugar de hacer un pase separado. Esto permite deteccion temprana de errores, reduce consumo de memoria y simplifica la arquitectura.

### Sin Promocion en Llamadas

Se decidio NO permitir promocion automatica de tipos en argumentos de funciones, aunque si se permite en operaciones aritmeticas. Esto hace que las llamadas sean mas estrictas y predecibles, evitando conversiones implicitas que podrian causar confusion.

### Scope Simple

Se implemento un sistema de scope de dos niveles (global y local) en lugar de scopes anidados arbitrarios. Esto es suficiente para Patito y simplifica la implementacion.

---

Fin de la Documentacion
