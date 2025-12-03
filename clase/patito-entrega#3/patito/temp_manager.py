"""
Temporary Variable Manager for Patito Compiler.

Generates unique temporary variable names for intermediate results
during code generation (quadruples).
"""


class TempManager:
    """Manages generation of temporary variables."""

    def __init__(self, prefix='t'):
        """
        Initialize the temporary variable manager.

        Args:
            prefix (str): Prefix for temporary variables (default: 't')
        """
        self.prefix = prefix
        self.counter = 0

    def generate(self):
        """
        Generate a new temporary variable name.

        Returns:
            str: Temporary variable name (e.g., 't1', 't2', ...)
        """
        self.counter += 1
        return f"{self.prefix}{self.counter}"

    def reset(self):
        """Reset the counter to 0."""
        self.counter = 0

    def get_count(self):
        """Get the current count of temporaries generated."""
        return self.counter

    def __str__(self):
        """String representation."""
        return f"TempManager(prefix='{self.prefix}', count={self.counter})"


if __name__ == '__main__':
    print("DEMO: Temporary Variable Manager\n")

    temp_mgr = TempManager()

    print("Generating temporaries for expression: x = a + b * c")
    print()

    print("Step 1: b * c")
    t1 = temp_mgr.generate()
    print(f"  {t1} = b * c")
    print()

    print("Step 2: a + t1")
    t2 = temp_mgr.generate()
    print(f"  {t2} = a + {t1}")
    print()

    print("Step 3: x = t2")
    print(f"  x = {t2}")
    print()

    print(f"Total temporaries generated: {temp_mgr.get_count()}")
    print(f"Manager state: {temp_mgr}")
    print()

    print("Resetting for new function...")
    temp_mgr.reset()
    print(f"After reset: {temp_mgr}")
    print()

    print("New expression: y = p + q")
    t1 = temp_mgr.generate()
    print(f"  {t1} = p + q")
    print(f"  y = {t1}")
