class CharacterNameAndId:
    def __init__(self, id: int, name: str):
        """Initialize a CharacterNameAndId instance."""
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        """Return the character ID."""
        return self._id

    @property
    def name(self) -> str:
        """Return the character name."""
        return self._name
