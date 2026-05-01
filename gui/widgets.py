from kivy.uix.image import Image

class Indicator(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 255
        self.switched_on = True
        
    def on_off(self):
        self.opacity, self.switched_on = (0, False) if self.opacity == 255 else (255, True)
