from typing import Tuple

from flatlandasp.core.flatland.schemas.action import Action
from flatlandasp.core.flatland.schemas.cell_type import CellType
from flatlandasp.core.flatland.schemas.orientation import (Orientation,
                                                           OrientationChange)

CELL_TYPE_TO_ACTION_MAP: dict[CellType, list[list[Action, OrientationChange]]] = {

    CellType.EMPTY: [[]],
    CellType.STRAIGHT: [
        [(Action.FORWARD, OrientationChange.KEEP)],
        [],
        [(Action.FORWARD, OrientationChange.KEEP)],
        []
    ],
    CellType.SIMPLE_SWITCH: [
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_LEFT, OrientationChange.LEFT)],
        [(Action.FORWARD, OrientationChange.RIGHT)],
        [(Action.FORWARD, OrientationChange.KEEP)],
        []
    ],
    CellType.DIAMOND_CROSSING: [
        [(Action.FORWARD, OrientationChange.KEEP)],
        [(Action.FORWARD, OrientationChange.KEEP)],
        [(Action.FORWARD, OrientationChange.KEEP)],
        [(Action.FORWARD, OrientationChange.KEEP)]
    ],
    CellType.SINGLE_SLIP: [
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_LEFT, OrientationChange.LEFT)],
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_RIGHT, OrientationChange.RIGHT)],
        [(Action.FORWARD, OrientationChange.KEEP)],
        [(Action.FORWARD, OrientationChange.KEEP)]
    ],
    CellType.DOUBLE_SLIP: [
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_RIGHT, OrientationChange.RIGHT)],
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_LEFT, OrientationChange.LEFT)],
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_RIGHT, OrientationChange.RIGHT)],
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_LEFT, OrientationChange.LEFT)]
    ],
    CellType.SYMMETRICAL: [
        [(Action.TURN_RIGHT, OrientationChange.RIGHT),
         (Action.TURN_LEFT, OrientationChange.LEFT)],
        [(Action.FORWARD, OrientationChange.RIGHT)],
        [],
        [(Action.FORWARD, OrientationChange.LEFT)]
    ],
    CellType.DEAD_END: [
        [(Action.FORWARD, OrientationChange.TURN_AROUND)],
        [],
        [],
        []
    ],
    CellType.SIMPLE_TURN_RIGHT: [
        [(Action.FORWARD, OrientationChange.RIGHT)],
        [],
        [],
        [(Action.FORWARD, OrientationChange.LEFT)]
    ],
    CellType.SIMPLE_TURN_LEFT: [
        [(Action.FORWARD, OrientationChange.LEFT)],
        [(Action.FORWARD, OrientationChange.RIGHT)],
        [],
        []
    ],
    CellType.SIMPLE_SWITCH_MIRRORED: [
        [(Action.FORWARD, OrientationChange.KEEP),
         (Action.TURN_RIGHT, OrientationChange.RIGHT)],
        [],
        [(Action.FORWARD, OrientationChange.KEEP)],
        [(Action.FORWARD, OrientationChange.LEFT)]
    ],

}


CELL_ID_TO_TYPE_AND_ORIENTATON_MAP: dict[int, Tuple[CellType, Orientation]] = {
    0: (CellType.EMPTY, Orientation.NORTH),

    32800: (CellType.STRAIGHT, Orientation.NORTH),
    1025: (CellType.STRAIGHT, Orientation.EAST),

    37408: (CellType.SIMPLE_SWITCH, Orientation.NORTH),
    3089: (CellType.SIMPLE_SWITCH, Orientation.EAST),
    32872: (CellType.SIMPLE_SWITCH, Orientation.SOUTH),
    17411: (CellType.SIMPLE_SWITCH, Orientation.WEST),

    33825: (CellType.DIAMOND_CROSSING, Orientation.NORTH),

    38433: (CellType.SINGLE_SLIP, Orientation.NORTH),
    35889: (CellType.SINGLE_SLIP, Orientation.EAST),
    33897: (CellType.SINGLE_SLIP, Orientation.SOUTH),
    50211: (CellType.SINGLE_SLIP, Orientation.WEST),

    52275: (CellType.DOUBLE_SLIP, Orientation.NORTH),
    38505: (CellType.DOUBLE_SLIP, Orientation.EAST),

    20994: (CellType.SYMMETRICAL, Orientation.NORTH),
    6672: (CellType.SYMMETRICAL, Orientation.EAST),
    2136: (CellType.SYMMETRICAL, Orientation.SOUTH),
    16458: (CellType.SYMMETRICAL, Orientation.WEST),

    8192: (CellType.DEAD_END, Orientation.NORTH),
    256: (CellType.DEAD_END, Orientation.EAST),
    128: (CellType.DEAD_END, Orientation.SOUTH),
    4: (CellType.DEAD_END, Orientation.WEST),

    16386: (CellType.SIMPLE_TURN_RIGHT, Orientation.NORTH),
    4608: (CellType.SIMPLE_TURN_RIGHT, Orientation.EAST),
    2064: (CellType.SIMPLE_TURN_RIGHT, Orientation.SOUTH),
    72: (CellType.SIMPLE_TURN_RIGHT, Orientation.WEST),

    4608: (CellType.SIMPLE_TURN_LEFT, Orientation.NORTH),
    2064: (CellType.SIMPLE_TURN_LEFT, Orientation.EAST),
    72: (CellType.SIMPLE_TURN_LEFT, Orientation.SOUTH),
    16386: (CellType.SIMPLE_TURN_LEFT, Orientation.WEST),

    49186: (CellType.SIMPLE_SWITCH_MIRRORED, Orientation.NORTH),
    5633: (CellType.SIMPLE_SWITCH_MIRRORED, Orientation.EAST),
    34864: (CellType.SIMPLE_SWITCH_MIRRORED, Orientation.SOUTH),
    1097: (CellType.SIMPLE_SWITCH_MIRRORED, Orientation.WEST),
}
