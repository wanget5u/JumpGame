from enum import Enum, auto

class WindowState(Enum):
    MENU = auto()
    GAME = auto()
    PAUSE = auto()
    SELECT = auto()
    EDIT = auto()
    EDIT_CONFIRM = auto()
    SAVE_PROMPT = auto()
    LOAD_PROMPT = auto()
    LEVEL_COMPLETE = auto()