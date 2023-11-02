class InstanceNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"ASP instance not found.\nHas the instance been generated yet?")
