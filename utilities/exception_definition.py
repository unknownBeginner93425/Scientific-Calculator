class StackOverflowError(Exception):
    def __init__(self, message = 'Stack Overflow Error: stack is full'):
        super().__init__(message)
        
class StackUnderflowError(Exception):
    def __init__(self, message = 'Stack Underflow Error: stack is empty'):
        super().__init__(message)
        
class QueueOverflowError(Exception):
    def __init__(self, message = 'Queue Overflow Error: queue is full'):
        super().__init__(message)  
              
class QueueUnderflowError(Exception):
    def __init__(self, message = 'Queue Underflow Error: queue is empty'):
        super().__init__(message)
    

class MathError(Exception):
    def __init__(self, message = 'Math ERROR'):
        super().__init__(message)
        
class SyntaxError(Exception):
    def __init__(self, message = 'Syntax ERROR'):
        super().__init__(message)
        
class ZeroDivisionError(MathError):
    def __init__(self, message = 'Math ERROR: zero division error'):
        super().__init__(message)
        
class MultipleDecimalPointError(SyntaxError):
    def __init__(self, message = 'Syntax ERROR: more than one decimal point in number'):
        super().__init__(message)
        
class CommaError(SyntaxError):
    def __init__(self, message = 'Syntax ERROR: comma within parenthesis of single arg func'):
        super().__init__(message)
        
class BracketError(SyntaxError):
    def __init__(self, message = 'Syntax ERROR: more close bracket than open bracket in expression'):
        super().__init__(message)
        