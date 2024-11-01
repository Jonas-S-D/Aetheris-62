from net.sf.odinms.client import MapleCharacter
from net.sf.odinms.server import ChannelServer
from net.sf.odinms.tools import StringUtil, MaplePacketCreator
from CommandDefinition import CommandDefinition

class Donator(Command):
    def execute(self, c: MapleClient, mc: MessageCallback, args: list):
     
        args[0] = args[0].lower()
        player = client.getPlayer()
        channelServer = client.getChannelServer()

        if args[0] == "!buffme":
            skills = [9001000, 9101002, 9101003, 9101008, 2001002, 1101007, 1005, 2301003, 5121009, 1111002, 4111001, 4111002, 4211003, 4211005, 1321000, 2321004, 3121002]
            for skill in skills:
                skill = SkillFactory.getSkill(skill)
                skill.getEffect(skill.getMaxLevel()).applyTo(player)

        elif args[0] == "!goto":
            maps = {
                "gmmap": 180000000,
                "southperry": 60000,
                "amherst": 1010000,
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
                "ludi": 220000000,
                "aqua": 230000000,
                "leafre": 240000000,
                "mulung": 250000000,
                "herb": 251000000,
                "omega": 221000000,
                "korean": 222000000,
                "nlc": 600000000,
                "excavation": 990000000,
                "pianus": 230040420,
                "horntail": 240060200,
                "mushmom": 100000005,
                "griffey": 240020101,
                "manon": 240020401,
                "headless": 682000001,
                "balrog": 105090900,
                "zakum": 280030000,
                "papu": 220080001,
                "showa": 801000000,
                "guild": 200000301,
                "shrine": 800000000,
                "fm": 910000000,
                "skelegon": 240040511,
                "ariant": 260000100
            }
            if len(args) < 2:
                mc.dropMessage("Syntax: !goto <mapname> <optional_target>, where target is char name and mapname is one of:")
                builder = StringBuilder()
                i = 0
                for mapss in maps.keys():
                    if 1 % 10 == 0:
                        mc.dropMessage(builder.toString())
                    else:
                        builder.append(mapss + ", ")
                mc.dropMessage(builder.toString())
            else:
                message = args[1]
                if message in maps:
                    if len(args) == 2:
                        player.changeMap(maps[message])
                    elif len(args) == 3:
                        victim = channelServer.getPlayerStorage().getCharacterByName(args[2])
                        victim.changeMap(maps[message])
                else:
                    mc.dropMessage("Could not find map")
            maps.clear()

        elif args[0] == "!sexchange":
            if player.getGender() == 1:
                player.setGender(0)
            else:
                player.setGender(1)
            mc.dropMessage(player.getName() + " sex Change!")
        
        elif args[0] == "!storage":
            player.getStorage().sendStorage(c, 2080005)

    pass

    def get_definition(self):
        return [
            CommandDefinition("buffme", 1),
            CommandDefinition("goto", 1),
            CommandDefinition("sexchange", 1),
            CommandDefinition("storage", 1)
        ]