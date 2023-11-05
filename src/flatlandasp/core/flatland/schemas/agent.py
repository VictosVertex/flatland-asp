from flatlandasp.core.flatland.schemas.orientation import Orientation
from flatlandasp.core.flatland.schemas.position import Position
from pydantic import BaseModel


class Agent(BaseModel):
    """ Representation of a train."""
    id: int
    """ Unique identifier of the agent."""
    position: Position
    """ Current position of the agent."""
    orientation: Orientation
    """ Current orientation of the agent."""
    target: Position
    """ Position of the train station the agent needs to travel to."""
