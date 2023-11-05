import time
from typing import Any, Tuple

from clingo import Model
from clingo.control import Control
from flatland.envs.rail_env import RailEnv, RailEnvActions
from flatland.utils.rendertools import RenderTool

from flatlandasp.core.asp.instance_descriptions.naive_instance import \
    NaiveInstance
from flatlandasp.core.asp.instance_generator import InstanceGenerator
from flatlandasp.core.flatland.schemas.action import Action
from flatlandasp.core.utils.image_utils import get_image_bytes_from_np_array


class FlatlandASP:
    """ Main class used to interact with Flatland ASP.
    """

    def __init__(self, *, env: RailEnv, env_renderer: RenderTool, clingo_control: Control) -> None:
        self.env = env
        self.env.reset()

        for index, agent in enumerate(self.env.agents):
            # agent.earliest_departure = index*2
            print(
                f"agent: {index} should depart at: {agent.earliest_departure} state:{agent.state}")

        self.env_renderer = env_renderer
        self.clingo_control = clingo_control
        self.agent_actions = {}
        """ Actions each agent is supposed to make."""
        self.agent_paths: dict[Any, list[Tuple[int, int]]] = {}
        """ Path for each agent resulting from the given actions."""

    def _on_clingo_model(self, model: Model):
        """ Populate FlatlandASP with data based on model.

            Args:
                model: Model that was found, which satisfies the provided instance/encoding
        """

        for symbol in model.symbols(shown=True):
            print(symbol)
            if symbol.name == "agent_action":
                id = symbol.arguments[0].number
                action = symbol.arguments[1].number

                self.agent_actions.setdefault(id, []).append(action)

            if symbol.name == "agent_position":
                id = symbol.arguments[0].number
                x = symbol.arguments[1].number
                y = symbol.arguments[2].number
                handle = self.env.agents[id].handle

                self.agent_paths.setdefault(handle, []).append((y, x))

    def simulate_environment(self, max_steps: int = 30,
                             step_delay: float = 0.5) -> None:

        try:
            step = 0
            agents_step = {}
            for id, l in self.agent_actions.items():
                print(f"Agent {id} action count {len(l)}")
            while not self.env.dones["__all__"] and step < max_steps:
                actionsdict = {}
                print(f"Actions for step: {step}")
                for idx, agent in enumerate(self.env.agents):
                    if agent.position:
                        if not self.env.dones[idx]:
                            if idx in agents_step:
                                agents_step[idx] += 1
                            else:
                                agents_step[idx] = 0
                            actionsdict[agent.handle] = self.agent_actions[idx][agents_step[idx]]
                    else:
                        actionsdict[agent.handle] = RailEnvActions.MOVE_FORWARD

                    if idx in agents_step:
                        print(
                            f"Agent({idx}) is at {agent.position} and chose {Action(actionsdict[agent.handle])} at step {agents_step[idx]}/{len(self.agent_actions[idx])-1}.")
                    else:
                        print(
                            f"Agent({idx}) not spawned yet. {agent.state}")

                self.env.step(actionsdict)

                self.env_renderer.render_env(show=True,
                                             return_image=True, show_rowcols=True, show_predictions=True, step=0)

                time.sleep(step_delay)
                step += 1
        except Exception as e:
            print(
                f"An exception occured which would otherwise have closed the rendering window.\n\n{e}\n")

    def get_image_bytes(self):
        image = self.env_renderer.render_env(
            show_rowcols=True,
            show_predictions=True,
            return_image=True
        )

        return get_image_bytes_from_np_array(image)

    def solve(self, instance_description=NaiveInstance()):
        self.env._max_episode_steps = 50

        asp_generator = InstanceGenerator(
            instance_description=instance_description)
        asp_generator.generate_instance_for_environment(
            env=self.env, step_limit=20)
        asp_generator.store_instance('naive_test_instance')

        # Load instance from file
        self.clingo_control.load("asp/instances/naive_test_instance.lp")
        # Load encoding from file
        self.clingo_control.load(
            "asp/encodings/passing_siding_naive_encoding.lp")
        # Ground the program
        self.clingo_control.ground()
        # ctl.configuration.solve.models = 5
        self.clingo_control.solve(
            on_model=lambda x: self._on_clingo_model(x))
