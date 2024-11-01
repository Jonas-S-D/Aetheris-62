from config import SERVER_NAME, SERVER_PORT, SERVER_MSG, EXTRA_COMMANDS
from properties import EXP, DROP, MESO, BOSS_DROP, PET_EXP, MULTI_LEVEL, LVL_CAP, GM_ITEMS, GODLY_ITEMS, GODLY_ITEMS_RATE, ITEM_STAT_MULTIPLIER, DROP_UNDROPPABLE, MORE_THAN_ONE, AB, CS, MT
from database.DatabaseConnection import DatabaseConnection
from ChannelServerMBean import ChannelServerMBean
from collections import defaultdict, deque
import os  
import socket  
import threading 
import logging 
import configparser

class ChannelServer(threading.Thread, ChannelServerMBean):
    def __init__(self):
        super().__init__()
        self.port = SERVER_PORT
        self.serverName = SERVER_NAME
        self.expRate = EXP
        self.mesoRate = MESO
        self.dropRate = DROP
        self.bossdropRate = BOSS_DROP
        self.petExpRate = PET_EXP
        self.serverMessage = SERVER_MSG
        self.dropUndroppables = DROP_UNDROPPABLE
        self.moreThanOne = MORE_THAN_ONE
        self.channel = 1
        self.key = ""
        self.GMItems = GM_ITEMS
        self.godlyItems = GODLY_ITEMS
        self.godlyItemRate = GODLY_ITEMS_RATE
        self.itemStatMultiplier = 1
        self.multiLevel = MULTI_LEVEL
        self.levelCap = LVL_CAP
        self.AB = AB
        self.CS = CS
        self.MT = MT
        self.extraCommands = EXTRA_COMMANDS
        self.PvPis = 4
        self.worldReady = True

        self.mapFactory = None
        self.eventSM = None
        self.worldRegistry = None

        self.shutdown = False
        self.finishedShutdown = False

        self.ip = ""
        self.arrayString = ""
        self.props = None
        self.acceptor = None
        self.wci = None
        self.cwi = None
        self.players = defaultdict()
        self.instances = defaultdict()
        self.pendingInstances = defaultdict()
        self.gsStore = defaultdict()
        self.mapleSquads = defaultdict()
        self.clans = defaultdict()
        self.clones = deque()

        self.properties = configparser.ConfigParser()
        self.uniqueID = 1
        

    def run(self):
        try:
            self.cwi = ChannelWorldInterfaceImpl(self)
            self.wci = self.worldRegistry.registerChannelServer(self.key, self.cwi)
            
            conn = DatabaseConnection.getConnection()
            try: 
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE accounts SET loggedin = 0")
                    cursor.execute("UPDATE characters SET HasMerchant = 0")
                    conn.commit()
            except Exception as ex:
                print(f"Could not reset databases: {ex}")
            
            self.port = int(self.props["net.sf.odinms.channel.net.port"])
            self.ip = f"{self.props['net.sf.odinms.channel.net.interface']}:{self.port}"
            ByteBuffer.setUseDirectBuffers(False)
            ByteBuffer.setAllocator(SimpleByteBufferAllocator())

            self.acceptor = SocketAcceptor()
            cfg = SocketAcceptorConfig()
            cfg.getFilterChain().addLast("codec", ProtocolCodecFilter(MapleCodecFactory()))

            TimerManager.getInstance().start()
            TimerManager.getInstance().register(AutobanManager.getInstance(), 60000)

            try:
                serverHandler = MapleServerHandler(PacketProcessor.getProcessor(PacketProcessor.Mode.CHANNELSERVER), self.channel)
                self.acceptor.bind(InetSocketAddress(self.port), serverHandler, cfg)
                print(f"Channel {self.channel}: Listening on port: {self.port}")
                self.wci.serverReady()
                self.eventSM.init()
            except Exception as e:
                print(f"Binding to port {self.port} failed (ch: {self.channel}): {e}")

        except Exception as e:
            raise RuntimeError(e)
        
    def reconnectWorld(self):
        try:
            if not self.worldReady:
                print("World server is not ready to reconnect.")
                return
            
            self.cwi = ChannelWorldInterfaceImpl(self)
            self.wci = self.worldRegistry.registerChannelServer(self.key, self.cwi)

            print(f"Reconnected to world server. Channel server key: {self.key}")
        
        except Exception as ex:
            print(f"Failed to reconnect to world server: {ex}")
            

    def shutdown(self):
        self.shutdown = True
        futures = []
        allchars = self.players.getAllCharacters()
        chrs = allchars.toArray(new MapleCharacter[allchars.size()])
        for chr in chrs:
            if chr.getTrade() != None:
                MapleTrade.cancelTrade(chr)
            if chr.getEventInstance() != None:
                chr.getEventInstance().playerDisconnected(chr)
            if not chr.getClient().isGuest():
                chr.saveToDB(True, True)
            if chr.getCheatTracker() != None:
                chr.getCheatTracker().dispose()
            self.removePlayer(chr)
        for chr in chrs:
            futures.add(chr.getClient().getSession().close())
        for future in futures:
            future.join(500)
        self.finishedShutdown = True
        self.wci = None
        self.cwi = None

        def unbind():
            self.acceptor.unbindAll()

        def hasFinishedShutdown():
            return self.finishedShutdown
        
        def getMapFactory():
            return self.mapFactory
        
        def addPlayer(chr):
            self.players.registerPlayer(chr)
            if chr.getClan() > -1:
                self.clans.playerOnline(chr)

        def removePlayer(chr):
            self.players.deregisterPlayer(chr)
            if chr.getClan() > -1:
                self.clans.deregisterPlayer(chr)

        def getPlayerStorage():
            return self.players
        
        def addToClan(chr):
            self.clans.registerPlayer(chr)

        def getClanHolder():
            return self.clans
        
        def getConnectedClients():
            return len(self.players.getAllCharacters())
        
        def getChannel():
            return self.channel
        
        def getExpRate():
            return self.expRate
        
        def getMesoRate():
            return self.mesoRate
        
        def getDropRate():
            return self.dropRate
        
        def getBossDropRate():
            return self.bossdropRate
        
        def getPetExpRate():
            return self.petExpRate
        
        def getIP():
            return self.ip
        
        def isShutdown():
            return self.shutdown
        
        def setExpRate(expRate):
            self.expRate = expRate

        def setMesoRate(mesoRate):
            self.mesoRate = mesoRate

        def setDropRate(dropRate):
            self.dropRate = dropRate

        def setBossDropRate(bossdropRate):
            self.bossdropRate = bossdropRate

        def setPetExpRate(petExpRate):
            self.petExpRate = petExpRate

        def allowUndroppableDrops():
            return self.dropUndroppables
        
        def allowMoreThanOne():
            return self.moreThanOne
        
        def isGodlyItems():
            return self.godlyItems
        
        def getGodlyItemRate():
            return self.godlyItemRate
        
        def getItemStatMultiplier():
            return self.itemStatMultiplier
        
        def SetGodlyItems(godlyItems):
            self.godlyItems = godlyItems
        
        def setGodlyItemRate(godlyItemRate):
            self.godlyItemRate = godlyItemRate

        def setItemMultiplier(itemMultiplier):
            self.itemMultiplier = itemMultiplier

        def getMultiLevel():
            return self.multiLevel
        
        def getLevelCap():
            return self.levelCap
        
        def getGMItems():
            return self.GMItems
        
        def AutoBan():
            return self.AB
        
        def CashShop2FM():
            return self.CS
    
        def MTS2FM():
            return self.MT
        
        def getExtraCommands():
            return self.extraCommands
        
        def AddClone(fc):
            self.clones.add(fc)

        def RemoveClone(fc):
            self.clones.remove(fc)

        def getAllClones():
            return self.clones
        
        def getServerName():
            return self.serverName
        
        def GetLoadedMaps():
            return self.mapFactory.getLoadedMaps()
        
        def getEventSM():
            return self.eventSM
        
        def getWorldRegistry():
            return self.worldRegistry
        
        def getServerMessage():
            return self.serverMessage
        
        def setServerMessage(newMessage):
            self.serverMessage = newMessage
            self.broadcastPacket(MaplePacketCreator.serverMessage(serverMessage))

        def broadcastPacket(self, data):
            for chr in self.players.getAllCharacters():
                chr.getClient().getSession().write

        def getInstance(self, channel):
            return self.instances.get(channel)
        
        def getProperties(name):
            return self.props.getProperty(name)
        
        def shutdown(time):
            self.broadcastPacket(MaplePacketCreator.serverNotice(0, "The world will be shut down in " + (time / 60000) + " minutes, please log off safely"))
            TimerManager.getInstance().schedule(ShutdownServer(getChannel()), time)

        def shutdownWorld(time):
            try:
                getWorldInterface().shutdown(time)
            except RemoteException e:
                reconnectWorld()

        def reloadEvents():
            eventSM.cancel()
            eventSM = EventScriptManager(self, props.getProperty("net.sf.odinms.channel.events").split(","))
            eventSM.init()

        def getGuild(MapleGuildCharacter mgc):
            gid = mgc.getGuildId()
            g = None
            try:
                g = getWorldInterface().getGuild(gid, mgc)
            except RemoteException re:
                print("RemoteException while fetching MapleGuild." + re)
                return None

            if gsStore.get(gid) == None:
                gsStore.put(gid, MapleGuildSummary(g))

            return g
        
        def getGuildSummary(gid):
            if gsStore.containsKey(gid):
                return gsStore.get(gid)
            else:
                try:
                    g = getWorldInterface().getGuild(gid, None)
                    if g != None:
                        gsStore.put(gid, MapleGuildSummary(g))
                    return gsStore.get(gid)
                except RemoteException re:
                    print("RemoteException while fetching GuildSummary." + re)
                    return None
                
        def updateGuildSummary(gid, mgs):
            gsStore.put(gid, mgs)

        def reloadGuildSummary():
            try:
                MapleGuild g
                for i in gsStore.keySet():
                    g = getWorldInterface().getGuild(i, None)
                    if g != None:
                        gsStore.put(i, MapleGuildSummary(g))
                    else:
                        gsStore.remove(i)
            except RemoteException re:
                print("RemoteException while reloading GuildSummary." + re)

        def setChannel(channel):
            if pendingInstances.containsKey(key):
                pendingInstances.remove(key)
            if instances.containsKey(channel):
                instances.remove(channel)
            instances.put(channel, this)
            this.channel = channel
            this.mapFactory.setChannel(channel)

        def PVPis():
            if PvPis > 0 and PvPis < 21 || PvPis >= 100000000 && PvPis <=990000000:
                return PvPis
            else:
                return 4
            
        def ChannelServer(key):
            mapFactory = MapleMapFactory(MapleDataProviderFactory.getDataProvider(File(System.getProperty("net.sf.odinms.wzpath") + "/Map.wz")), MapleDataProviderFactory.getDataProvider(File(System.getProperty("net.sf.odinms.wzpath") + "/String.wz")))
            self.key = key
        
        def newInstance(key):
            return ChannelServer(key)
        
        def getArrayString():
            return arrayString
        
        def setArrayString(newStr):
            arrayString = newStr

        def getAllInstances():
            return Collections.unmodifiableCollection(instances.values())
        
        def getIP(channel):
            try:
                return getWorldInterface().getIP(channel)
            except RemoteException e:
                print("Lost connection to world server" + e)
                raise RuntimeException("Lost connection to world server")
            
        def getWorldInterface():
            synchronized(worldReady):
            while not worldReady:
                    try:
                        worldReady.wait()
                    except InterruptedException e:
                        pass
            return wci
        
        def main(args):
            initialProp = Properties()
            initialProp.load(FileReader(System.getProperty("net.sf.odinms.channel.config")))
            registry = LocateRegistry.getRegistry(initialProp.getProperty("net.sf.odinms.world.host"), Registry.REGISTRY_PORT, SslRMIClientSocketFactory())
            worldRegistry = registry.lookup("WorldRegistry")
            for i in range(0, Integer.parseInt(initialProp.getProperty("net.sf.odinms.channel.count", "0"))):
                newInstance(initialProp.getProperty("net.sf.odinms.channel." + i + ".key")).run()
            DatabaseConnection.getConnection()
            CommandProcessor.registerMBean()
            ClanHolder.loadAllClans()
            Runtime.getRuntime().addShutdownHook(Thread() {
                def run():
                    for channel in getAllInstances():
                        for i in range(910000001, 910000022):
                            for obj in channel.getMapFactory().getMap(i).getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.HIRED_MERCHANT)):
                                hm = obj
                                hm.closeShop(True)
                        for mc in channel.getPlayerStorage().getAllCharacters():
                            mc.saveToDB(True, True)

        def getMapleSquad(type):
            return mapleSquads.get(type)

        def addMapleSquad(squad, type):
            if mapleSquads.get(type) == None:
                mapleSquads.remove(type)
                mapleSquads.put(type, squad)
                return True
            else:
                return False

        def removeMapleSquad(squad, type):
            if mapleSquads.containsKey(type):
                if mapleSquads.get(type) == squad:
                    mapleSquads.remove(type)
                    return True
            return False

        def broadcastSMega(MaplePacket data):
            for chr in players.getAllCharacters():
                if chr.getSmegaEnabled():
                    chr.getClient().getSession().write(data)

        def broadcastGMPacket(MaplePacket data):
            for chr in players.getAllCharacters():
                if chr.isGM():
                    chr.getClient().getSession().write(data)

        def broadcastToClan(MaplePacket data, clan):
            for chr in clans.getAllOnlinePlayersFromClan(clan):
                chr.getClient().getSession().write(data)

        def onlineClanMembers(clan):
            return clans.countOnlineByClan(clan)

        def getPartyMembers(party):
            partym = LinkedList()
            for partychar in party.getMembers():
                if partychar.getChannel() == getChannel():
                    chr = getPlayerStorage().getCharacterByName(partychar.getName())
                    if chr != None:
                        partym.add(chr)
            return partym