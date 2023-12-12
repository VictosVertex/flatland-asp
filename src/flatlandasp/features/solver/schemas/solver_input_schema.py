from typing import Optional

from pydantic import BaseModel


class SolverInput(BaseModel):
    environment_name: str
    encoding_name: str
    number_of_agents: Optional[int] = None
    step_limit: int = 20
