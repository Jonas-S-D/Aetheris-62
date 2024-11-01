from net.sf.odinms.client import MapleCharacter
from net.sf.odinms.server import ChannelServer
from net.sf.odinms.tools import StringUtil, MaplePacketCreator
from CommandDefinition import CommandDefinition

class Extras(Command):
    def execute(self, c: MapleClient, mc: MessageCallback, args: list):
     
        args[0] = args[0].lower()
        player = client.getPlayer()
        channelServer = client.getChannelServer()

        if (player.getClient().getChannelServer().extraCommands()):
            if args[0] == "@cody":
                NPCScriptManager.getInstance().start(c, 9200000)
            elif args[0] == "@storage":
                player.getStorage().sendStorage(c, 2080005)
            elif args[0] == "@news":
                NPCScriptManager.getInstance().start(c, 9040011)
            elif args[0] == "@kin":
                NPCScriptManager.getInstance().start(c, 9900000)
            elif args[0] == "@nimakin":
                NPCScriptManager.getInstance().start(c, 9900001)
            elif args[0] == "@reward":
                NPCScriptManager.getInstance().start(c, 2050019)
            elif args[0] == "@reward1":
                NPCScriptManager.getInstance().start(c, 2020004)
            elif args[0] == "@fredrick":
                NPCScriptManager.getInstance().start(c, 9030000)
            elif args[0] == "@spinel":
                NPCScriptManager.getInstance().start(c, 9000020)
            elif args[0] == "@clan":
                NPCScriptManager.getInstance().start(c, 9201061, "ClanNPC", None)
            elif args[0] == "@banme":
                player.ban(player.getName() + " banned him/her self.", False)
            elif args[0] == "@goafk":
                player.setChalkboard("I'm AFK! Drop me a message!")
            elif args[0] == "@slime":
                if player.getMeso() >= 50000000:
                    player.gainMeso(-50000000)
                    MapleInventoryManipulator.addById(c, 4001013, 1)
            elif args[0] == "@go":
                maps = {
                    "fm": 910000000,
                    "henesys": 100000000,
                    "ellinia": 101000000,
                    "perion": 102000000,
                    "kerning": 103000000,
                    "lith": 104000000,
                    "sleepywood": 105040300,
                    "florina": 110000000,
                    "orbis": 200000000,
                    "happy": 209000000,
                    "elnath": 211000000,
                    "ludi": 220000,
                    "aqua": 230000000,
                    "leafre": 240000000,
                    "mulung": 250000000,
                    "herb": 251000000,
                    "omega": 221000000,
                    "korean": 222000000,
                    "nlc": 600000000,
                    "excavation": 990000000,
                    "mushmom": 100000005,
                    "griffey": 240020101,
                    "manon": 240020401,
                    "horseman": 682000001,
                    "balrog": 105090900,
                    "showa": 801000000,
                    "guild": 200000301,
                    "shrine": 800000000,
                    "skelegon": 104040001,
                    "mall": 910000022
                }
                if len(args) != 2:
                    mc.dropMessage("Syntax: @go <mapname>")
                    builder = StringBuilder()
                    i = 0
                    for mapss in maps.keys():
                        if 1 % 10 == 0:
                            mc.dropMessage(builder.toString())
                        else:
                            builder.append(mapss + ", ")
                    mc.dropMessage(builder.toString())

                else:
                    if maps.containsKey(args[1]):
                        map = maps.get(args[1])
                        if map == 910000000:
                            player.saveLocation(SavedLocationType.FREE_MARKET)
                        player.changeMap(map)
                        mc.dropMessage("Please feel free to suggest any more locations")
                    else:
                        mc.dropMessage("I could not find the map that you requested, go get an eye test.")
                    maps.clear()

            elif args[0] == "@buynx":
                if len(args) != 2:
                    mc.dropMessage("Syntax: @buynx <number>")
                    return
                nxamount = int(args[1])
                nxcost = 5000
                cost = nxamount * nxcost
                if nxamount > 0 and nxamount < 420000:
                    if player.getMeso() >= cost:
                        player.gainMeso(-cost, True, True, True)
                        player.modifyCSPoints(1, nxamount)
                        mc.dropMessage("You spent " + cost + " mesos. You have gained " + nxamount + " nx.")
                    else:
                        mc.dropMessage("You don't have enough mesos. 1 NX is " + nxcost + " mesos.")
                else:
                    mc.dropMessage("You can only buy 1-420000 NX at a time.")

            pass

    def get_definition(self):
        return [
            CommandDefinition("@cody", 1),
            CommandDefinition("@storage", 1),
            CommandDefinition("@news", 1),
            CommandDefinition("@kin", 1),
            CommandDefinition("@nimakin", 1),
            CommandDefinition("@reward", 1),
            CommandDefinition("@reward1", 1),
            CommandDefinition("@fredrick", 1),
            CommandDefinition("@spinel", 1),
            CommandDefinition("@clan", 1),
            CommandDefinition("@banme", 1),
            CommandDefinition("@goafk", 1),
            CommandDefinition("@slime", 1),
            CommandDefinition("@go", 1),
            CommandDefinition("@buynx", 1)
        ]