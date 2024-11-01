import time
from net.sf.odinms.client.anticheat import CheatingOffense
from net.sf.odinms.client import MapleCharacter

class CheatingOffenseEntry:
    def __init__(self, offense, chrfor):
        self.offense = offense                # Instance of CheatingOffense
        self.count = 0
        self.chrfor = chrfor                  # Instance of MapleCharacter
        self.first_offense = time.time() * 1000  # Convert to milliseconds
        self.last_offense = self.first_offense
        self.param = None
        self.dbid = -1

    def get_offense(self):
        return self.offense

    def get_count(self):
        return self.count

    def get_chrfor(self):
        return self.chrfor

    def increment_count(self):
        self.count += 1
        self.last_offense = time.time() * 1000  # Update to current time in milliseconds

    def is_expired(self):
        # Check if the offense is expired based on validity duration
        return self.last_offense < (time.time() * 1000 - self.offense.validity_duration)

    def get_points(self):
        # Calculate points based on count and offense points
        return self.count * self.offense.points

    def get_param(self):
        return self.param

    def set_param(self, param):
        self.param = param

    def get_last_offense_time(self):
        return self.last_offense

    def get_dbid(self):
        return self.dbid

    def set_dbid(self, dbid):
        self.dbid = dbid

    def __eq__(self, other):
        if not isinstance(other, CheatingOffenseEntry):
            return False
        return (
            self.chrfor.get_id() == other.chrfor.get_id() and
            self.offense == other.offense and
            self.first_offense == other.first_offense
        )

    def __hash__(self):
        # Use chrfor ID, offense hash, and first_offense to generate hash
        prime = 31
        result = 1
        result = prime * result + (self.chrfor.get_id() if self.chrfor else 0)
        result = prime * result + hash(self.offense)
        result = prime * result + hash(self.first_offense)
        return result
