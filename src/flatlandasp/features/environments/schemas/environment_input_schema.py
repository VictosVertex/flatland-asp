from typing import Optional

from flatlandasp.core.flatland.schemas.cell import Cell
from flatlandasp.core.flatland.schemas.unit import Unit
from flatlandasp.features.environments.schemas.dimensions_schema import Dimensions
from pydantic import BaseModel


class EnvironmentInput(BaseModel):
    dimensions: Dimensions
    cells: list[Cell]
    stations: list[Unit]
    agents: Optional[list[Unit]]
