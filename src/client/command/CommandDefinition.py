class CommandDefinition:
    def __init__(self, command: str, required_level: int):
        self.command = command
        self.required_level = required_level

    def get_command(self) -> str:
        return self.command

    def get_required_level(self) -> int:
        return self.required_level