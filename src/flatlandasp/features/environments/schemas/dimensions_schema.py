from pydantic import BaseModel


class Dimensions(BaseModel):
    width: int
    height: int
