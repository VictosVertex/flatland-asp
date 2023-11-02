import inspect
from app.core.flatland.mappings import CELL_TYPE_TO_ACTION_MAP
from app.core.flatland.schemas.agent import Agent
from app.core.flatland.schemas.cell import Cell
from app.core.flatland.schemas.cell_type import CellType


class NaiveInstance:
    def get_full_description(self, *, cells: list[Cell], cell_types: list[CellType], agents: list[Agent], include_headers: bool = True) -> list[str]:
        # Get all literals
        cell_literals = [self.get_cell_literal(cell) for cell in cells]

        agent_literals = [self.get_agent_literal(agent) for agent in agents]
        target_literals = [self.get_target_literal_for_agent(
            agent) for agent in agents]
        possible_action_literals = self.get_possible_action_literals(
            cell_types)

        # Get all headers if necessary
        if include_headers:
            cells_header = self.get_cells_header()
            agents_header = self.get_agents_header()
            targets_header = self.get_targets_header()
            possible_actions_header = self.get_possible_actions_header()

        # Combine everything into one description
        if include_headers:
            full_description = [*cells_header,
                                *cell_literals, "",
                                *agents_header,
                                *agent_literals, "",
                                *targets_header,
                                *target_literals, "",
                                *possible_actions_header,
                                *possible_action_literals
                                ]
        else:
            full_description = [*cell_literals, "",
                                *agent_literals, "",
                                *target_literals, "",
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
                %   possible_action(C,O,A).
                %
                %   - C: Type of cell
                %   - O: Orientation of the agent entering the cell
                %   - A: One of the actions the agent can choose
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
        action_maps = []
        for cell_type in cell_types:
            actions = CELL_TYPE_TO_ACTION_MAP[cell_type]

            for agent_orientation, row in enumerate(actions):
                for action in row:
                    possible_action = f"possible_action({cell_type.value}, {agent_orientation}, {action.value})."
                    possible_actions.append(possible_action)
            # (4+i-cell.orientation.value) % 4
        return possible_actions

    def get_agents_header(self) -> list[str]:
        header = inspect.cleandoc(
            f"""% Agents are defined as
                %   agent(I,X,Y,O,T).
                %
                %   - I: Id
                %   - X: X coordinate of position
                %   - Y: Y coordinate of position
                %   - O: Orientation
                %   - T: Time step, default is 0
            """
        ).splitlines()

        return header

    def get_agent_literal(self, agent: Agent) -> str:
        """ Get agent description as an ASP literal.

            Form of the literal:
                agent(I,X,Y,O,T).

                - I: Id
                - X: X coordinate of position
                - Y: Y coordinate of position
                - O: Orientation
                - T: Time step, default is 0
        """
        return f'agent({agent.id},{agent.position.x},{agent.position.y},{agent.orientation.value},0).'

    def get_targets_header(self) -> list[str]:
        header = inspect.cleandoc(
            f"""% Targets are defined as
                %   target(I,X,Y).
                %
                %   - I: Id of the agent
                %   - X: X coordinate of target position
                %   - Y: Y coordinate of target position
            """
        ).splitlines()

        return header

    def get_target_literal_for_agent(self, agent: Agent) -> str:
        """ Get target description of an agent as an ASP literal.

            Form of the literal:
                target(I,X,Y).

                - I: Id of the agent
                - X: x coordinate of target position
                - Y: y coordinate of target position
        """
        return f'target({agent.id},{agent.target.x},{agent.target.y}).'
