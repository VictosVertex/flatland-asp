from flatlandasp.core.flatland.schemas.cell_type import CellType
from flatlandasp.core.flatland.schemas.orientation import Orientation
from flatlandasp.core.flatland.schemas.position import Position
from pydantic import BaseModel


class Cell(BaseModel):
    """ Building block of the 2D-Grid-Environment of Flatland"""
    type: CellType
    """ Type of cell like empty or tracks like straight, simple switch and others."""
    position: Position
    """ Position of the cell within the grid."""
    orientation: Orientation
    """ Orientation of the cell. 
    
        (Default of every cell is north).
    """
