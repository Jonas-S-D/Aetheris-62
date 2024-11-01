from enum import Enum, unique

@unique
class MapleJob(Enum):
    BEGINNER = 0
    WARRIOR = 100
    FIGHTER = 110
    CRUSADER = 111
    HERO = 112
    PAGE = 120
    WHITE_KNIGHT = 121
    PALADIN = 122
    SPEARMAN = 130
    DRAGON_KNIGHT = 131
    DARK_KNIGHT = 132
    MAGICIAN = 200
    FP_WIZARD = 210
    FP_MAGE = 211
    FP_ARCHMAGE = 212
    IL_WIZARD = 220
    IL_MAGE = 221
    IL_ARCHMAGE = 222
    CLERIC = 230
    PRIEST = 231
    BISHOP = 232
    BOWMAN = 300
    HUNTER = 310
    RANGER = 311
    BOWMASTER = 312
    CROSSBOWMAN = 320
    SNIPER = 321
    CROSSBOWMASTER = 322
    THIEF = 400
    ASSASSIN = 410
    HERMIT = 411
    NIGHTLORD = 412
    BANDIT = 420
    CHIEFBANDIT = 421
    SHADOWER = 422
    PIRATE = 500
    BRAWLER = 510
    MARAUDER = 511
    BUCCANEER = 512
    GUNSLINGER = 520
    OUTLAW = 521
    CORSAIR = 522
    GM = 900
    SUPER_GM = 910

    @property
    def job_id(self):
        """Return the job ID."""
        return self.value

    @classmethod
    def get_by_id(cls, job_id: int):
        """Return the MapleJob corresponding to the job ID, or None if not found."""
        for job in cls:
            if job.job_id == job_id:
                return job
        return None

    @classmethod
    def get_by_5_byte_encoding(cls, encoded: int):
        """Return the MapleJob corresponding to the 5-byte encoding."""
        encoding_map = {
            2: cls.WARRIOR,
            4: cls.MAGICIAN,
            8: cls.BOWMAN,
            16: cls.THIEF,
            32: cls.PIRATE
        }
        return encoding_map.get(encoded, cls.BEGINNER)

    def is_a(self, base_job):
        """Check if this job is of the specified base job."""
        return self.job_id >= base_job.job_id and self.job_id // 100 == base_job.job_id // 100

    @staticmethod
    def get_job_name(job_id: int) -> str:
        """Return the name of the job based on its ID."""
        job_names = {
            0: "Beginner",
            100: "Warrior",
            110: "Fighter",
            111: "Crusader",
            112: "Hero",
            120: "Page",
            121: "White Knight",
            122: "Paladin",
            130: "Spearman",
            131: "Dragon Knight",
            132: "Dark Knight",
            200: "Magician",
            210: "Fire/Poison Wizard",
            211: "Fire/Poison Mage",
            212: "Fire/Poison Archmage",
            220: "Ice/Lightning Wizard",
            221: "Ice/Lightning Mage",
            222: "Ice/Lightning Archmage",
            230: "Cleric",
            231: "Priest",
            232: "Bishop",
            300: "Bowman",
            310: "Hunter",
            320: "Crossbowman",
            311: "Ranger",
            321: "Sniper",
            312: "Bowmaster",
            322: "Marksman",
            400: "Thief",
            410: "Assassin",
            420: "Bandit",
            411: "Hermit",
            421: "Bandit",
            412: "Night Lord",
            422: "Shadower",
            500: "Pirate",
            510: "Brawler",
            511: "Marauder",
            512: "Buccaneer",
            520: "Gunslinger",
            521: "Outlaw",
            522: "Corsair",
            900: "GM",
            910: "Super GM"
        }
        return job_names.get(job_id, "")
