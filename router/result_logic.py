from router.input_action import InputAction, ActionKind
from router.logic_abc import Router
from utilities.custom_types import DisplayState
    
class ResultLogic(Router):
    class __NonExprFunc():
        @staticmethod
        def equal():
            return [InputAction(kind=ActionKind.EVA_EXPR)]
        
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
            
        @staticmethod
        def placeholder():
            return InputAction(kind=ActionKind.IGNORE)
        
    def __init__(self):
        self.__implicit_Ans_op = {301, 302, 303, 304, 305, 308, 312, 314, 315,
                                322, 323, 331, 333, 334, 335, 336, 342}
        
        self.__non_expr_func = {403: lambda: self.__NonExprFunc.placeholder(),
                                404: lambda: self.__NonExprFunc.placeholder(),
                                406: lambda: self.__NonExprFunc.placeholder(),
                                407: lambda: self.__NonExprFunc.placeholder(),
                                408: lambda: self.__NonExprFunc.placeholder(),
                                409: lambda: self.__NonExprFunc.placeholder(),
                                410: lambda: self.__NonExprFunc.placeholder(),
                                411: lambda: self.__NonExprFunc.placeholder(),
                                412: lambda: self.__NonExprFunc.placeholder(),
                                413: lambda: self.__NonExprFunc.placeholder(),
                                414: lambda: self.__NonExprFunc.placeholder(),
                                418: lambda: self.__NonExprFunc.all_clear(),
                                420: lambda: self.__NonExprFunc.equal(),
                                422: lambda: self.__NonExprFunc.placeholder(),
                                423: lambda: self.__NonExprFunc.placeholder(),
                                424: lambda: self.__NonExprFunc.left_arrow(),
                                425: lambda: self.__NonExprFunc.right_arrow()}
        
    def on_button_press(self, token: int) -> InputAction | list[InputAction]:
        '''token is validated'''
        # context: high priority tokens of turn on/off & shift/alpha = dealt with already
        
        match token // 100:
            case 1 | 2:
                return [InputAction(kind=ActionKind.SET_STATE, state=DisplayState.INPUT),
                        InputAction(kind=ActionKind.CLEAR_EXPR),
                        InputAction(kind=ActionKind.INSERT_TOKEN, tokens=[token]),
                        InputAction(kind=ActionKind.MOVE_CURSOR, cursor_move=+999)]
            case 3:
                insert_tokens = [token]
                if token in self.__implicit_Ans_op: insert_tokens.insert(0, 209)
                
                return [InputAction(kind=ActionKind.SET_STATE, state=DisplayState.INPUT),
                        InputAction(kind=ActionKind.CLEAR_EXPR),
                        InputAction(kind=ActionKind.INSERT_TOKEN, tokens=insert_tokens),
                        InputAction(kind=ActionKind.MOVE_CURSOR, cursor_move=+999)]
            case 4:
                return self.__non_expr_func.get(token, lambda: self.__NonExprFunc.placeholder())()
            case 6: return [InputAction(kind=ActionKind.SET_STATE, state=DisplayState.INPUT),
                            InputAction(kind=ActionKind.CLEAR_EXPR),
                            InputAction(kind = ActionKind.INSERT_TOKEN, tokens = [209, 408, token-400]),
                            InputAction(kind = ActionKind.EVA_EXPR)]
                
                
        