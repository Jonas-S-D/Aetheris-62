from net.sf.odinms.client import MapleCharacter
from net.sf.odinms.server import ChannelServer
from net.sf.odinms.tools import StringUtil, MaplePacketCreator
from CommandDefinition import CommandDefinition

class Admins(Command):
    def execute(self, client: MapleClient, message_callback: MessageCallback, args: list):
        # Convert the command to lowercase
        args[0] = args[0].lower()
        player = client.getPlayer()
        channelServer = client.getChannelServer()

        if args[0] == "!speakall":
            text = StringUtil.joinStringFrom(args, 1)
            for mch in player.getMap().getCharacters():
                mch.get_map().broadcastMessage(MaplePacketCreator.getChatText(mch.get_id(), text, False, 0))

        elif args[0] == "!dcall":
            for channel in ChannelServer.getAllInstances():
                for cplayer in channel.getPlayerStorage().getAllCharacters():
                    if cplayer != player:
                        cplayer.getClient().disconnect()
                        cplayer.getClient().getSession().close()

        elif args[0] == "!packet":
            if len(args) > 1:
                client.sendPacket(MaplePacketCreator.sendPacket(StringUtil.joinStringFrom(args, 1)))
            else:
                messageCallback.dropMessage("Please enter packet data")

        elif args[0] == "!drop":
            item_id = int(args[1])
            quantity = int(args[2]) if len(args) > 2 else 1
            item = Item(item_id, 0, quantity)
            player.getMap().spawnItemDrop(player, player, item, player.getPosition(), True, True)

        elif args[0] == "!startprofiling":
            sampler = CPUSampler.getInstance()
            sampler.addIncluded("net.sf.odinms")
            sampler.start()

        elif args[0] == "!stopprofiling":
            sampler = CPUSampler.getInstance()
            try:
                filename = "odinprofile.txt"
                if len(args) > 1:
                    filename = args[1]
                
                if os.path.exists(filename):
                    os.remove(filename)

                sampler.stop()
                with open(filename, "w") as file:
                    sampler.save(file, 1, 10)
            except Exception as e:
                pass
            finally:
                sampler.reset()

        elif args[0] == "!reloadops":
            try:
                ExternalCodeTableGetter.populate_values(SendPacketOpcode.get_default_properties(), SendPacketOpcode.values())
                ExternalCodeTableGetter.populate_values(RecvPacketOpcode.get_default_properties(), RecvPacketOpcode.values())
            except Exception as e:
                pass
            PacketProcessor.get_processor(PacketProcessor.Mode.CHANNEL_SERVER).reset(PacketProcessor.Mode.CHANNEL_SERVER)
            PacketProcessor.get_processor(PacketProcessor.Mode.CHANNEL_SERVER).reset(PacketProcessor.Mode.CHANNEL_SERVER)

        elif args[0] == "!closemerchants":
            mc.drop_message("Closing and saving merchants, please wait...")
            for channel in ChannelServer.getAllInstances():
                for players in channel.getPlayerStorage().getAllCharacters():
                    players.getInteraction().closeShop(True)
            mc.drop_message("All merchants have been closed and saved.")

        elif args[0] == "!shutdown":
            time = 60000
            if len(args) > 1:
                time = int(args[1]) * 60000
            CommandProcessor.forcePersisting()
            c.getChannelServer().shutdown(time)

        elif args[0] == "!shutdownworld":
            time = 60000
            if len(args) > 1:
                time = int(args[1]) * 60000
            CommandProcessor.forcePersisting()
            c.getChannelServer().shutdownWorld(time)

        elif args[0] == "!shutdownnow":
            CommandProcessor.forcePersisting()
            ShutdownServer(c.getChannel()).run()

        elif args[0] == "!setrebirths":
            rebirths = int(args[2])
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                victim.setReborns(rebirths)
            else:
                mc.dropMessage("Player was not found")
        
        elif args[0] == "!mesoperson":
            mesos = int(args[2])
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                victim.gainMeso(mesos, true, true, true)
            else:
                mc.dropMessage("Player was not found")

        elif args[0] == "!jobperson":
            job = int(args[2])
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                victim.setJob(job)
            else:
                mc.dropMessage("Player not found")

        elif args[0] == "!spawndebug":
            player.getMap().spawnDebug(mc)

        elif args[0] == "!timerdebug":
            TimerManager.getInstance().dropDebugInfo(mc)

        elif args[0] == "!threads":
            threads = Thread.activeCount()
            filter = ""
            if len(args) > 1:
                filter = args[1]
            for i in range(threads):
                tstring = threads[i].toString()
                if tstring.lower().find(filter.lower()) > -1:
                    mc.dropMessage(i + ": " + tstring)

        elif args[0] == "!showtrace":
            threads = Thread.activeCount()
            t = threads[int(args[1])]
            mc.dropMessage(t.toString() + ":")
            for elem in t.getStackTrace():
                mc.dropMessage(elem.toString())

        elif args[0] == "!shopitem":
            if len(args) < 5:
                mc.dropMessage("!shopitem <shopid> <itemid> <price> <position>")
            else:
                try:
                    con = DatabaseConnection.getConnection()
                    ps = con.prepareStatement("INSERT INTO shopitems (shopid, itemid, price, position) VALUES (?, ?, ?, ?)")
                    ps.setInt(1, int(args[1]))
                    ps.setInt(2, int(args[2]))
                    ps.setInt(3, int(args[3]))
                    ps.setInt(4, int(args[4]))
                    ps.executeUpdate()
                    ps.close()
                    MapleShopFactory.getInstance().clear()
                    mc.dropMessage("Done adding shop item.")
                except SQLException as e:
                    mc.dropMessage("Something wrong happened.")

        elif args[0] == "!pnpc":
            npcId = int(args[1])
            xpos = player.getPosition().x
            ypos = player.getPosition().y
            fh = player.getMap().getFootholds().findBelow(player.getPosition()).getId()
            npc = MapleLifeFactory.getNPC(npcId);
;
            if npc and npc.getName() != "MISSINGNO":
                npc.setPosition(player.getPosition())
                npc.setCy(ypos)
                npc.setRx0(xpos + 50)
                npc.setRx1(xpos - 50)
                npc.setFh(fh)
                npc.setCustom(true)

                try:
                    con = DatabaseConnection.getConnection()
                    ps = con.prepareStatement("INSERT INTO spawns ( idd, f, fh, cy, rx0, rx1, type, x, y, mid ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )")
                    ps.setInt(1, npcId)
                    ps.setInt(2, 0)
                    ps.setInt(3, fh)
                    ps.setInt(4, ypos)
                    ps.setInt(5, xpos + 50)
                    ps.setInt(6, xpos - 50)
                    ps.setString(7, "n")
                    ps.setInt(8, xpos)
                    ps.setInt(9, ypos)
                    ps.setInt(10, player.getMapId())
                    ps.execute_update()
                except SQLException as e:
                    mc.dropMessage("Failed to save NPC to the database")
                player.getMap().addMapObject(npc)
                player.getMap().broadcastMessage(MaplePacketCreator.spawnNPC(npc))
            else:
                mc.dropMessage("You have entered an invalid Npc-Id")

        elif args[0] == "!saveall":
            for channel in ChannelServer.getAllInstances():
                for player in channel.getPlayerStorage().getAllCharacters():
                    player.saveToDB(True, False)
            mc.dropMessage("save complete")

        elif args[0] == "!notice":
            joinmod = 1;
            range = -1;
            if args[1].equalsIgnoreCase("m"):
                range = 0;
            elif args[1].equalsIgnoreCase("c"):
                range = 1;
            elif args[1].equalsIgnoreCase("w"):
                range = 2;
            tfrom = 2;
            type = 0;
            if range == -1:
                range = 2;
                tfrom = 1;
            if args[tfrom].equalsIgnoreCase("n"):
                type = 0;
            elif args[tfrom].equalsIgnoreCase("p"):
                type = 1;
            elif args[tfrom].equalsIgnoreCase("l"):
                type = 2;
            elif args[tfrom].equalsIgnoreCase("nv"):
                type = 5;
            elif args[tfrom].equalsIgnoreCase("v"):
                type = 5;
            elif args[tfrom].equalsIgnoreCase("b"):
                type = 6;
            else:
                type = 0;
                joinmod = 0;
            prefix = "";
            if args[tfrom].equalsIgnoreCase("nv"):
                prefix = "[Notice] ";
            joinmod += tfrom;
            outputMessage = StringUtil.join_string_from(args, joinmod)
            if outputMessage.equalsIgnoreCase("!array"):
                outputMessage = c.getChannelServer().getArrayString()
            packet = MaplePacketCreator.serverNotice(type, prefix + outputMessage)
            if range == 0:
                player.getMap().broadcastMessage(packet)
            elif range == 1:
                ChannelServer.getInstance(c.getChannel()).broadcastPacket(packet)
            elif range == 2:
                try:
                    ChannelServer.getInstance(c.getChannel()).getWorldInterface().broadcastMessage(player.getName(), packet.getBytes())
                except RemoteException as e:
                    c.getChannelServer().reconnectWorld()
                    
        elif args[0] == "!monsterdebug":
            map = player.getMap()
            range = Double.POSITIVE_INFINITY
            if len(args) > 1:
                irange = int(args[1])
                if len(args) <= 2:
                    range = irange * irange
                else:
                    map = c.getChannelServer().getMapFactory().getMap(int(args[2]))
            monsters = map.getMapObjectsInRange(player.getPosition(), range, Arrays.asList(MapleMapObjectType.MONSTER))
            for monstermo in monsters:
                monster = monstermo
                mc.dropMessage("Monster " + monster.to_string())

        elif args[0] == "!itemperson":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            item = int(args[2])
            quantity = int(args[3]) if len(args) > 3 else 1
            if victim:
                MapleInventoryManipulator.addById(victim.getClient(), item, quantity)
            else:
                mc.dropMessage("Player not found")

        elif args[0] == "!servercheck":
            try:
                cserv.getWorldInterface().broadcastMessage(None, MaplePacketCreator.serverNotice(1, "Server check will commence soon. Please @save, and log off safely.").getBytes())
            except RemoteException as e:
                cserv.reconnectWorld()

        elif args[0] == "!itemvac":
            items = player.getMap().getMapObjectsInRange(player.getPosition(), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.ITEM))
            for item in items:
                mapItem = item
                if mapItem.getMeso() > 0:
                    player.gainMeso(mapItem.getMeso(), True)
                elif mapItem.getItem().getItemId() >= 5000000 and mapItem.getItem().getItemId() <= 5000100:
                    petId = MaplePet.createPet(mapItem.getItem().getItemId())
                    if petId == -1:
                        return
                    MapleInventoryManipulator.addById(c, mapItem.getItem().getItemId(), mapItem.getItem().getQuantity(), None, petId)
                else:
                    MapleInventoryManipulator.addFromDrop(c, mapItem.getItem(), True)
                mapItem.setPickedUp(True)
                layer.getMap().removeMapObject(item)
                player.getMap().broadcastMessage(MaplePacketCreator.removeItemFromMap(mapItem.getObjectId(), 2, player.getId()), mapItem.getPosition())

        elif args[0] == "!playernpc":
            scriptId = int(args[2])
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            npcId = 0
            if len(args) != 3:
                mc.dropMessage("Pleaase use the correct syntax. !playernpc <char name> <script name>")
            elif scriptId < 9901000 or scriptId > 9901319:
                mc.dropMessage("Please enter a script name between 9901000 and 9901319")
            elif not victim:
                mc.dropMessage("The character is not in this channel")
            else:
                try:
                    con = DatabaseConnection.getConnection()
                    ps = con.prepareStatement("SELECT * FROM playernpcs WHERE ScriptId = ?")
                    ps.setInt(1, scriptId)
                    rs = ps.executeQuery()
                    if rs.next():
                        mc.dropMessage("The script id is already in use !")
                        rs.close()
                    else:
                        rs.close()
                        ps = con.prepareStatement("INSERT INTO playernpcs (name, hair, face, skin, x, cy, map, ScriptId, Foothold, rx0, rx1, gender, dir) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                        ps.setString(1, victim.getName())
                        ps.setInt(2, victim.getHair())
                        ps.setInt(3, victim.getFace())
                        ps.setInt(4, victim.getSkinColor().getId())
                        ps.setInt(5, player.getPosition().x)
                        ps.setInt(6, player.getPosition().y)
                        ps.setInt(7, player.getMapId())
                        ps.setInt(8, scriptId)
                        ps.setInt(9, player.getMap().getFootholds().findBelow(player.getPosition()).getId())
                        ps.setInt(10, player.getPosition().x + 50)
                        ps.setInt(11, player.getPosition().x - 50)
                        ps.setInt(12, victim.getGender())
                        ps.setInt(13, victim.isFacingLeft() ? 0 : 1)
                        ps.executeUpdate()
                        rs = ps.getGeneratedKeys()
                        rs.next()
                        npcId = rs.getInt(1)
                        ps.close()
                        ps = con.prepareStatement("INSERT INTO playernpcs_equip (NpcId, equipid, equippos) VALUES (?, ?, ?)")
                        ps.setInt(1, npcId)
                        for equip in victim.getInventory(MapleInventoryType.EQUIPPED):
                            ps.setInt(2, equip.getItemId())
                            ps.setInt(3, equip.getPosition())
                            ps.executeUpdate()
                        ps.close()
                        rs.close()
                        ps = con.prepareStatement("SELECT * FROM playernpcs WHERE ScriptId = ?")
                        ps.setInt(1, scriptId)
                        rs = ps.executeQuery()
                        rs.next()
                        pn = PlayerNPCs(rs)
                        for channel in ChannelServer.getAllInstances():
                            map = channel.getMapFactory().getMap(player.getMapId())
                            map.broadcastMessage(MaplePacketCreator.SpawnPlayerNPC(pn))
                            map.broadcastMessage(MaplePacketCreator.getPlayerNPC(pn))
                            map.addMapObject(pn)

                        rs.close()
                        ps.close()
                    con.close()
                except SQLException as e:
                    mc.dropMessage("Failed to save NPC to the database")

        elif args[0] == "!removeplayernpcs":
            for channel in ChannelServer.getAllInstances():
                for obj in channel.getMapFactory().getMap(player.getMapId()).getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.PLAYER_NPC)):
                    channel.getMapFactory().getMap(player.getMapId()).removeMapObject(obj)
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("DELETE FROM playernpcs WHERE map = ?")
            ps.setInt(1, player.getMapId())
            ps.executeUpdate()
            ps.close()

        elif args[0] == "!pmob":
            npcId = int(args[1])
            mobTime = int(args[2])
            xpos = player.getPosition().x
            ypos = player.getPosition().y
            fh = player.getMap().getFootholds().findBelow(player.getPosition()).getId()
            if args[2] == None:
                mobTime = 0
            mob = MapleLifeFactory.getMonster(npcId)
            if mob and mob.getName() != "MISSINGNO":
                mob.setPosition(player.getPosition())
                mob.setCy(ypos)
                mob.setRx0(xpos + 50)
                mob.setRx1(xpos - 50)
                mob.setFh(fh)
                try:
                    con = DatabaseConnection.getConnection()
                    ps = con.prepareStatement("INSERT INTO spawns ( idd, f, fh, cy, rx0, rx1, type, x, y, mid, mobtime ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )")
                    ps.setInt(1, npcId)
                    ps.setInt(2, 0)
                    ps.setInt(3, fh)
                    ps.setInt(4, ypos)
                    ps.setInt(5, xpos + 50)
                    ps.setInt(6, xpos - 50)
                    ps.setString(7, "m")
                    ps.setInt(8, xpos)
                    ps.setInt(9, ypos)
                    ps.setInt(10, player.getMapId())
                    ps.setInt(11, mobTime)
                    ps.executeUpdate()
                except SQLException as e:
                    mc.dropMessage("Failed to save MOB to the database")
                player.getMap().addMonsterSpawn(mob, mobTime)
            else:
                mc.dropMessage("You have entered an invalid Npc-Id")

        pass

    def get_definition(self):
        return [
            CommandDefinition("speakall", 4),
            CommandDefinition("dcall", 4),
            CommandDefinition("packet", 4),
            CommandDefinition("drop", 4),
            CommandDefinition("startprofiling", 4),
            CommandDefinition("stopprofiling", 4),
            CommandDefinition("reloadops", 4),
            CommandDefinition("closemerchants", 4),
            CommandDefinition("shutdown", 4),
            CommandDefinition("shutdownworld", 4),
            CommandDefinition("shutdownnow", 4),
            CommandDefinition("setrebirths", 4),
            CommandDefinition("mesoperson", 4),
            CommandDefinition("jobperson", 4),
            CommandDefinition("spawndebug", 4),
            CommandDefinition("timerdebug", 4),
            CommandDefinition("threads", 4),
            CommandDefinition("showtrace", 4),
            CommandDefinition("shopitem", 4),
            CommandDefinition("pnpc", 4),
            CommandDefinition("saveall", 4),
            CommandDefinition("notice", 4),
            CommandDefinition("monsterdebug", 4),
            CommandDefinition("itemperson", 4),
            CommandDefinition("servercheck", 4),
            CommandDefinition("itemvac", 4),
            CommandDefinition("playernpc", 4),
            CommandDefinition("removeplayernpcs", 4),
            CommandDefinition("pmob", 4)
        ]