from abc import ABC, abstractmethod

class MessageCallback(ABC):
    
    @abstractmethod
    def drop_message(self, message: str) -> None:
        pass
