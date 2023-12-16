import inspect

from flatland.envs.rail_env import RailEnv
from flatlandasp.core.flatland.schemas.orientation import Orientation
from flatlandasp.core.log_config import get_logger

logger = get_logger()


def schedule_header() -> list[str]:
    """ Get header describing how schedules are defined."""
    return inspect.cleandoc(
        f"""% Schedules are defined as
            %   schedule(ID,S,T,O,D).
            %  
            %   - ID: identifier of the agent
            %   - S: Start position in the form (X,Y) (Flatland style)
            %   - T: Target position in the form (X,Y) (Flatland style)
            %   - O: Initial orientation of the agent
            %   - D: Earliest departure of the agent
        """
    ).splitlines()


def schedule_literal(agent) -> str:
    """ Get agent schedule as ASP literal.

        Form of the literal:
            schedule(ID,S,T,O,D).

            - ID: identifier of the agent
            - S: Start position in the form (X,Y) (Flatland style)
            - T: Target position in the form (X,Y) (Flatland style)
            - O: Initial orientation of the agent
            - D: Earliest departure of the agent
    """
    return (f"schedule("
            f"{agent.handle}"
            f",({agent.initial_position[0]},{agent.initial_position[1]})"
            f",({agent.target[0]},{agent.target[1]})"
            f",{agent.direction}"
            f",{agent.earliest_departure}"
            f").")


def cell_header() -> list[str]:
    """ Get header describing how cells are defined."""
    return inspect.cleandoc(
        f"""% Cells are defined as
            %   cell(P,O,D).
            %  
            %   - P: Position of the cell in the form (X,Y) (Flatland style)
            %   - O: Orientation of the agent
            %   - D: Set of possible directions
        """
    ).splitlines()


def cell_literal(x: int, y: int,
                 agent_orientation: Orientation,
                 directions: list[Orientation]) -> str:
    """ Get cell description as ASP literal.

        Form of the literal:
            cell(P,O,D).

            - P: Position of the cell in the form (X,Y) (Flatland style)
            - O: Orientation of the agent
            - D: Set of possible directions
    """
    return (f"cell("
            f"({x},{y})"
            f",{agent_orientation.value}"
            f",({';'.join([str(direction.value) for direction in directions])})).")


def delta_header() -> list[str]:
    """ Get header describing how deltas are defined."""
    return inspect.cleandoc(
        f"""% Deltas describing coordinate changes induced by movement.
            %   delta(D,C).
            %  
            %   - D: Direction of movement
            %   - C: Coordinate change in the form (X,Y) (Flatland style)
        """
    ).splitlines()


def delta_literals():
    """ Get delta description as an ASP literal.
        Form of the literal:
            delta(D,C).

            - D: Direction of movement
            - C: Coordinate change in the form (X,Y) (Flatland style)
    """
    return ["delta(0,(-1,0)). % North",
            "delta(1,(0,1)).  % East",
            "delta(2,(1,0)).  % South",
            "delta(3,(0,-1)). % West",]


def generate_instance_lines(env: RailEnv, limit: int) -> list[str]:
    """ Generate ASP instance lines from Flatland environment."""

    if (env.rail is None):
        return []

    logger.info("Generating ASP instance.")

    schedules = [schedule_literal(agent) for agent in env.agents]

    logger.info(f"Schedule literals ({len(schedules)}) done.")

    cells = []
    for y, row in enumerate(env.rail.grid):
        for x, cell in enumerate(row):
            if not cell:
                continue

            for i in range(4):
                facing_direction = (cell >> (12-4*i)) & 0xF

                valid_directions = []

                for j in range(4):
                    valid = (facing_direction >> (3 - j)) & 0xb1

                    if valid:
                        valid_directions.append(Orientation(j))

                # Create cell with Flatland style coordinates
                # In Flatland Y goes to the right and X goes down
                if len(valid_directions) > 0:
                    cells.append(cell_literal(
                        y, x, Orientation(i), valid_directions))

    logger.info(f"Cell literals ({len(cells)}) done.")

    limit_literal = f"limit({limit})."

    return [limit_literal,
            *schedule_header(),
            *schedules,
            *cell_header(),
            *cells,
            *delta_header(),
            *delta_literals()]
