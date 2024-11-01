from abc import ABC, abstractmethod

class ChannelServerMBean(ABC):

    @abstractmethod
    def shutdown(self, time: int) -> None:
        """Shut down the server after a specified time."""
        pass

    @abstractmethod
    def shutdown_world(self, time: int) -> None:
        """Shut down the world server after a specified time."""
        pass

    @abstractmethod
    def get_server_message(self) -> str:
        """Get the current server message."""
        pass

    @abstractmethod
    def set_server_message(self, new_message: str) -> None:
        """Set a new server message."""
        pass

    @abstractmethod
    def get_channel(self) -> int:
        """Get the channel number."""
        pass

    @abstractmethod
    def get_exp_rate(self) -> int:
        """Get the experience rate."""
        pass

    @abstractmethod
    def get_meso_rate(self) -> int:
        """Get the meso rate."""
        pass

    @abstractmethod
    def get_drop_rate(self) -> int:
        """Get the drop rate."""
        pass

    @abstractmethod
    def get_boss_drop_rate(self) -> int:
        """Get the boss drop rate."""
        pass

    @abstractmethod
    def get_pet_exp_rate(self) -> int:
        """Get the pet experience rate."""
        pass

    @abstractmethod
    def set_exp_rate(self, exp_rate: int) -> None:
        """Set the experience rate."""
        pass

    @abstractmethod
    def set_meso_rate(self, meso_rate: int) -> None:
        """Set the meso rate."""
        pass

    @abstractmethod
    def set_drop_rate(self, drop_rate: int) -> None:
        """Set the drop rate."""
        pass

    @abstractmethod
    def set_boss_drop_rate(self, boss_drop_rate: int) -> None:
        """Set the boss drop rate."""
        pass

    @abstractmethod
    def set_pet_exp_rate(self, pet_exp_rate: int) -> None:
        """Set the pet experience rate."""
        pass

    @abstractmethod
    def get_connected_clients(self) -> int:
        """Get the number of connected clients."""
        pass

    @abstractmethod
    def get_loaded_maps(self) -> int:
        """Get the number of loaded maps."""
        pass
