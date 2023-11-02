from pydantic import BaseModel


class Position(BaseModel):
    """ Position of an entity or object in the 2D-environment of Flatland."""
    x: int
    """ Horizontal component of the position."""
    y: int
    """ Vertical component of the position."""
