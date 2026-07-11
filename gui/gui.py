from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

from gui.textbox_screen import InputTextbox, OutputTextbox
from gui.bitmap_screen import BitmapScreen
from gui.widgets import Indicator

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Main

class WindowManager():
    def __init__(self):
        self.__ASPECT_RATIO = 0.47
        self.__dpi_scale = self.__get_dpi_scale()
        self.__DEBOUNCE_DELAY = 0.3
        self.__resize_event = None
        
        self.__config_window()
        
    def __get_dpi_scale(self) -> float:
        if platform == 'win':
            return 96 / Window.dpi 
        elif platform in ('android', 'ios'):
            return 160 / Window.dpi 
        else:
            return 1
    
    def update_dpi_scale(self):
        self.__dpi_scale = self.__get_dpi_scale()
                    
    def __config_window(self):
        Window.bind(on_resize = self.on_window_resize, on_dpi = self.update_dpi_scale)
        Window.size = (411,874)
        
    def on_window_resize(self, instance, width, height):
        if self.__resize_event:
            self.__resize_event.cancel()
            
        self.__resize_event = Clock.schedule_once(lambda dt: self.__apply_aspect_ratio(
            width, height, Window.size), self.__DEBOUNCE_DELAY)

    def __apply_aspect_ratio(self, width, height, ori_size):
        correct_height = int(width / self.__ASPECT_RATIO)
        correct_width = int(height * self.__ASPECT_RATIO)

        if ori_size[0] == width:
            new_size = (correct_width, height)
        elif ori_size[1] == height:
            new_size = (width, correct_height)
        else:
  
            if abs(correct_height - height) * width > abs(correct_width - width) * height:
                new_size = (correct_width, height)
            else:
                new_size = (width, correct_height)
                    
        Window.unbind(on_resize = self.on_window_resize)
        Window.size = (new_size[0] * self.__dpi_scale, new_size[1] * self.__dpi_scale)
        Clock.schedule_once(lambda dt: Window.bind(on_resize = self.on_window_resize), self.__DEBOUNCE_DELAY)

        self.__resize_event = None

class CalculatorApp(App):
    def __init__(self, main_ref: 'Main', **kwargs):
        """initiate App class as build() method don't take parameter

        Args:
            reference (Main, essential): obj. reference of Main class. Defaults to None.
        """
        super().__init__(**kwargs)
        self.__window_manager = WindowManager()
        self.__main_ref = main_ref
         
    def build(self):
        self.window = Calculator(main_ref = self.__main_ref)
        self.window.bind(size=lambda instance, value: setattr(instance, 'size', Window.size))
        
        return self.window

class Calculator(RelativeLayout):
    # token within GUI = widget ids -> str
                    # token outside -> int
    def __init__(self, main_ref: 'Main', **kwargs):
        self.__main_ref = main_ref
        super().__init__(**kwargs)
        
        for id in range(501, 514): self.indicator_on_off(id)
        self.indicator_states = {id: False for id in range(501, 514)}
        
        self.__widget_to_token = {ref: id for id, ref in self.ids.items()}
        
        self.set_cursor()
        self.set_framebuffer()

    def on_button_press(self, button_ref):
        # testing code
        from time import perf_counter
        self.start_time = perf_counter()
        # end testing code
        
        pressed = self.__widget_to_token[button_ref]
        self.__main_ref.button_pressed(int(pressed)) 
        
        # testing code
        Clock.schedule_once(self.after_frame, 0)
        # end testing code
        
    def screen_test_func(self, button_ref):
        pressed = int(self.__widget_to_token[button_ref])
        #from bitmap.token_rendering import draw_glyph
        #draw_glyph(self.ids["screen"], 0, 0, 324)
        self.ids["screen"].update_texture()
        #self.ids["screen"].random_test_pattern()
        
    # testing function
    def after_frame(self, dt):
        from time import perf_counter
        end_time = perf_counter()
        print(f'UI latency: {1000*(end_time-self.start_time)}ms')
    # end testing function
    
    def update_indicator_states(self):
        '''refresh indicator_states dict with respect to current states'''
        self.indicator_states = {id: self.ids[str(id)].switched_on for id in range(501, 514)}
            
    def indicator_on_off(self, token: int):
        '''on-off switch for specified indicator ; stateless'''
        self.ids[str(token)].on_off()
        self.update_indicator_states()
        
    def set_cursor(self):
        '''link cursor obj in CoreLogic to textbox screen'''
        self.ids['txt_box_screen_I'].set_cursor_ref(self.__main_ref.get_cursor())
        
    def set_framebuffer(self):
        '''link FrameBuffer obj in CoreLogic to bitmap mono screen'''
        self.ids['screen'].set_framebuffer_ref(self.__main_ref.get_framebuffer())
           
if __name__ == '__main__':
    app = CalculatorApp()
    app.run()
