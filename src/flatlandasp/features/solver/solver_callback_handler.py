from logging import Logger
from typing import Any, Tuple

from clingo import Model


class SolverCallbackHandler:
    def __init__(self, *, logger: Logger) -> None:
        self._logger = logger

        self._models = []

        self._agent_actions = {}
        """ Actions each agent is supposed to make."""
        self._agent_paths: dict[Any, list[Tuple[int, int]]] = {}
        """ Path for each agent resulting from the given actions."""
        self._number_of_symbols = None

    def on_model(self, model: Model):
        """ Populate SolverCallbackHandler with data based on model.

            Args:
                model: Model that was found by the solver
        """
        symbols = model.symbols(shown=True)
        self._models.append([str(symbol) for symbol in symbols])

        if self._number_of_symbols is None or len(symbols) < self._number_of_symbols:
            self._logger.info(
                f"Shorter model found {self._number_of_symbols} > {len(symbols)}")
            self._number_of_symbols = len(symbols)
        else:
            return

        agent_actions = {}

        for symbol in symbols:
            if symbol.name == "agent_action":
                id = symbol.arguments[0].number
                action = symbol.arguments[1].number
                time_step = symbol.arguments[2].number

                agent_actions.setdefault(id, {})[time_step] = action

            if symbol.name == "agent_position":
                id = symbol.arguments[0].number
                x = symbol.arguments[1].number
                y = symbol.arguments[2].number

                self._agent_paths.setdefault(id, []).append((y, x))

        self._agent_actions = {
            agent_id: [agent_actions[agent_id][step]
                       for step in sorted(agent_actions[agent_id])]
            for agent_id in sorted(agent_actions)
        }

    def get_last_model_strings(self) -> list[str]:
        if (len(self._models) == 0):
            return []

        return self._models[-1]

    def get_actions(self) -> dict:
        return self._agent_actions

    def get_paths(self) -> dict:
        return self._agent_paths

    def get_full_solution(self) -> dict:
        return {
            "solution": {
                "agent_paths": self._agent_paths,
                "agent_actions": self._agent_actions
            },
            "models": self._models
        }
