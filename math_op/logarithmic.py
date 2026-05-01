from math_op.utilities import RecursionTermCal, int_pow
from math_op.utilities import sf_round as round
from math_op.arithmetic_and_numerical import Factorial
from math_op.constants import Constant

class NaturalExponentialFunction(RecursionTermCal):
    expression = staticmethod(lambda arg, nth: 
        int_pow(base = arg, power = nth) / Factorial()(nth)
        )
    
    def __call__(self, power):
        if power >= 231:
            raise ValueError('MathError, exceed calculation range')
        elif power <= -228:
            return 0

        return round(self.__reduce_arg(power))
    
    def __reduce_arg(self, argument):
        if argument >= 100:     return Constant.e100 * self.__reduce_arg(argument - 100)
        elif argument <= -100:  return self.__reduce_arg(argument + 100) / Constant.e100
        elif argument >= 10:    return Constant.e10 * self.__reduce_arg(argument - 10)
        elif argument <= -10:   return self.__reduce_arg(argument + 10) / Constant.e10
        
        return self.term_cal(argument)
    
class NaturalLogarithm(RecursionTermCal):
    expression = staticmethod(lambda arg, nth: 
        int_pow(base = -1, power = nth + 1) 
        * int_pow(base = arg, power = nth) / nth
        )
        
    def __call__(self, argument):
        if argument <= 0: raise ValueError('Cannot perform logarithm on negative number or zero')
        if argument == 1: return 0
        return round(self.__reduce_arg(argument))
    
    def __reduce_arg(self, argument):
        if argument > 1.5: return Constant.ln2 + self.__reduce_arg(argument / 2)
        elif argument < 0.5: return self.__reduce_arg(argument * 2) - Constant.ln2
        else: return self.term_cal(argument - 1, 1)

class LogarithmCustomBase():
    def __call__(self, base: float, argument: float):
        return round( NaturalLogarithm()(argument) / NaturalLogarithm()(base)) 
    
class LogarithmBase10():
    def __call__(self, argument: float):
        return round( LogarithmCustomBase()(10, argument))
    
class Cube():
    def __call__(self, base: float):
        return round( int_pow(base, 3))
    
class Square():
    def __call__(self, base: float):
        return round( int_pow(base, 2))
    
class Reciprocal():
    def __call__(self, base: float):
        return round( 1 / base)
    
class CustomPower():
    def __call__(self, base: float, power: float) -> float:
        if power == 0: return 1
        elif base == 0: return 0
        return round( NaturalExponentialFunction()(power * NaturalLogarithm()(base)))
    
class TenToPow():
    def __call__(self, power: float):
        return round( CustomPower()(10, power))

class TenToIntPow():
    def __call__(self, base: float, power: int):
        return round( base * int_pow(10, power))
class CustomRoot():
    def __call__(self, order, radicand):
        return round( CustomPower()(radicand, 1/order))
    
class CubeRoot():
    def __call__(self, radicand: float):
        return round( CustomRoot()(3, radicand))
    
class SquareRoot():
    def __call__(self, radicand: float):
        return round( CustomRoot()(2, radicand))