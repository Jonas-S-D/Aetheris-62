import logging
from database.DatabaseConnection import DatabaseConnection

log = logging.getLogger(__name__)

class Marriage:

    @staticmethod
    def create_marriage(player, partner):
        con = DatabaseConnection.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO marriages (husbandid, wifeid) VALUES (%s, %s)", (player.getId(), partner.getId()))
            con.commit()
        except Exception as ex:
            log.warning(f"Problem marrying {player.getName()} and {partner.getName()}", ex)
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def create_engagement(player, partner):
        con = DatabaseConnection.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO engagements (husbandid, wifeid) VALUES (%s, %s)", (player.getId(), partner.getId()))
            con.commit()
        except Exception as ex:
            log.warning(f"Problem announcing engagement with " + player.getName() + " and " + partner.getName(), ex)
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def divorce_engagement(player):
        con = DatabaseConnection.get_connection()
        cursor = con.cursor()
        try:
            if player.get_gender() != 0:
                cursor.execute("DELETE FROM engagements WHERE wifeid = %s", (player.getId(),))
            else:
                cursor.execute("DELETE FROM engagements WHERE husbandid = %s", (player.getId(),))
            con.commit()
        except Exception as ex:
            log.warning(f"Problem divorcing " + player.getName() + " from their partner", ex)
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def divorce_marriage(player):
        con = DatabaseConnection.get_connection()
        cursor = con.cursor()
        try:
            if player.get_gender() != 0:
                cursor.execute("DELETE FROM marriages WHERE wifeid = %s", (player.getId(),))
            else:
                cursor.execute("DELETE FROM marriages WHERE husbandid = %s", (player.getId(),))
            cursor.execute("UPDATE characters SET married = 0 WHERE id = %s", (player.get_partner_id(),))
            cursor.execute("UPDATE characters SET partnerid = 0 WHERE id = %s", (player.get_partner_id(),))
            con.commit()
        except Exception as ex:
            log.warning(f"Problem divorcing " + player.getName() + " from their partner", ex)
        finally:
            cursor.close()
            con.close()