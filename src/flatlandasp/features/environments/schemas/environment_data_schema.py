import numpy as np
from pydantic import BaseModel, validator

CITY_POSITIONS_TYPE = list[tuple[int, int]]
""" Type for city positions in optionals parameter.

    Example:
        [(0,2),(10,1)]
"""
TRAIN_STATIONS_TYPE = list[list[tuple[tuple[int, int], int]]]
""" Type for train stations in optionals parameter.

    Example:
        [[((0,2),0)],[((10,1),0)]]
"""
CITY_ORIENTATIONS_TYPE = list[int]
""" Type for city orientations in optionals parameter."""


class EnvironmentData(BaseModel):
    """ Holds data required for creating a specific environment."""
    grid: list[list[int]]
    """ Environment grid in form of a numpy array."""
    optionals: dict[
        str,
        dict[
            str,
            CITY_POSITIONS_TYPE |
            TRAIN_STATIONS_TYPE |
            CITY_ORIENTATIONS_TYPE
        ]
    ]
    """ Optional parameters such as agent hints containing cities and stations."""
    number_of_agents: int
    """ Number of agents in the environment."""

    @validator('grid')
    def grid_to_numpy_array(cls, v: list):
        """ Convert given list to actual numpy array.

            Since pydantic doesn't natively work with numpy arrays,
            grid still can't use proper type hints
        """
        return np.array(v)
