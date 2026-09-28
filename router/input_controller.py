from router.input_action import ActionKind
from utilities.custom_types import Token

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Main
    from core.core_logics import CalculatorStateManager,\
        DisplayManager, ExpressionEvaluator, CalculatorController
    from router.input_action import InputAction 
    
class InputController():
    def __init__(self, program_controller: "CalculatorController",
                 state_manager: "CalculatorStateManager",
                 expr_evaluator: "ExpressionEvaluator",
                 display_manager: "DisplayManager"):
        self.__program_controller = program_controller
        self.__state_manager = state_manager
        self.__expr_evaluator = expr_evaluator
        self.__display_manager = display_manager

    def handle_input_action(self, action: 'InputAction') -> None:
        match action.kind:
            case ActionKind.INSERT_TOKEN:
                for token in action.tokens:
                    self.__token_insertion_logic(token)
            case ActionKind.SET_STATE:
                self.__state_manager.set_display_state(state=action.state)
            case ActionKind.CLEAR_EXPR:
                self.__state_manager.reset_expression()
            case ActionKind.MOVE_CURSOR:
                self.__state_manager.move_cursor(action.cursor_move)
            case ActionKind.EVA_EXPR:
                self.__expr_evaluator.expr_evaluate_and_result_output()
            case ActionKind.TURN_ON:
                self.__program_controller.cal_turn_on()
            case ActionKind.TURN_OFF:
                self.__program_controller.cal_turn_off()
            case ActionKind.EXPR_REMOVE_ONE_TOKEN:
                self.__state_manager.get_current_expression().remove()
            case ActionKind.I_SCREEN_REFRESH:
                self.__display_manager.current_ui_IO_interface.input_screen_refresh()
            case ActionKind.IGNORE:
                pass
                
    def __token_insertion_logic(self, token: int) -> None:
        math_input_exclus_func = {309, 313}
        currently_out_of_scope = {321, 333, 334, 343}
        require_op_bracket = {306, 307, 310, 311, 314, 315, 316, 317, 318, 319,
                              324, 325, 326, 327, 328, 329, 337, 338, 339, 341}
        
        if self.__state_manager.get_setting('I_method') == 1 and \
            token not in math_input_exclus_func \
                and token not in currently_out_of_scope:
                    self.__state_manager.expression_add_token(token)
                    if token in require_op_bracket:
                        self.__state_manager.expression_add_token(Token.OP_BRACKET)