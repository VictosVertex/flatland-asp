from clingo import Control
from fastapi import APIRouter, HTTPException

from flatlandasp.core.asp.instance_generation import generate_instance_lines
from flatlandasp.core.flatland import environment_crud
from flatlandasp.core.log_config import get_logger
from flatlandasp.core.utils.file_utils import (
    write_json_file,
    write_lines_to_file_in_output,
)
from flatlandasp.features.solver.schemas.solver_input_schema import SolverInput
from flatlandasp.features.solver.solver_callback_handler import SolverCallbackHandler
from flatlandasp.flatland_asp_config import get_config

router = APIRouter()

logger = get_logger()


@router.post("/solve")
def solve(input: SolverInput):
    try:
        # Create Environment
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

        # Create ASP instance from environment
        instance_file_name = f"{input.environment_name}.lp"
        instance_lines = generate_instance_lines(environment, input.step_limit)
        write_lines_to_file_in_output(
            path=get_config().asp_instances_path, file_name=instance_file_name, lines=instance_lines)

        # Solve instance with selected encoding
        clingo_control = Control()

        # Load instance from file
        clingo_control.load(
            f"{get_config().asp_instances_path}{instance_file_name}")

        # Load encoding from file
        clingo_control.load(
            f"{get_config().asp_encodings_path}{input.encoding_name}.lp")

        logger.info("Start grounding.")

        clingo_control.ground()

        callback_handler = SolverCallbackHandler(logger=logger)

        logger.info("Start solving.")

        clingo_control.solve(on_model=callback_handler.on_model)

        logger.info(
            f"Finished solving, best model has {len(callback_handler.get_last_model_strings())} symbols.")

        solution = callback_handler.get_full_solution()

        write_json_file(path=get_config().solver_output_path,
                        file_name=f"{input.environment_name}__{input.encoding_name}.json",
                        json_data=solution)

        write_json_file(path=get_config().solver_output_path,
                        file_name=f"{input.environment_name}__{input.encoding_name}__stats.json",
                        json_data=clingo_control.statistics)

        return solution
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, detail="File not found.") from e
