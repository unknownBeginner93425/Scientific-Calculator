from bitmap.font import METADATA
from bitmap.token_rendering import token_render

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.custom_types import Cursor, FrameBuffer

class RenderEngine():
    def __init__(self, framebuffer: "FrameBuffer"):
        self.__framebuffer = framebuffer
        self.__cursor = None
        self.__expr: list[int] = []
        self.__pen_x, self.__pen_y = 0, 0     # top-left corner of glyph
        self.__screen = []      # List[List[Token, pen_x, pen_y]]
        self.__DEFAULT_TOKEN_ADvANCE_WIDTH = 1
        self.__DEFAULT_GLYPH_ADVANCE_WIDTH = 2
    
    def set_cursor_ref(self, cursor: "Cursor") -> None:
        self.__cursor = cursor 
        
    def update_screen(self, expr: List[int]) -> None:
        self.__expr = expr
        self.reconstruct_screen()
        self.__render_screen()
            
    def reconstruct_screen(self):
        self.__screen = []
        self.__pen_x, self.__pen_y = 0, 0
        for token in self.__expr:
            self.__screen.append([token, self.__pen_x, self.__pen_y])
            for glyph_data in METADATA[token]:
                self.__pen_x += glyph_data[1] + glyph_data[5] \
                    + self.__DEFAULT_GLYPH_ADVANCE_WIDTH
                
            self.__pen_x += self.__DEFAULT_TOKEN_ADvANCE_WIDTH
            
    def __render_screen(self) -> None:
        self.__framebuffer.reset()
        for value_pair in self.__screen:
            token, pen_x, pen_y = value_pair
            token_render(self.__framebuffer, pen_x, pen_y, token)
            
    def display_result(self, result: str):
        digit_to_token = {"0": 101, "1": 102, "2": 103, "3": 104, 
                          "4": 105, "5": 106, "6": 107, "7": 108, 
                          "8": 109, "9": 110, ".": 111, "+": 301,
                          "-": 302, "e": 990, "E": 990}
        self.__pen_x, self.__pen_y = 192, (63-12)
        for digit in result[::-1]:
            token = digit_to_token[digit]
            metadata = METADATA[token][0]
            self.__pen_x -= metadata[1]+ metadata[5] \
                    + self.__DEFAULT_GLYPH_ADVANCE_WIDTH
            self.__screen.append([token, self.__pen_x, self.__pen_y])
            self.__pen_x -= self.__DEFAULT_TOKEN_ADvANCE_WIDTH
        self.__render_screen()
        
            
                    