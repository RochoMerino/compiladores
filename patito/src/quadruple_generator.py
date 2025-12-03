
class Quadruple:
    def __init__(self, operator, operand1, operand2, result):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

    def __str__(self):
        """String representation of quadruple."""
        if self.operand2 is None:
            return f"({self.operator}, {self.operand1}, _, {self.result})"
        return f"({self.operator}, {self.operand1}, {self.operand2}, {self.result})"

    def __repr__(self):
        """Detailed representation."""
        return self.__str__()

    def to_tuple(self):
        """Convert to tuple format."""
        return (self.operator, self.operand1, self.operand2, self.result)


class QuadrupleGenerator:
    def __init__(self):
        self.quadruples = []

    def generate(self, operator, operand1, operand2, result):
        quad = Quadruple(operator, operand1, operand2, result)
        self.quadruples.append(quad)
        return len(self.quadruples) - 1

    def get_quadruples(self):
        return self.quadruples

    def get_quadruple(self, index):
        if 0 <= index < len(self.quadruples):
            return self.quadruples[index]
        return None

    def size(self):
        return len(self.quadruples)

    def get_next_address(self):
        return len(self.quadruples)

    def fill_quad(self, index, value):
        if 0 <= index < len(self.quadruples):
            self.quadruples[index].result = str(value)

    def clear(self):
        self.quadruples = []

    def print_quadruples(self):
        """Print all quadruples in a formatted table."""
        if not self.quadruples:
            print("No quadruples generated.")
            return

        print("\n" + "="*70)
        print("QUADRUPLES GENERATED")
        print("="*70)
        print(f"{'#':<5} {'Operator':<10} {'Operand1':<15} {'Operand2':<15} {'Result':<15}")
        print("-"*70)

        for i, quad in enumerate(self.quadruples):
            op2 = quad.operand2 if quad.operand2 is not None else "_"
            print(f"{i:<5} {quad.operator:<10} {str(quad.operand1):<15} {str(op2):<15} {str(quad.result):<15}")

        print("="*70)
        print(f"Total: {len(self.quadruples)} quadruples\n")

    def __str__(self):
        """String representation."""
        return f"QuadrupleGenerator({len(self.quadruples)} quadruples)"

