from kivy.clock import Clock
from kivy.uix.label import Label

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.custom_types import Cursor
    
class InputTextbox(Label):
    '''text should always be consistent to Expression'''
    text_content = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = None
        self.blink_event = None
        self.cursor_visible = False
        
    def set_cursor_ref(self, cursor: 'Cursor'):
        self.cursor = cursor
        
    def activate_cursor(self):
        self.cursor_visible = True   # current state
        self.blink_event = Clock.schedule_interval(self.blink_cursor, 0.5)
        
    def deactivate_cursor(self):
        '''cancel cursor blinking'''
        if self.blink_event: self.blink_event.cancel()
        if self.cursor_visible: Clock.schedule_once(self.blink_cursor, 0.01)

    def blink_cursor(self, dt):
        self.cursor_visible = not self.cursor_visible
        
        text = deepcopy(self.text_content)
        if self.cursor_visible: text.insert(self.cursor.pos, '|')
        self.__set_text(text)
        
    def update_text(self, new_text_array: list[str]):
        self.text_content = new_text_array
        self.__set_text(self.text_content)
    
    def __set_text(self, text: list[str]):
        self.text = ''.join(text)
        
class OutputTextbox(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def update_text(self, text: str) -> None:
        self.text = text
        
    def reset(self) -> None:
        self.text = ''
        