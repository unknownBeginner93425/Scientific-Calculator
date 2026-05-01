from math_op.utilities import sf_round as round
from utilities.exception_definition import ZeroDivisionError

class Addition():
    def __call__(self, value1: float, value2: float) -> float:
        return round(value1 + value2)
    
class Subtraction():
    def __call__(self, value1: float, value2: float) -> float:
        return round(value1 - value2)
    
class Multiplication():
    def __call__(self, value1: float, value2: float) -> float:
        return round(value1 * value2)
    
class Division():
    def __call__(self, dividend: float, divisor: float) -> float:
        if divisor == 0: raise ZeroDivisionError
        return round(dividend / divisor)
    
class Negative():
    def __call__(self, value: float) -> float:
        return round(-1 * value)
    
class AbsoluteValue():
    def __call__(self, value: float) -> float:
        if value >= 0: return value
        else: return value * -1
        
class Factorial():
    def __call__(self, end_pt: int) -> int:
        if end_pt % 1 != 0 and end_pt < 0: raise ValueError('For n!, n must be non-negative integer')
        elif end_pt > 69: raise ValueError('Exceed accepted input range of n!: 0 <= n <= 69')
        return round(self.__recursion(end_pt))
    
    def __recursion(self, value): 
        if value == 0: return 1
        return value * self.__recursion(value - 1)
    
class Permutation():
    def __call__(self, n: int, r: int) -> int:
        if not (0 <= r <= n and r % 1 == 0 and n % 1 == 0):
            raise ValueError('Argument must be integer and 0 <= r <= n')
        return round(Factorial()(n) / Factorial()(n-r))
    
class Combination():
    def __call__(self, n: int, r: int) -> int:
        if not (0 <= r <= n and r % 1 == 0 and n % 1 == 0):
            raise ValueError('Argument must be integer and 0 <= r <= n')
        return round(Permutation()(n, r) / Factorial()(r))
    
class Percentage():
    def __call__(self, value: float) -> float:
        return round(0.01 * value)