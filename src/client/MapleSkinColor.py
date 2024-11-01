from enum import Enum, unique

@unique
class MapleSkinColor(Enum):
    NORMAL = 0
    DARK = 1
    BLACK = 2
    PALE = 3
    BLUE = 4
    WHITE = 9

    @property
    def id(self):
        """Return the ID of the skin color."""
        return self.value

    @classmethod
    def get_by_id(cls, skin_color_id: int):
        """Return the MapleSkinColor corresponding to the ID, or None if not found."""
        for color in cls:
            if color.id == skin_color_id:
                return color
        return None
