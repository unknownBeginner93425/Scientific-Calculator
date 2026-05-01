from utilities.exception_definition import StackOverflowError, StackUnderflowError
from utilities.exception_definition import QueueOverflowError, QueueUnderflowError

from typing import Any
class Stack():
    def __init__(self, max_size = 99):
        self.__array = [None] * max_size
        self.__pointer = 0          # value = index of next available space
        self.__max_size = max_size
        
    def push(self, value: Any) -> None:
        if self.is_full(): raise StackOverflowError
        self.__array[self.__pointer] = value
        self.__pointer += 1
        
    def pop(self) -> Any:
        if self.is_empty(): raise StackUnderflowError
        self.__pointer -= 1
        value = self.__array[self.__pointer]
        self.__array[self.__pointer] = None
        return value
        
    def peek(self) -> Any:
        if self.is_empty(): raise StackUnderflowError
        return self.__array[self.__pointer - 1]
        
    def is_empty(self) -> bool:
        return self.__pointer == 0
    
    def is_full(self) -> bool:
        return self.__pointer == self.__max_size
    
    def size(self) -> int:
        return self.__pointer
    
    def count(self, value: Any) -> int:
        '''count occurance of value in stack'''
        return self.__get_elements().count(value)
    
    def __get_elements(self) -> list[Any]:
        return self.__array[:self.__pointer]
    
    def __repr__(self):
        return f'Stack({self.__get_elements()})'
    
class CircularQueue():
    '''Circular Queue: default size = 99'''
    def __init__(self, max_size = 99):
        self.__queue = [None] * max_size
        
        self.__front_pt = -1        # index of first element
        self.__rear_pt = -1         # index of last element
        
        self.__max_size = max_size
        
    def __next_rear(self) -> int:
        return (self.__rear_pt + 1) % self.__max_size
    
    def __next_front(self) -> int:
        return (self.__front_pt + 1) % self.__max_size
        
    def enqueue(self, value: Any) -> None:
        if self.is_full():
            raise QueueOverflowError
        
        if self.__front_pt == -1: self.__front_pt = 0
        
        self.__rear_pt = self.__next_rear()
        
        self.__queue[self.__rear_pt] = value
        
    def dequeue(self) -> Any:
        value = self.inspect_front()
        
        if self.__front_pt == self.__rear_pt:
            self.__front_pt, self.__rear_pt = -1, -1
        else:
            self.__front_pt = self.__next_front()
        
        return value
        
    def is_empty(self) -> bool:
        return self.__front_pt == -1
    
    def is_full(self) -> bool:
        return self.__next_rear() == self.__front_pt
    
    def size(self) -> int:
        if self.__front_pt == -1:
            return 0
        if self.__rear_pt >= self.__front_pt:
            return self.__rear_pt - self.__front_pt + 1
        else:
            return self.__max_size - (self.__front_pt - self.__rear_pt - 1)
    
    def count(self, value) -> int:
        return self.__get_elements().count(value)
    
    def inspect_front(self) -> Any:
        if self.is_empty(): raise QueueUnderflowError
        return self.__queue[self.__front_pt]
    
    def __get_elements(self) -> list[Any]:
        if self.__front_pt <= self.__rear_pt:
            return self.__queue[self.__front_pt: self.__rear_pt + 1]
        else:
            return self.__queue[self.__front_pt:] + self.__queue[:self.__rear_pt +1 ]
    
    def __repr__(self):
        return f'Queue({self.__get_elements()})'
        
def stack_to_queue(stack: Stack) -> CircularQueue:
    temp_stack = Stack()
    while not stack.is_empty():
        temp_stack.push(stack.pop())
        
    queue = CircularQueue()
    while not temp_stack.is_empty():
        queue.enqueue(temp_stack.pop())
        
    return queue

def queue_to_stack(queue: CircularQueue) -> Stack:
    stack = Stack()
    while not queue.is_empty():
        stack.push(queue.dequeue())
        
    return stack