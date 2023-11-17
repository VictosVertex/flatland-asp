from typing import Any, Tuple

from clingo import Model
from clingo.control import Control
from flatland.envs.rail_env import RailEnv

from flatlandasp.core.asp.instance_generator import InstanceGenerator
from flatlandasp.flatland_asp_config import FlatlandASPConfig, get_config


class FlatlandASPSolver:
    def __init__(self, *, environment: RailEnv, clingo_control: Control,
                 instance_generator: InstanceGenerator,
                 config: FlatlandASPConfig = get_config()) -> None:
        self.environment = environment
        self.environment.reset()

        self.instance_generator = instance_generator

        self._config = config
        self.clingo_control = clingo_control

        self.agent_actions = {}
        """ Actions each agent is supposed to make."""
        self.agent_paths: dict[Any, list[Tuple[int, int]]] = {}
        """ Path for each agent resulting from the given actions."""
        self.symbols = 10000

    def _on_clingo_model(self, model: Model):
        """ Populate FlatlandASP with data based on model.

            Args:
                model: Model that was found, which satisfies the provided instance/encoding
        """
        symbols = model.symbols(shown=True)
        if len(symbols) < self.symbols:
            print(
                f"----------------------- SHORTER MODEL FOUND {self.symbols} > {len(symbols)}")
            self.symbols = len(symbols)
            self.agent_actions = {}
        else:
            print("----------------------- SKIPPED")
            return

        for symbol in symbols:
            print(symbol)
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
        # Ground the program
        self.clingo_control.ground()

        self.clingo_control.solve(
            on_model=lambda x: self._on_clingo_model(x))
