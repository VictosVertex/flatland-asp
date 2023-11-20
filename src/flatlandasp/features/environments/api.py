from fastapi import APIRouter
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map

from flatlandasp.core.flatland import environment_crud
from flatlandasp.core.flatland.environment_file_type import EnvironmentFileType
from flatlandasp.core.flatland.schemas.environment_data_schema import (
    EnvironmentData,
)
from flatlandasp.core.flatland.static_maps import multi_passing_siding_map
from flatlandasp.core.utils.file_utils import get_file_names_in_path
from flatlandasp.flatland_asp_config import get_config

router = APIRouter()


@router.get("/{name}/save")
def save_data_and_environment(name: str):
    """ This is for now just a dummy to store static python maps."""
    grid_transition_map, optionals = multi_passing_siding_map()

    environment_data = EnvironmentData(
        grid=grid_transition_map.grid, optionals=optionals, number_of_agents=2)

    environment_crud.create_data_as_json_file(file_name=f'{name}.json',
                                              environment_data=environment_data
                                              )

    env = RailEnv(width=grid_transition_map.width,
                  height=grid_transition_map.height,
                  rail_generator=rail_from_grid_transition_map(
                      grid_transition_map, optionals),
                  line_generator=sparse_line_generator(),
                  number_of_agents=2,
                  obs_builder_object=GlobalObsForRailEnv()
                  )
    env.reset()

    environment_crud.create_as_pickle_file(file_name=f'{name}.pkl', env=env)


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
