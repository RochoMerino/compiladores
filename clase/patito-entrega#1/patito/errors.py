class PatitoError(Exception):
    pass

class LexerError(PatitoError):
    def __init__(self, char, line):
        self.char = char
        self.line = line
        super().__init__(f"Lexical error at line {line}: Illegal character '{char}'")

class SyntaxError(PatitoError):
    def __init__(self, message, line=None, token=None):
        self.line = line
        self.token = token
        if line and token:
            super().__init__(f"Syntax error at line {line}: {message} (near '{token}')")
        elif line:
            super().__init__(f"Syntax error at line {line}: {message}")
        else:
            super().__init__(f"Syntax error: {message}")

class SemanticError(PatitoError):
    def __init__(self, message, line=None):
        self.line = line
        if line:
            super().__init__(f"Semantic error at line {line}: {message}")
        else:
            super().__init__(f"Semantic error: {message}")

class TypeError(PatitoError):
    def __init__(self, message, line=None):
        self.line = line
        if line:
            super().__init__(f"Type error at line {line}: {message}")
        else:
            super().__init__(f"Type error: {message}")

class UndefinedVariableError(SemanticError):
    def __init__(self, var_name, line=None):
        super().__init__(f"Undefined variable '{var_name}'", line)
        self.var_name = var_name

class RedefinitionError(SemanticError):
    def __init__(self, name, line=None):
        super().__init__(f"Redefinition of '{name}'", line)
        self.name = name

