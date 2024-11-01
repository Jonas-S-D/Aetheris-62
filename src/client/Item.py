from abc import ABC, abstractmethod

class IItem(ABC):
    ITEM = 1

    @abstractmethod
    def getItemId(self):
        pass

    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def getQuantity(self):
        pass

    @abstractmethod
    def getType(self):
        pass

    @abstractmethod
    def getOwner(self):
        pass

    @abstractmethod
    def getPetId(self):
        pass

    @abstractmethod
    def compareTo(self, other):
        pass


class Item(IItem):
    def __init__(self, id: int, position: int, quantity: int, petid: int = -1):
        self.id = id
        self.position = position
        self.quantity = quantity
        self.petid = petid
        self.owner = ""

    def copy(self) -> 'Item':
        ret = Item(self.id, self.position, self.quantity, self.petid)
        ret.owner = self.owner
        return ret

    def setPosition(self, position: int):
        self.position = position

    def setQuantity(self, quantity: int):
        self.quantity = quantity

    def getItemId(self) -> int:
        return self.id

    def getPosition(self) -> int:
        return self.position

    def getQuantity(self) -> int:
        return self.quantity

    def getType(self) -> int:
        return IItem.ITEM

    def getOwner(self) -> str:
        return self.owner

    def setOwner(self, owner: str):
        self.owner = owner

    def getPetId(self) -> int:
        return self.petid

    def compareTo(self, other: 'IItem') -> int:
        if abs(self.position) < abs(other.getPosition()):
            return -1
        elif abs(self.position) == abs(other.getPosition()):
            return 0
        else:
            return 1

    def __str__(self) -> str:
        return f"Item: {self.id} quantity: {self.quantity}"
