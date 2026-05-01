from router.input_action import ActionKind

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Main, CoreLogics
    from router.input_action import InputAction 
    
class InputController():
    def __init__(self, main_ref: 'Main', logic: 'CoreLogics'):
        self.__main = main_ref
        self.__main_logic = logic
        self.__cal_states = self.__main_logic.get_setting_manager()
    
    def handle_input_action(self, action: 'InputAction') -> None:
        match action.kind:
            case ActionKind.INSERT_TOKEN:
                for token in action.tokens:
                    self.__token_insertion_logic(token)
            case ActionKind.SET_STATE:
                self.__main_logic.set_display_state(state=action.state)
            case ActionKind.CLEAR_EXPR:
                self.__main_logic.reset_expression()
            case ActionKind.MOVE_CURSOR:
                self.__main_logic.move_cursor(action.cursor_move)
            case ActionKind.EVA_EXPR:
                self.__main_logic.expr_evaluate_and_result_output()
            case ActionKind.TURN_ON:
                self.__main_logic.cal_turn_on()
            case ActionKind.TURN_OFF:
                self.__main_logic.cal_turn_off()
            case ActionKind.EXPR_REMOVE_ONE_TOKEN:
                self.__main_logic.get_current_expression().remove()
            case ActionKind.I_SCREEN_REFRESH:
                self.__main.input_screen_refresh()
            case ActionKind.IGNORE:
                pass
                
    def __token_insertion_logic(self, token: int) -> None:
        math_input_exclus_func = {309, 313}
        currently_out_of_scope = {321, 333, 334, 343}
        
        if self.__cal_states.get('I_method') == 1 and \
            token not in math_input_exclus_func \
                and token not in currently_out_of_scope:
                    self.__main.expression_add_token(token)