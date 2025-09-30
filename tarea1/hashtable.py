from collections import deque

description = '''
Hash Table (Hash Map / Dictionary)

A hash table is a data structure that implements an associative array abstract data type, a structure that can map keys to values.

Hash table operations:
- Insert: Add a key-value pair to the table.
- Delete: Remove a key-value pair from the table.
- Search: Find the value associated with a key.

      
Common implementations:
      - Caching data for quick retrieval (e.g., memoization).
      - Implementing associative arrays or dictionaries.
      - Counting occurrences of items (e.g., word frequency).

TEST CASES:
- Initialize the dictionary with key-value pairs: ('name', 'Rodrigo'), ('Age', 23), ('Matricula', 'A00836396'), ('Enrolled', True)
- Search for existing key: 'name' -> should return 'Rodrigo'
- Insert new key-value pair: ('lastname', 'Merino')
- Delete existing key: 'Enrolled'
      '''

print(description)


table = {
         'name': 'Rodrigo',
         'Age': 23,
         'Matriculpa': 'A00836396',
         'Enrolled': True
         }

print(f"Table/Hash/Dictionary: {table}")

print(f"Searching 'name': {table['name']}")

table['lastname'] = 'Merino'
print(f"Table after inserting 'lastname': {table}")

del table['Enrolled']
print(f"Table after deleting 'Enrolled': {table}")

