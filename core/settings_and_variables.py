from utilities.custom_types import Keymod
from typing import Literal, get_args

class SettingsManager():
    __switched_on = False
    __keymod = Keymod.KEYCAP
    
    @property
    def switched_on(self):
        return self.__switched_on
    
    @switched_on.setter
    def switched_on(self, value: bool):
        self.__switched_on = value
        
    @property
    def keymod(self):
        return self.__keymod
    
    @keymod.setter
    def keymod(self, value: Keymod):
        self.__keymod = value
      
    __settings = {'I_method': 1,                # nevermind now as only one I/O method
                  'O_method': 1,
                  'angle_unit': 'D',
                  'number_format': 0,           # nevermind now
                  'fraction_result': 0,         # nevermind
                  'statistics': False,          # nevermind
                  'table': 0,                   # nevermind
                  'recurring_dec': False,       # nevermind
                  'decimal_mark': 0,            # nevermind
                  'digit_separator': False,     # nevermind
                  'multiLine_font': 0,          # nevermind
                  'screen_type': 1              # 0 for txtbox; 1 for bitmap
                  }
    
    __settings_name = Literal['I_method', 'O_method', 'angle_unit', 
                                'number_format', 'fraction_result',
                                'statistics', 'table','recurring_dec', 
                                'decimal_mark', 'digit_separator', 
                                'multiLine_font', 'screen_type']
    
    def set(self, name: __settings_name, value: int|bool|str) -> None:
        '''set single setting'''
        if name in self.__settings:
            self.__settings[name] = value
            
    def get(self, name: __settings_name) -> int|bool|str:
        '''get single setting'''
        return self.__settings.get(name, None)
    
    def apply_settings(self, settings: tuple[int]) -> None:
        for name, value in zip(get_args(self.__settings_name), settings):
            if name == 'angle_unit':
                self.__settings[name] = {0: 'D', 1: 'R', 2: 'G'}[value]
            else:
                self.__settings[name] = bool(value) if name in \
                    ('statistics', 'recurring_dec', 'digit_separator') else value
 
    def get_settings(self) -> tuple[int]:
        '''get all settings; include translation into int'''
        return tuple( [ int(self.__settings[setting]) \
            if setting in ('statistics', 'recurring_dec', 'digit_separator') \
                else {'D': 0, 'R': 1, 'G': 2}[self.__settings[setting]] if setting == 'angle_unit' \
                    else self.__settings[setting] \
                        for setting in get_args(self.__settings_name) ] )
               
class VariableMemory():
    __var_names = Literal['A', 'B', 'C', 'D', 'E', 'F', 'X', 'Y', 'M', 'Ans']
    __vars = {name: 0 for name in get_args(__var_names)}
    
    def set(self, name: __var_names, value: float|int) -> None:
        if name in self.__vars:
            self.__vars[name] = value
            
    def set_all(self, values: tuple[float|int]) -> None:
        '''setter for all variables except Ans; values from SQL'''
        if len(values) != 9: raise IndexError('Parameter "values" has wrong size')
        
        names = get_args(self.__var_names)
        for _ in range(9):
            self.__vars[names[_]] = values[_]
            
    def get(self, name: __var_names) -> float| int:
        return self.__vars.get(name, 0)

    # not including the Ans var as not stored in memory -> volatile
    def get_all(self) -> tuple[float|int]:
        return tuple(self.__vars.values())[:-1]
