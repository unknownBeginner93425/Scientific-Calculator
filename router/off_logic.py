from router.input_action import InputAction, ActionKind
from router.logic_abc import Router

class OffLogic(Router):
    def __init__(self):
        pass
        
    def on_button_press(self, token: int) -> InputAction:
        return InputAction(kind=ActionKind.IGNORE)