from asyncio.queues import Queue
import socket


class PeerConnection:
    """
    Peer connection used to download and upload pieces.

    The peer connection will consume one available peer from the given queue.
    Based on peer details the PeerConnection will try to open a connection
    and perform BitTorrent handshake.

    After successful handshake, the PeerConnection will be in a *choked*
    state, not allowed to request any data from the remote peer. After sending 
    an interrested message the PeerConnection will be waiting to get *unchoked*

    Once the remote peer unchoke us, we can start requesting pieces. 
    The PeerConnection will continue to request pieces for as long as there are 
    pieces left to request, or until the remote peer disconects. 

    If the connection with a remote peer drops, the PeerConnection will consume 
    the next available peer from off the queue and try to connect to that one instead.
    """

    def __init__(self, queue: Queue, client_id: str) -> None:
        """
        Args:
            peer (str): Address of peer. Example: 91.75.12.2:1234
        """
        self.connection = socket.socket(socket.SOCK_STREAM)

    def _handshake(self) -> None:
        pass

    def stop(self) -> None:
        """
        Stop getting peaces and close all network resources
        """
        pass


class Message:
    pass


class KeepAlive(Message):
    data = b""


class Choke(Message):
    data = b""
