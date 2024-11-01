from abc import ABC, abstractmethod
from client.maple_client import MapleClient

class Command(ABC):
    @abstractmethod
    def get_definition(self):
        """Method to return command definitions."""
        pass

    @abstractmethod
    def execute(self, c: MapleClient, mc, splitted_line):
        """Method to execute the command."""
        pass