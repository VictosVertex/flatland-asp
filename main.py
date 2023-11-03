import time
from typing import Any, Tuple
from app.core.asp.instance_descriptions.naive_instance import NaiveInstance
from app.core.asp.instance_generator import InstanceGenerator
from app.core.flatland.static_maps import straight_map
from clingo.control import Control
from clingo import Model
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.rendertools import RenderTool, AgentRenderVariant
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.rail_env import RailEnvActions


def create_environment() -> RailEnv:
    grid_transition_map, optionals = straight_map(
        length=5, padding=3)
    # grid_transition_map, optionals = example_basic_static_map()

    env = RailEnv(width=grid_transition_map.grid.shape[1],
                  height=grid_transition_map.grid.shape[0],
                  rail_generator=rail_from_grid_transition_map(
                      grid_transition_map, optionals),
                  line_generator=sparse_line_generator(),
                  number_of_agents=1,
                  obs_builder_object=GlobalObsForRailEnv(),
                  )

    return env


def simulate_environment(env: RailEnv,
                         env_renderer: RenderTool,
                         max_steps: int = 30,
                         step_delay: float = 0.5) -> None:

    step = 0
    while not env.dones[0] and step < max_steps:
        for agent in env.agents:
            env.step({agent.handle: RailEnvActions.MOVE_FORWARD})

        env_renderer.render_env(
            show=True, show_rowcols=True, show_predictions=True)
        time.sleep(step_delay)
        step += 1


def on_model(model: Model) -> None:
    """ Prints the current model to the terminal

        Args:
            model: Model that was found, which satisfies the provided instance/encoding
    """
    print(model)
    x = model.symbols(shown=True)[0]
    env.dev_pred_dict: dict[Any, list[Tuple[int, int]]] = {}
    for symbol in model.symbols(shown=True):
        if symbol.name == "agent_position":
            id = symbol.arguments[0].number
            x = symbol.arguments[1].number
            y = symbol.arguments[2].number
            print(f"Agent ID: {id} X: {x} Y: {y}")
            handle = env.agents[id].handle
            if handle in env.dev_pred_dict:
                env.dev_pred_dict[handle].append((y, x))
            else:
                env.dev_pred_dict[handle] = [(y, x)]


env = create_environment()

if __name__ == '__main__':

    env.reset()
    asp_generator = InstanceGenerator(instance_description=NaiveInstance())
    asp_generator.generate_instance_for_environment(env=env)
    asp_generator.store_instance('naive_test_instance')

    ctl = Control()
    # Load instance from file
    ctl.load("asp/instances/naive_test_instance.lp")
    # Load encoding from file
    ctl.load("asp/encodings/straight_line_naive_encoding.lp")
    # Ground the program
    ctl.ground()
    # ctl.configuration.solve.models = 5
    result = ctl.solve(on_model=on_model)

    print(result)

    render = True

    if render:
        env_renderer = RenderTool(
            env, agent_render_variant=AgentRenderVariant.AGENT_SHOWS_OPTIONS)

        try:
            simulate_environment(env, env_renderer)
            env_renderer.render_env(
                show=True, show_predictions=True, show_rowcols=True)
        except Exception as e:
            print(
                f"An exception occured which would otherwise have closed the rendering window.\n\n{e}\n")

        input("Press key to close...")
        env_renderer.close_window()
