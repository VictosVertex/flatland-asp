from enum import Enum


class Action(Enum):
    """ Action space of an agent."""
    NO_OP = 0
    """ The agent continues the previous action."""
    TURN_LEFT = 1
    """ The agent decides to turn left at a switch and moves to the next cell.
    
        Results in orientation of the agent decreasing by 1.
    """
    FORWARD = 2
    """ The agent continues to move to the next cell.
    
        Special cases:
            - Simple turns change the orientation of the agent
            - Dead ends result in the agent turning around
    """

    TURN_RIGHT = 3
    """ The agent decides to turn right at a switch and moves to the next cell.
    
        Results in orientation of the agent increasing by 1.
    """
    HALT = 4
    """ The agent stops all movement and keeps the same position and orientation."""
