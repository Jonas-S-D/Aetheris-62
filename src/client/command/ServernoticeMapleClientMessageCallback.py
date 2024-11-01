from typing import Any
from MessageCallback import MessageCallback
    
class ServernoticeMapleClientMessageCallback(MessageCallback):
    def __init__(self, client: Any) -> None:
        self.client = client
        self.mode = 6

    def dropMessage(self, message: str) -> Any:
        self.client.getSession().write(MaplePacketCreator.serverNotice(self.mode, message))

        