import logging
from threading import Timer
from database.DatabaseConnection import DatabaseConnection 
from CommandProcessorMBean import CommandProcessorMBean
from MessageCallback import MessageCallback
from StringMessageCallback import StringMessageCallback
from ServernoticeMapleClientMessageCallback import ServerNoticeMapleClientMessageCallback
from abc import ABC, abstractmethod
import os
from queue import Queue
from typing import List, Dict, Optional, Tuple, Any


class CommandProcessor:
    gmLog: List[Pair[MapleCharacter, str]] = []
    commands: Dict[str, 'DefinitionCommandPair'] = {}
    instance: 'CommandProcessor' = None

    def __init__(self):
        CommandProcessor.instance = self
        self.reloadCommands()
        self.startPersistingTask()

    @classmethod
    def startPersistingTask(cls):
        def persistingTask():
            with cls.lock:
                con = DatabaseConnection.getConnection()
                try:
                    with con.cursor() as cursor:
                        for logEntry in cls.gmLog:
                            cursor.execute("INSERT INTO gmlog (cid, command) VALUES (%s, %s)", (logEntry.getLeft().getId(), logEntry.getRight()))
                    con.commit()
                except Exception as e:
                    logging.error(f"Error persisting cheatlog: {e}")
                cls.gmLog.clear()

        cls.lock = threading.Lock()
        Timer(62, persistingTask).start()

    @staticmethod
    def registerMBean():
        try:
            mBeanServer = ManagementFactory.getPlatformMBeanServer()
            mBeanServer.registerMBean(CommandProcessor.instance, ObjectName("net.sf.odinms.client.messages:name=CommandProcessor"))
        except Exception as e:
            print("Error registering CommandProcessor MBean")

    @staticmethod
    def joinAfterString(splitted: List[str], str_value: str) -> Optional[str]:
        for i in range(1, len(splitted)):
            if splitted[i].lower() == str_value.lower() and i + 1 < len(splitted):
                return StringUtil.joinStringFrom(splitted, i + 1)
        return None

    @staticmethod
    def getOptionalIntArg(splitted: List[str], position: int, default: int) -> int:
        if len(splitted) > position:
            try:
                return int(splitted[position])
            except ValueError:
                return default
        return default

    @staticmethod
    def getNamedArg(splitted: List[str], startpos: int, name: str) -> Optional[str]:
        for i in range(startpos, len(splitted)):
            if splitted[i].lower() == name.lower() and i + 1 < len(splitted):
                return splitted[i + 1]
        return None

    @staticmethod
    def getNamedIntArg(splitted, startpos, name):
        arg = CommandProcessor.getNamedArg(splitted, startpos, name)
        if arg is not None:
            try:
                return int(arg)
            except ValueError as nfe:
                pass
        return None

    @staticmethod
    def getNamedIntArg(splitted: List[str], startpos: int, name: str) -> Optional[int]:
        arg = CommandProcessor.getNamedArg(splitted, startpos, name)
        if arg is not None:
            try:
                return int(arg)
            except ValueError:
                pass
        return None
    
    @staticmethod
    def getNamedIntArgWithDefault(splitted: List[str], startpos: int, name: str, default: int) -> int:
        ret = CommandProcessor.getNamedIntArg(splitted, startpos, name)
        return default if ret is None else ret

    @staticmethod
    def getNamedDoubleArg(splitted: List[str], startpos: int, name: str) -> Optional[float]:
        arg = CommandProcessor.getNamedArg(splitted, startpos, name)
        if arg is not None:
            try:
                return float(arg)
            except ValueError:
                pass
        return None
    
    def processCommandJmx(self, cserver: int, mapid: int, command: str) -> str:
        cserv = ChannelServer.getInstance(cserver)
        if cserv is None:
            return "The specified channel Server does not exist in this server process."

        c = MapleClient(None, None, MockIOSession())
        chr = MapleCharacter.getDefault(c, 26023)
        c.setPlayer(chr)
        map_ = cserv.getMapFactory().getMap(mapid)

        if map_ is not None:
            chr.setMap(map_)
            SkillFactory.getSkill(9101004).getEffect(1).applyTo(chr)
            map_.addPlayer(chr)
        cserv.addPlayer(chr)

        mc = StringMessageCallback()
        try:
            self.processCommandInternal(c, mc, command)
        finally:
            if map_ is not None:
                map_.removeRlayer(chr)
            cserv.removePlayer(chr)
        
        return str(mc)
    
    def process_command(self, c: MapleClient, line: str) -> bool:
        return self.processCommandInternal(c, ServerNoticeMapleClientMessageCallback(c), line)

    @classmethod
    def forcePersisting(cls):
        cls.startPersistingTask()

    @classmethod
    def getInstance(cls) -> 'CommandProcessor':
        if cls.instance is None:
            cls.instance = CommandProcessor()
        return cls.instance
    
    def reloadCommands(self):
        self.commands.clear()
        try:
            classFinder = ClassFinder()
            classes = classFinder.listClasses("net.sf.odinms.client.messages.commands", True)
            for clazz in classes:
                clasz = __import__(clazz, fromlist=['Command'])
                if issubclass(clasz.Command, Command):
                    try:
                        new_instance = clasz.Command()
                        self.registerCommand(new_instance)
                    except Exception as e:
                        logging.error(f"ERROR INSTANTIATING COMMAND CLASS: {e}")
        except ImportError as e:
            logging.error(f"THROW: {e}")

    def registerCommand(self, command: 'Command'):
        for defn in command.getDefinition():
            self.commands[defn.getCommand().lower()] = DefinitionCommandPair(command, defn)

    def dropHelp(self, chr: MapleCharacter, mc: MessageCallback, page: int):
        allCommands = list(self.commands.values())
        startEntry = (page - 1) * 20
        mc.dropMessage(f"Commands Page: {page}")
        for i in range(startEntry, startEntry + 20):
            if i >= len(allCommands):
                break
            commandDefinition = allCommands[i].get_definition()
            if chr.getGmLevel() == commandDefinition.getRequiredLevel():
                self.dropHelpForDefinition(mc, commandDefinition)

    def writeCommandList(self):
        try:
            allCommands = list(self.commands.values())
            with open("Commands.txt", "w") as fw:
                for x in range(4, -1, -1):
                    fw.write("---------------------------------\n")
                    fw.write(f"          LEVEL {x} Commands.\n")
                    fw.write("---------------------------------\n\n")
                    for cmdPair in allCommands:
                        if cmdPair.getDefinition().getRequiredLevel() == x:
                            fw.write(f"{cmdPair.getDefinition().getCommand()}\n")
        except IOError as e:
            logging.error(f"THROW: {e}")

    def dropHelpForDefinition(self, mc: MessageCallback, commandDefinition: 'CommandDefinition'):
        mc.dropMessage(commandDefinition.getCommand())

    def processCommandInternal(self, c: MapleClient, mc: MessageCallback, line: str) -> bool:
        if line.startswith(('!', '@')):  # GM or Player commands
            splitted = line.split()
            if len(splitted) > 0:
                cmdPair = self.commands.get(splitted[0][1:].lower())
                if cmdPair is not None and c.getPlayer().getGmLevel() >= cmdPair.getDefinition().getRequiredLevel():
                    if cmdPair.getDefinition().getRequiredLevel() >= 3:
                        self.gmLog.append(Pair(c.getPlayer(), line))
                        logging.info(f"Notice: {c.getPlayer().getName()} used a command: {line}")
                    elif c.getPlayer().getCheatTracker().spam(1000, 7):
                        c.getPlayer().dropMessage(1, "Please try again later.")
                        return True
                    try:
                        cmdPair.getCommand().execute(c, mc, splitted)
                    except Exception as e:
                        logging.error(f"Command Error: {line}. Exception: {e}")
                    return True
        return False


class DefinitionCommandPair:
    def __init__(self, command: 'Command', definition: 'CommandDefinition'):
        self.command = command
        self.definition = definition

    def get_command(self) -> 'Command':
        return self.command

    def get_definition(self) -> 'CommandDefinition':
        return self.definition