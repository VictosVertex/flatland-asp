from flatlandasp.core.flatland.schemas.cell_type import CellType
from flatlandasp.core.flatland.schemas.unit import Unit


class Cell(Unit):
    """ Building block of the 2D-Grid-Environment of Flatland"""
    type: CellType
    """ Type of cell like empty or tracks like straight, simple switch and others."""
