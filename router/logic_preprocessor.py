from typing import TYPE_CHECKING, Literal

from router.input_action import InputAction, ActionKind

from utilities.custom_types import Keymod, Token
from utilities.sql_handler import SQL

if TYPE_CHECKING:
    from main import Main
    from core.settings_and_variables import SettingsManager    
    
class LogicPreprocessor():
    def __init__(self, main_ref: 'Main', settings_manager: 'SettingsManager'):
        self.__main = main_ref
        #self.__main_logic = logic
        self.__cal_state = settings_manager

        # defined as those taking same effect in all non-off display mode
        # i.e. shift, alpha, on and off
        self.__high_lvl_func = {401: lambda: self.__set_keymod(Keymod.SHIFT),
                                402: lambda: self.__set_keymod(Keymod.ALPHA),
                                408: lambda: self.__set_keymod(Keymod.STORE),
                                405: lambda: InputAction(kind=ActionKind.TURN_ON),
                                419: lambda: InputAction(kind=ActionKind.TURN_OFF)}
    
    def on_button_press(self, token: int) -> int| InputAction:
        # exit if calculator switched off and is not turning it on
        if not self.__cal_state.switched_on and token != Token.TURN_ON: 
            return InputAction(kind=ActionKind.IGNORE)
        
        # find corresponding token if shift/alpha/store mode is on
        # token == None = invalid = no further actions needed
        token = self.__keymod_handler(token)
        if token == None: 
            return InputAction(kind=ActionKind.IGNORE)
        
        if token in self.__high_lvl_func:
            return self.__high_lvl_func[token]()
            
        return token
    
        
    def __keymod_handler(self, token: int) -> tuple[int|None, Keymod]:
        # valid choice = return int token
        # invalid      = return None
        # shift / alpha (401/402) = return None
        # None = identified by caller (on_button_press) = no further actions
        
        keymod = self.__cal_state.keymod  
              
        # no need to go through SQL statements if shift/alpha/store button pressed
        # as retrieved token = None and will impact func mapping afterwards
        if token in {Token.SHIFT, Token.ALPHA, Token.STO}:
            # exception = RECALL (409) which is shift func of STORE (408)
            if keymod == Keymod.SHIFT and token == Token.STO: #'shift' and token == 408:
                token = Token.RECALL; self.__set_keymod(Keymod.KEYCAP)
            return token
        
        sql = SQL()
        # find the corresponding token if keypad is shifted or alpha"ed"
        # cancel shift or alpha mode by default
        match keymod:
            case Keymod.KEYCAP: output = token
            case Keymod.SHIFT:  output = sql.find_shift_func(token); self.__set_keymod(Keymod.KEYCAP)
            case Keymod.ALPHA:  output = sql.find_alpha_func(token); self.__set_keymod(Keymod.KEYCAP)
            case Keymod.STORE:  output = sql.find_store_func(token); self.__set_keymod(Keymod.KEYCAP)
        del sql
            
        return output
        
    def __set_keymod(self, new_mode: Keymod):
        mode_indi = {Keymod.KEYCAP: None,
                     Keymod.SHIFT: 501,
                     Keymod.ALPHA: 502,
                     Keymod.STORE: 504}
        
        ori_mode = self.__cal_state.keymod
        
        # shifted mode + press shift button = cancel shift mode
        if ori_mode == new_mode:        self.__main.indicator_on_off(mode_indi[ori_mode]); new_mode = Keymod.KEYCAP
        elif ori_mode == Keymod.KEYCAP:      self.__main.indicator_on_off(mode_indi[new_mode])
        elif new_mode == Keymod.KEYCAP:      self.__main.indicator_on_off(mode_indi[ori_mode])
        else:                       
            self.__main.indicator_on_off(mode_indi[ori_mode])
            self.__main.indicator_on_off(mode_indi[new_mode])
            
        self.__cal_state.keymod = new_mode
        
        # default output
        return InputAction(kind=ActionKind.IGNORE)