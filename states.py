from enum import Enum, auto

class State(Enum):
    MENU = auto()
    PLAY = auto()
    QUIT = auto()

class MenuState(Enum):
    ABOUT = auto()
    SETTINGS = auto()

class PlayState(Enum):
    PLAY_LOOP = auto()
    PLAY_PAUSE = auto()
    PLAY_FINISH = auto()
    PLAY_QUIT = auto()

class WindowClosed(Exception):
    pass