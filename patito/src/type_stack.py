"""
Type Stack for Patito Compiler.

Manages type information (int, float) for operands during
expression evaluation and type checking.
"""

from stack import Stack


class TypeStack(Stack):
    """
    Stack for types during expression parsing.

    Stores type information (int, float) corresponding to operands.
    """

    def __init__(self):
        """Initialize the type stack."""
        super().__init__()

    def push_type(self, type_name):
        """
        Push a type onto the stack.

        Args:
            type_name (str): Type ('int' or 'float')
        """
        if type_name not in ['int', 'float']:
            raise ValueError(f"Invalid type: {type_name}. Must be 'int' or 'float'")
        self.push(type_name)

    def pop_type(self):
        """
        Pop and return the top type.

        Returns:
            str: Top type ('int' or 'float') or None if empty
        """
        return self.pop()

    def peek_type(self):
        """
        Peek at the top type without removing it.

        Returns:
            str: Top type or None if empty
        """
        return self.peek()

    def __repr__(self):
        """Detailed representation."""
        return f"TypeStack({self.stack})"


if __name__ == '__main__':
    print("DEMO: Type Stack\n")

    type_stack = TypeStack()

    print("Expression: x + y * 3.5")
    print("  x: int, y: int, 3.5: float")
    print()

    print("Parsing 'x' (int)...")
    type_stack.push_type('int')
    print(f"  Stack: {type_stack}")

    print("Parsing '+'...")
    print(f"  Stack: {type_stack}")

    print("Parsing 'y' (int)...")
    type_stack.push_type('int')
    print(f"  Stack: {type_stack}")

    print("Parsing '*'...")
    print(f"  Stack: {type_stack}")

    print("Parsing '3.5' (float)...")
    type_stack.push_type('float')
    print(f"  Stack: {type_stack}")

    print("\nType checking for 'y * 3.5'...")
    right_type = type_stack.pop_type()
    left_type = type_stack.pop_type()
    print(f"  Popped types: {left_type}, {right_type}")
    print(f"  int * float -> float (type promotion)")
    result_type = 'float'
    type_stack.push_type(result_type)
    print(f"  Stack after push result type: {type_stack}")

    print("\nType checking for 'x + (temp_float)'...")
    right_type = type_stack.pop_type()
    left_type = type_stack.pop_type()
    print(f"  Popped types: {left_type}, {right_type}")
    print(f"  int + float -> float (type promotion)")
    result_type = 'float'
    type_stack.push_type(result_type)
    print(f"  Stack after push result type: {type_stack}")

    print(f"\nFinal result type: {type_stack.peek_type()}")

    print("\n\nTrying to push invalid type...")
    try:
        type_stack.push_type('string')
    except ValueError as e:
        print(f"  Error caught: {e}")
