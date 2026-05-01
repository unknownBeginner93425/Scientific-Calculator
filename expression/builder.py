from copy import deepcopy
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from utilities.custom_types import Cursor

class ExpressionArray():
    def __init__(self, cursor: 'Cursor'):
        self.__array = []
        self.__pointer = cursor
        
    def __append(self, value: int):
        '''insert to the end + increment cursor'''
        self.__array.append(value)
        self.__pointer.increment()
                    
    def __insert(self, value: int):
        self.__array.insert(self.__pointer.pos, value)
        self.__pointer.increment()
        
    def update(self, value: int):
        '''add token to expr.'''
        if self.__pointer.pos == len(self.__array):
            self.__append(value)
        else:
            self.__insert(value)
        
    def remove(self) -> int:
        '''pop token before cursor'''
        self.__pointer.decrement()
        return self.__array.pop(self.__pointer.pos)
        
    def repr(self) -> List[int]:
        '''return entire array'''
        return deepcopy(self.__array)