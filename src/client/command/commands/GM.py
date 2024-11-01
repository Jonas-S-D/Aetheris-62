import os
import socket
import urllib.request
import sqlite3  # If you're using SQLite for database
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime
from client.item import IItem  # Assuming similar structure
from client.character import MapleCharacter
from client.client import MapleClient
from client.inventory import MapleInventoryType, MapleInventoryManipulator
from client.messages import Command, MessageCallback
from server.item_information import MapleItemInformationProvider
from server.packet_creator import MaplePacketCreator
from server.channel import ChannelServer
from server.stat import MapleStat
from server.pet import MaplePet
from server.equip import Equip
from server.character_util import MapleCharacterUtil
from server.disease import MapleDisease
from server.job import MapleJob
from server.ring import MapleRing
from server.skill import SkillFactory
from server.database import DatabaseConnection  # If you have a database connection module
from server.life import MapleLifeFactory, MapleMonster, MapleMonsterStats, MapleNPC
from server.maps import MapleMap, MapleMapObject, MapleMapObjectType
from server.shop import MapleShopFactory
from server.portal import MaplePortal
from scripting.npc import NPCScriptManager
from tools.pair import Pair  # Create or adapt if necessary
from tools.string_util import StringUtil  # Create or adapt if necessary
from server.trade import MapleTrade
from CommandDefinition import CommandDefinition

class (Command):

    @staticmethod
    def get_banned_reason(name: str) -> str:
        con = DatabaseConnection.get_connection()
        try:
            ps = con.prepareStatement("SELECT name, banned, banreason, macs FROM accounts WHERE name = ?")
            ps.setString(1, name)
            rs = ps.executeQuery()
            if rs.next():
                if rs.getInt("banned") > 0:
                    user, reason, mac = rs.getString("name"), rs.getString("banreason"), rs.getString("macs")
                    rs.close()
                    ps.close()
                    return "Username: " + user + " | BanReason: " + reason + " | Macs: " + mac
                else:
                    rs.close()
                    ps.close()
                    return "Player is not banned."
            rs.close()
            ps.close()
            accid = 0
            ps = con.prepareStatement("SELECT accountid FROM characters WHERE name = ?")
            ps.setString(1, name)
            rs = ps.executeQuery()
            if not rs.next():
                rs.close()
                ps.close()
                return "This character / account does not exist."
            else:
                accid = rs.getInt("accountid")
            ps = con.prepareStatement("SELECT name, banned, banreason, macs FROM accounts WHERE id = ?")
            ps.setInt(1, accid)
            rs = ps.executeQuery()
            if rs.getInt("banned") > 0:
                user, reason, mac = rs.getString("name"), rs.getString("banreason"), rs.getString("macs")
                rs.close()
                ps.close()
                return "Username: " + user + " | BanReason: " + reason + " | Macs: " + mac
            else:
                rs.close()
                ps.close()
                return "Player is not banned."
        except SQLException as exe:
            return "Player is not banned."
        
    @staticmethod
    def clear_slot(c: MapleClient, type: int) -> None:
        invent: MapleInventoryType
        if type == 1:
            invent = MapleInventoryType.EQUIP
        elif type == 2:
            invent = MapleInventoryType.USE
        elif type == 3:
            invent = MapleInventoryType.ETC
        elif type == 4:
            invent = MapleInventoryType.SETUP
        else:
            invent = MapleInventoryType.CASH
        item_map = []
        for item in c.player.get_inventory(invent).list():
            item_map.append(item.get_item_id())
        for itemid in item_map:
            MapleInventoryManipulator.remove_all_by_id(c, itemid, False)
    
    def execute(self, c: MapleClient, mc: MessageCallback, args: list):
        args[0] = args[0].lower()
        player = client.getPlayer()
        cserv = c.getChannelServer()
        cservs = ChannelServer.getAllInstances()

        if args[0] == "!lowhp":
            player.set_hp(1)
            player.update_single_stat(MapleStat.HP, 1)

        elif args[0] == "!sp":
            if len(args) != 2:
                return
            sp = int(args[1])
            player.setRemainingSp(sp + player.get_remaining_sp())
            player.updateSingleStat(MapleStat.AVAILABLESP, player.getRemainingSp())

        elif args[0] == "!ap":
            if len(args) != 2:
                return
            ap = int(args[1])
            player.setRemainingAp(ap + player.getRemainingAp())
            player.updateSingleStat(MapleStat.AVAILABLEAP, player.getRemainingAp())

        elif args[0] == "!job":
            if len(args) != 2:
                return
            job = int(args[1])
            player.setJob(job)

        elif args[0] == "!whereami":
            mc.dropMessage("You are on map " + player.getMap().getId())

        elif args[0] == "!shop":
            if len(args) != 2:
                return
            shopid = int(args[1])
            MapleShopFactory.getInstance().getShop(shopid).sendShop(c)

        elif args[0] == "!opennpc":
            if len(args) != 2:
                return
            npcid = int(args[1])
            npc = MapleLifeFactory.get_npc(npcid)
            if npc and npc.get_name() != "MISSINGNO":
                NPCScriptManager.getInstance().start(c, npcid)
            else:
                mc.dropMessage("UNKNOWN NPC")

        elif args[0] == "!levelup":
            player.levelUp()
            player.setExp(0)
            player.updateSingleStat(MapleStat.EXP, 0)

        elif args[0] == "!setmaxmp":
            if len(args) != 2:
                return
            amt = int(args[1])
            player.setMaxMp(amt)
            player.updateSingleStat(MapleStat.MAXMP, player.getMaxMp())

        elif args[0] == "!setmaxhp":
            if len(args) != 2:
                return
            amt = int(args[1])
            player.setMaxHp(amt)
            player.updateSingleStat(MapleStat.MAXHP, player.getMaxHp())

        elif args[0] == "!healmap":
            for map in player.getMap().getCharacters():
                if map:
                    map.setHp(map.getCurrentMaxHp())
                    map.updateSingleStat(MapleStat.HP, map.getHp())
                    map.setMp(map.getCurrentMaxMp())
                    map.updateSingleStat(MapleStat.MP, map.getMp())

        elif args[0] == "!item":
            ii = MapleItemInformationProvider.getInstance()
            if len(args) < 2:
                return
            item = int(args[1])
            quantity = int(args[2]) if len(args) > 2 else 1
            if 5000000 <= item <= 5000100:
                if quantity > 1:
                    quantity = 1
                petid = MaplePet.createPet(item)
                MapleInventoryManipulator.addById(c, item, quantity, player.getName(), petid)
            elif ii.getInventoryType(item) == MapleInventoryType.EQUIP and not ii.isThrowingStar(ii.getEquipById(item).getItemId()) and not ii.isBullet(ii.getEquipById(item).getItemId()):
                MapleInventoryManipulator.addFromDrop(c, ii.randomizeStats(c, ii.getEquipById(item)), True, player.getName())
            else:
                MapleInventoryManipulator.addById(c, item, quantity)

        elif args[0] == "!dropmesos" or args[0] == "dropmeso":
            if len(args) < 2:
                return
            amount = int(args[1])
            player.getMap().spawnMesoDrop(amount, amount, player.getPosition(), player, player, False)

        elif args[0] == "!level":
            if len(args) != 2:
                return
            level = int(args[1])
            player.setLevel(level)
            player.levelUp()
            player.setExp(0)
            player.updateSingleStat(MapleStat.EXP, 0)

        elif args[0] == "!online":
            i = 0
            for cs in ChannelServer.getAllInstances():
                if cs.getPlayerStorage().getAllCharacters().size() > 0:
                    sb = StringBuilder()
                    mc.dropMessage("Channel " + cs.getChannel())
                    for chr in cs.getPlayerStorage().getAllCharacters():
                        i += 1
                        if sb.length() > 150:
                            mc.dropMessage(sb.toString())
                            sb = StringBuilder()
                        sb.append(MapleCharacterUtil.makeMapleReadable(chr.getName() + "   "))
                    mc.dropMessage(sb.toString())

        elif args[0] == "!banreason":
            if len(args) != 2:
                return
            mc.dropMessage(getBannedReason(args[1]))

        elif args[0] == "!joinguild":
            if len(args) != 2:
                return
            con = DatabaseConnection.getConnection()
            try:
                ps = con.prepareStatement("SELECT guildid FROM guilds WHERE name = ?")
                ps.setString(1, args[1])
                rs = ps.executeQuery()
                if rs.next():
                    if player.getGuildId() > 0:
                        try:
                            cserv.getWorldInterface().leaveGuild(player.getMGC())
                        except java.rmi.RemoteException as re:
                            c.getSession().write(MaplePacketCreator.serverNotice(5, "Unable to connect to the World Server. Please try again later."))
                            return
                        c.getSession().write(MaplePacketCreator.showGuildInfo(None))
                        player.setGuildId(0)
                        player.saveGuildStatus()
                    player.setGuildId(rs.getInt("guildid"))
                    player.setGuildRank(2)
                    try:
                        cserv.getWorldInterface().addGuildMember(player.getMGC())
                    except RemoteException as e:
                        cserv.reconnectWorld()
                    c.getSession().write(MaplePacketCreator.showGuildInfo(player))
                    player.getMap().broadcastMessage(player, MaplePacketCreator.removePlayerFromMap(player.getId()), False)
                    player.getMap().broadcastMessage(player, MaplePacketCreator.spawnPlayerMapobject(player), False)
                    if player.getNoPets() > 0:
                        for pet in player.getPets():
                            player.getMap().broadcastMessage(player, MaplePacketCreator.showPet(player, pet, False, False), False)
                    player.saveGuildStatus()
                else:
                    mc.dropMessage("Guild name does not exist.")
                rs.close()
                ps.close()
            except SQLException as e:
                return
            
        elif args[0] == "!unbuffmap":
            for map in player.getMap().getCharacters():
                if map and map != player:
                    map.cancelAllBuffs()

        elif args[0] == "!mesos":
            if len(args) != 2:
                return
            meso = int(args[1])
            player.setMeso(meso)

        elif args[0] == "!clearslot":
            if len(args) != 2:
                return
            if args[1].equalsIgnoreCase("all"):
                clearSlot(c, 1)
                clearSlot(c, 2)
                clearSlot(c, 3)
                clearSlot(c, 4)
                clearSlot(c, 5)
            elif args[1].equalsIgnoreCase("equip"):
                clearSlot(c, 1)
            elif args[1].equalsIgnoreCase("use"):
                clearSlot(c, 2)
            elif args[1].equalsIgnoreCase("etc"):
                clearSlot(c, 3)
            elif args[1].equalsIgnoreCase("setup"):
                clearSlot(c, 4)
            elif args[1].equalsIgnoreCase("cash"):
                clearSlot(c, 5)
            else:
                mc.dropMessage("!clearslot " + args[1] + " does not exist!")

        elif args[0] == "!killall":
            mapMessage = ""
            map = player.getMap()
            range = Double.POSITIVE_INFINITY
            if len(args) > 1:
                irange = int(args[1])
                if len(args) <= 2:
                    range = irange * irange
                else:
                    map = cserv.getMapFactory().getMap(int(args[2]))
                    mapMessage = " in " + map.getStreetName() + " : " + map.getMapName()
            monsters = map.getMapObjectsInRange(player.getPosition(), range, Arrays.asList(MapleMapObjectType.MONSTER))
            for monstermo in monsters:
                monster = monstermo
                map.killMonster(monster, player, False)
            mc.dropMessage("Killed " + monsters.size() + " monsters" + mapMessage + ".")

        elif args[0] == "!say":
            if len(args) > 1:
                try:
                    cserv.getWorldInterface().broadcastMessage(player.getName(), MaplePacketCreator.serverNotice(6, "[" + player.getName() + "] " + StringUtil.joinStringFrom(args, 1)).getBytes())
                except RemoteException as e:
                    cserv.reconnectWorld()
            else:
                mc.dropMessage("Syntax: !say <message>")

        elif args[0] == "!spy":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                mc.dropMessage("Players stats are:")
                mc.dropMessage("Level: " + victim.getLevel() + "  ||  Rebirthed: " + victim.getReborns())
                mc.dropMessage("Fame: " + victim.getFame())
                mc.dropMessage("Str: " + victim.getStr() + "  ||  Dex: " + victim.getDex() + "  ||  Int: " + victim.getInt() + "  ||  Luk: " + victim.getLuk())
                mc.dropMessage("Player has " + victim.getMeso() + " mesos.")
                mc.dropMessage("Hp: " + victim.getHp() + "/" + victim.getCurrentMaxHp() + "  ||  Mp: " + victim.getMp() + "/" + victim.getCurrentMaxMp())
                mc.dropMessage("NX Cash: " + victim.getCSPoints(0))
            else:
                mc.dropMessage("Player not found.")

        elif args[0] == "!setall":
            if len(args) != 2:
                return
            max = int(args[1])
            player.setStr(max)
            player.setDex(max)
            player.setInt(max)
            player.setLuk(max)
            player.updateSingleStat(MapleStat.STR, max)
            player.updateSingleStat(MapleStat.DEX, max)
            player.updateSingleStat(MapleStat.INT, max)
            player.updateSingleStat(MapleStat.LUK, max)

        elif args[0] == "!giftnx":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                amount = int(args[2])
                type = getOptionalIntArg(args, 3, 1)
                victim.modifyCSPoints(type, amount)
                victim.dropMessage(5, player.getName() + " has gifted you " + amount + " NX points.")
                mc.dropMessage("NX recieved.")
            else:
                mc.dropMessage("Player not found.")

        elif args[0] == "!maxskills":
            player.maxAllSkills()

        elif args[0] == "!fame":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                victim.setFame(getOptionalIntArg(args, 2, 1))
                victim.updateSingleStat(MapleStat.FAME, victim.getFame())
            else:
                mc.dropMessage("Player not found")

        elif args[0] == "!heal":
            if len(args) == 2:
                heal = cserv.getPlayerStorage().getCharacterByName(args[1])
                if heal:
                    heal.setHp(heal.getCurrentMaxHp())
                    heal.setMp(heal.getCurrentMaxMp())
                    heal.updateSingleStat(MapleStat.HP, heal.getCurrentMaxHp())
                    heal.updateSingleStat(MapleStat.MP, heal.getCurrentMaxMp())
            else:
                player.setHp(player.getCurrentMaxHp())
                player.setMp(player.getCurrentMaxMp())
                player.updateSingleStat(MapleStat.HP, player.getCurrentMaxHp())
                player.updateSingleStat(MapleStat.MP, player.getCurrentMaxMp())

        elif args[0] == "!clock":
            player.getMap().broadcastMessage(MaplePacketCreator.getClock(getOptionalIntArg(args, 1, 60)))

        elif args[0] == "!warp":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                if len(args) == 2:
                    target = victim.getMap()
                    player.changeMap(target, target.findClosestSpawnpoint(victim.getPosition()))
                else:
                    target = cserv.getMapFactory().getMap(int(args[2]))
                    victim.changeMap(target, target.getPortal(0))
            else:
                try:
                    victim = player
                    loc = cserv.getWorldInterface().getLocation(args[1])
                    if loc:
                        mc.dropMessage("You will be cross-channel warped. This may take a few seconds.")
                        target = cserv.getMapFactory().getMap(loc.map)
                        victim.cancelAllBuffs()
                        ip = cserv.getIP(loc.channel)
                        victim.getMap().removePlayer(victim)
                        victim.setMap(target)
                        socket = ip.split(":")
                        if victim.getTrade():
                            MapleTrade.cancelTrade(player)
                        victim.saveToDB(True, True)
                        if victim.getCheatTracker():
                            victim.getCheatTracker().dispose()
                        ChannelServer.getInstance(c.getChannel()).removePlayer(player)
                        c.updateLoginState(MapleClient.LOGIN_SERVER_TRANSITION)
                        try:
                            c.getSession().write(MaplePacketCreator.getChannelChange(InetAddress.getByName(socket[0]), int(socket[1])))
                        except Exception as e:
                            raise RuntimeException(e)
                    else:
                        target = cserv.getMapFactory().getMap(int(args[1]))
                        player.changeMap(target, target.getPortal(0))
                except:
                    pass

        elif args[0] == "!warphere":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                victim.changeMap(player.getMap(), player.getPosition())
            else:
                try:
                    name = args[1]
                    wci = cserv.getWorldInterface()
                    channel = wci.find(name)
                    if channel > -1:
                        pserv = ChannelServer.getInstance(channel)
                        world_victim = pserv.getPlayerStorage().getCharacterByName(name)
                        if world_victim:
                            ChangeChannelHandler.changeChannel(c.getChannel(), world_victim.getClient())
                            world_victim.changeMap(player.getMap(), player.getPosition())
                    else:
                        mc.dropMessage("Player not online.")
                except RemoteException as e:
                    cserv.reconnectWorld()

        elif args[0] == "!jail":
            victim = cserv.getPlayerStorage().getCharacterByName(args[1])
            if victim:
                victim.changeMap(980000404, 0)
                mc.dropMessage(victim.getName() + " was jailed!")
                victim.dropMessage("You've been jailed.")
            else:
                mc.dropMessage(args[1] + " not found!")

        elif args[0] == "!map":
            mapid = int(args[1])
            player.changeMap(mapid, getOptionalIntArg(args, 2, 0))

        elif args[0] == "!rate":
            if len(args) == 4:
                try: 
                    rateType = args[1].lower()
                    multiplier = int(args[2])
                    hours = int(args[3])
                    
                    if hours < 0:
                        mc.dropMessage("Duration cannot be negative.")
                        return
                    
                    if rateType == "all":
                        for channel in cservs:
                            mesoRate = channel.getMesoRate()
                            dropRate = channel.getDropRate()
                            bossDropRate = channel.getBossDropRate()
                            expRate = channel.getExpRate()
                            channel.setMesoRate(mesoRate * multiplier)
                            channel.setDropRate(dropRate * multiplier)
                            channel.setBossDropRate(bossDropRate * multiplier)
                            channel.setExpRate(expRate * multiplier)

                        def resetRates():  
                            for channel in cservs:
                                channel.setMesoRate(mesoRate)
                                channel.setDropRate(dropRate)
                                channel.setBossDropRate(bossDropRate)
                                channel.setExpRate(expRate)
                                channel.broadcastPacket(MaplePacketCreator.serverNotice(0, f"All Rates have been reset to their original values."))
                        
                        revertTimer = threading.Timer(hours * 3600, resetRates)
                        revertTimer.start()
                        return
                    
                    if rateType not in ["meso", "drop", "bossDrop", "exp"]:
                        mc.dropMessage("Invalid rate type. Please use 'meso', 'drop', 'exp', 'bossDrop'.")
                        return

                    getRateName = f"get{rateType.capitalize()}Rate"
                    rate = getattr(cserv, getRateName)()
                    setRateName = f"set{rateType.capitalize()}Rate"
                    
                    for channel in cservs:
                        getattr(channel, setRateName)(rate * multiplier)
                        channel.broadcastPacket(MaplePacketCreator.serverNotice(0, f"{rateType.capitalize()} Rate has been changed to {rate * multiplier}x for the next {hours} hours."))
                    
                    def resetRates():
                        for channel in cservs:
                            getattr(channel, setRateName)(rate)
                            channel.broadcastPacket(MaplePacketCreator.serverNotice(0, f"{rateType.capitalize()} Rate has been reset to {rate}x."))

                    revertTimer = threading.Timer(hours * 3600, resetRates)
                    revertTimer.start()
                except ValueError:
                    mc.dropMessage("Invalid input.")
            else:
                mc.dropMessage("Syntax: !rate <meso/drop/exp/bossdrop/all> <multiplier> <hours>")

        elif args[0] == "!servermessage":
            message = StringUtil.joinStringFrom(args, 1)
            if message == "!array":
                message = cserv.getArrayString()
            cserv.setServerMessage(message)

        elif args[0] == "!unban":
            if MapleCharacter.unban(args[1]):
                mc.dropMessage("Sucess!")
            else:
                mc.dropMessage("Error while unbanning.")

        elif args[0] == "!spawn":
            mid = int(args[1])
            num = getOptionalIntArg(args, 2, 1)
            if num > 20:
                mc.dropMessage("Remember that we know what you're doing ;] please dont over summon")
            hp = getNamedIntArg(args, 1, "hp")
            exp = getNamedIntArg(args, 1, "exp")
            php = getNamedDoubleArg(args, 1, "php")
            pexp = getNamedDoubleArg(args, 1, "pexp")
            onemob = MapleLifeFactory.getMonster(mid)
            newhp = 0
            newexp = 0
            if hp:
                newhp = hp
            elif php:
                newhp = int(onemob.getMaxHp() * (php / 100))
            else:
                newhp = onemob.getMaxHp()
            if exp:
                newexp = exp
            elif pexp:
                newexp = int(onemob.getExp() * (pexp / 100))
            else:
                newexp = onemob.getExp()
            if newhp < 1:
                newhp = 1
            overrideStats = MapleMonsterStats()
            overrideStats.setHp(newhp)
            overrideStats.setExp(newexp)
            overrideStats.setMp(onemob.getMaxMp())
            if num > 20:
                num = 20
            for i in range(num):
                mob = MapleLifeFactory.getMonster(mid)
                mob.setHp(newhp)
                mob.setOverrideStats(overrideStats)
                player.getMap().spawnMonsterOnGroudBelow(mob, player.getPosition())

        elif args[0] == "!ban":
            originalReason = StringUtil.joinStringFrom(args, 2)
            reason = player.getName() + " banned " + args[1] + ": " + originalReason
            target = cserv.getPlayerStorage().getCharacterByName(args[1])
            if target:
                if not target.isGM() or player.getGMLevel() > 3:
                    readableTargetName = MapleCharacterUtil.makeMapleReadable(target.getName())
                    ip = target.getClient().getSession().getRemoteAddress().toString().split(":")[0]
                    reason += "  IP: " + ip
                    target.ban(reason, False)
                    try:
                        cserv.getWorldInterface().broadcastMessage(None, MaplePacketCreator.serverNotice(6, readableTargetName + " has been banned for " + originalReason).getBytes())
                    except RemoteException as e:
                        cserv.reconnectWorld()
                else:
                    mc.dropMessage("Please dont ban " + cserv.getServerName() + " GMs")
            else:
                if MapleCharacter.ban(args[1], reason, False):
                    readableTargetName = MapleCharacterUtil.makeMapleReadable(target.getName())
                    ip = target.getClient().getSession().getRemoteAddress().toString().split(":")[0]
                    reason += " (IP: " + ip + ")"
                    try:
                        cserv.getWorldInterface().broadcastMessage(None, MaplePacketCreator.serverNotice(6, readableTargetName + " has been banned for " + originalReason).getBytes())
                    except RemoteException as e:
                        cserv.reconnectWorld()
                else:
                    mc.dropMessage("Failed to ban " + args[1])

        elif args[0] == "!search":
            if len(args) > 2:
                type = args[1]
                search = StringUtil.joinStringFrom(args, 2)
                data = None
                dataProvider = MapleDataProviderFactory.getDataProvider(File(System.getProperty("net.sf.odinms.wzpath") + "/" + "String.wz"))
                mc.dropMessage("<<Type: " + type + " | Search: " + search + ">>")
                if type.equalsIgnoreCase("NPC") or type.equalsIgnoreCase("NPCS"):
                    retNpcs = []
                    data = dataProvider.getData("Npc.img")
                    npcPairList = LinkedList()
                    for npcIdData in data.getChildren():
                        npcIdFromData = Integer.parseInt(npcIdData.getName())
                        npcNameFromData = MapleDataTool.getString(npcIdData.getChildByPath("name"), "NO-NAME")
                        npcPairList.add(Pair(npcIdFromData, npcNameFromData))
                    for npcPair in npcPairList:
                        if npcPair.getRight().toLowerCase().contains(search.toLowerCase()):
                            retNpcs.add(npcPair.getLeft() + " - " + npcPair.getRight())
                    if retNpcs != None and len(retNpcs) > 0:
                        for singleRetNpc in retNpcs:
                            mc.dropMessage(singleRetNpc)
                    else:
                        mc.dropMessage("No NPC's Found")
                elif type.equalsIgnoreCase("MAP") or type.equalsIgnoreCase("MAPS"):
                    retMaps = []
                    data = dataProvider.getData("Map.img")
                    mapPairList = LinkedList()
                    for mapAreaData in data.getChildren():
                        for mapIdData in mapAreaData.getChildren():
                            mapIdFromData = Integer.parseInt(mapIdData.getName())
                            mapNameFromData = MapleDataTool.getString(mapIdData.getChildByPath("streetName"), "NO-NAME") + " - " + MapleDataTool.getString(mapIdData.getChildByPath("mapName"), "NO-NAME")
                            mapPairList.add(Pair(mapIdFromData, mapNameFromData))
                    for mapPair in mapPairList:
                        if mapPair.getRight().toLowerCase().contains(search.toLowerCase()):
                            retMaps.add(mapPair.getLeft() + " - " + mapPair.getRight())
                    if retMaps != None and len(retMaps) > 0:
                        for singleRetMap in retMaps:
                            mc.dropMessage(singleRetMap)
                    else:
                        mc.dropMessage("No Maps Found")
                elif type.equalsIgnoreCase("MOB") or type.equalsIgnoreCase("MOBS") or type.equalsIgnoreCase("MONSTER") or type.equalsIgnoreCase("MONSTERS"):
                    retMobs = []
                    data = dataProvider.getData("Mob.img")
                    mobPairList = LinkedList()
                    for mobIdData in data.getChildren():
                        mobIdFromData = Integer.parseInt(mobIdData.getName())
                        mobNameFromData = MapleDataTool.getString(mobIdData.getChildByPath("name"), "NO-NAME")
                        mobPairList.add(Pair(mobIdFromData, mobNameFromData))
                    for mobPair in mobPairList:
                        if mobPair.getRight().toLowerCase().contains(search.toLowerCase()):
                            retMobs.add(mobPair.getLeft() + " - " + mobPair.getRight())
                    if retMobs != None and len(retMobs) > 0:
                        for singleRetMob in retMobs:
                            mc.dropMessage(singleRetMob)
                    else:
                        mc.dropMessage("No Mob's Found")
                elif type.equalsIgnoreCase("ITEM") or type.equalsIgnoreCase("ITEMS"):
                    retItems = []
                    for itemPair in MapleItemInformationProvider.getInstance().getAllItems():
                        if itemPair.getRight().toLowerCase().contains(search.toLowerCase()):
                            retItems.add(itemPair.getLeft() + " - " + itemPair.getRight())
                    if retItems != None and len(retItems) > 0:
                        for singleRetItem in retItems:
                            mc.dropMessage(singleRetItem)
                    else:
                        mc.dropMessage("No Item's Found")
                elif type.equalsIgnoreCase("SKILL") or type.equalsIgnoreCase("SKILLS"):
                    retSkills = []
                    data = dataProvider.getData("Skill.img")
                    skillPairList = LinkedList()
                    for skillIdData in data.getChildren():
                        skillIdFromData = Integer.parseInt(skillIdData.getName())
                        skillNameFromData = MapleDataTool.getString(skillIdData.getChildByPath("name"), "NO-NAME")
                        skillPairList.add(Pair(skillIdFromData, skillNameFromData))
                    for skillPair in skillPairList:
                        if skillPair.getRight().toLowerCase().contains(search.toLowerCase()):
                            retSkills.add(skillPair.getLeft() + " - " + skillPair.getRight())
                    if retSkills != None and len(retSkills) > 0:
                        for singleRetSkill in retSkills:
                            mc.dropMessage(singleRetSkill)
                    else:
                        mc.dropMessage("No Skills Found")
                elif type.equalsIgnoreCase("REACTOR") or type.equalsIgnoreCase("REACTORS"):
                    mc.dropMessage("NOT ADDED YET")
                else:
                    mc.dropMessage("Sorry, that search call is unavailable")

        elif args[0] == "!npc":
            try:
                npcId = int(args[1])
                npc = MapleLifeFactory.getNPC(npcId)
                if npc and not npc.getName().equalsIgnoreCase("MISSINGNO"):
                    npc.setPosition(player.getPosition())
                    npc.setCy(player.getPosition().y)
                    npc.setRx0(player.getPosition().x + 50)
                    npc.setRx1(player.getPosition().x - 50)
                    npc.setFh(player.getMap().getFootholds().findBelow(player.getPosition()).getId())
                    npc.setCustom(True)
                    player.getMap().addMapObject(npc)
                    player.getMap().broadcastMessage(MaplePacketCreator.spawnNPC(npc))
                else:
                    mc.dropMessage("You have entered an invalid Npc-Id")
            except NumberFormatException as nfe:
                return

        elif args[0] == "!removenpcs":
            npcs = player.getMap().getMapObjectsInRange(player.getPosition(), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.NPC))
            for npcmo in npcs:
                npc = npcmo
                if npc.isCustom():
                    player.getMap().removeMapObject(npc.getObjectId())

        elif args[0] == "!cleardrops":
            map = player.getMap()
            range = Double.POSITIVE_INFINITY
            items = map.getMapObjectsInRange(player.getPosition(), range, Arrays.asList(MapleMapObjectType.ITEM))
            for itemmo in items:
                map.removeMapObject(itemmo)
                map.broadcastMessage(MaplePacketCreator.removeItemFromMap(itemmo.getObjectId(), 0, player.getId()))
            mc.dropMessage("You have destroyed " + items.size() + " items on the ground.")

        elif args[0] == "!proitem":
            if len(args) == 3:
                itemid = int(args[1])
                multiply = Short.parseShort(args[2])
                ii = MapleItemInformationProvider.getInstance()
                item = ii.getEquipById(itemid)
                type = ii.getInventoryType(itemid)
                if type.equals(MapleInventoryType.EQUIP):
                    MapleInventoryManipulator.addFromDrop(c, ii.hardcoreItem((Equip) item, multiply))
                else:
                    mc.dropMessage("Make sure it's an equippable item.")
            else:
                mc.dropMessage("Invalid syntax.")

        elif args[0] == "!maxmesos" or args[0] == "!maxmeso":
            player.gainMeso(Integer.MAX_VALUE - player.getMeso())

    pass 
       
        
  def get_definition(self):
        [
            CommandDefinition("lowhp", 3),
            CommandDefinition("sp", 3),
            CommandDefinition("ap", 3),
            CommandDefinition("job", 3),
            CommandDefinition("whereami", 3),
            CommandDefinition("shop", 3),
            CommandDefinition("opennpc", 3),
            CommandDefinition("levelup", 3),
            CommandDefinition("setmaxmp", 3),
            CommandDefinition("setmaxhp", 3),
            CommandDefinition("healmap", 3),
            CommandDefinition("item", 3),
            CommandDefinition("dropmeso", 3),
            CommandDefinition("level", 3),
            CommandDefinition("online", 3),
            CommandDefinition("banreason", 3),
            CommandDefinition("joinguild", 3),
            CommandDefinition("unbuffmap", 3),
            CommandDefinition("mesos", 3),
            CommandDefinition("clearslot", 3),
            CommandDefinition("killall", 3),
            CommandDefinition("say", 3),
            CommandDefinition("spy", 3),
            CommandDefinition("setall", 3),
            CommandDefinition("giftnx", 3),
            CommandDefinition("maxskills", 3),
            CommandDefinition("fame", 3),
            CommandDefinition("heal", 3),
            CommandDefinition("clock", 3),
            CommandDefinition("warp", 3),
            CommandDefinition("warphere", 3),
            CommandDefinition("jail", 3),
            CommandDefinition("map", 3),
            CommandDefinition("rate", 3),
            CommandDefinition("servermessage", 3),
            CommandDefinition("unban", 3),
            CommandDefinition("spawn", 3),
            CommandDefinition("ban", 3),
            CommandDefinition("search", 3),
            CommandDefinition("npc", 3),
            CommandDefinition("removenpcs", 3),
            CommandDefinition("cleardrops", 3),
            CommandDefinition("proitem", 3),
            CommandDefinition("maxmesos", 3)
        ]