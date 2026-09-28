from __future__ import annotations

from utilities.sql_handler import SQL
from utilities.custom_types import Cursor, DisplayState, Token, FrameBuffer

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

from bitmap.expr_rendering import RenderEngine

from typing import TYPE_CHECKING, Callable, Literal, List
from copy import deepcopy

if TYPE_CHECKING:
    from main import Main
    from core.ui_io_interface import UI_IO_Interface, BitmapScreenInterface, TextboxScreenInterface

class CoreLogics():
    """master class; all logic classes should only be related via this class
    no cross referencing"""
    
    def __init__(self, main_ref: "Main"):
        self.__main = main_ref
        self.__program_state = CalculatorState()
        
        self.display_manager = DisplayManager(self.__program_state)
        self.state_manager = CalculatorStateManager(self.__main, self.__program_state,
                                                    self.display_manager.set_current_io_interface,
                                                    self.display_manager.get_ui_io_interface)
        
        
        self.controller = CalculatorController(self.__main, self.__program_state, self.state_manager,
                                               self.display_manager.expr_render_engine)
        
        self.expr_evaluator = ExpressionEvaluator(self.__program_state, self.state_manager,
                                                  self.display_manager)
        
        self.button_press_handler = ButtonPressHandler(self.__main, self.__program_state, self.controller,
                                                       self.state_manager,
                                                       self.expr_evaluator, self.display_manager)
        
        
class CalculatorState():
    """contains all the states of the calculator, including the current expression,
    cursor, display state, settings and variable memory
    all public attributes as the object is expected to only be passed between
    classes in this program file"""
    def __init__(self):
        self.display_state = DisplayState.OFF
        self.settings_manager = SettingsManager()
        self.variable_mem = VariableMemory()
        self.cursor = Cursor()
        
        self.expression = ExpressionArray(self.cursor)
        self.expr_hist: List["ExpressionArray"] = []
        
        
class DisplayManager():
    def __init__(self, states: CalculatorState):
        self.__states = states
        self.__ui_framebuffer = FrameBuffer()
        self.expr_render_engine = RenderEngine(self.__ui_framebuffer)
        self.current_ui_IO_interface = None
        
    def get_framebuffer(self) -> FrameBuffer:
        return self.__ui_framebuffer
    
    def get_ui_io_interface(self):
        return self.current_ui_IO_interface
    
    def set_io_interface_ref(self, bitmap: "BitmapScreenInterface", txtbox: "TextboxScreenInterface"):
        self.__bitmap_screen_interface = bitmap
        self.__txtbox_screen_interface = txtbox
    
    def set_current_io_interface(self, interface: Literal[0, 1]) -> None:
        print(f'DisplayManager: set_current_io_interface({interface})')
        if interface == 0:
            self.current_ui_IO_interface = self.__txtbox_screen_interface
        else:
            self.current_ui_IO_interface = self.__bitmap_screen_interface
            
    def bitmap_screen_refresh(self):
        self.expr_render_engine.update_screen(self.__states.expression.repr())
        
    def bitmap_process_cal_result(self, result: str):
        self.expr_render_engine.display_result(result)

class CalculatorStateManager():
    def __init__(self, main_ref: "Main", states: CalculatorState,
                 io_interface_setter: Callable[[Literal[0, 1]], None], 
                 ui_io_interface_getter: Callable[[None], UI_IO_Interface]):
        self.__main = main_ref
        self.__states = states
        self.__io_interface_setter = io_interface_setter
        
        self.__ui_io_interface_getter = ui_io_interface_getter
          
    def update_io_interface(self) -> None:       
        '''update current_io_IO_interface in DisplayManager according to screen_type'''
        self.__io_interface_setter(self.__states.settings_manager.get("screen_type"))
        
    def get_cursor(self) -> Cursor:
        return self.__states.cursor
    
    def get_setting(self, setting: str) -> int | str:
        return self.__states.settings_manager.get(setting)
        
    def move_cursor(self, step: Literal[1, -1, 999, -999]) -> None:
        '''step = +999 -> move cursor to end of expr
           step = -999 -> move cursor to start'''
        if step == 0: return
        elif step == +1:
            if self.__states.cursor.pos == len(self.__states.expression.repr()):
                self.__states.cursor.reset()
            else: self.__states.cursor.increment()
        elif step == -1:
            if self.__states.cursor.pos == 0:
                self.__states.cursor.set(len(self.__states.expression.repr()))
            else: self.__states.cursor.decrement()
        elif step == +999:
            self.__states.cursor.set(len(self.__states.expression.repr()))
        elif step == -999:
            self.__states.cursor.reset()
        else: raise AttributeError(f'Invalid attribute value: step = {step}')
        
    def set_display_state(self, state: DisplayState) -> None:
            '''router procedure; update display state & perform state-entry actions'''
            ui_io_interface = self.__ui_io_interface_getter()
            
            if self.__states.display_state != state:
                self.__states.display_state = state
            match state:
                case DisplayState.RESULT:
                    self.__main.gui_input_screen_cursor_off()
                case DisplayState.INPUT:
                    ui_io_interface.gui_input_screen_cursor_on()
                    ui_io_interface.input_screen_refresh()
                    ui_io_interface.gui_output_screen_off()
                    
                case DisplayState.OFF:
                    ui_io_interface.gui_input_screen_cursor_off()
                    ui_io_interface.gui_output_screen_off()
                    self.reset_expression()
                case DisplayState.ERROR:
                    ui_io_interface.gui_input_screen_cursor_off()
    
    def reset_expression(self) -> None:
        '''reset current expr var. into new instance; reset cursor; update gui'''
        self.__states.expression = ExpressionArray(self.__states.cursor)
        self.__states.cursor.reset()
        self.__ui_io_interface_getter().input_screen_refresh()
              
    def get_current_expression(self) -> ExpressionArray:
        return self.__states.expression
    
    def expression_add_token(self, token: int):
        '''called by input logic -> add token to expr, then update gui output'''
        self.get_current_expression().update(token)
        self.__ui_io_interface_getter().input_screen_refresh()
        
    def expression_to_str(self) -> list[str]:
        '''translate current expression array into list of corr. str'''
        sql = SQL()
        expr = [sql.get_txt_from_token(token) for token in self.__states.expression.repr()]
        del sql
        return expr
       
        
class CalculatorController():
    # button press, evaluation, state transition
    def __init__(self, main_ref: 'Main', program_state: CalculatorState, 
                 state_manager: CalculatorStateManager,
                 expr_render_engine: RenderEngine):
        self.__main = main_ref
        self.__states = program_state
        self.__state_manager = state_manager
        self.__expr_render_engine = expr_render_engine

    def cal_turn_on(self) -> None:
        # internal states update
        if self.__states.settings_manager.switched_on == True: 
            self.cal_turn_off()
        self.__state_manager.set_display_state(DisplayState.INPUT)
        self.__states.settings_manager.switched_on = True

        # settings & variable value update
        sql = SQL()
        settings = sql.retrieve_current_states('Settings')
        self.__states.settings_manager.apply_settings(settings)

        self.__states.variable_mem.set_all(sql.retrieve_current_states('Variables'))

        del sql
        
        # GUI preparatopm
            # turn on indicators
        self.__activate_indicators()
        
        # expression initialisation
        self.__states.expression = ExpressionArray(self.__states.cursor)
        self.__states.expr_hist = []
        
        # render engine preparation
        self.__expr_render_engine.set_cursor_ref(self.__states.cursor)
    
    def cal_turn_off(self) -> None:
        # internal states update
        self.__state_manager.set_display_state(DisplayState.OFF)
        self.__states.settings_manager.switched_on = False

        # save settings and variable values
        self.__save_settings_and_variables()
        
        # GUI
            # turn off indicators
        self.__deactivate_indicators()   

    def __activate_indicators(self) -> None:
        # will only be called when all indicators are deactivated
        if self.__states.variable_mem.get('M') != 0:              self.__main.indicator_on_off(503)
        if self.__states.settings_manager.get('I_method') == 0:   self.__main.indicator_on_off(505)
        
        # angle unit indicator
        token = {'D': 506, 'R': 507, 'G': 508}[self.__states.settings_manager.get('angle_unit')]
        self.__main.indicator_on_off(token)
        
        # number format indicator # ignore first
        token = {0: 509, 1: 510}[self.__states.settings_manager.get('number_format')]
        
        # other few indicators = not for this model -> ignore
        
    def __deactivate_indicators(self) -> None:
        states = self.__main.get_indicators_state()
        for token, state in states.items():
            if state == True: self.__main.indicator_on_off(token)
    
    def __save_settings_and_variables(self) -> None:
        settings = self.__states.settings_manager.get_settings()
        variables = self.__states.variable_mem.get_all()
        sql = SQL()
        sql.save_current_states(settings, variables)
        del sql    
        
    
class ButtonPressHandler():
    def __init__(self, main_ref: "Main", states: "CalculatorState", 
                 program_controller: CalculatorController,
                 state_manager: CalculatorStateManager, expr_evaluator: "ExpressionEvaluator",
                 display_manager: DisplayManager):
        self.__main = main_ref
        self.__input_controller = InputController(program_controller, state_manager, 
                                                  expr_evaluator, display_manager)
        self.__states = states
        self.__state_manager = state_manager
        self.__display_manager = display_manager
    
    def on_button_press(self, token: int) -> None:
        processed_token_or_action = self.__preprocess_token(token)
        #try:
        self.__process_router(processed_token_or_action)
        #except Exception as e:
        #    self.__handle_error(e)
        
    def __preprocess_token(self, token: int) -> int | InputAction:
            preprocessor = LogicPreprocessor(main_ref=self.__main, 
                                             settings_manager = self.__states.settings_manager)
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
        self.__state_manager.set_display_state(DisplayState.ERROR)
        self.__display_manager.current_ui_IO_interface.display_error_message(f'{error}')
        #self.__main.display_error_message(f'{error}')
    
    def __get_button_press_handler(self) \
    -> type[InputLogic] | type[OffLogic] | type[ResultLogic] | type[ErrorLogic] | None:
        handler = { DisplayState.INPUT:  InputLogic,
                    DisplayState.RESULT: ResultLogic,
                    DisplayState.ERROR:  ErrorLogic,
                    DisplayState.MENU:   None,
                    DisplayState.OFF:    OffLogic}
        
        return handler[self.__states.display_state]
    
class ExpressionEvaluator():
    def __init__(self, states: CalculatorState, state_manager: CalculatorStateManager,
                 display_manager: DisplayManager):
        self.__states = states
        self.__state_manager = state_manager
        self.__display_manager = display_manager
    
    def expr_evaluate_and_result_output(self) -> None:
        self.__state_manager.set_display_state(DisplayState.RESULT)
        self.__update_history()
        
        exprs = self.__prepare_evaluation()
        
        self.__eva_router(exprs)
        
    def __prepare_evaluation(self) -> list[list[int]]:
        '''return expr as 2d array; element = steps in muli-step expression'''
        expr = self.__states.expression.repr()
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
        self.__states.variable_mem.set(var[expr[1]], self.__states.variable_mem.get('Ans'))
    
    def __handle_evaluation(self, expr: list[int]) -> None:
        '''evaluate expr; display output on screen; store result to Ans'''
        result = self.__expr_evaluate(expr)
        self.__display_manager.current_ui_IO_interface.display_output(str(result))
        self.__store_result(result)
    
    def __update_history(self) -> None:
        '''append current ExpressionArray to expression_hist'''
        self.__states.expr_hist.append(deepcopy(self.__states.expression))
        
        # testing code
        print(f'Updated expr hist: {[expr.repr() for expr in self.__states.expr_hist]}')
        # end testing code
    
    def __store_result(self, result: float) -> None:
        '''store result to Ans var'''
        self.__states.variable_mem.set('Ans', result)
    
    def __expr_evaluate(self, expr: list[int]) -> float:
        '''sequencer; call Normalisation, ShuntingYard, Evaluation in order'''
        
        # testing code
        from time import perf_counter
        start_time1 = perf_counter()
        # end testing code
        
        normaliser = Normalisation(self.__states.settings_manager.get('I_method'), self.__states.variable_mem)
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