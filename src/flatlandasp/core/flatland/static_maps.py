from typing import Any, Tuple

import numpy as np
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap

from flatlandasp.core.flatland.schemas.cell_type import CellType


def straight_map(*, length: int, padding: int) -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    transitions = RailEnvTransitions()
    cell_types = transitions.transition_list
    empty = cell_types[0]
    sn_straight = cell_types[1]
    we_straight = transitions.rotate_transition(sn_straight, 90)

    grid = np.array(
        [[empty] * (length+2*padding)]*padding +
        [[empty]*padding + [we_straight] * length + [empty]*padding] +
        [[empty] * (length+2*padding)]*padding
    )

    print(grid)

    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    grid_transition_map.grid = grid

    city_positions = [(padding, padding), (padding, padding+length-1)]

    city_orientations = [1, 3]

    train_stations = [[((padding, padding), 0)],
                      [((padding, padding+length-1), 0)]]

    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    optionals = {'agents_hints': agents_hints}

    print(optionals)
    return grid_transition_map, optionals


def example_basic_static_map() -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    transitions = RailEnvTransitions()
    cell_types = transitions.transition_list
    empty = cell_types[0]

    sn_straight = cell_types[1]
    we_straight = transitions.rotate_transition(sn_straight, 90)
    se_turn = cell_types[8]
    ws_turn = transitions.rotate_transition(se_turn, 90)
    nw_turn = transitions.rotate_transition(ws_turn, 90)
    en_turn = transitions.rotate_transition(nw_turn, 90)

    number_of_straight_rails = 15

    grid = np.array(
        [[empty] * (4+number_of_straight_rails)] +
        [[empty] + [se_turn] + [we_straight] * number_of_straight_rails + [ws_turn] + [empty]] +
        [[empty] + [sn_straight] + [empty] * number_of_straight_rails + [sn_straight] + [empty]] * number_of_straight_rails +
        [[empty] + [en_turn] + [we_straight] * number_of_straight_rails + [nw_turn] + [empty]] +
        [[empty] * (4+number_of_straight_rails)], dtype=np.uint16
    )

    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    grid_transition_map.grid = grid

    city_positions = [(1, 2), (number_of_straight_rails +
                               2, number_of_straight_rails+1)]

    city_orientations = [1, 3]

    train_stations = [
        [((1, 2), 0)],
        [((number_of_straight_rails +
           2, number_of_straight_rails+1), 0)],
    ]

    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    optionals = {'agents_hints': agents_hints}
    print(optionals)
    return grid_transition_map, optionals


def passing_siding_map() -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    transitions = RailEnvTransitions()
    cell_types = transitions.transition_list
    empty = cell_types[CellType.EMPTY.value]

    sn_straight = cell_types[CellType.STRAIGHT.value]
    we_straight = transitions.rotate_transition(sn_straight, 90)
    se_turn = cell_types[CellType.SIMPLE_TURN_RIGHT.value]
    ws_turn = transitions.rotate_transition(se_turn, 90)
    sw_simple_switch = cell_types[CellType.SIMPLE_SWITCH.value]
    en_simple_switch = transitions.rotate_transition(sw_simple_switch, 90)
    se_simple_switch = cell_types[CellType.SIMPLE_SWITCH_MIRRORED.value]
    wn_simple_switch = transitions.rotate_transition(se_simple_switch, 270)

    grid = np.array(
        [[empty] * (14)] +
        [[empty]*5 + [se_turn] + [we_straight]*2 + [ws_turn] + [empty]*5] +
        [[empty] + [we_straight]*4+[en_simple_switch] +
            [we_straight]*2+[wn_simple_switch] + [we_straight]*4 + [empty]] +
        [[empty] * (14)], dtype=np.uint16
    )
    print(grid)
    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    grid_transition_map.grid = grid

    city_positions = [(2, 1), (2, 12)]

    city_orientations = [1, 3]

    train_stations = [
        [((2, 1), 0)],
        [((2, 12), 0)],
    ]

    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    optionals = {'agents_hints': agents_hints}
    return grid_transition_map, optionals


def multi_passing_siding_map() -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    transitions = RailEnvTransitions()
    cell_types = transitions.transition_list
    empty = cell_types[CellType.EMPTY.value]

    sn_straight = cell_types[CellType.STRAIGHT.value]
    we_straight = transitions.rotate_transition(sn_straight, 90)
    se_turn = cell_types[CellType.SIMPLE_TURN_RIGHT.value]
    ws_turn = transitions.rotate_transition(se_turn, 90)
    sw_simple_switch = cell_types[CellType.SIMPLE_SWITCH.value]
    en_simple_switch = transitions.rotate_transition(sw_simple_switch, 90)
    se_simple_switch = cell_types[CellType.SIMPLE_SWITCH_MIRRORED.value]
    wn_simple_switch = transitions.rotate_transition(se_simple_switch, 270)

    grid = np.array(
        [[empty] * (14)] +
        [[empty]*5 + [se_turn] + [we_straight]*2 + [ws_turn] + [empty]*5] +
        [[empty]*5 + [se_simple_switch] + [we_straight]*2 + [sw_simple_switch] + [empty]*5] +
        [[empty]*5 + [se_simple_switch] + [we_straight]*2 + [sw_simple_switch] + [empty]*5] +
        [[empty] + [we_straight]*4+[en_simple_switch] +
            [we_straight]*2+[wn_simple_switch] + [we_straight]*4 + [empty]] +
        [[empty] * (14)], dtype=np.uint16
    )
    print(grid)
    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    grid_transition_map.grid = grid

    city_positions = [(4, 1), (4, 12)]

    city_orientations = [1, 3]

    train_stations = [
        [((4, 1), 0)],
        [((4, 12), 0)],
    ]

    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    optionals = {'agents_hints': agents_hints}
    return grid_transition_map, optionals


def simple_switch_map() -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    transitions = RailEnvTransitions()
    cell_types = transitions.transition_list
    empty = cell_types[CellType.EMPTY.value]

    se_turn = cell_types[CellType.SIMPLE_TURN_RIGHT.value]
    sw_simple_switch = cell_types[CellType.SIMPLE_SWITCH.value]
    en_simple_switch = transitions.rotate_transition(sw_simple_switch, 90)
    sn_dead_end = cell_types[CellType.DEAD_END.value]
    we_dead_end = transitions.rotate_transition(sn_dead_end, 90)
    ew_dead_end = transitions.rotate_transition(sn_dead_end, 270)

    grid = np.array(
        [[empty] + [se_turn] + [we_dead_end]] +
        [[ew_dead_end] + [en_simple_switch] + [we_dead_end]], dtype=np.uint16
    )
    print(grid)
    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    grid_transition_map.grid = grid

    city_positions = [(1, 0), (1, 2)]

    city_orientations = [1, 3]

    train_stations = [
        [((1, 0), 0)],
        [((1, 2), 0)],
    ]

    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    optionals = {'agents_hints': agents_hints}
    return grid_transition_map, optionals
