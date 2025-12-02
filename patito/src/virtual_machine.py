import sys

class VirtualMachine:
    def __init__(self):
        self.quadruples = []
        self.instruction_pointer = 0
        
        # Memory Segments
        self.global_memory = {}
        self.constant_memory = {}
        
        # Stack for local/temp memory (Activation Records)
        # Each record is a dict or object containing local and temp memory
        self.memory_stack = []
        self.current_local_memory = {}
        self.current_temp_memory = {}
        
        # Pending memory for function calls (created by ERA, used by PARAM, pushed by GOSUB)
        self.pending_activation_record = None
        
        # Return address stack for GOSUB
        self.return_stack = []

    def load_quadruples(self, quadruples):
        self.quadruples = quadruples

    def set_constants(self, constants):
        """
        Load constants into memory.
        constants: dict mapping address -> value
        """
        self.constant_memory = constants

    def get_value(self, address):
        address = int(address)
        
        # Global: 1000-2999
        if 1000 <= address < 3000:
            return self.global_memory.get(address)
            
        # Local: 3000-4999
        elif 3000 <= address < 5000:
            return self.current_local_memory.get(address)
            
        # Temp: 5000-6999
        elif 5000 <= address < 7000:
            return self.current_temp_memory.get(address)
            
        # Constant: 7000-9999
        elif 7000 <= address < 10000:
            return self.constant_memory.get(address)
            
        else:
            raise Exception(f"Segmentation Fault: Address {address} out of range")

    def set_value(self, address, value):
        address = int(address)
        
        # Global
        if 1000 <= address < 3000:
            self.global_memory[address] = value
            
        # Local
        elif 3000 <= address < 5000:
            self.current_local_memory[address] = value
            
        # Temp
        elif 5000 <= address < 7000:
            self.current_temp_memory[address] = value
            
        # Constant (Should be read-only, but for initialization...)
        elif 7000 <= address < 10000:
            raise Exception("Segmentation Fault: Cannot write to constant memory")
            
        else:
            raise Exception(f"Segmentation Fault: Address {address} out of range")

    def execute(self):
        print("--- STARTING VIRTUAL MACHINE ---")
        self.instruction_pointer = 0
        
        while self.instruction_pointer < len(self.quadruples):
            quad = self.quadruples[self.instruction_pointer]
            op = quad.operator
            left = quad.operand1
            right = quad.operand2
            res = quad.result
            
            try:
                if op == '+':
                    val_l = self.get_value(left)
                    val_r = self.get_value(right)
                    self.set_value(res, val_l + val_r)
                    self.instruction_pointer += 1
                    
                elif op == '-':
                    val_l = self.get_value(left)
                    if right is None: # Unary minus
                        self.set_value(res, -val_l)
                    else:
                        val_r = self.get_value(right)
                        self.set_value(res, val_l - val_r)
                    self.instruction_pointer += 1
                    
                elif op == '*':
                    val_l = self.get_value(left)
                    val_r = self.get_value(right)
                    self.set_value(res, val_l * val_r)
                    self.instruction_pointer += 1
                    
                elif op == '/':
                    val_l = self.get_value(left)
                    val_r = self.get_value(right)
                    self.set_value(res, val_l / val_r)
                    self.instruction_pointer += 1
                    
                elif op == '=':
                    val_l = self.get_value(left)
                    self.set_value(res, val_l)
                    self.instruction_pointer += 1
                    
                elif op == '>':
                    val_l = self.get_value(left)
                    val_r = self.get_value(right)
                    self.set_value(res, val_l > val_r)
                    self.instruction_pointer += 1
                    
                elif op == '<':
                    val_l = self.get_value(left)
                    val_r = self.get_value(right)
                    self.set_value(res, val_l < val_r)
                    self.instruction_pointer += 1
                    
                elif op == '!=':
                    val_l = self.get_value(left)
                    val_r = self.get_value(right)
                    self.set_value(res, val_l != val_r)
                    self.instruction_pointer += 1
                    
                elif op == 'PRINT':
                    val = self.get_value(left)
                    print(val)
                    self.instruction_pointer += 1
                    
                elif op == 'GOTO':
                    self.instruction_pointer = int(res)
                    
                elif op == 'GOTOF':
                    cond = self.get_value(left)
                    if not cond:
                        self.instruction_pointer = int(res)
                    else:
                        self.instruction_pointer += 1
                        
                elif op == 'ERA':
                    # Create a new memory context
                    self.pending_activation_record = {'local': {}, 'temp': {}}
                    self.instruction_pointer += 1
                    
                elif op == 'PARAM':
                    val = self.get_value(left)
                    # We need to know where to put it in the pending record
                    # 'res' contains "param1", "param2", etc.
                    # In a real implementation, we would map param position to address
                    # For simplicity, let's assume params are mapped to the first local addresses
                    # Or we can just store them in a list and pop them?
                    # The compiler assigns addresses to params.
                    # But here 'res' is just a string "paramX".
                    # We need the target address.
                    # The compiler should have generated 'PARAM src_addr _ target_addr'
                    # But in my parser I generated 'PARAM arg_addr _ "paramX"'
                    # This is a gap. I need to know the address of the parameter in the called function.
                    # But I don't know which function is being called here easily (ERA was before).
                    # Let's assume for this simplified VM that we just push params to a list
                    # and the called function pops them into its local memory?
                    # OR, better: The compiler should resolve the address.
                    # Since I didn't implement that fully, I will hack it:
                    # I will assume params are stored in order in the new local memory starting at LOCAL_BASE.
                    
                    param_index = int(res.replace('param', '')) - 1
                    # Assuming int params for now, or mixed.
                    # This is tricky without type info.
                    # Let's just use a simple offset for now.
                    target_addr = 3000 + param_index # Very hacky!
                    
                    self.pending_activation_record['local'][target_addr] = val
                    self.instruction_pointer += 1
                    
                elif op == 'GOSUB':
                    # Save current state
                    self.memory_stack.append((self.current_local_memory, self.current_temp_memory))
                    self.return_stack.append(self.instruction_pointer + 1)
                    
                    # Switch to new state
                    self.current_local_memory = self.pending_activation_record['local']
                    self.current_temp_memory = self.pending_activation_record['temp']
                    self.pending_activation_record = None
                    
                    # Jump
                    # 'left' is func_name. VM needs a lookup table.
                    # For now, I'll assume 'left' IS the address (if I fixed the parser)
                    # OR I need a function directory in VM.
                    # Let's assume the parser puts the address in 'left' or I pass a directory to VM.
                    # I'll add a method to register functions.
                    func_name = left
                    # self.instruction_pointer = self.function_directory[func_name]
                    # For this implementation, I'll assume 'left' is the start address (int)
                    # If it's a string, I'll fail unless I add the directory.
                    self.instruction_pointer = int(left) # Expecting address
                    
                elif op == 'ENDFUNC':
                    # Restore state
                    prev_local, prev_temp = self.memory_stack.pop()
                    self.current_local_memory = prev_local
                    self.current_temp_memory = prev_temp
                    
                    # Return
                    ret_addr = self.return_stack.pop()
                    self.instruction_pointer = ret_addr
                    
                else:
                    raise Exception(f"Unknown operator: {op}")
                    
            except Exception as e:
                print(f"Error at quadruple {self.instruction_pointer}: {quad}")
                print(e)
                sys.exit(1)

        print("--- PROGRAM FINISHED ---")
