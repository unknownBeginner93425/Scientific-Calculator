from math_op.utilities import RecursionTermCal, get_OoM, int_pow
from math_op.utilities import sf_round as round
from math_op.arithmetic_and_numerical import Factorial
from math_op.constants import Constant

class Sin(RecursionTermCal):
    expression = staticmethod(lambda arg, nth:
        int_pow(-1, nth) / Factorial()(2 * nth + 1) 
        * int_pow(arg, 2 * nth + 1)
        )
    
    def __call__(self, value) -> float:
        return round(self.__reduce_arg(value))
    
    def __reduce_arg(self, value):
        return self.term_cal(value % (2 * Constant.pi))

class Cos(RecursionTermCal):
    expression = staticmethod(lambda arg, nth:
        int_pow(-1, nth) / Factorial()(2 * nth)
        * int_pow(arg, 2 * nth)
        )
    
    def __call__(self, value) -> float:
        return round(self.__reduce_arg(value))
    
    def __reduce_arg(self, value):
        return self.term_cal(value % (2 * Constant.pi))

class Tan(RecursionTermCal):
    expression = staticmethod(lambda arg, nth:
        Constant.Bernoulli_number[2 * nth] * int_pow(-4, nth) 
        * (1 - int_pow(4, nth)) / Factorial()(2 * nth) 
        * int_pow(arg, 2 * nth - 1)
        )
    
    def __call__(self, value) -> float:
        return round(self.__reduce_arg(value))
    
    def __reduce_arg(self, value):
        from math_op.arithmetic_and_numerical import AbsoluteValue
        
        magnitude = AbsoluteValue()(value)
        if magnitude > Constant.pi: return self.__reduce_arg(value % Constant.pi)

        if magnitude > 0.7:
            tan_half_x = super().term_cal(value / 2, 1)
            return 2 * tan_half_x / (1 - int_pow(tan_half_x, 2))
        else: return super().term_cal(value, 1)

class Arcsin(RecursionTermCal):
    # expression can't be made as lambda func -> as subroutine
    
    def __call__(self, value) -> float:
        return round(self.__reduce_arg(value))
    
    def __reduce_arg(self, value):
        from math_op.logarithmic import SquareRoot

        if value < -0.7:
            return -1 * ( Constant.pi / 2 - self.term_cal( SquareRoot()(1-int_pow(value, 2)), 0) )
        elif value > 0.7: return Constant.pi / 2 - self.term_cal( SquareRoot()(1-int_pow(value, 2)), 0)
        else: return super().term_cal(value)
    
    @staticmethod
    def expression(arg, nth: int = 0):
        if nth < 35:
            term = Factorial()(2 * nth) * int_pow(arg, 2*nth + 1)\
            / (int_pow(4, nth) * int_pow(Factorial()(nth), 2) * (2*nth + 1))
        else:
            term = Constant.fact35 * int_pow(arg, 2*nth + 1)\
            / (int_pow(4, nth) * (2*nth + 1))

            temp = Constant.fact35
            count = 36
            while count <= nth: temp *= count ; term *= count ; count += 1
            while count <= 2*nth: term *= count ; count += 1
            term /= int_pow(temp, 2)

        return term

class Arccos():
    def __call__(self, value):
        return round(Constant.pi / 2 - Arcsin()(value))

class Arctan(RecursionTermCal):
    expression = staticmethod(lambda arg, nth: 
        int_pow(-1, nth) * int_pow(arg, 2*nth + 1) / (2*nth + 1))
    
    def __call__(self, value) -> float:
        return round(self.__reduce_arg(value))
    
    def __reduce_arg(self, value):
        from math_op.arithmetic_and_numerical import AbsoluteValue

        if AbsoluteValue()(value) >= 1: return Constant.pi / 2 - super().term_cal(1 / value)
        else: return super().term_cal(value)
