from math_op.logarithmic import NaturalLogarithm, NaturalExponentialFunction, int_pow
from math_op.utilities import get_OoM
from math_op.utilities import sf_round as round

numbers = [456, 0, 1, 156456789123456, 1234567891023654,
           0.025, 4564.1654, 0.000000000000001235, 0.000000000001235, 0.0000544847112154841215, 21348413213.216841231,
           1.235e+100, 9.999e+99, 9.999999999e+99, 0.999999999e-99, 1.258e-99, 5.44847112154841215e+15, 214e+7]

test_values = [
    # Boundary / Extremes
    1e-99,
    -1e-99,
    9.999999999e+99,
    -9.999999999e+99,
    -9.999999999e+98,
    0.0,

    # Rounding-sensitive values
    1.00000000005,
    0.99999999995,
    1/3,                         # Repeating decimal
    1.23456789123456789e10,
    2.5,

    # Typical numbers
    42,
    -17,
    3.14159265,
    -2.71828182,
    230,
    -227,
    -228,

    # Scientific notation edge play
    1e-45,
    1e+45,

    # Mathematical constants
    3.141592653589793,           # Pi
    2.718281828459045,           # Euler's number e
    1.6180339887                 # Golden Ratio φ
]


for number in test_values:
    try:
        print(f'argument:\t{number}\tln(arg):\t{NaturalLogarithm()(number)}')
        
    except ValueError as e:
        print(f'argument:\t{number}\terror:\t{e}')
    try:
        print(f'argument:\t{number}\te^(arg):\t{NaturalExponentialFunction()(number)}')
        
    except ValueError as e:
        print(f'argument:\t{number}\terror:\t{e}')
        
    
#print(round(9.94e-123), get_OoM(9.94e-123))
#print(round(0.00))