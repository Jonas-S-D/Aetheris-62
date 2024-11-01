import weakref
import threading
import time
from collections import defaultdict
from enum import Enum


class CheatingOffense(Enum):
    FASTATTACK = "Fast Attack"
    FAST_TAKE_DAMAGE = "Fast Take Damage"
    MOVE_MONSTERS = "Move Monsters"
    FAST_HP_REGEN = "Fast HP Regen"
    FAST_MP_REGEN = "Fast MP Regen"
    FAST_SUMMON_ATTACK = "Fast Summon Attack"
    TUBI = "Tubi"  # Picking up too fast


class CheatTracker:
    def __init__(self, character):
        self.character = weakref.ref(character)
        self.offenses = defaultdict(lambda: {'count': 0, 'last_time': 0})
        self.last_attack_time = time.time()
        self.num_sequential_attacks = 0
        self.regen_hp_since = time.time()
        self.regen_mp_since = time.time()
        self.num_hp_regens = 0
        self.num_mp_regens = 0
        self.attack_without_hit = 0
        self.attack_lock = threading.Lock()
        self.movement_lock = threading.Lock()
        self.invalidation_task = threading.Timer(60, self.invalidate_offenses)
        self.invalidation_task.start()

    def check_attack(self, skill_id):
        with self.attack_lock:
            self.num_sequential_attacks += 1
            current_time = time.time()
            attack_interval = current_time - self.last_attack_time
            self.last_attack_time = current_time

            divisor = 30 if skill_id in {3121004, 5221004} else 300
            if attack_interval * divisor < self.num_sequential_attacks:
                self.register_offense(CheatingOffense.FASTATTACK)
                return False
            return True

    def check_damage(self):
        # Logic to monitor and register if taking damage too quickly
        self.register_offense(CheatingOffense.FAST_TAKE_DAMAGE)

    def check_move_monster(self):
        # Logic to monitor and register monster movement violations
        self.register_offense(CheatingOffense.MOVE_MONSTERS)

    def check_hp_regen(self, healed_hp):
        current_time = time.time()
        if current_time - self.regen_hp_since < 10:
            self.num_hp_regens += 1
            if self.num_hp_regens > 5:  # Threshold for offense
                self.register_offense(CheatingOffense.FAST_HP_REGEN)
        else:
            self.regen_hp_since = current_time
            self.num_hp_regens = 0

    def check_mp_regen(self, healed_mp):
        current_time = time.time()
        if current_time - self.regen_mp_since < 10:
            self.num_mp_regens += 1
            if self.num_mp_regens > 5:
                self.register_offense(CheatingOffense.FAST_MP_REGEN)
        else:
            self.regen_mp_since = current_time
            self.num_mp_regens = 0

    def check_summon_attack(self, summon_id):
        with self.attack_lock:
            self.num_sequential_attacks += 1
            current_time = time.time()
            attack_interval = current_time - self.last_attack_time
            self.last_attack_time = current_time

            divisor = 30  # Summon attack specific divisor
            if attack_interval * divisor < self.num_sequential_attacks:
                self.register_offense(CheatingOffense.FAST_SUMMON_ATTACK)
                return False
            return True

    def reset_summon_attack(self):
        """ Resets the sequential attack counter for summons. """
        with self.attack_lock:
            self.num_sequential_attacks = 0

    def check_pickup_again(self):
        """ Check if picking up items again too quickly. """
        self.register_offense(CheatingOffense.TUBI)

    def pickup_complete(self):
        """ Marks the completion of an item pickup. """
        # Logic to handle item pickup completion, could reset counters or log the event
        pass

    def get_attacks_without_hit(self):
        """ Returns the count of attacks that occurred without a hit. """
        return self.attack_without_hit

    def set_attacks_without_hit(self, count):
        """ Sets the count of attacks that occurred without a hit. """
        self.attack_without_hit = count

    def get_points(self):
        """ Example placeholder for calculating points or penalties based on offenses. """
        total_points = sum(entry['count'] for entry in self.offenses.values())
        return total_points

    def register_offense(self, offense):
        entry = self.offenses[offense]
        entry['count'] += 1
        entry['last_time'] = time.time()

    def get_offense_count(self, offense):
        """ Retrieve the count of a specific offense """
        return self.offenses[offense]['count'] if offense in self.offenses else 0

    def invalidate_offenses(self):
        """ Periodically clears expired offenses """
        current_time = time.time()
        for offense, entry in list(self.offenses.items()):
            if current_time - entry['last_time'] > 60:  # Example timeout
                del self.offenses[offense]
        # Restart the timer
        self.invalidation_task = threading.Timer(60, self.invalidate_offenses)
        self.invalidation_task.start()

    def dispose(self):
        self.invalidation_task.cancel()

    def check_tubi(self):
        """ Check and register 'Tubi' offense if picking up items too fast """
        self.register_offense(CheatingOffense.TUBI)


# Example usage of CheatTracker
class MapleCharacter:
    def __init__(self, name):
        self.name = name
        # Additional character attributes would go here

# Usage example
character = MapleCharacter("ExampleCharacter")
tracker = CheatTracker(character)

# Simulating a series of actions
tracker.check_attack(skill_id=3121004)
tracker.check_hp_regen(healed_hp=50)
tracker.check_mp_regen(healed_mp=30)
tracker.check_move_monster()
tracker.check_tubi()

# Disposing the tracker when done
tracker.dispose()
