"""
Operator Stack for Patito Compiler.

Manages operators during expression evaluation with precedence handling.
"""

from stack import Stack


class OperatorStack(Stack):
    """
    Stack for operators during expression parsing.

    Stores arithmetic and relational operators with precedence support.
    """

    # Operator precedence levels (higher number = higher precedence)
    PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '>': 0,
        '<': 0,
        '!=': 0,
        '=': -1,  # Assignment has lowest precedence
    }

    def __init__(self):
        """Initialize the operator stack."""
        super().__init__()

    def push_operator(self, operator):
        """
        Push an operator onto the stack.

        Args:
            operator (str): Operator symbol (+, -, *, /, >, <, !=, =)
        """
        self.push(operator)

    def pop_operator(self):
        """
        Pop and return the top operator.

        Returns:
            str: Top operator or None if empty
        """
        return self.pop()

    def peek_operator(self):
        """
        Peek at the top operator without removing it.

        Returns:
            str: Top operator or None if empty
        """
        return self.peek()

    def get_precedence(self, operator):
        """
        Get the precedence level of an operator.

        Args:
            operator (str): Operator symbol

        Returns:
            int: Precedence level (higher = more precedence)
        """
        return self.PRECEDENCE.get(operator, -1)

    def should_reduce(self, current_operator):
        """
        Check if we should reduce based on operator precedence.

        Args:
            current_operator (str): The incoming operator

        Returns:
            bool: True if top operator has >= precedence than current
        """
        if self.is_empty():
            return False

        top_operator = self.peek_operator()
        return self.get_precedence(top_operator) >= self.get_precedence(current_operator)

    def __repr__(self):
        """Detailed representation."""
        return f"OperatorStack({self.stack})"


if __name__ == '__main__':
    print("DEMO: Operator Stack with Precedence\n")

    op_stack = OperatorStack()

    print("Expression: a + b * c")
    print()

    print("Parsing '+'...")
    op_stack.push_operator('+')
    print(f"  Stack: {op_stack}")
    print(f"  Precedence of '+': {op_stack.get_precedence('+')}")

    print("\nParsing '*'...")
    print(f"  Should reduce before push? {op_stack.should_reduce('*')}")
    op_stack.push_operator('*')
    print(f"  Stack: {op_stack}")
    print(f"  Precedence of '*': {op_stack.get_precedence('*')}")

    print("\nAfter parsing 'c', end of expression...")
    print(f"  Top operator: {op_stack.peek_operator()}")
    print(f"  Process '*' first (higher precedence)")
    op = op_stack.pop_operator()
    print(f"  Popped: {op}")
    print(f"  Stack: {op_stack}")

    print(f"\n  Now process '+'")
    op = op_stack.pop_operator()
    print(f"  Popped: {op}")
    print(f"  Stack: {op_stack}")

    print("\n\n=== Precedence Table ===")
    print(f"{'Operator':<10} {'Precedence':<10}")
    print("-" * 20)
    for op in ['+', '-', '*', '/', '>', '<', '!=', '=']:
        prec = op_stack.get_precedence(op)
        print(f"{op:<10} {prec:<10}")
