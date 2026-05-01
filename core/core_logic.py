from utilities.sql_handler import SQL
from utilities.custom_types import Cursor, DisplayState, Token

from core.settings_and_variables import SettingsManager, VariableMemory

from expression.builder import ExpressionArray
from expression.normaliser import Normalisation
from expression.shunting_yard import ShuntingYard
from expression.evaluator import Evaluation

from router.logic_preprocessor import LogicPreprocessor
from router.input_controller import InputController
from router.input_action import InputAction
from router.input_logic import InputLogic
from router.off_logic import OffLogic
from router.result_logic import ResultLogic
from router.error_logic import ErrorLogic

from typing import TYPE_CHECKING, Literal
from copy import deepcopy

if TYPE_CHECKING:
    from main import Main

class CoreLogics():
    def __init__(self, main: 'Main'):      
        self.__main = main
        
        self.__display_state = DisplayState.OFF
        self.__settings_manager = SettingsManager()
        self.__variables_mem = VariableMemory()
        self.__input_controller = InputController(self.__main, self)
        
        self.__cursor = Cursor()
        self.__current_expression = ExpressionArray(self.__cursor)
        self.__expression_hist = []
        
    def get_setting_manager(self) -> SettingsManager:
        return self.__settings_manager
    
    def get_current_expression(self) -> ExpressionArray:
        return self.__current_expression
    
    def get_cursor(self) -> Cursor:
        return self.__cursor
    
    def move_cursor(self, step: Literal[1, -1, 999, -999]) -> None:
        '''step = +999 -> move cursor to end of expr
           step = -999 -> move cursor to start'''
        if step == 0: return
        elif step == +1:
            if self.__cursor.pos == len(self.__current_expression.repr()):
                self.__cursor.reset()
            else: self.__cursor.increment()
        elif step == -1:
            if self.__cursor.pos == 0:
                self.__cursor.set(len(self.__current_expression.repr()))
            else: self.__cursor.decrement()
        elif step == +999:
            self.__cursor.set(len(self.__current_expression.repr()))
        elif step == -999:
            self.__cursor.reset()
        else: raise AttributeError(f'Invalid attribute value: step = {step}')
       
    def set_display_state(self, state: DisplayState) -> None:
        '''router procedure; update display state & perform state-entry actions'''
        
        # testing code
        print(f'Ori display state: {self.__display_state}')
        print(f'New display state: {state}')
        # end testing code
        
        if self.__display_state != state:
            self.__display_state = state
        
        match state:
            case DisplayState.RESULT:
                self.__main.gui_input_screen_cursor_off()
            case DisplayState.INPUT:
                self.__main.gui_input_screen_cursor_on()
                self.__main.input_screen_refresh()
                self.__main.gui_output_screen_off()
            case DisplayState.OFF:
                self.__main.gui_input_screen_cursor_off()
                self.__main.gui_output_screen_off()
                self.reset_expression()
            case DisplayState.ERROR:
                self.__main.gui_input_screen_cursor_off()
                
    def on_button_press(self, token: int) -> None:
        processed_token_or_action = self.__preprocess_token(token)
        #try:
        self.__process_router(processed_token_or_action)
        #except Exception as e:
        #    self.__handle_error(e)
                  
    def __preprocess_token(self, token: int) -> int | InputAction:
        preprocessor = LogicPreprocessor(main_ref=self.__main, logic=self)
        # return validated token or action
        return preprocessor.on_button_press(token)
    
    def __process_router(self, token_or_actions: int | InputAction | list[InputAction]) -> None:
        if isinstance(token_or_actions, int):
            handler = self.__get_button_press_handler()()
            actions = handler.on_button_press(token_or_actions)
            self.__process_router(actions)
        elif isinstance(token_or_actions, InputAction):
            self.__dispatch_action(token_or_actions)
        else:
            for action in token_or_actions: self.__dispatch_action(action) 

    def __dispatch_action(self, action: InputAction) -> None:
        self.__input_controller.handle_input_action(action)
 
    def __handle_error(self, error: Exception) -> None:
        self.set_display_state(DisplayState.ERROR)
        self.__main.display_error_message(f'{error}')
    
    def __get_button_press_handler(self) \
    -> type[InputLogic] | type[OffLogic] | type[ResultLogic] | type[ErrorLogic] | None:
        handler = {DisplayState.INPUT: InputLogic,
                    DisplayState.RESULT: ResultLogic,
                    DisplayState.ERROR: ErrorLogic,
                    DisplayState.MENU: None,
                    DisplayState.OFF: OffLogic}
        
        return handler[self.__display_state]
            
    def cal_turn_on(self) -> None:
        # internal states update
        if self.__settings_manager.switched_on == True: 
            self.cal_turn_off()
        self.set_display_state(DisplayState.INPUT)
        self.__settings_manager.switched_on = True

        # settings & variable value update
        sql = SQL()
        settings = sql.retrieve_current_states('Settings')
        self.__settings_manager.apply_settings(settings)

        self.__variables_mem.set_all(sql.retrieve_current_states('Variables'))

        del sql
        
        # GUI preparatopm
            # turn on indicators
        self.__activate_indicators()
        
        # expression initialisation
        self.__current_expression = ExpressionArray(self.__cursor)
        self.__expression_hist = []
    
    def cal_turn_off(self) -> None:
        # internal states update
        self.set_display_state(DisplayState.OFF)
        self.__settings_manager.switched_on = False

        # save settings and variable values
        self.__save_settings_and_variables()
        
        # GUI
            # turn off indicators
        self.__deactivate_indicators()   

    def __activate_indicators(self) -> None:
        # will only be called when all indicators are deactivated
        if self.__variables_mem.get('M') != 0:             self.__main.indicator_on_off(503)
        if self.__settings_manager.get('I_method') == 0:   self.__main.indicator_on_off(505)
        
        # angle unit indicator
        token = {'D': 506, 'R': 507, 'G': 508}[self.__settings_manager.get('angle_unit')]
        self.__main.indicator_on_off(token)
        
        # number format indicator # ignore first
        token = {0: 509, 1: 510}[self.__settings_manager.get('number_format')]
        
        # other few indicators = not for this model -> ignore
        
    def __deactivate_indicators(self) -> None:
        states = self.__main.get_indicators_state()
        for token, state in states.items():
            if state == True: self.__main.indicator_on_off(token)
    
    def __save_settings_and_variables(self) -> None:
        settings = self.__settings_manager.get_settings()
        variables = self.__variables_mem.get_all()
        sql = SQL()
        sql.save_current_states(settings, variables)
        del sql
    
    def expression_to_str(self) -> list[str]:
        '''translate current expression array into list of corr. str'''
        sql = SQL()
        expr = [sql.get_txt_from_token(token) for token in self.__current_expression.repr()]
        del sql
        return expr
    
    def reset_expression(self) -> None:
        '''reset current expr var. into new instance; reset cursor; update gui'''
        self.__current_expression = ExpressionArray(self.__cursor)
        self.__cursor.reset()
        self.__main.input_screen_refresh()
    
    def expr_evaluate_and_result_output(self) -> None:
        self.set_display_state(DisplayState.RESULT)
        self.__update_history()
        
        exprs = self.__prepare_evaluation()
        
        self.__eva_router(exprs)
        
    def __prepare_evaluation(self) -> list[list[int]]:
        '''return expr as 2d array; element = steps in muli-step expression'''
        expr = self.__current_expression.repr()
        processed_expr, temp = [], []
        for token in expr:
            if token in {Token.STO}:
                if temp != []: processed_expr.append(temp)
                temp = []
            temp.append(token)
        if temp != []: processed_expr.append(temp)
        return processed_expr
    
    def __eva_router(self, expr_list: list[list[int]]):
        for expr in expr_list:
            if Token.STO in expr:
                self.__handle_store(expr)
            else:
                self.__handle_evaluation(expr)
                
    def __handle_store(self, expr: list[int]) -> None:
        ''' default store value of Ans into var ; expect expr as [STO (to), var]
         as prepare_evaluation = split expr like 3+2->A into [[3+2],[->A]'''
        from utilities.custom_types import TokenToVariable
        var = TokenToVariable()
        self.__variables_mem.set(var[expr[1]], self.__variables_mem.get('Ans'))
    
    def __handle_evaluation(self, expr: list[int]) -> None:
        '''evaluate expr; display output on screen; store result to Ans'''
        result = self.__expr_evaluate(expr)
        self.__main.display_output(str(result))
        self.__store_result(result)
    
    def __update_history(self) -> None:
        '''append current ExpressionArray to expression_hist'''
        self.__expression_hist.append(deepcopy(self.__current_expression))
        
        # testing code
        print(f'Updated expr hist: {[expr.repr() for expr in self.__expression_hist]}')
        # end testing code
    
    def __store_result(self, result: float) -> None:
        '''store result to Ans var'''
        self.__variables_mem.set('Ans', result)
    
    def __expr_evaluate(self, expr: list[int]) -> float:
        '''sequencer; call Normalisation, ShuntingYard, Evaluation in order'''
        
        # testing code
        from time import perf_counter
        start_time1 = perf_counter()
        # end testing code
        
        normaliser = Normalisation(self.__settings_manager.get('I_method'), self.__variables_mem)
        expr_queue = normaliser.normalise(expr)
        
        shunting_yard = ShuntingYard(expr_queue)
        shunting_yard.run()
        
        # testing code
        start_time2 = perf_counter()
        # end testing code
        
        RPN_expr = shunting_yard.get_output()
        evaluator = Evaluation(RPN_expr)
        
        # testing code
        end_time = perf_counter()
        print(f'Evaluation: {1000*(end_time-start_time1)}ms')
        print(f'Calculation: {1000*(end_time-start_time2)}ms')
        # end testing code
        
        return evaluator.evaluate()