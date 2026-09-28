from core.ui_io_interface import BitmapScreenInterface, TextboxScreenInterface
from gui.gui import CalculatorApp
from core.core_logics import CoreLogics

import os, sys

class Main():
    def __init__(self):
        self.__app = CalculatorApp(main_ref = self)
        self.__logic = CoreLogics(main_ref = self)
        
        self.__bitmap_io = BitmapScreenInterface(self.__app, self.__logic)
        self.__txtbox_io = TextboxScreenInterface(self.__app, self.__logic)
        print('Main: GUI and logic initialized')
        
        self.__logic.display_manager.set_io_interface_ref(self.__bitmap_io, self.__txtbox_io)
        self.__logic.state_manager.update_io_interface()
        print('Main: IO interface references set')

        self.__app.run()
        
    def button_pressed(self, token: int) -> None:
        self.__logic.button_press_handler.on_button_press(token)
    
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
        return self.__logic.state_manager.get_cursor()
    
    def get_framebuffer(self):
        return self.__logic.display_manager.get_framebuffer()

if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
    print(sys.executable)
    Main()