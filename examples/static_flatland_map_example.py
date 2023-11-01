""" This module acts an an introductory example for Flatland.

    This example deals with the creation of a simple static map
    and introduces the user to the basics of functionalities such as:
        - transitions
        - cells
        - agents
        - cities
        - train stations
        - environment generation
        - rendering


"""
import time
from typing import Any, Tuple

import numpy as np

from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.rendertools import RenderTool
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.rail_env import RailEnvActions


def basic_static_map() -> Tuple[GridTransitionMap, dict[str, dict[str, Any]]]:
    """ Create a basic static map using transitions.

        Return: Tuple consisting of
            grid transition map: Map containing the grid and transitions
            optionals: Parameters like hints for agents (For example city/station positions)
    """
    # Get all possible transitions
    transitions = RailEnvTransitions()
    # Get base cell types with default orientation
    cell_types = transitions.transition_list

    # Empty cell where no agent can be positioned at any time
    empty = cell_types[0]

    # In all other cell types, which are tracks
    # only one agent can be positioned at any time
    #
    # Straight track from south to north
    sn_straight = cell_types[1]
    # Straight track from west to east
    # This track is simply a 90 degree rotation of the straight south-north track
    we_straight = transitions.rotate_transition(sn_straight, 90)
    # Simple turn from south to east (right turn)
    se_turn = cell_types[8]
    # All other simple turns are rotations of the south-east turn
    # Simple turn from west to south
    ws_turn = transitions.rotate_transition(se_turn, 90)
    # Simple turn from north to west
    nw_turn = transitions.rotate_transition(ws_turn, 90)
    # Simple turn from east to north
    en_turn = transitions.rotate_transition(nw_turn, 90)

    # The number of straight rails used in each direction
    # This helps to quickly adjust the size of the map
    number_of_straight_rails = 15

    # The grid consisting of previously defined cell types.
    # In this example the track is a simple round trip
    # with a padding of empty cells and empty cells in the middle
    grid = np.array(
        [[empty] * (4+number_of_straight_rails)] +
        [[empty] + [se_turn] + [we_straight] * number_of_straight_rails + [ws_turn] + [empty]] +
        [[empty] + [sn_straight] + [empty] * number_of_straight_rails + [sn_straight] + [empty]] * number_of_straight_rails +
        [[empty] + [en_turn] + [we_straight] * number_of_straight_rails + [nw_turn] + [empty]] +
        [[empty] * (4+number_of_straight_rails)], dtype=np.uint16
    )

    # Create the transition map for the grid
    # It is important to note that in a matrix (array of arrays)
    #   shape[0]    corresponds to the number of arrays within the array
    #               which in this case corresponds to the height
    #   shape[1]    conversely corresponds to the width of the grid
    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    # Add the grid to the grid_transition_map
    grid_transition_map.grid = grid

    # City positions for two cities
    # These are required in order to place stations
    # since a station can only be placed in a city
    #
    # Important to note is that in Flatland positions are defined by:
    #   first parameter: y-coordinate (north-sourth)
    #   second parameter: x-coordinate (west-east)
    #
    # Example:
    #   Since the top left corner is the point (0,0) the
    #   position (1,2) refers to the point that is
    #   2 from the top and 3 from the left
    city_positions = [(1, 2), (number_of_straight_rails +
                               2, number_of_straight_rails+1)]

    # Orientation of both cities
    city_orientations = [1, 3]

    # Position and track number for one station for each city
    train_stations = [
        [((1, 2), 0)],
        [((number_of_straight_rails +
           2, number_of_straight_rails+1), 0)],
    ]

    # Combine city positions and orientations as well as train station
    # positions and track numbers into hints for agents
    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    # Add agent hints to optional parameters
    # which will later be used by the rail generator
    optionals = {'agents_hints': agents_hints}
    return grid_transition_map, optionals


def create_environment() -> RailEnv:
    """ Create a railway environment from a predefined (static) map.

        Returns:
            The created railway environment
    """

    # Create a basic static map consisting of
    #   grid_transition_map: Contains the grid and all transitions corresponding to each cell
    #   optionals: Optional parameters such as hints containing city/station positions
    grid_transition_map, optionals = basic_static_map()

    # Create the actual railway environment from the given parameters
    #
    # In this example the environment is based on the static map above.
    # Height and width are provided by the grid, while the grid transition map and
    # optionals are used by the rail generator to generate rails for the environment.
    #
    # A simple line generator and observation builder are used to create basic start
    # and target points as well as global observation of the entire environment
    #
    # The number of agents describes how many trains try to traverse from their starting
    # location to their target location
    env = RailEnv(width=grid_transition_map.grid.shape[1],
                  height=grid_transition_map.grid.shape[0],
                  rail_generator=rail_from_grid_transition_map(
                      grid_transition_map, optionals),
                  line_generator=sparse_line_generator(),
                  number_of_agents=2,
                  obs_builder_object=GlobalObsForRailEnv(),
                  )

    return env


def simulate_environment(env: RailEnv,
                         env_renderer: RenderTool,
                         steps: int = 10,
                         step_delay: float = 0.5) -> None:
    """ Simulate the environment for a given number of steps.

        Args:
            env: The environment which should be simulated
            env_renderer: The environment renderer used to display the environment
            steps: The number of steps the simulation should run
            step_delay: Sleep time between each step
    """
    for _ in range(steps):
        # In this example all agents use the same action at every step
        for handle in env.get_agent_handles():
            env.step({handle: RailEnvActions.MOVE_FORWARD})

        # Render the environment to the screen
        env_renderer.render_env(show=True, show_observations=True)
        time.sleep(step_delay)


if __name__ == '__main__':
    # Create the railway environment for this example
    env = create_environment()

    # Initialize the environment
    env.reset()

    # Set up a renderer
    env_renderer = RenderTool(env)
    env_renderer.render_env(show=True, show_observations=True)
    # Simulate the environment and use the renderer to display it
    try:
        simulate_environment(env, env_renderer)
    except Exception as e:
        print(
            f"An exception occured which would otherwise have closed the rendering window.\n\n{e}\n")

    # Wait for user input before closing the renderer (window)
    # in order to view the last state of the map
    input("Press key to close...")
    env_renderer.close_window()
