from net.sf.odinms.client import MapleCharacter
from net.sf.odinms.server import ChannelServer
from net.sf.odinms.tools import StringUtil, MaplePacketCreator
from CommandDefinition import CommandDefinition

class PlayerCommands(Command):
    def execute(self, c: MapleClient, mc: MessageCallback, args: list):
     
        args[0] = args[0].lower()
        player = client.getPlayer()
        channelServer = client.getChannelServer()

        if args[0] == "@command" or args[0] == "@commands" or args[0] == "@help":
            mc.dropMessage("================================================================")
            mc.dropMessage("                  " + c.getChannelServer().getServerName() + " Commands")
            mc.dropMessage("================================================================")
            mc.dropMessage("@checkstat - | - Displays your stats.")
            mc.dropMessage("@save - | - Saves your progress.")
            mc.dropMessage("@expfix - | - Fixes your negative experience.")
            mc.dropMessage("@dispose - | - Unstucks you.")
            mc.dropMessage("@emo - | - Sets your HP zero.")
            mc.dropMessage("@rebirth - | - Resets your HP/MP and sets your level to 1 to be stronger.")
            mc.dropMessage("@togglesmega - | - Turn smegas OFF/ON.")
            mc.dropMessage("@str/@dex/@int/@luk <number> - | - Automatically add AP to your stats.")
            mc.dropMessage("@gm <message> - | - Sends a message to the GM's online.")
            mc.dropMessage("@revive - | - Revives anyone on the channel besides yourself.")
            mc.dropMessage("@afk - | - Shows how long a perosn has been AFK.")
            mc.dropMessage("@onlinetime - | - Shows how long a person has been online.")
            if player.getClient().getChannelServer().extraCommands():
                mc.dropMessage("@cody/@storage/@news/@kin/@nimakin/@reward/@reward1/@fredrick/@spinel/@clan")
                mc.dropMessage("@banme - | - This command will ban you, SGM's will not unban you from this.")
                mc.dropMessage("@goafk - | - Uses a CB to say that you are AFK.")
                mc.dropMessage("@slime - | - For a small cost, it summons smiles for you.")
                mc.dropMessage("@go - | - Takes you to many towns and fighting areas.")
                mc.dropMessage("@buynx - | - You can purchase NX with this command.")

        elif args[0] == "@checkstats":
            mc.dropMessage("Your stats are:")
            mc.dropMessage("Str: " + player.getStr())
            mc.dropMessage("Dex: " + player.getDex())
            mc.dropMessage("Int: " + player.getInt())
            mc.dropMessage("Luk: " + player.getLuk())
            mc.dropMessage("Available AP: " + player.getRemainingAp())
            mc.dropMessage("Rebirths: " + player.getReborns())

        elif args[0] == "@save":
            if not player.getCheatTracker().Spam(900000, 0):
                player.saveToDB(True, True)
                mc.dropMessage("Saved.")
            else:
                mc.dropMessage("You cannot save more than once every 15 minutes.")

        elif args[0] == "@expfix":
            player.setExp(0)
            player.updateSingleStat(MapleStat.EXP, player.getExp())

        elif args[0] == "@dispose":
            NPCScriptManager.getInstance().dispose(c)
            mc.dropMessage("You have been disposed.")

        elif args[0] == "@rebirth" or args[0] == "@reborn":
            if player.getLevel() >= 200:
                player.doReborn()
            else:
                mc.dropMessage("You must be at least level 200.")

        elif args[0] == "@togglesmega":
            if player.getMeso() >= 10000000:
                player.setSmegaEnabled(not player.getSmegaEnabled())
                text = "[Disable] Smegas are now disable." if not player.getSmegaEnabled() else "[Enable] Smegas are now enable."
                mc.dropMessage(text)
                player.gainMeso(-10000000, True)
            else:
                mc.dropMessage("You need 10,000,000 mesos to toggle smegas.")

        elif args[0] == "@str" or args[0] == "@dex" or args[0] == "@int" or args[0] == "@luk" or args[0] == "@hp" or args[0] == "@mp":
            if len(args) != 2:
                mc.dropMessage("Syntax: @<Stat> <amount>")
                mc.dropMessage("Stat: <STR> <DEX> <INT> <LUK> <HP> <MP>")
                return
            x = int(args[1])
            max = 30000
            if x > 0 and x <= player.getRemainingAp() and x < Short.MAX_VALUE:
                if args[0] == "@str" and x + player.getStr() < max:
                    player.addAP(c, 1, x)
                elif args[0] == "@dex" and x + player.getDex() < max:
                    player.addAP(c, 2, x)
                elif args[0] == "@int" and x + player.getInt() < max:
                    player.addAP(c, 3, x)
                elif args[0] == "@luk" and x + player.getLuk() < max:
                    player.addAP(c, 4, x)
                elif args[0] == "@hp" and x + player.getMaxHp() < max:
                    player.addAP(c, 5, x)
                elif args[0] == "@mp" and x + player.getMaxMp() < max:
                    player.addAP(c, 6, x)
                else:
                    mc.dropMessage("Make sure the stat you are trying to raise will not be over " + Short.MAX_VALUE + ".")
            else:
                mc.dropMessage("Please make sure your AP is valid.")

        elif args[0] == "@gm":
            if len(args) < 2:
                return
            if not player.getCheatTracker().Spam(300000, 1):
                try:
                    c.getChannelServer().getWorldInterface().broadcastGMMessage(None, MaplePacketCreator.serverNotice(6, "Channel: " + c.getChannel() + "  " + player.getName() + ": " + StringUtil.joinStringFrom(args, 1)).getBytes())
                except RemoteException:
                    c.getChannelServer().reconnectWorld()
                mc.dropMessage("Message sent.")
            else:
                player.dropMessage(1, "Please don't flood GMs with your messages.")

        elif args[0] == "@revive":
            if len(args) == 2:
                victim = c.getChannelServer().getPlayerStorage().getCharacterByName(args[1])
                if player != victim:
                    if player.getMeso() >= 50000000:
                        if victim != None:
                            if not victim.isAlive():
                                victim.setHp(victim.getMaxHp() / 2)
                                player.gainMeso(-50000000)
                                victim.updateSingleStat(MapleStat.HP, victim.getMaxHp() / 2)
                                mc.dropMessage("You have revived " + victim.getName() + ".")
                            else:
                                mc.dropMessage(victim.getName() + " is not dead.")
                        else:
                            mc.dropMessage("The player is not online.")
                    else:
                        mc.dropMessage("You need 50 million mesos to do this.")
                else:
                    mc.dropMessage("You can't revive yourself.")
            else:
                mc.dropMessage("Syntax: @revive <player name>")

        elif args[0] == "@afk":
            if len(args) >= 2:
                name = args[1]
                victim = c.getChannelServer().getPlayerStorage().getCharacterByName(name)
                if victim == None:
                    try:
                        wci = c.getChannelServer().getWorldInterface()
                        channel = wci.find(name)
                        if channel == -1 or victim.isGM():
                            mc.dropMessage("This player is not online.")
                            return
                        victim = ChannelServer.getInstance(channel).getPlayerStorage().getCharacterByName(name)
                    except RemoteException:
                        c.getChannelServer().reconnectWorld()
                blahblah = System.currentTimeMillis() - victim.getAfkTime()
                if Math.floor(blahblah / 60000) == 0:
                    mc.dropMessage("Player has not been afk!")
                else:
                    sb = StringBuilder()
                    sb.append(victim.getName())
                    sb.append(" has been afk for")
                    compareTime(sb, blahblah)
                    mc.dropMessage(sb.toString())
            else:
                mc.dropMessage("Incorrect Syntax.")

        elif args[0] == "@onlinetime":
            if len(args) >= 2:
                name = args[1]
                victim = c.getChannelServer().getPlayerStorage().getCharacterByName(name)
                if victim == None:
                    try:
                        wci = c.getChannelServer().getWorldInterface()
                        channel = wci.find(name)
                        if channel == -1 or victim.isGM():
                            mc.dropMessage("This player is not online.")
                            return
                        victim = ChannelServer.getInstance(channel).getPlayerStorage().getCharacterByName(name)
                    except RemoteException:
                        c.getChannelServer().reconnectWorld()
                blahblah = System.currentTimeMillis() - victim.getLastLogin()
                sb = StringBuilder()
                sb.append(victim.getName())
                sb.append(" has been online for")
                compareTime(sb, blahblah)
                mc.dropMessage(sb.toString())
            else:
                mc.dropMessage("Incorrect Syntax.")

        pass

    def compareTime(self, sb: StringBuilder, timeDiff: long):
        secondsAway = timeDiff / 1000
        minutesAway = 0
        hoursAway = 0

        while secondsAway > 60:
            minutesAway += 1
            secondsAway -= 60
        while minutesAway > 60:
            hoursAway += 1
            minutesAway -= 60
        hours = False
        minutes = False
        if hoursAway > 0:
            sb.append(" ")
            sb.append(int(hoursAway))
            sb.append(" hours")
            hours = True
        if minutesAway > 0:
            if hours:
                sb.append(" -")
            sb.append(" ")
            sb.append(int(minutesAway))
            sb.append(" minutes")
            minutes = True
        if secondsAway > 0:
            if minutes:
                sb.append(" and")
            sb.append(" ")
            sb.append(int(secondsAway))
            sb.append(" seconds !")


  def get_definition(self):
        return [
            CommandDefinition("@command", 1),
            CommandDefinition("@commands", 1),
            CommandDefinition("@help", 1),
            CommandDefinition("@checkstats", 1),
            CommandDefinition("@save", 1),
            CommandDefinition("@expfix", 1),
            CommandDefinition("@dispose", 1),
            CommandDefinition("@rebirth", 1),
            CommandDefinition("@reborn", 1),
            CommandDefinition("@togglesmega", 1),
            CommandDefinition("@str", 1),
            CommandDefinition("@dex", 1),
            CommandDefinition("@int", 1),
            CommandDefinition("@luk", 1),
            CommandDefinition("@hp", 1),
            CommandDefinition("@mp", 1),
            CommandDefinition("@gm", 1),
            CommandDefinition("@revive", 1),
            CommandDefinition("@afk", 1),
            CommandDefinition("@onlinetime", 1)
        ]