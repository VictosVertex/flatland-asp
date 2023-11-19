import inspect

from flatlandasp.core.flatland.mappings import CELL_TYPE_TO_ACTION_MAP
from flatlandasp.core.flatland.schemas.action import Action
from flatlandasp.core.flatland.schemas.agent import Agent
from flatlandasp.core.flatland.schemas.cell import Cell
from flatlandasp.core.flatland.schemas.cell_type import CellType
from flatlandasp.core.flatland.schemas.orientation import OrientationChange


class BaseInstance:
    def get_full_description(self, *,
                             cells: list[Cell],
                             cell_types: list[CellType],
                             agents: list[Agent],
                             include_headers: bool = True) -> list[str]:
        """ Get full ASP instance description."""

        cell_literals = [self.get_cell_literal(cell) for cell in cells]

        agent_literals = [
            self.get_agent_literal(agent) for agent in agents]
        agent_target_literals = [self.get_agent_target_literal(
            agent) for agent in agents]
        possible_action_literals = self.get_possible_action_literals(
            cell_types)

        # Get all headers if necessary
        if include_headers:
            cells_header = self.get_cells_header()
            agents_header = self.get_agents_header()
            possible_actions_header = self.get_possible_actions_header()

            full_description = [*cells_header,
                                *cell_literals, "",
                                *agents_header,
                                *agent_literals,
                                *agent_target_literals, "",
                                *possible_actions_header,
                                *possible_action_literals
                                ]
        else:
            full_description = [*cell_literals, "",
                                *agent_literals, "",
                                *agent_target_literals, "",
                                *possible_action_literals
                                ]

        return full_description

    def get_cells_header(self) -> list[str]:
        """ Get header describing how cells are defined."""
        return inspect.cleandoc(
            f"""% Cells are defined as
                %   cell(X,Y,C,O).
                %  
                %   - X: X coordinate of position
                %   - Y: Y coordinate of position
                %   - C: Type of the cell
                %   - O: Orientation
            """
        ).splitlines()

    def get_cell_literal(self, cell: Cell) -> str:
        """ Get cell description as an ASP literal.

            Form of the literal:
                cell(X,Y,C,O).

                - X: X coordinate of position
                - Y: Y coordinate of position
                - C: Type of the cell
                - O: Orientation
        """
        x = cell.position.x
        y = cell.position.y
        cell_type = cell.type.value
        orientation = cell.orientation.value
        return f'cell({x},{y},{cell_type},{orientation}).'

    def get_possible_actions_header(self) -> list[str]:
        """ Get header describing how possible actions are defined."""
        return inspect.cleandoc(
            f"""% Possible actions an agent can take in each cell are defined as
                %   possible_action(C,O,A,OC).
                %
                %   - C: Type of cell
                %   - O: Orientation of the agent entering the cell
                %   - A: One of the actions the agent can choose
                %   - OC: Change in orientation of the agent after taking action A
            """
        ).splitlines()

    def get_possible_action_literals(self, cell_types: list[CellType]) -> list[str]:
        """ Get all possible action descriptions for all cells as ASP literals.

            Form of the literal:
                possible_action(C,O,A).

                - C: Type of cell
                - O: Orientation of the agent entering the cell
                - A: One of the actions the agent can choose
                - OC: Change in orientation of the agent after taking action A
        """

        return [
            (f'possible_action({cell_type.value}'
             f',{agent_orientation}'
             f',{action[0].value}'
             f',{action[1].value}).')
            for cell_type in cell_types
            for agent_orientation, row in enumerate(CELL_TYPE_TO_ACTION_MAP[cell_type])
            # Halting is always possible
            # for now we add it like this for every cell
            for action in [*row, (Action.HALT, OrientationChange.KEEP)]
        ]

    def get_agents_header(self) -> list[str]:
        return inspect.cleandoc(
            f"""% Agent's initial values are defined in three literals
                %   agent(I,X,Y,O,D).
                %
                %   - I: Id
                %   - X: X coordinate of position
                %   - Y: Y coordinate of position
                %   - O: Orientation
                %   - D: Earliest departure
                %
                %   agent_target(I,X,Y).
                %
                %   - I: Id of the agent
                %   - X: X coordinate of target position
                %   - Y: Y coordinate of target position
            """
        ).splitlines()

    def get_agent_literal(self, agent: Agent) -> str:
        """ Get agent description as an ASP literal.

            Form of the literal:
                agent(I,X,Y,T).

                - I: Id
                - X: X coordinate of position
                - Y: Y coordinate of position
                - O: Orientation
                - D: Earliest departure
        """
        return (f'agent({agent.id}'
                f',{agent.position.x}'
                f',{agent.position.y}'
                f',{agent.orientation.value}'
                f',{agent.earliest_departure}).')

    def get_agent_target_literal(self, agent: Agent) -> str:
        """ Get target description of an agent as an ASP literal.

            Form of the literal:
                agent_target(I,X,Y).

                - I: Id of the agent
                - X: x coordinate of target position
                - Y: y coordinate of target position
        """
        return f'agent_target({agent.id},{agent.target.x},{agent.target.y}).'
