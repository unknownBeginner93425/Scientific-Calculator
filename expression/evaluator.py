from utilities.stack_and_queue import Stack
from utilities.exception_definition import SyntaxError

from math_op.arithmetic_and_numerical import *
from math_op.constants import *
from math_op.logarithmic import *
from math_op.trigonometric import *
from math_op.utilities import sf_round as round

import inspect

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.stack_and_queue import CircularQueue
    
class Evaluation():
    __token_to_class = {301: Addition,
                      302: Subtraction,
                      303: Multiplication,
                      304: Division,
                      305: Cube,
                      306: AbsoluteValue,
                      307: LogarithmCustomBase,
                      310: SquareRoot,
                      311: CubeRoot,
                      312: Square,
                      314: CustomPower,
                      315: CustomRoot,
                      316: LogarithmBase10,
                      317: TenToPow,
                      318: NaturalLogarithm,
                      319: NaturalExponentialFunction,
                      320: Negative,
                      322: Reciprocal,
                      323: Factorial,
                      324: Sin,
                      325: Arcsin,
                      326: Cos,
                      327: Arccos,
                      328: Tan,
                      329: Arctan,
                      335: Permutation,
                      336: Combination,
                      342: Percentage,
                      344: TenToIntPow,
                      345: Multiplication
                      }
    
    def __init__(self, RPN_expr: 'CircularQueue'):
        self.__expr = RPN_expr
        
    def evaluate(self) -> float:
        output_stack = Stack()
        
        while not self.__expr.is_empty():
            value = self.__expr.dequeue()
            
            if isinstance(value, Decimal):    # is a number
                output_stack.push(value)
            else:                           # is a func. or op.
                # find num. of required parameters
                class_ref = self.__token_to_class.get(value)
                method_sig = inspect.signature(class_ref())     # get sig of __call__ method
                num_of_arg = len([p for p in method_sig.parameters.values() 
                                  if p.default == inspect._empty 
                                  and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)])
                
                match num_of_arg:
                    case 1:
                        op = output_stack.pop()
                        output_stack.push(class_ref()(op))
                    case 2:
                        op2 = output_stack.pop()
                        op1 = output_stack.pop()
                        output_stack.push(class_ref()(op1, op2))
        
        if output_stack.size() == 1:        
            return round(output_stack.pop(), 10)
        else:
            raise SyntaxError
            