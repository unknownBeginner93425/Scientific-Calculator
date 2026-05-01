from router.input_action import InputAction, ActionKind
from router.logic_abc import Router
  
class InputLogic(Router):
    class __NonExprFunc():
        @staticmethod
        def delete():
            return [InputAction(kind=ActionKind.EXPR_REMOVE_ONE_TOKEN),
                    InputAction(kind=ActionKind.I_SCREEN_REFRESH)]
        
        @staticmethod
        def all_clear():
            return InputAction(kind=ActionKind.CLEAR_EXPR)
            
        @staticmethod
        def left_arrow():
            return InputAction(kind=ActionKind.MOVE_CURSOR, cursor_move=-1)
   
        @staticmethod
        def right_arrow():
            return InputAction(kind=ActionKind.MOVE_CURSOR, cursor_move=+1)

        @staticmethod
        def equal():
            return InputAction(kind=ActionKind.EVA_EXPR)
        
        @staticmethod
        def placeholder():
            return InputAction(kind=ActionKind.IGNORE)    
            
    def __init__(self):
        self.__non_expr_func = {403: lambda: self.__NonExprFunc.placeholder(),
                              404: lambda: self.__NonExprFunc.placeholder(),
                              406: lambda: self.__NonExprFunc.placeholder(),
                              408: lambda: self.__NonExprFunc.placeholder(),
                              409: lambda: self.__NonExprFunc.placeholder(),
                              414: lambda: self.__NonExprFunc.placeholder(),
                              415: lambda: self.__NonExprFunc.delete(),
                              416: lambda: self.__NonExprFunc.placeholder(),
                              417: lambda: self.__NonExprFunc.placeholder(),
                              418: lambda: self.__NonExprFunc.all_clear(),
                              420: lambda: self.__NonExprFunc.equal(),
                              421: lambda: self.__NonExprFunc.placeholder(),
                              424: lambda: self.__NonExprFunc.left_arrow(),
                              425: lambda: self.__NonExprFunc.right_arrow()
                              }
        
    def on_button_press(self, token: int) -> InputAction | list[InputAction]:
        '''token is validated'''
        # context: high priority tokens of turn on/off & shift/alpha = dealt with already
        
        match token // 100:
            case 1 | 2 | 3:
                return InputAction(kind=ActionKind.INSERT_TOKEN, tokens=[token])
            case 4: return self.__non_expr_func.get(token, lambda: self.__NonExprFunc.placeholder())()
            case 6: return [InputAction(kind = ActionKind.INSERT_TOKEN, tokens = [408, token-400]),
                            InputAction(kind = ActionKind.EVA_EXPR)]
            
            