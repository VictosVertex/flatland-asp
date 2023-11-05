from enum import Enum


class OrientationChange(Enum):
    KEEP = 0
    RIGHT = 1
    TURN_AROUND = 2
    LEFT = 3


class Orientation(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
