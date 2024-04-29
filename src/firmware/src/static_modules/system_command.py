from micropython import const

class system_command:
    UNKNOWN: int = const(-1)
    COMMAND_TYPE_NAVIGATION: int = const(0)
    COMMAND_TYPE_SCALE_VALUE: int = const(1)
    COMMAND_TYPE_TIMER_IRQ: int = const(2)

    NAVIGATION_LEFT: int = const(0)
    NAVIGATION_RIGHT: int = const(1)
    NAVIGATION_ENTER: int = const(2)
    NAVIGATION_EXIT: int = const(3)

    SCALE_CURRENT_VALUE: int = const(10)

    TIMER_TICK = int = const(11)

    type: int = UNKNOWN
    action: int = UNKNOWN
    value: any = None

    def __init__(self, _type: int = UNKNOWN, _action: int = UNKNOWN, _value: any = None):
        self.type = _type
        self.action = _action
        self.value = _value