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
    def __init__(self, message=None, line=None, identifier=None, var_name=None):
        if identifier or var_name:
            name = identifier or var_name
            super().__init__(f"Undefined variable '{name}'", line)
            self.var_name = name
            self.identifier = name
        else:
            super().__init__(message, line)
            self.var_name = None
            self.identifier = None

class RedefinitionError(SemanticError):
    def __init__(self, message=None, line=None, identifier=None, name=None):
        if identifier or name:
            id_name = identifier or name
            super().__init__(f"Redefinition of '{id_name}'", line)
            self.name = id_name
            self.identifier = id_name
        else:
            super().__init__(message, line)
            self.name = None
            self.identifier = None

