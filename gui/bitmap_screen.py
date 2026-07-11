from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture

from random import random

from typing import Literal, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.custom_types import FrameBuffer

class BitmapScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.WIDTH, self.HEIGHT = 192, 63
        
        #self.framebuffer = bytearray(self.WIDTH * self.HEIGHT * 4)
        
        self.texture = Texture.create(size = (self.WIDTH, self.HEIGHT),
                                      colorfmt = "rgba")
        self.texture.mag_filter = "nearest"
        
        with self.canvas:
            self.rect = Rectangle(
                texture = self.texture,
                pos = self.pos,
                size = self.size
            )
            
        self.bind(pos = self._update_rect, size = self._update_rect)
        
    def set_framebuffer_ref(self, framebuffer: "FrameBuffer"):
        self.framebuffer = framebuffer
        self.update_texture()
        
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def update_texture(self):
        self.texture.blit_buffer(self.framebuffer.get_data(), 
                                 colorfmt = "rgba", 
                                 bufferfmt = "ubyte")
        
    def clear(self):
        for _ in range(0, len(self.framebuffer) + 1, 4):
            self.framebuffer[_] = 0
        self.update_texture()
        
    def set_pixel(self, column: int, row: int, data: Literal[0, 1]):
        row = (self.HEIGHT - 1) - row
        index = (row * self.WIDTH + column) * 4 + 3
        
        self.framebuffer[index] = 0 if data == 0 else 255
        