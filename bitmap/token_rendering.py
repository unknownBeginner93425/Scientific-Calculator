from bitmap.font import METADATA, FONT

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.custom_types import FrameBuffer

def token_render(framebuffer: "FrameBuffer", pen_x: int, pen_y: int, token: int):
    DEFAULT_ADVANCE_WIDTH = 2
    for glyph_data in METADATA[token]:
        offset, width, height, x_offset, y_offset, advance_width = glyph_data
        approx_end = offset + width * height // 8 + 2
        
        data = FONT[offset: approx_end]
        
        bit_counter = 7
        byte_index = 0
        
        pen_x += x_offset
        
        for y in range(height):
            for x in range(width):
                bit = data[byte_index] >> bit_counter & 1
                framebuffer.set_pixel(pen_x + x, 
                                      pen_y + y + y_offset,
                                      bit)
    
                bit_counter -= 1
                if bit_counter == -1: bit_counter = 7; byte_index += 1
        
        pen_x += width + advance_width + DEFAULT_ADVANCE_WIDTH
        