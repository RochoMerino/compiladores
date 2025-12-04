import sys

class VirtualMachine:
    def __init__(self):
        self.quadruples = []
        self.instruction_pointer = 0
        
        self.global_memory = {}
        self.constant_memory = {}
        
        self.memory_stack = []
        self.current_local_memory = {}
        self.current_temp_memory = {}
        
        self.pending_activation_record = None
        
        self.return_stack = []

    def load_quadruples(self, quadruples):
        self.quadruples = quadruples

    def set_constants(self, constants):
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
        print("--- VIRTUAL MACHINE ---")
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
                    param_index = int(res.replace('param', '')) - 1
                    target_addr = 3000 + param_index
                    
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
                    
                    func_name = left

                    self.instruction_pointer = int(left)
                    
                elif op == 'ENDFUNC':
                    prev_local, prev_temp = self.memory_stack.pop()
                    self.current_local_memory = prev_local
                    self.current_temp_memory = prev_temp
                    
                    ret_addr = self.return_stack.pop()
                    self.instruction_pointer = ret_addr
                    
                else:
                    raise Exception(f"Unknown operator: {op}")
                    
            except Exception as e:
                print(f"Error at quadruple {self.instruction_pointer}: {quad}")
                print(e)
                sys.exit(1)

        print("--- PROGRAM FINISHED ---")
