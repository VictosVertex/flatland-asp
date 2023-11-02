import numpy as np
from typing import Any, Tuple
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap


def straight_hirozontal_line_map(*, length: int, padding: int) -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    transitions = RailEnvTransitions()
    cell_types = transitions.transition_list
    empty = cell_types[0]
    sn_straight = cell_types[1]
    we_straight = transitions.rotate_transition(sn_straight, 90)

    grid = np.array(
        [[empty] * (length+2*padding)]*padding +
        [[empty] + [we_straight] * length + [empty]] +
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
        [[empty] + [se_turn] + [we_straight] * (number_of_straight_rails-1)+[empty] + [ws_turn] + [empty]] +
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
