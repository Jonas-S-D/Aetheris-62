from typing import Collection

class InventoryContainer:
    def all_inventories(self) -> Collection['MapleInventory']:
        raise NotImplementedError("This method should be implemented by subclasses.")
