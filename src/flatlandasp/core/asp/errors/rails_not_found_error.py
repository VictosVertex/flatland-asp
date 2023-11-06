class RailsNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Rails not found.\nMake sure rails are added to the environment.")
