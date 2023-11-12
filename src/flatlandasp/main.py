import base64
import io
import logging
import sys
import time
from functools import lru_cache

import uvicorn
from clingo.control import Control
from fastapi import FastAPI, Request, status
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import rail_from_grid_transition_map
from flatland.utils.rendertools import AgentRenderVariant, RenderTool
from PIL import Image

from flatlandasp import FlatlandASP
from flatlandasp.core.flatland.static_maps import (multi_passing_siding_map,
                                                   simple_switch_map)

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="title", version="0.01")
templates = Jinja2Templates(directory="templates")


def create_environment() -> RailEnv:
    # grid_transition_map, optionals = straight_map(
    #    length=5, padding=3)
    grid_transition_map, optionals = simple_switch_map()
    # grid_transition_map, optionals = multi_passing_siding_map()
    env = RailEnv(width=grid_transition_map.grid.shape[1],
                  height=grid_transition_map.grid.shape[0],
                  rail_generator=rail_from_grid_transition_map(
                      grid_transition_map, optionals),
                  line_generator=sparse_line_generator(),
                  number_of_agents=2,
                  obs_builder_object=GlobalObsForRailEnv()
                  )

    return env


@lru_cache
def get_fa():
    env = create_environment()
    env_renderer = RenderTool(
        env, agent_render_variant=AgentRenderVariant.AGENT_SHOWS_OPTIONS)
    ctl = Control(["10"])

    fa = FlatlandASP(env=env, env_renderer=env_renderer, clingo_control=ctl)
    return fa


@app.get("/{step}")
def step(step: int, request: Request):
    fa = get_fa()
    image_bytes = fa.get_image_bytes_at_simulation_step(step)
    return templates.TemplateResponse("test.html",  context={"request": request, "img": image_bytes})


@app.get("/")
def test(request: Request):
    fa = get_fa()
    fa.solve()
    print(fa.clingo_control.statistics)
    fa.simulate_environment()
    image_bytes = fa.get_image_bytes_at_simulation_step(0)
    return templates.TemplateResponse("test.html",  context={"request": request, "img": image_bytes})


def main():
    uvicorn.run("flatlandasp.main:app", host='0.0.0.0',
                port=8000, reload=True)


if __name__ == "__main__":
    main()
