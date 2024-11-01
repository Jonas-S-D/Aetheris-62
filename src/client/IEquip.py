from enum import Enum
from abc import ABC, abstractmethod

class ScrollResult(Enum):
    SUCCESS = 1
    FAIL = 2
    CURSE = 3

class IItem(ABC):
    ITEM = 2
    EQUIP = 1

    @abstractmethod
    def get_type(self) -> int:
        pass

    @abstractmethod
    def get_position(self) -> int:
        pass

    @abstractmethod
    def get_item_id(self) -> int:
        pass

    @abstractmethod
    def get_pet_id(self) -> int:
        pass

    @abstractmethod
    def get_quantity(self) -> int:
        pass

    @abstractmethod
    def get_owner(self) -> str:
        pass

    @abstractmethod
    def copy(self) -> 'IItem':
        pass

    @abstractmethod
    def set_owner(self, owner: str):
        pass

    @abstractmethod
    def set_position(self, position: int):
        pass

    @abstractmethod
    def set_quantity(self, quantity: int):
        pass

class IEquip(IItem):

    @abstractmethod
    def get_upgrade_slots(self) -> int:
        pass

    @abstractmethod
    def get_locked(self) -> int:
        pass

    @abstractmethod
    def get_level(self) -> int:
        pass

    @abstractmethod
    def get_ring_id(self) -> int:
        pass

    @abstractmethod
    def get_str(self) -> int:
        pass

    @abstractmethod
    def get_dex(self) -> int:
        pass

    @abstractmethod
    def get_int(self) -> int:
        pass

    @abstractmethod
    def get_luk(self) -> int:
        pass

    @abstractmethod
    def get_hp(self) -> int:
        pass

    @abstractmethod
    def get_mp(self) -> int:
        pass

    @abstractmethod
    def get_watk(self) -> int:
        pass

    @abstractmethod
    def get_matk(self) -> int:
        pass

    @abstractmethod
    def get_wdef(self) -> int:
        pass

    @abstractmethod
    def get_mdef(self) -> int:
        pass

    @abstractmethod
    def get_acc(self) -> int:
        pass

    @abstractmethod
    def get_avoid(self) -> int:
        pass

    @abstractmethod
    def get_hands(self) -> int:
        pass

    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def get_jump(self) -> int:
        pass
