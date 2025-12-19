from enum import Enum, auto


class CallSiteKind(Enum):
    SYNC_FACTORY = auto()
    CONSTRUCTOR = auto()
