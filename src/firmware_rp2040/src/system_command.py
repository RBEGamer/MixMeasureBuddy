from micropython import const

class system_command:
    UNKNOWN: int = const(-1)
    COMMAND_TYPE_NAVIGATION: int = const(0)

    NAVIGATION_LEFT: int = const(0)
    NAVIGATION_RIGHT: int = const(1)
    NAVIGATION_ENTER: int = const(2)
    NAVIGATION_EXIT: int = const(3)



    type: int = UNKNOWN
    action: int = UNKNOWN

    def __init__(self, _type: int = UNKNOWN, _action: int = UNKNOWN):
        self.type = _type
        self.action = _action