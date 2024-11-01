import logging
import sqlite3
import threading
import time
from datetime import datetime
from net.sf.odinms.client.anticheat import CheatingOffenseEntry
from net.sf.odinms.database import DatabaseConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CheatingOffensePersister")

class CheatingOffensePersister:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CheatingOffensePersister, cls).__new__(cls)
            cls._instance.to_persist = set()
            cls._instance.start_persisting_task()
        return cls._instance

    def start_persisting_task(self):
        # Run the persisting task every 61 seconds
        self.persisting_task = threading.Thread(target=self._persisting_task, daemon=True)
        self.persisting_task.start()

    def persist_entry(self, offense_entry):
        # Thread-safe operation to add entries to persist
        with threading.Lock():
            self.to_persist.discard(offense_entry)
            self.to_persist.add(offense_entry)

    def _persisting_task(self):
        while True:
            offenses = []
            with threading.Lock():
                offenses = list(self.to_persist)
                self.to_persist.clear()

            # Connect to database
            con = DatabaseConnection.get_connection()
            try:
                cursor = con.cursor()
                for offense in offenses:
                    param = offense.get_param() if offense.get_param() is not None else ""
                    if offense.get_dbid() == -1:
                        # Insert new offense
                        cursor.execute(
                            "INSERT INTO cheatlog (cid, offense, count, lastoffensetime, param) VALUES (?, ?, ?, ?, ?)",
                            (offense.get_chrfor().get_id(), offense.get_offense().name(), offense.get_count(),
                             datetime.fromtimestamp(offense.get_last_offense_time() / 1000), param)
                        )
                        offense.set_dbid(cursor.lastrowid)
                    else:
                        # Update existing offense
                        cursor.execute(
                            "UPDATE cheatlog SET count = ?, lastoffensetime = ?, param = ? WHERE id = ?",
                            (offense.get_count(), datetime.fromtimestamp(offense.get_last_offense_time() / 1000), param, offense.get_dbid())
                        )
                con.commit()
            except sqlite3.Error as e:
                logger.error("Error persisting cheatlog: %s", e)
            finally:
                con.close()

            # Wait for 61 seconds
            time.sleep(61)

# Singleton instance
def get_cheating_offense_persister_instance():
    return CheatingOffensePersister()
