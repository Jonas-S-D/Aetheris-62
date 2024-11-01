from MessageCallback import MessageCallback

class StringMessageCallback(MessageCallback):
    def __init__(self) -> None:
        self.ret = []

    def drop_message(self, message: str) -> None:
        self.ret.append(message + "\n")

    def __str__(self) -> str:
        return ''.join(self.ret)