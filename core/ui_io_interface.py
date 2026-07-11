from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.gui import CalculatorApp
    from core.core_logic import CoreLogics 
class UI_IO_Interface(ABC):
    @abstractmethod
    def gui_input_screen_cursor_on(self):
        pass
    
    @abstractmethod    
    def gui_input_screen_cursor_off(self):
        pass
    
    @abstractmethod    
    def gui_output_screen_off(self):
        pass

    @abstractmethod    
    def input_screen_refresh(self):
         '''no specific caller; to keep gui output consistent with expr'''
         pass
     
    @abstractmethod    
    def display_output(self, cal_result: str):
        '''display calculation output only; not error message'''
        pass
    
    @abstractmethod    
    def display_error_message(self, error_type: str):
        pass
    
    
class TextboxScreenInterface(UI_IO_Interface):
    def __init__(self, gui_ref: "CalculatorApp", logic_ref: "CoreLogics"):
        self.__gui = gui_ref
        self.__logic = logic_ref
        
    def gui_input_screen_cursor_on(self):
        self.__gui.window.ids['txt_box_screen_I'].activate_cursor()
        
    def gui_input_screen_cursor_off(self):
        self.__gui.window.ids['txt_box_screen_I'].deactivate_cursor()
        
    def gui_output_screen_off(self):
        self.__gui.window.ids['txt_box_screen_O'].reset()
        
    def input_screen_refresh(self):
         '''no specific caller; to keep gui output consistent with expr'''
         self.__gui.window.ids['txt_box_screen_I'].update_text(self.__logic.expression_to_str())
        
    def display_output(self, cal_result: str):
        '''display calculation output only; not error message'''
        self.__gui.window.ids['txt_box_screen_O'].update_text(cal_result)
        
    def display_error_message(self, error_type: str):
        self.__gui.window.ids['txt_box_screen_I'].update_text([error_type])
        self.__gui.window.ids['txt_box_screen_O'].update_text('[AC]  :Cancel\n[←][→]:Goto')

class BitmapScreenInterface(UI_IO_Interface):
    def __init__(self, gui_ref: "CalculatorApp", logic_ref: "CoreLogics"):
        self.__gui = gui_ref
        self.__logic = logic_ref
        
    def gui_input_screen_cursor_on(self):
        self.__gui.window.ids['txt_box_screen_I'].activate_cursor()
        
    def gui_input_screen_cursor_off(self):
        self.__gui.window.ids['txt_box_screen_I'].deactivate_cursor()
        
    def gui_output_screen_off(self):
        self.__gui.window.ids['txt_box_screen_O'].reset()
            
    def input_screen_refresh(self):
        '''no specific caller; to keep gui output consistent with expr'''
        self.__logic.bitmap_screen_refresh()
        self.__gui.window.ids['screen'].update_texture()
        
    def display_output(self, cal_result: str):
        '''display calculation output only; not error message'''
        self.__logic.bitmap_process_cal_result(cal_result)
        self.__gui.window.ids['screen'].update_texture()
        
    def display_error_message(self, error_type: str):
        self.__gui.window.ids['txt_box_screen_I'].update_text([error_type])
        self.__gui.window.ids['txt_box_screen_O'].update_text('[AC]  :Cancel\n[←][→]:Goto')

