from concurrent.futures import Future
from typing import Dict, Optional
from tools.array_map import ArrayMap
from client.iskill import ISkill 
from client.monster_status import MonsterStatus

class MonsterStatusEffect:
    def __init__(self, stati: Dict[MonsterStatus, int], skill: ISkill, monsterSkill: bool) -> None:
        self.stati = ArrayMap(stati)
        self.skill = skill
        self.monsterSkill = monsterSkill
        self.cancelTask: Optional[Future] = None
        self.poisonSchedule: Optional[Future] = None

    def getStati(self) -> Dict[MonsterStatus, int]:
        return self.stati
    
    def setValue(self, status: MonsterStatus, newVal: int) -> Optional[int]:
        return self.stati.put(status, newVal)
    
    def getSkill(self) -> ISkill:
        return self.skill
    
    def isMonsterSkill(self) -> bool:
        return self.monsterSkill
    
    def getCancelTask(self) -> Optional[Future]:
        return self.cancelTask
    
    def setCancelTask(self, cancelTask: Future) -> None:
        self.cancelTask = cancelTask

    def removeActiveStatus(self, stat: MonsterStatus) -> None:
        self.stati.remove(stat)

    def setPoisonSchedule(self, poisonSchedule: Future) -> None:
        self.poisonSchedule = poisonSchedule

    def cancelPoisonSchedule(self) -> None:
        if self.poisonSchedule is not None:
            self.poisonSchedule.cancel()