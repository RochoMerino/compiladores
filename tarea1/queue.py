description = '''
Queue (FIFO - First In First Out)

A queue is a linear data structure that follows FIFO principle.
First element that is added to the queue is the first one to be removed.

Queue operations:
- Enqueue: Add an element to the back of the queue.
- Dequeue: Remove the front element from the queue.
- Peek: Get the value of the front element without removing it.

Common implementations:
      - Queues in order to join a game or service and follow the order of arrival.

TEST CASES:
- Initialize an empty queue.
- Enqueue elements: 1, 2, 3.
- Peek the front element -> should return 1.
- Dequeue an element -> should remove and return 1.
- Check if the queue is empty -> should return False.
- Get the size of the queue -> should return 2.
      '''

print(description)

from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        return None

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def __str__(self):
        return str(list(self.queue))


print("--- QUEUE ---")
my_queue = Queue()
print(f"Empty queue: {my_queue}")

my_queue.enqueue(1)
my_queue.enqueue(2)
my_queue.enqueue(3)
print(f"Queue after enqueue: {my_queue}")

print(f"Peek: {my_queue.peek()}")

print(f"Dequeue: {my_queue.dequeue()}")

print(f"Final queue: {my_queue}")
print(f"Is the queue empty?: {my_queue.is_empty()}")
print(f"Queue size: {my_queue.size()}")