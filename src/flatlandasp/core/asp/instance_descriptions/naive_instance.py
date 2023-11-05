import inspect

from flatlandasp.core.flatland.mappings import CELL_TYPE_TO_ACTION_MAP
from flatlandasp.core.flatland.schemas.action import Action
from flatlandasp.core.flatland.schemas.agent import Agent
from flatlandasp.core.flatland.schemas.cell import Cell
from flatlandasp.core.flatland.schemas.cell_type import CellType
from flatlandasp.core.flatland.schemas.orientation import OrientationChange


class NaiveInstance:
    def get_full_description(self, *, cells: list[Cell], cell_types: list[CellType], agents: list[Agent], include_headers: bool = True) -> list[str]:
        # Get all literals
        cell_literals = [self.get_cell_literal(cell) for cell in cells]

        agent_position_literals = [
            self.get_agent_position_literal(agent) for agent in agents]
        agent_orientation_literals = [
            self.get_agent_orientation_literal(agent) for agent in agents]
        agent_target_literals = [self.get_agent_target_literal(
            agent) for agent in agents]
        possible_action_literals = self.get_possible_action_literals(
            cell_types)

        # Get all headers if necessary
        if include_headers:
            cells_header = self.get_cells_header()
            agents_header = self.get_agents_header()
            possible_actions_header = self.get_possible_actions_header()

        # Combine everything into one description
        if include_headers:
            full_description = [*cells_header,
                                *cell_literals, "",
                                *agents_header,
                                *agent_position_literals,
                                *agent_orientation_literals,
                                *agent_target_literals, "",
                                *possible_actions_header,
                                *possible_action_literals
                                ]
        else:
            full_description = [*cell_literals, "",
                                *agent_position_literals,
                                *agent_orientation_literals, "",
                                *agent_target_literals, "",
                                *possible_action_literals
                                ]

        return full_description

    def get_cells_header(self) -> list[str]:
        header = inspect.cleandoc(
            f"""% Cells are defined as
                %   cell(X,Y,C,O).
                %
                %   - X: X coordinate of position
                %   - Y: Y coordinate of position
                %   - C: Type of the cell
                %   - O: Orientation
            """
        ).splitlines()

        return header

    def get_cell_literal(self, cell: Cell) -> str:
        """ Get cell description as an ASP literal.

            Form of the literal:
                cell(X,Y,C,O).

                - X: X coordinate of position
                - Y: Y coordinate of position
                - C: Type of the cell
                - O: Orientation
        """
        return f'cell({cell.position.x},{cell.position.y},{cell.type.value},{cell.orientation.value}).'

    def get_possible_actions_header(self) -> list[str]:
        header = inspect.cleandoc(
            f"""% Possible actions an agent can take in each cell are defined as
                %   possible_action(C,O,A,OC).
                %
                %   - C: Type of cell
                %   - O: Orientation of the agent entering the cell
                %   - A: One of the actions the agent can choose
                %   - OC: Change in orientation of the agent after taking action A
            """
        ).splitlines()

        return header

    def get_possible_action_literals(self, cell_types: list[CellType]) -> list[str]:
        """ Get all possible action descriptions for all cells as ASP literals.

            Form of the literal:
                possible_action(C,O,A).

                - C: Type of cell
                - O: Orientation of the agent entering the cell
                - A: One of the actions the agent can choose
        """

        possible_actions = []
        for cell_type in cell_types:
            actions = CELL_TYPE_TO_ACTION_MAP[cell_type]

            for agent_orientation, row in enumerate(actions):
                # Halting is always possible
                # for now we add it like this for every cell
                possible_action = f"possible_action({cell_type.value}, {agent_orientation}, {Action.HALT.value}, {OrientationChange.KEEP.value})."
                possible_actions.append(possible_action)

                for action in row:
                    possible_action = f"possible_action({cell_type.value}, {agent_orientation}, {action[0].value}, {action[1].value})."
                    possible_actions.append(possible_action)
        return possible_actions

    def get_agents_header(self) -> list[str]:
        header = inspect.cleandoc(
            f"""% Agents are defined in three literals
                %   agent_position(I,X,Y,T).
                %
                %   - I: Id
                %   - X: X coordinate of position
                %   - Y: Y coordinate of position
                %   - T: Time step, default is 0
                %
                %   agent_orientation(I,O,T).
                %
                %   - I: Id
                %   - O: Orientation
                %   - T: Time step, default is 0
                %   agent_target(I,X,Y).
                %
                %   - I: Id of the agent
                %   - X: X coordinate of target position
                %   - Y: Y coordinate of target position
            """
        ).splitlines()

        return header

    def get_agent_position_literal(self, agent: Agent) -> str:
        """ Get agent position description as an ASP literal.

            Form of the literal:
                agent(I,X,Y,T).

                - I: Id
                - X: X coordinate of position
                - Y: Y coordinate of position
                - T: Time step, default is 0
        """
        return f'agent_position({agent.id},{agent.position.x},{agent.position.y},{agent.earliest_departure}).'

    def get_agent_orientation_literal(self, agent: Agent) -> str:
        """ Get agent orientation description as an ASP literal.

            Form of the literal:
                agent_orientation(I,O,T).

                - I: Id
                - O: Orientation
                - T: Time step, default is 0
        """
        return f'agent_orientation({agent.id},{agent.orientation.value},{agent.earliest_departure}).'

    def get_agent_target_literal(self, agent: Agent) -> str:
        """ Get target description of an agent as an ASP literal.

            Form of the literal:
                target(I,X,Y).

                - I: Id of the agent
                - X: x coordinate of target position
                - Y: y coordinate of target position
        """
        return f'agent_target({agent.id},{agent.target.x},{agent.target.y}).'
