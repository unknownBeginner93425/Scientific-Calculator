from abc import ABC, abstractmethod
from decimal import Decimal, getcontext
from typing import Literal

getcontext().prec = 30

class TaylorSeriesFunction(ABC):
    @abstractmethod
    def __call__(self, arg):
        pass

    @abstractmethod
    def _reduce_arg(self, arg):
        pass

    @abstractmethod
    def _arg_validation(self, arg):
        pass

class RecursionTermCal():
    expression = lambda: None

    def __call__(self, arg) -> Decimal:
        return sf_round(self._arg_validation(arg))
    
    def term_cal(self, arg, nth: int = 0, max_OoM = 'dafault'):
        term = self.expression(arg, nth)
        OoM = get_OoM(term)
        if max_OoM == 'dafault' or OoM > max_OoM: max_OoM = OoM
        else:
            estimate_sum = sf_round(int_pow(10, max_OoM))
            print(nth, term)
            if sf_round(term + estimate_sum) == estimate_sum: return Decimal('0')
        return term + self.term_cal(arg, nth+1, max_OoM)

def int_pow(base, power):
    def iterate(base, power):
        if power == 0: return 1
        return base * iterate(base, power-1)

    if power < 0:
        return Decimal(1 / iterate(base, -1 * power))
    else: return Decimal(iterate(base, power))

def get_OoM(value):
    str_value = str(value)
    
    e_index = str_value.lower().find('e')
    if e_index != -1:
        OoM = int(str_value[e_index + 1:])
    else:
        str_value = str_value.strip('-')
        OoM = -1
        if str_value[0] == '0':
            for number in str_value[2:]:
                if number != '0': break
                OoM -= 1
        else:
            for number in str_value:
                if number == '.': break
                OoM += 1     
    return OoM

def sf_round(value: Decimal, MAX_LENGTH: int = 15) -> Decimal:
    def number_formating(value: Decimal, str_value: str, OoM: int):
        number = str_value.strip('0')
        match len(number):
            case 0:
                return Decimal('0')
            case 1:
                rounded_num = Decimal(f'{number}e{OoM}')
            case _:
                rounded_num = Decimal(f'{number[0]}.{number[1:]}e{OoM}')    
        
        if value < 0: rounded_num *= -1
        return rounded_num
    
    OoM = get_OoM(value)
    
    if OoM > 99: raise ValueError('MathError, exceed calculation range')
    elif OoM < -99: return 0
    
    str_value = str(value).strip('-0.')
    str_value = str_value.replace('.','')
    str_value = str_value.split('e')[0].split('E')[0]
    
    if len(str_value) <= MAX_LENGTH:
        return number_formating(value, str_value, OoM)
    else:
        number = str_value[:MAX_LENGTH]
        if int(str_value[MAX_LENGTH]) >= 5:
            number = str(int(number) + 1)
            if len(number) == 16: OoM += 1 # if incremented

        return number_formating(value, number, OoM)

def sf_round1(value, MAX_LENGTH: int = 15):
    OoM = get_OoM(value)
    print(value, OoM)
    if OoM > 99: raise ValueError('MathError, exceed calculation range')
    elif OoM < -99: return 0
    
    str_value = str(value).strip('-0.')
    str_value = str_value.replace('.','')

    if str_value.find('e') != -1:
        str_value = str_value[:str_value.find('e')]
        
    if len(str_value) <= MAX_LENGTH:
        return return_type_fix(value)
    else:
        number = str_value[:MAX_LENGTH]; temp = len(number)
        if int(str_value[MAX_LENGTH]) >= 5:
            number = str(int(number) + 1)
            if temp + 1 == len(number): # increments
                OoM += 1
        number = number.strip('0')
        
        if len(number) == 1:
            rounded_num = int(number[0])
        else:
            rounded_num = float(number[0]+'.'+number[1:])
        if value < 0: rounded_num *= -1
        return return_type_fix(float(f'{rounded_num}e{OoM}'))
        
def return_type_fix(value):
    if value % 1 == 0:
        return int(value)
    return value