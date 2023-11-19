class RailsNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Rails not found.\nMake sure rails are added to the environment.")
