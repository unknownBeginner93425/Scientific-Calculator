from router.input_action import InputAction, ActionKind
from router.logic_abc import Router
from utilities.custom_types import DisplayState

class ErrorLogic(Router):
    class __NonExprFunc():
        @staticmethod
        def all_clear():
            return [InputAction(kind=ActionKind.SET_STATE, state=DisplayState.INPUT),
                    InputAction(kind=ActionKind.CLEAR_EXPR)]
            
        @staticmethod
        def left_arrow():
            return [InputAction(kind=ActionKind.SET_STATE, state=DisplayState.INPUT),
                    InputAction(kind=ActionKind.MOVE_CURSOR, cursor_move=+999)]
        
        @staticmethod
        def right_arrow():
            return [InputAction(kind=ActionKind.SET_STATE, state=DisplayState.INPUT),
                    InputAction(kind=ActionKind.MOVE_CURSOR, cursor_move=-999)]
            
            
    def __init__(self):
        
        self.__non_expr_func = {418: lambda: self.__NonExprFunc.all_clear(),
                                424: lambda: self.__NonExprFunc.left_arrow(),
                                425: lambda: self.__NonExprFunc.right_arrow()}
        
    def on_button_press(self, token: int) -> InputAction | list[InputAction]:
        '''token is validated'''
        # context: high priority tokens of turn on/off & shift/alpha = dealt with already
        
        return self.__non_expr_func.get(token, lambda: InputAction(kind=ActionKind.IGNORE))()