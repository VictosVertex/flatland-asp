from flatlandasp.core.flatland.schemas.position import Position
from flatlandasp.core.flatland.schemas.unit import Unit


class Agent(Unit):
    """ Representation of a train."""
    id: int
    """ Unique identifier of the agent."""
    target: Position
    """ Position of the train station the agent needs to travel to."""
    earliest_departure: int
    """ Earliest time step at which the agent departs"""
