from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

from utilities.custom_types import DisplayState

class ActionKind(Enum):
    INSERT_TOKEN = auto()
    SET_STATE = auto()
    MOVE_CURSOR = auto()
    CLEAR_EXPR = auto()
    EVA_EXPR = auto()
    TURN_ON = auto()
    TURN_OFF = auto()
    I_SCREEN_REFRESH = auto()
    EXPR_REMOVE_ONE_TOKEN = auto()
    STORE_VAR = auto()
    IGNORE = auto()

@dataclass(frozen=True)
class InputAction():
    kind: ActionKind
    
    tokens: Optional[list[int]] = None
    state: Optional[DisplayState] = None
    cursor_move: Optional[int] = None
    