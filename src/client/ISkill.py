from abc import ABC, abstractmethod
from typing import Any


class ISkill(ABC):

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_effect(self, level: int) -> Any: 
        pass

    @abstractmethod
    def get_max_level(self) -> int:
        pass

    @abstractmethod
    def get_animation_time(self) -> int:
        pass

    @abstractmethod
    def can_be_learned_by(self, job: 'MapleJob') -> bool:
        pass

    @abstractmethod
    def is_fourth_job(self) -> bool:
        pass

    @abstractmethod
    def is_beginner_skill(self) -> bool:
        pass

    @abstractmethod
    def is_gm_skill(self) -> bool:
        pass

    @abstractmethod
    def get_element(self) -> 'Element':
        pass
