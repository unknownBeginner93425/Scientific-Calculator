'''Storing classes of custom data types'''

import os

from enum import StrEnum, IntEnum, auto
from typing import Literal
from copy import deepcopy

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
        
class FrameBuffer():
    def __init__(self):
        self.WIDTH, self.HEIGHT = 192, 63
        self.__rgba_data = bytearray(self.WIDTH * self.HEIGHT * 4)
        
    def set_pixel(self, column: int, row: int, data: Literal[0,1]) -> None:
        row = self.__translate_row(row)
        index = (row * self.WIDTH + column) * 4 + 3
        
        self.__rgba_data[index] = 0 if data == 0 else 255
        
    def reset(self, col0: int = 0, row0: int = 0, col1: int = 192, row1: int = 63) -> None:
        for row in range(row0, row1):
            for col in range (col0, col1):
                index = ((self.__translate_row(row)) * self.WIDTH + col) * 4 + 3
                self.__rgba_data[index] = 0
                
    def __translate_row(self, row: int) -> int:
        # translate the conceptual row number (starting from top)
        #   to actual row num in frame buffer (starting from bottom)
        return (self.HEIGHT - 1) - row
        
    def get_data(self) -> bytearray:
        return deepcopy(self.__rgba_data)
        
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
    ADD = 301
    SUB = 302
    NEGATIVE = 320
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