from enum import Enum, unique

@unique
class MapleStat(Enum):
    SKIN = 0x1
    FACE = 0x2
    HAIR = 0x4
    LEVEL = 0x10
    JOB = 0x20
    STR = 0x40
    DEX = 0x80
    INT = 0x100
    LUK = 0x200
    HP = 0x400
    MAXHP = 0x800
    MP = 0x1000
    MAXMP = 0x2000
    AVAILABLEAP = 0x4000
    AVAILABLESP = 0x8000
    EXP = 0x10000
    FAME = 0x20000
    MESO = 0x40000
    PET = 0x180008

    def get_value(self) -> int:
        """Return the integer value of the enum."""
        return self.value

    @classmethod
    def get_by_value(cls, value: int):
        """Return the enum member corresponding to the given value, or None if not found."""
        for stat in cls:
            if stat.value == value:
                return stat
        return None
