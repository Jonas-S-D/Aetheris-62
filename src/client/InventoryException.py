class InventoryException(Exception):
    """Custom exception for inventory-related errors."""
    
    def __init__(self, message: str = ""):
        super().__init__(message)
