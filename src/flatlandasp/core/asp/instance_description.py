from typing import Protocol
from flatlandasp.core.flatland.schemas.agent import Agent
from flatlandasp.core.flatland.schemas.cell import Cell
from flatlandasp.core.flatland.schemas.cell_type import CellType


class InstanceDescription(Protocol):
    def get_full_description(self, *, cells: list[Cell], cell_types: list[CellType], agents: list[Agent]) -> list[str]:
        ...
