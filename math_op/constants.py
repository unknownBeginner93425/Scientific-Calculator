from decimal import Decimal

class __ReadOnlyMeta(type):
    def __setattr__(cls, name, value):
        raise AttributeError(f"Cannot modify read-only attribute '{name}'")
        
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if isinstance(value, (float,int)): return Decimal(value)
        else: return value            
    
class Constant(metaclass=__ReadOnlyMeta):
    # define a List class with set access block 
    class LookUpTable():
        def __init__(self, array):
            self.__array = array

        def __setitem__(self, index, new_value):
            raise AttributeError(f"Cannot modify look-up table")
        
        def __getitem__(self, index):
            return Decimal(self.__array[index])

    e =         2.718281828459045
    e10 =       22026.465794806716516957900645284
    e100 =      2.68811714181613544841262555158e+43
    ln2 =       0.69314718055994530941723212145818
    pi =        3.1415926535897932384626433832795
    fact35 =    1.03331479663861449296666513375232e+40
    fact69 =    1.711224524281413113724683388812728e+98

    Bernoulli_number = LookUpTable({
        0: 1,
        1: -1/2,
        2: 1/6,
        4: -1/30,
        6: 1/42,
        8: -1/30,
        10: 5/66,
        12: -691/2730,
        14: 7/6,
        16: -3617/510,
        18: 43867/798,
        20: -174611/330,
        22: 854513/138,
        24: -236364091/2730,
        26: 8553103/6,
        28: -23749461029/870,
        30: 8615841276005/14322,
        32: -7709321041217/510,
        34: 2577687858367/6,
        36: -26315271553053477373/1919190,
        38: 2929993913841559/6,
        40: -261082718496449122051/13530,
        42: 1520097643918070802691/1806,
        44: -27833269579301024235023/690,
        46: 596451111593912163277961/282,
        48: -5609403368997817686249127547/46410,
        50: 495057205241079648212477525/66
        })
