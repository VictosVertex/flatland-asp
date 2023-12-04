import copy
import time

from flatland.envs.rail_env import RailEnv, RailEnvActions
from flatland.utils.rendertools import RenderTool
from PIL import Image

from flatlandasp.core.flatland.schemas.action import Action
from flatlandasp.core.utils.image_utils import get_image_bytes_from_image
from flatlandasp.flatland_asp_config import FlatlandASPConfig, get_config


class FlatlandASPSimulator:
    def __init__(self, *,
                 env: RailEnv,
                 env_renderer: RenderTool,
                 config: FlatlandASPConfig = get_config()) -> None:
        self.env = env
        self._config = config

        for index, agent in enumerate(self.env.agents):
            # agent.earliest_departure = index*2
            print(
                f"agent: {index} should depart at: {agent.earliest_departure} state:{agent.state}")

        self.env_renderer = env_renderer
        self.agents_at_step = {}

    def simulate_environment(self,
                             agent_actions: dict,
                             max_steps: int = 30,
                             step_delay: float = 0.5,
                             render: bool = False) -> None:

        try:
            # Set Flatland horizon,
            # this should be similar to the ASP horizon
            self.env._max_episode_steps = max_steps

            step = 0
            agents_step = {}
            for id, l in agent_actions.items():
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
                            actionsdict[agent.handle] = agent_actions[idx][agents_step[idx]]
                    else:
                        actionsdict[agent.handle] = RailEnvActions.MOVE_FORWARD

                    if idx in agents_step:
                        print(
                            f"Agent({idx}) is at {agent.position} and chose {Action(actionsdict[agent.handle])} at step {agents_step[idx]}/{len(agent_actions[idx])-1}.")
                    else:
                        print(
                            f"Agent({idx}) not spawned yet. {agent.state}")

                self.env.step(actionsdict)

                self.agents_at_step[step] = copy.deepcopy(self.env.agents)

                if render:
                    self.env_renderer.render_env(show=True,
                                                 return_image=True, show_rowcols=True, show_predictions=True, step=0)

                    time.sleep(step_delay)
                step += 1
        except Exception as e:
            print(
                f"An exception occured which would otherwise have closed the rendering window.\n\n{e}\n")

    def get_image_bytes_at_simulation_step(self, step: int = 0):
        old_agents = self.env.agents
        self.env.agents = self.agents_at_step[step]
        image_bytes = self.get_image_bytes()
        self.env.agents = old_agents
        return image_bytes

    def get_image_bytes(self):
        image_array = self.env_renderer.render_env(
            show_rowcols=True,
            show_predictions=True,
            return_image=True
        )
        image = Image.fromarray(image_array)
        return get_image_bytes_from_image(image)
