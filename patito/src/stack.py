"""
Stack (LIFO) implementation for the Patito compiler.
Adapted from tarea1/stack.py

Used for:
- Operand stack (variable names and constants)
- Operator stack (arithmetic and relational operators)
- Type stack (int, float types)
"""


class Stack:
    """Generic Stack implementation using Python list."""

    def __init__(self):
        self.stack = []

    def push(self, item):
        """Add an element to the top of the stack."""
        self.stack.append(item)

    def pop(self):
        """Remove and return the top element from the stack."""
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        """Get the value of the top element without removing it."""
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.stack) == 0

    def size(self):
        """Get the number of elements in the stack."""
        return len(self.stack)

    def clear(self):
        """Remove all elements from the stack."""
        self.stack = []

    def __str__(self):
        """String representation of the stack."""
        return str(self.stack)

    def __repr__(self):
        """Detailed representation of the stack."""
        return f"Stack({self.stack})"

    def __len__(self):
        """Allow len() function to work on Stack."""
        return len(self.stack)


if __name__ == '__main__':
    # Demo
    print("DEMO: Stack for Patito Compiler\n")

    print("=== Operand Stack Example ===")
    operand_stack = Stack()
    operand_stack.push('x')
    operand_stack.push('5')
    operand_stack.push('y')
    print(f"Stack: {operand_stack}")
    print(f"Pop: {operand_stack.pop()}")
    print(f"Peek: {operand_stack.peek()}")
    print()

    print("=== Operator Stack Example ===")
    operator_stack = Stack()
    operator_stack.push('+')
    operator_stack.push('*')
    print(f"Stack: {operator_stack}")
    print(f"Top operator: {operator_stack.peek()}")
    print()

    print("=== Type Stack Example ===")
    type_stack = Stack()
    type_stack.push('int')
    type_stack.push('float')
    type_stack.push('int')
    print(f"Stack: {type_stack}")
    print(f"Top type: {type_stack.peek()}")
