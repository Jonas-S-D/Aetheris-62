from enum import Enum

class CheatingOffense(Enum):
    FASTATTACK = (1, 60000, 300)
    MOVE_MONSTERS = (1, 60000, -1)
    TUBI = (1, 60000, -1)
    FAST_HP_REGEN = (1, 60000, -1)
    FAST_MP_REGEN = (1, 60000, 500)
    SAME_DAMAGE = (10, 300000, 20)
    ATTACK_WITHOUT_GETTING_HIT = (1, 60000, -1)
    HIGH_DAMAGE = (10, 300000)
    ATTACK_FARAWAY_MONSTER = (5, 60000, -1)
    REGEN_HIGH_HP = (50, 60000, -1)
    REGEN_HIGH_MP = (50, 60000, -1)
    ITEMVAC = (5, 60000, -1)
    SHORT_ITEMVAC = (2, 60000, -1)
    USING_FARAWAY_PORTAL = (30, 300000, -1)
    FAST_TAKE_DAMAGE = (1, 60000, -1)
    FAST_MOVE = (1, 60000, -1)
    HIGH_JUMP = (1, 60000, -1)
    MISMATCHING_BULLETCOUNT = (50, 60000, -1)
    ETC_EXPLOSION = (50, 300000, -1)
    FAST_SUMMON_ATTACK = (1, 60000, -1)
    ATTACKING_WHILE_DEAD = (10, 300000, -1)
    USING_UNAVAILABLE_ITEM = (10, 300000, -1)
    FAMING_SELF = (10, 300000, -1)
    FAMING_UNDER_15 = (10, 300000, -1)
    EXPLODING_NONEXISTANT = (1, 60000, -1)
    SUMMON_HACK = (1, 60000, -1)
    HEAL_ATTACKING_UNDEAD = (1, 60000, 5)
    COOLDOWN_HACK = (10, 300000, 10)

    def __init__(self, points=1, validity_duration=60000, autobancount=-1):
        self._points = points
        self._validity_duration = validity_duration
        self._autobancount = autobancount
        self._enabled = True

    @property
    def points(self):
        return self._points

    @property
    def validity_duration(self):
        return self._validity_duration

    @property
    def autobancount(self):
        return self._autobancount

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    def should_autoban(self, count):
        if self.autobancount == -1:
            return False
        return count > self.autobancount
