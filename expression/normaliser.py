from utilities.stack_and_queue import CircularQueue, Stack, stack_to_queue, queue_to_stack
from utilities.exception_definition import CommaError, BracketError
from utilities.custom_types import Token, TokenToVariable

from expression.utilities import NumberTokenQueue

from copy import deepcopy
from typing import Literal, List, Set, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from core.settings_and_variables import VariableMemory

class Normalisation():
    def __init__(self, input_method: Literal[0, 1], num_var: 'VariableMemory'):
        '''0: MathI    ;    1: LineI'''
        self.__input_method = input_method
        self.__var = num_var
        
    def normalise(self, expr: List[int]) -> CircularQueue:
        match self.__input_method: # difference = parenthesis 
            case 0: pass
            case 1: return self.__lineI_normalise(expr)
            
    def __lineI_normalise(self, expr: List[int]) -> CircularQueue:
        # i.e. those with a left bracket -> ^(, log(, sin(
        parenthesis_func = {306, 307, 310, 311, 314, 315, 316, 317, 318, 319,
                            324, 325, 326, 327, 328, 329, 337, 338, 339, 341}
        
        func_token = {306, 307, 310, 311, 316, 318, 319,
                      324, 325, 326, 327, 328, 329, 337, 338, 339, 341}
        
        multi_arg_func   = {307, 316, 337, 338, 341}
        
        var_name  = TokenToVariable()
        
        # object nature = new_expr will be passed around & altered
        ''' --- Normalisation pipeline --- '''
        new_expr = StructuralNormalisation()(expr, parenthesis_func, multi_arg_func)
        new_expr = SemanticNormalisation()(new_expr, func_token)
        new_expr = FinaliseNormalisation()(new_expr, self.__var, var_name)
        ''' -------------------------------'''
        
        return stack_to_queue(new_expr)        
    
class StructuralNormalisation():
    def __call__(self, expr: List[int], parenthesis_func: Set[int], multi_arg_func: Set[int]):
        new_expr = Stack()
        self.__insertion_logic(expr, new_expr, parenthesis_func)
        self.__finalize_num_if_needed(new_expr)
        self.__balance_parenthesis(new_expr)
        self.__validate_comma_usage(new_expr, multi_arg_func)
        return new_expr
        
    def __insertion_logic(self, ori_expr: List[int], expr: Stack, parenthesis_func: Set[int]) -> None:
        '''loop through tokens in expr; translate digit tokens into number 
        & add left parenthesis for function token'''
        for token in ori_expr:
            match token // 100:
                case 1: 
                    if expr.is_empty() or not self.__expr_top_is_num_queue(expr):  # if is first digit of number
                        self.__start_new_num_queue(expr)
                    expr.peek().enqueue(token)
                        
                case 2: 
                    self.__finalize_num_if_needed(expr)
                    expr.push(token)                        # variables & constants dealt at last
                    
                case 3:
                    self.__finalize_num_if_needed(expr)
                    self.__handle_func_token(token, expr, parenthesis_func)
                    
    def __expr_top_is_num_queue(self, expr: Stack) -> bool:
        return isinstance(expr.peek(), NumberTokenQueue)
    
    def __start_new_num_queue(self, expr: Stack) -> None:
        new_num = NumberTokenQueue()
        expr.push(new_num)
        
    def __finalize_num_if_needed(self, expr: Stack) -> None:
        '''convert the number queue into float value'''
        if not expr.is_empty() and self.__expr_top_is_num_queue(expr):
            number = expr.pop().convert_to_num()
            expr.push(number)
            
    def __handle_func_token(self, token: int, expr: Stack, parenthesis_func: Set[int]) -> None:
        expr.push(token)
        if token in parenthesis_func:
            expr.push(Token.OP_BRACKET)  # opening bracket
            
    def __balance_parenthesis(self, expr: Stack) -> None:
        '''if more open bracket than close bracket -> add close brack in the end of expr'''
        while expr.count(Token.OP_BRACKET) > expr.count(Token.CL_BRACKET):
            expr.push(Token.CL_BRACKET)
        
        if expr.count(Token.OP_BRACKET) < expr.count(Token.CL_BRACKET):
            raise BracketError
            
    def __validate_comma_usage(self, expr: Stack, multi_arg_func: Set[int]) -> None:
        '''deal with comma
        -> comma = only valid in some functions'''
        
        temp_expr1 = deepcopy(expr)
        
        for _ in range(expr.count(Token.COMMA)):
            while temp_expr1.pop() != Token.COMMA:
                pass
            
            pre_close_brack = 0
            temp_expr2 = deepcopy(temp_expr1)
            
            valid = False
            while temp_expr2.size() > 0:
                # match-case = for comma usage validation overall
                match temp_expr2.pop():
                    case Token.CL_BRACKET:   
                        pre_close_brack += 1
                    case Token.OP_BRACKET:   
                        pre_close_brack -= 1
                        
                        if pre_close_brack == -1:
                            # when pre_close_brack = -1 -> reach open bracket near the comma's corr. func.
                            if not temp_expr2.peek() in multi_arg_func:
                                raise CommaError
                            else: valid = True; break
            if not valid: raise CommaError

    def __unary_plus_minus(self, expr: Stack):
        output_stack = Stack()
        
        for token in expr:
            if token not in {301, 302, 320}: # is not plus/minus sign
                output_stack.push(token)
                continue
            if output_stack.is_empty():
                if token == 301: continue
                else: output_stack.push(320); continue
            if expr.pop() in {301, 302, 320}: pass
        
class SemanticNormalisation():
    def __call__(self, expr: Stack, func_token: Set[int]) -> Stack:
        expr = self.__normalise_log(expr)
        expr = self.__insert_implicit_mult(expr, func_token)
        return expr
    
    def __normalise_log(self, expr: Stack) -> Stack:
        '''deal with log base 10 VS log custom base
        convertable in LineI mode'''

        ori_expr_ref = stack_to_queue(deepcopy(expr))
        expr_new_ver = Stack()
        
        temp_queue = CircularQueue()
            
        checking = False   # checkinging log func.
        
        while not ori_expr_ref.is_empty():
            element = ori_expr_ref.dequeue()
            
            if element in {307, 316} and not checking: 
                checking = True; pre_open_brack = 0
                comma = False   # there's a corr. comma
            
            if not checking:
                expr_new_ver.push(element); continue
                
            # if checking
            temp_queue.enqueue(element)
            
            if element == Token.OP_BRACKET:   
                pre_open_brack += 1
            elif element == Token.CL_BRACKET:  
                pre_open_brack -= 1
                if pre_open_brack == 0:
                    checking = False
                            
                    temp_queue.dequeue()    # discard the log token
                            
                    expr_new_ver.push(307 if comma else 316)

                    while not ori_expr_ref.is_empty():
                        temp_queue.enqueue(ori_expr_ref.dequeue())
                    ori_expr_ref = deepcopy(temp_queue); temp_queue = CircularQueue()
                                
            elif element == Token.COMMA:  
                if pre_open_brack == 1:
                    comma = True

        return expr_new_ver 
                                   
    def __insert_implicit_mult(self, expr: Stack, func_token: Set[int]) -> Stack:
        '''add token 345 for implicit multiplication (where sign is omitted)
        e.g. (...)(...) -> (...)x(...)
        e.g. 6sin(7) -> 6 x sin(7)
        e.g. 2pi -> 2 x pi
        e.g. AB -> A x B
        invalid syntax -> e.g. A3, sin(4)9.2, e2pi'''
        expr_new_ver = CircularQueue()
        expr_ori_ref = stack_to_queue(deepcopy(expr))
        
        while not expr_ori_ref.is_empty():
            element = expr_ori_ref.dequeue()
            expr_new_ver.enqueue(element)
            
            if not expr_ori_ref.is_empty():
                next_element = expr_ori_ref.inspect_front()
                # current value is close bracket or number, followed by open bracket or function
                # current value is number or variable or constant, followed by variable or constant
                if (element == Token.CL_BRACKET or element // 100 == 2 or isinstance(element, Decimal)) \
                    and (next_element == Token.OP_BRACKET or next_element in func_token or next_element // 100 == 2):
                        expr_new_ver.enqueue(345)

        return queue_to_stack(expr_new_ver)
    
class FinaliseNormalisation():
    def __call__(self, expr: Stack, vars: 'VariableMemory', var_names: dict[int,str]) -> Stack:
        self.__var = vars
        self.__var_name = var_names
        return self.__resolve_symbols(expr)
    
    def __resolve_symbols(self, expr: Stack) -> Stack:
        '''convert remaining variable/constant token into actual value'''
        temp = stack_to_queue(expr)
        finalised_expr = Stack()
        while not temp.is_empty():
            value = temp.dequeue()
            if value // 100 != 2:
                finalised_expr.push(value)
            else:
                if value not in {211, 212}:
                    finalised_expr.push(self.__var.get(self.__var_name[value]))
                else:
                    from math_op.constants import Constant
                    var = {211: Constant.pi, 212: Constant.e}
                    finalised_expr.push(var[value])
                            
        return finalised_expr
    
