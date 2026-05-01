from utilities.stack_and_queue import CircularQueue, Stack
from utilities.sql_handler import SQL
from decimal import Decimal

class ShuntingYard():

    def __init__(self, expr: 'CircularQueue'):
        # in expr, all numbers = float; tokens = int
        self.__INFIX_expr = expr
        self.__RPN_queue = CircularQueue()
        self.__operator_stack = Stack()
        
        self.__func_token = {306, 307, 310, 311, 316, 317, 318, 319, 324, 325, 326, 327, 328, 
                  329, 337, 338, 339, 340, 341}

        # defined here first for clarity; value assigned to later
        self.__associativity = {}   
        self.__precedence    = {}
        
        self.__prep()
        
    def __prep(self):
        sql = SQL()
        op_dict = sql.get_op_attribute()
        del sql
        
        for token, attr in op_dict.items():
            self.__associativity[token] = 'left' if attr[0] == 0 else 'right'
            self.__precedence[token] = attr[1]
        
    def run(self):
        while not self.__INFIX_expr.is_empty():
            value = self.__INFIX_expr.dequeue()
            if isinstance(value, Decimal):                                # is a number
                self.__RPN_queue.enqueue(value)
            elif value in self.__func_token:                              # is a function
                self.__operator_stack.push(value)
            elif value in self.__associativity.keys() and value in self.__precedence.keys():        # is a operator
                op1 = value
                op2 = self.__get_top_operator()
                while op2 in self.__associativity.keys()  \
                    and (self.__precedence[op2] > self.__precedence[op1] \
                        or (self.__precedence[op2] == self.__precedence[op1] \
                            and self.__associativity[op1] == 'left')):
                        self.__pop_op_stack_to_RPN_queue()
                        op2 = self.__get_top_operator()
                self.__operator_stack.push(op1)
            elif value == 332:      # is a comma
                op = self.__get_top_operator()
                while op != 330:
                    self.__pop_op_stack_to_RPN_queue()
                    op = self.__get_top_operator()
            elif value == 330:      # is a open bracket
                self.__operator_stack.push(value)
            elif value == 331:      # is a close bracket
                op = self.__get_top_operator()
                while op != 330:
                    self.__pop_op_stack_to_RPN_queue()
                    op = self.__get_top_operator()
                self.__operator_stack.pop()     # pop and discard the top left parenthesis (330)
                
                next_token = self.__get_top_operator()
                if next_token in self.__func_token:
                    self.__pop_op_stack_to_RPN_queue()
            else: print('error, token not recognized')
                    
        while not self.__operator_stack.is_empty():
            self.__pop_op_stack_to_RPN_queue()
            
    def get_output(self) -> CircularQueue:
        return self.__RPN_queue
                        
    def __get_top_operator(self) -> int | None:
        return self.__operator_stack.peek() if not self.__operator_stack.is_empty() else None
    
    def __pop_op_stack_to_RPN_queue(self) -> None:
        self.__RPN_queue.enqueue(self.__operator_stack.pop())
        