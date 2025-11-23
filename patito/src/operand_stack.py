"""
Operand Stack for Patito Compiler.

Manages operands (variables, constants, and temporaries) during
expression evaluation and quadruple generation.
"""

from stack import Stack


class OperandStack(Stack):
    """
    Stack for operands during expression parsing.

    Stores variable names, constants, and temporary variables.
    """

    def __init__(self):
        """Initialize the operand stack."""
        super().__init__()

    def push_operand(self, operand):
        """
        Push an operand onto the stack.

        Args:
            operand (str): Variable name, constant, or temporary
        """
        self.push(operand)

    def pop_operand(self):
        """
        Pop and return the top operand.

        Returns:
            str: Top operand or None if empty
        """
        return self.pop()

    def peek_operand(self):
        """
        Peek at the top operand without removing it.

        Returns:
            str: Top operand or None if empty
        """
        return self.peek()

    def __repr__(self):
        """Detailed representation."""
        return f"OperandStack({self.stack})"


if __name__ == '__main__':
    print("DEMO: Operand Stack\n")

    operand_stack = OperandStack()

    print("Expression: a + b * c")
    print()

    print("Parsing 'a'...")
    operand_stack.push_operand('a')
    print(f"  Stack: {operand_stack}")

    print("Parsing '+'...")
    print(f"  Stack: {operand_stack}")

    print("Parsing 'b'...")
    operand_stack.push_operand('b')
    print(f"  Stack: {operand_stack}")

    print("Parsing '*'...")
    print(f"  Stack: {operand_stack}")

    print("Parsing 'c'...")
    operand_stack.push_operand('c')
    print(f"  Stack: {operand_stack}")

    print("\nGenerating quadruple for 'b * c'...")
    right = operand_stack.pop_operand()
    left = operand_stack.pop_operand()
    print(f"  Popped: {left}, {right}")
    print(f"  Quadruple: (* {left} {right} t1)")
    operand_stack.push_operand('t1')
    print(f"  Stack after push t1: {operand_stack}")

    print("\nGenerating quadruple for 'a + t1'...")
    right = operand_stack.pop_operand()
    left = operand_stack.pop_operand()
    print(f"  Popped: {left}, {right}")
    print(f"  Quadruple: (+ {left} {right} t2)")
    operand_stack.push_operand('t2')
    print(f"  Stack after push t2: {operand_stack}")

    print(f"\nFinal result in stack: {operand_stack.peek_operand()}")
