import socket


class PeerConnection:
    """
    Class to work with logic between client and peers.
    """

    def __init__(self, peer: str) -> None:
        """
        Args:
            peer (str): Address of peer. Example: 91.75.12.2:1234
        """
        self.connection = socket.socket(socket.SOCK_STREAM)

    def _handshake(self) -> None:
        pass


class Message:
    pass


class KeepAlive(Message):
    data = b""


class Choke(Message):
    data = b""
