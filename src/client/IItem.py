from abc import ABC, abstractmethod

class IItem(ABC):
    ITEM = 2
    EQUIP = 1

    @abstractmethod
    def get_type(self) -> byte:
        """Return the type of the item."""
        pass

    @abstractmethod
    def get_position(self) -> byte:
        """Return the position of the item."""
        pass

    @abstractmethod
    def get_item_id(self) -> int:
        """Return the item ID."""
        pass

    @abstractmethod
    def get_pet_id(self) -> int:
        """Return the pet ID associated with the item."""
        pass

    @abstractmethod
    def get_quantity(self) -> int:
        """Return the quantity of the item."""
        pass

    @abstractmethod
    def get_owner(self) -> str:
        """Return the owner of the item."""
        pass

    @abstractmethod
    def copy(self) -> 'IItem':
        """Return a copy of the item."""
        pass

    @abstractmethod
    def set_owner(self, owner: str):
        """Set the owner of the item."""
        pass

    @abstractmethod
    def set_position(self, position: byte):
        """Set the position of the item."""
        pass

    @abstractmethod
    def set_quantity(self, quantity: int):
        """Set the quantity of the item."""
        pass
