from MessageCallback import MessageCallback
from mapleclient import MapleClient
from maplepacketcreator import MaplePacketCreator

class WhisperMapleClientMessageCallback(MessageCallback):
    def __init__(self, whisperfrom: str, client: MapleClient) -> None:
        self.whisperfrom = whisperfrom
        self.client = client

    def drop_message(self, message: str) -> None:
        packet = MaplePacketCreator.get_whisper(self.whisperfrom, self.client.get_channel(), message)
        self.client.get_session().write(packet)
