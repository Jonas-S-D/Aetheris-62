from abc import ABC, abstractmethod

class CommandProcessorMBean(ABC):
    
    @abstractmethod
    def process_command_jmx(self, cserver: int, mapid: int, command: str) -> str:
        pass