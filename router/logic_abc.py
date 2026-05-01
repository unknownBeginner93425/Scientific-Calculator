from abc import ABC, abstractmethod

class Router(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def on_button_press(self, token: int):
        pass