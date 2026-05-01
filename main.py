from gui.gui import CalculatorApp
from core.core_logic import CoreLogics

class Main():
    def __init__(self):
        self.__app = CalculatorApp(main_ref = self)
        self.__logic = CoreLogics(main = self)

        self.__app.run()
        
    def button_pressed(self, token: int) -> None:
        self.__logic.on_button_press(token)
    
    def indicator_on_off(self, token: int| None) -> None:
        if token == None: return
        self.__app.window.indicator_on_off(token)
        
    def get_indicators_state(self):
        return self.__app.window.indicator_states

    def gui_input_screen_cursor_on(self):
        self.__app.window.ids['txt_box_screen_I'].activate_cursor()
        
    def gui_input_screen_cursor_off(self):
        self.__app.window.ids['txt_box_screen_I'].deactivate_cursor()
        
    def gui_output_screen_off(self):
        self.__app.window.ids['txt_box_screen_O'].reset()
        
    def get_cursor(self):
        return self.__logic.get_cursor()
    
    def expression_add_token(self, token: int):
        '''called by input logic -> add token to expr, then update gui output'''
        self.__logic.get_current_expression().update(token)
        self.input_screen_refresh()
        
    def input_screen_refresh(self):
         '''no specific caller; to keep gui output consistent with expr'''
         self.__app.window.ids['txt_box_screen_I'].update_text(self.__logic.expression_to_str())
        
    def display_output(self, cal_result: str):
        '''display calculation output only; not error message'''
        self.__app.window.ids['txt_box_screen_O'].update_text(cal_result)
        
    def display_error_message(self, error_type: str):
        self.__app.window.ids['txt_box_screen_I'].update_text([error_type])
        self.__app.window.ids['txt_box_screen_O'].update_text('[AC]  :Cancel\n[←][→]:Goto')

        
if __name__ == '__main__':
    Main()