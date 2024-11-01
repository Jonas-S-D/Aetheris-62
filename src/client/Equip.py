from Item import Item
from IEquip import IEquip

class Equip(Item, IEquip):
    def __init__(self, id: int, position: int):
        super().__init__(id, position, 1)
        self.ringid = -1

    def __init__(self, id: int, position: int, ringid: int):
        super().__init__(id, position, 1)
        self.ringid = ringid

    def copy(self) -> 'Equip':
        ret = Equip(self.getItemId(), self.getPosition(), self.ringid)
        ret.str = self.str
        ret.dex = self.dex
        ret._int = self._int
        ret.luk = self.luk
        ret.hp = self.hp
        ret.mp = self.mp
        ret.matk = self.matk
        ret.mdef = self.mdef
        ret.watk = self.watk
        ret.wdef = self.wdef
        ret.acc = self.acc
        ret.avoid = self.avoid
        ret.hands = self.hands
        ret.speed = self.speed
        ret.jump = self.jump
        ret.locked = self.locked
        ret.upgradeSlots = self.upgradeSlots
        ret.level = self.level
        ret.setOwner(self.getOwner())
        ret.setQuantity(self.getQuantity())
        return ret
    
    def getType(self) -> int:
        return IEquip.EQUIP
    
    def getUpgradeSlots(self) -> int:
        return self.upgradeSlots
    
    def getLocked(self) -> int:
        return self.locked
    
    def getRingId(self) -> int:
        return self.ringid
    
    def getStr(self) -> int:
        return self.str
    
    def getDex(self) -> int:
        return self.dex
    
    def getInt(self) -> int:
        return self._int
    
    def getLuk(self) -> int:
        return self.luk
    
    def getHp(self) -> int:
        return self.hp
    
    def getMp(self) -> int:
        return self.mp
    
    def getWatk(self) -> int:
        return self.watk
    
    def getMatk(self) -> int:
        return self.matk
    
    def getWdef(self) -> int:
        return self.wdef
    
    def getMdef(self) -> int:
        return self.mdef
    
    def getAcc(self) -> int:
        return self.acc
    
    def getAvoid(self) -> int:
        return self.avoid
    
    def getHands(self) -> int:
        return self.hands
    
    def getSpeed(self) -> int:
        return self.speed
    
    def getJump(self) -> int:
        return self.jump
    
    def getJob(self) -> MapleJob:
        return self.job
    
    def setStr(self, str: int):
        self.str = str

    def setDex(self, dex: int):
        self.dex = dex

    def setInt(self, _int: int):
        self._int = _int

    def setLuk(self, luk: int):
        self.luk = luk

    def setHp(self, hp: int):
        self.hp = hp

    def setMp(self, mp: int):
        self.mp = mp

    def setWatk(self, watk: int):
        self.watk = watk

    def setMatk(self, matk: int):
        self.matk = matk

    def setWdef(self, wdef: int):
        self.wdef = wdef

    def setMdef(self, mdef: int):
        self.mdef = mdef

    def setAcc(self, acc: int):
        self.acc = acc

    def setAvoid(self, avoid: int):
        self.avoid = avoid

    def setHands(self, hands: int):
        self.hands = hands

    def setSpeed(self, speed: int):
        self.speed = speed

    def setJump(self, jump: int):
        self.jump = jump

    def setLocked(self, locked: int):
        self.locked = locked

    def setUpgradeSlots(self, upgradeSlots: int):
        self.upgradeSlots = upgradeSlots

    def getLevel(self) -> int:
        return self.level
    
    def setLevel(self, level: int):
        self.level = level

    def setJob(self, job: MapleJob):
        self.job = job

    def setRingId(self, ringId: int):
        self.ringid = ringId

    def setQuantity(self, quantity: int):
        if quantity < 0 or quantity > 1:
            raise Exception("Setting the quantity to " + quantity + " on an equip (itemid: " + getItemId() + ")")
        super().setQuantity(quantity)