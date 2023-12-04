from flatlandasp.core.flatland.schemas.orientation import Orientation
from flatlandasp.core.flatland.schemas.position import Position
from pydantic import BaseModel


class Unit(BaseModel):
    position: Position
    """ Current position of this unit."""
    orientation: Orientation
    """ Current orientation of this unit."""
