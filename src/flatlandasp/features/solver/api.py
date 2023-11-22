import logging

from clingo import Control
from fastapi import APIRouter, HTTPException
from flatland.core.grid.rail_env_grid import RailEnvTransitions
from flatland.core.transition_map import GridTransitionMap
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map

from flatlandasp.core.asp.instance_descriptions.base_instance import BaseInstance
from flatlandasp.core.asp.instance_generator import InstanceGenerator
from flatlandasp.core.flatland import environment_crud
from flatlandasp.features.solver.flatland_asp_solver import FlatlandASPSolver
from flatlandasp.features.solver.schemas.solver_input_schema import SolverInput

router = APIRouter()

logger = logging.getLogger("solver.api")


def get_environment_from_json(file_name: str, number_of_agents: int):
    environment_data = environment_crud.read_data_from_json_file(
        file_name=file_name)

    grid_transition_map = GridTransitionMap(width=environment_data.grid.shape[1],
                                            height=environment_data.grid.shape[0],
                                            transitions=RailEnvTransitions())
    grid_transition_map.grid = environment_data.grid

    return RailEnv(width=grid_transition_map.width,
                   height=grid_transition_map.height,
                   rail_generator=rail_from_grid_transition_map(
                       grid_transition_map, environment_data.optionals),
                   line_generator=sparse_line_generator(),
                   number_of_agents=number_of_agents,
                   obs_builder_object=GlobalObsForRailEnv()
                   )


@router.post("/solve")
def solve(input: SolverInput):
    try:
        if input.number_of_agents is None or input.number_of_agents < 1:
            # If no number of agents is provided
            # or the provided number is lower than 1
            # load the pkl file directly
            environment = environment_crud.read_from_pickle_file(
                f'{input.environment_name}.pkl')
        else:
            environment = get_environment_from_json(
                f'{input.environment_name}.json', input.number_of_agents)

        environment.reset()

        cling_control = Control()

        instance_generator = InstanceGenerator(
            instance_description=BaseInstance())

        solver = FlatlandASPSolver(environment=environment,
                                   clingo_control=cling_control,
                                   instance_generator=instance_generator,
                                   logger=logger)

        solver.solve(input.encoding_name)
        solver.save()

        return solver.models
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, detail="File not found.") from e
