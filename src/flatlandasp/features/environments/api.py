
import numpy as np
from fastapi import APIRouter
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map

from flatlandasp.core.flatland import environment_crud
from flatlandasp.core.flatland.environment_file_type import EnvironmentFileType
from flatlandasp.core.flatland.mappings import CELL_TYPE_TO_BASE_CELL_ID
from flatlandasp.core.flatland.schemas.environment_data_schema import (
    EnvironmentData,
)
from flatlandasp.core.log_config import get_logger
from flatlandasp.core.utils.file_utils import get_file_names_in_path
from flatlandasp.core.utils.number_utils import n_roll_bits
from flatlandasp.features.environments.schemas.environment_input_schema import (
    EnvironmentInput,
)
from flatlandasp.flatland_asp_config import get_config

router = APIRouter()
logger = get_logger()


@router.post("/{name}/save")
def save_data_and_environment(name: str, input: EnvironmentInput):
    """ Save given environment input data as json and pkl environments."""

    logger.info(input)

    grid = np.full(
        (input.dimensions.height, input.dimensions.width), 0)

    for cell in input.cells:
        grid[cell.position.y][cell.position.x] = n_roll_bits(
            CELL_TYPE_TO_BASE_CELL_ID[cell.type], cell.orientation.value)

    transitions = RailEnvTransitions()

    grid_transition_map = GridTransitionMap(width=grid.shape[1],
                                            height=grid.shape[0],
                                            transitions=transitions)
    grid_transition_map.grid = grid

    city_positions = []
    train_stations = []
    city_orientations = []

    # for now each station is a city
    for station in input.stations:
        position = (station.position.y, station.position.x)
        city_positions.append(position)
        train_stations.append([(position, 0)])
        city_orientations.append(station.orientation.value)

    agents_hints = {'city_positions': city_positions,
                    'train_stations': train_stations,
                    'city_orientations': city_orientations
                    }

    optionals = {'agents_hints': agents_hints}

    # If no agents are set, the number of agents
    # is equivalent to the number of stations
    number_of_agents = len(input.stations)

    if (input.agents is not None):
        number_of_agents = len(input.agents)

    # Save as .json
    environment_data = EnvironmentData(
        grid=grid_transition_map.grid, optionals=optionals, number_of_agents=number_of_agents)

    environment_crud.create_data_as_json_file(file_name=f'{name}.json',
                                              environment_data=environment_data
                                              )

    # Save as .pkl
    environment = RailEnv(width=grid_transition_map.width,
                          height=grid_transition_map.height,
                          rail_generator=rail_from_grid_transition_map(
                              grid_transition_map, optionals),
                          line_generator=sparse_line_generator(),
                          number_of_agents=number_of_agents,
                          obs_builder_object=GlobalObsForRailEnv()
                          )
    environment.reset()

    environment_crud.create_as_pickle_file(
        file_name=f'{name}.pkl', env=environment)


@router.get("/")
def get_all():
    environments = {}

    for f in get_file_names_in_path(path=get_config().flatland_environments_path):
        name = f.split(".")[0]
        extension = f.split(".")[1]
        if name not in environments:
            environments[name] = {
                EnvironmentFileType.JSON: False, EnvironmentFileType.PKL: False}

        if EnvironmentFileType(extension) == EnvironmentFileType.JSON:
            environments[name][EnvironmentFileType.JSON] = True

        if EnvironmentFileType(extension) == EnvironmentFileType.PKL:
            environments[name][EnvironmentFileType.PKL] = True
    return environments


@router.get("/{file_name}")
def read_from_json(file_name: str):
    return environment_crud.read_data_from_json_file(file_name=file_name).dict()
