
from clingo import Control
from fastapi import APIRouter, HTTPException

from flatlandasp.core.asp.instance_descriptions.base_instance import BaseInstance
from flatlandasp.core.asp.instance_generator import InstanceGenerator
from flatlandasp.core.flatland import environment_crud
from flatlandasp.core.log_config import get_logger
from flatlandasp.features.solver.flatland_asp_solver import FlatlandASPSolver
from flatlandasp.features.solver.schemas.solver_input_schema import SolverInput

router = APIRouter()

logger = get_logger()


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
            environment = environment_crud.get_environment_from_json(
                f'{input.environment_name}.json', number_of_agents=input.number_of_agents)

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
