**Genera, como parte de la entrega, una documentación que describa brevemente los principales hallazgos del análisis de las diferentes herramientas. Agrega, a la documentación previa, cómo (en qué formato) diste de alta las reglas de construcción de Patito que contenga la definición de las expresiones regulares y reglas gramaticales desarrolladas. Agrega los principales Test-cases desarrollados para validar su funcionamiento. Considera que este documento irá creciendo conforme trabajes en las siguientes entregas.**

**Tests del Lexer:**

cd tests -> python3|python test_lexer.py

1\. Reconocimiento de palabras reservadas

2\. Validación de identificadores con letras, números y guiones bajos

3\. Reconocimiento de constantes enteras (positivas, negativas)

4\. Reconocimiento de constantes flotantes con signo

5\. Manejo de cadenas literales entre comillas

6\. Operadores aritméticos y comparación

7\. Delimitadores y puntuación (paréntesis, llaves, corchetes, comas, etc.)

8\. Ignorar comentarios de línea y de bloque

**Tests del Parser:**

cd tests -> python3|python test_parser.py

1\. Estructura mínima de programa válido

2\. Declaraciones de variables múltiples con tipos

3\. Asignaciones simples

4\. Expresiones aritméticas con operadores múltiples

5\. Expresiones de comparación

6\. Sentencias if simples

7\. Sentencias if-else completas

8\. Ciclos while-do

9\. Sentencias print con múltiples argumentos

10\. Declaración de funciones con parámetros

11\. Llamadas a funciones con argumentos

12\. Expresiones complejas con precedencia y paréntesis

13\. Detección de errores sintácticos (ej. punto y coma faltante)

14\. Programa completo integrando todas las características