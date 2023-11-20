import json
from logging import Logger
from typing import Any, Tuple

from clingo import Model
from clingo.control import Control
from flatland.envs.rail_env import RailEnv

from flatlandasp.core.asp.instance_generator import InstanceGenerator
from flatlandasp.core.utils.file_utils import create_path_if_not_exist
from flatlandasp.flatland_asp_config import FlatlandASPConfig, get_config


class FlatlandASPSolver:
    def __init__(self, *,
                 environment: RailEnv,
                 clingo_control: Control,
                 instance_generator: InstanceGenerator,
                 logger: Logger,
                 config: FlatlandASPConfig = get_config()) -> None:
        self.environment = environment
        self.environment.reset()
        self._logger = logger

        self.instance_generator = instance_generator

        self._config = config
        self.clingo_control = clingo_control

        self.models = []

        self.agent_actions = {}
        """ Actions each agent is supposed to make."""
        self.agent_paths: dict[Any, list[Tuple[int, int]]] = {}
        """ Path for each agent resulting from the given actions."""
        self.number_of_symbols = 10000

    def _on_clingo_model(self, model: Model):
        """ Populate FlatlandASP with data based on model.

            Args:
                model: Model that was found, which satisfies the provided instance/encoding
        """
        symbols = model.symbols(shown=True)

        self.models.append(
            [f'{symbol.name}({",".join([str(arg.number) for arg in symbol.arguments])})'
             for symbol in symbols])

        if len(symbols) < self.number_of_symbols:
            self._logger.info(
                f"Shorter model found {self.number_of_symbols} > {len(symbols)}")
            self.number_of_symbols = len(symbols)
            self.agent_actions = {}
        else:
            return

        for symbol in symbols:
            if symbol.name == "agent_action":
                id = symbol.arguments[0].number
                action = symbol.arguments[1].number

                self.agent_actions.setdefault(id, []).append(action)

            if symbol.name == "agent_position":
                id = symbol.arguments[0].number
                x = symbol.arguments[1].number
                y = symbol.arguments[2].number
                handle = self.environment.agents[id].handle

                self.agent_paths.setdefault(handle, []).append((y, x))

    def solve(self, encoding_name: str):
        self._logger.info("Creating instance.")

        self.instance_generator.generate_instance_for_environment(
            env=self.environment, step_limit=20)
        self.instance_generator.store_instance(
            self._config.asp_instances_path, 'naive_test_instance')

        # Load instance from file
        self.clingo_control.load(
            f"{self._config.asp_instances_path}naive_test_instance.lp")
        # Load encoding from file
        self.clingo_control.load(
            f"{self._config.asp_encodings_path}{encoding_name}.lp")

        self._logger.info("Start grounding.")
        self.clingo_control.ground()

        self._logger.info("Start solving.")
        self.clingo_control.solve(
            on_model=lambda x: self._on_clingo_model(x))

        self._logger.info(
            f"Finished solving, best model has {self.number_of_symbols} symbols.")

    def save(self) -> None:
        solve_data = {
            "solution": {
                "agent_paths": self.agent_paths,
                "agent_actions": self.agent_actions
            },
            "models": self.models
        }

        create_path_if_not_exist(path=self._config.solver_output_path)

        with open(f'{self._config.solver_output_path}solve.json', 'w') as f:
            f.write(json.dumps(solve_data, indent=4))
