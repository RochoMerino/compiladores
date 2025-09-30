from collections import deque

description = '''
Stack (LIFO - Last In First Out)
      
A stack is a linear data structure that follows LIFO principle.
Last element that is added to the stack is the first one to be removed.

Stack operations:
- Push: Add an element to the top of the stack.
- Pop: Remove the top element from the stack.
- Peek: Get the value of the top element without removing it.
      
Common implementations:
        - A stack of plates where you add and remove the top plate only (real world analogy).

TEST CASES:
- Initialize an empty stack.
- Push elements: 1, 2, 3.
- Peek the top element -> should return 3.
- Pop an element -> should remove and return 3.
- Check if the stack is empty -> should return False.
- Get the size of the stack -> should return 2.
      '''

print(description)

class Stack:
    def __init__(self):
        self.stack = []  

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):

        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)


print("--- STACK ---")
my_stack = Stack()
print(f"Empty stack: {my_stack}")
my_stack.push(1)
my_stack.push(2)
my_stack.push(3)
print(f"Stack after push: {my_stack}")
print(f"Peek: {my_stack.peek()}")
print(f"Pop: {my_stack.pop()}")
print(f"Final stack: {my_stack}")
