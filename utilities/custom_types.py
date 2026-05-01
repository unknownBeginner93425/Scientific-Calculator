'''Storing classes of custom data types'''

import os

from enum import StrEnum, IntEnum, auto

class FilePath(str):
    def __new__(cls, value):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(current_dir, value)
        return super().__new__(cls, abs_path)
    
    def __str__(self): 
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        return os.path.join(current_dir, super().__str__()) 
    
    def __fspath__(self): # For os.path functions 
        return str(self)
    
class Cursor():
    '''Value = index at which the new element will be inserted into;
    e.g. 3+7x4 VS cursor at 2 and insert "1" -> 3+27x4'''
    
    def __init__(self):
        self.__pos = 0
        
    @property
    def pos(self) -> int:
        return self.__pos
        
    def increment(self):
        '''+= 1'''
        self.__pos += 1
        
    def decrement(self):
        '''-= 1'''
        self.__pos -= 1
        
    def reset(self):
        '''cursor.pos = 0'''
        self.__pos = 0
        
    def set(self, index: int):
        '''can only be used to move cursor to end of expr; should minimal use'''
        self.__pos = index
        
class DisplayState(StrEnum):
    OFF = auto()
    INPUT = auto()
    RESULT = auto()
    ERROR = auto()
    MENU = auto()
    
class Keymod(StrEnum):
    KEYCAP = auto()
    ALPHA = auto()
    SHIFT = auto()
    STORE = auto()

class Token(IntEnum):
    ANS = 209
    OP_BRACKET = 330
    CL_BRACKET = 331
    COMMA = 332
    SHIFT = 401
    ALPHA = 402
    TURN_ON = 405
    STO = 408
    RECALL = 409
    
class TokenToVariable():
    def __init__(self):
        self.__array = {201: 'A', 202: 'B', 203: 'C', 204: 'D', 205: 'E', 
                        206: 'F', 207: 'X', 208: 'Y', 209: 'Ans', 210: 'M'}

    def __setitem__(self, index, new_value):
        raise AttributeError(f"Cannot modify look-up table")
    
    def __getitem__(self, index):
        return self.__array[index]