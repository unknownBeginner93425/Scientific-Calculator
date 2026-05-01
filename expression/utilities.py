from utilities.stack_and_queue import CircularQueue
from utilities.exception_definition import MultipleDecimalPointError

from decimal import Decimal, getcontext

class NumberTokenQueue(CircularQueue):
    def __init__(self):
        super().__init__()
        getcontext().prec = 30
        
    def enqueue(self, token: int) -> None:
        if token == 111:        # decimal point
            if self.count(111) != 0:    # if there's already a decimal point in the number
                raise MultipleDecimalPointError
            elif self.is_empty():
                super().enqueue(101)      # add a leading 0 before the decimal point
        super().enqueue(token)
    
    def convert_to_num(self) -> float:
        token_to_num = {101: '0', 102: '1', 103: '2', 104: '3', 105: '4', 
                        106: '5', 107: '6', 108: '7', 109: '8', 110: '9',
                        111: '.'}
        
        return float(''.join([token_to_num[self.dequeue()] for _ in range(self.size())]))
    


