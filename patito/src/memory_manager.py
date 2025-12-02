class MemoryManager:
    def __init__(self):
        # Memory ranges
        self.GLOBAL_BASE = 1000
        self.LOCAL_BASE = 3000
        self.TEMP_BASE = 5000
        self.CONST_BASE = 7000
        
        # Counters for each segment and type
        # Global
        self.global_int = 0
        self.global_float = 0
        
        # Local (resets for each function)
        self.local_int = 0
        self.local_float = 0
        
        # Temporal (resets for each function)
        self.temp_int = 0
        self.temp_float = 0
        self.temp_bool = 0 # For boolean results in conditions
        
        # Constants (persistent)
        self.const_int = 0
        self.const_float = 0
        self.const_string = 0
        
        # Constant Memory Map (Address -> Value)
        self.constant_memory = {}
        
        # Limits (optional, for safety)
        self.SEGMENT_SIZE = 1000

    def get_global_address(self, type_):
        if type_ == 'int':
            addr = self.GLOBAL_BASE + self.global_int
            self.global_int += 1
            return addr
        elif type_ == 'float':
            addr = self.GLOBAL_BASE + 1000 + self.global_float
            self.global_float += 1
            return addr
        return None

    def get_local_address(self, type_):
        if type_ == 'int':
            addr = self.LOCAL_BASE + self.local_int
            self.local_int += 1
            return addr
        elif type_ == 'float':
            addr = self.LOCAL_BASE + 1000 + self.local_float
            self.local_float += 1
            return addr
        return None

    def get_temp_address(self, type_):
        if type_ == 'int':
            addr = self.TEMP_BASE + self.temp_int
            self.temp_int += 1
            return addr
        elif type_ == 'float':
            addr = self.TEMP_BASE + 1000 + self.temp_float
            self.temp_float += 1
            return addr
        elif type_ == 'bool':
             # Let's put bools at the end of temp segment or give them their own range
             # For simplicity, let's say bools share int space or use a specific range
             # Let's use 6900 for bools
             addr = self.TEMP_BASE + 1900 + self.temp_bool
             self.temp_bool += 1
             return addr
        return None

    def get_const_address(self, type_, value):
        # Check if constant already exists (optimization)
        for addr, val in self.constant_memory.items():
            if val == value and self._get_type_from_addr(addr) == type_:
                return addr

        if type_ == 'int':
            addr = self.CONST_BASE + self.const_int
            self.const_int += 1
        elif type_ == 'float':
            addr = self.CONST_BASE + 1000 + self.const_float
            self.const_float += 1
        elif type_ == 'string':
            addr = self.CONST_BASE + 2000 + self.const_string
            self.const_string += 1
        else:
            return None
            
        self.constant_memory[addr] = value
        return addr

    def _get_type_from_addr(self, addr):
        if 7000 <= addr < 8000: return 'int'
        if 8000 <= addr < 9000: return 'float'
        if 9000 <= addr < 10000: return 'string'
        return None

    def get_constants(self):
        return self.constant_memory

    def reset_local_memory(self):
        """Resets local and temporal counters for a new function."""
        self.local_int = 0
        self.local_float = 0
        self.temp_int = 0
        self.temp_float = 0
        self.temp_bool = 0

    def get_memory_usage(self):
        """Returns the current usage of local and temporal memory."""
        return {
            'local_int': self.local_int,
            'local_float': self.local_float,
            'temp_int': self.temp_int,
            'temp_float': self.temp_float,
            'temp_bool': self.temp_bool
        }
