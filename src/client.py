import asyncio
import logging
import time
from typing import List

from connection import PeerConnection
from torrent import Torrent
from tracker import HTTTPTracker, TrackerError

MAX_PEERS = 10


class TorrentClient:
    """
    The torrent client is the local peer that holds peer-to-peer
    connactions to download and upload pieces for a given torrent.

    Once started, the client makes periodic announce calls to the tracker
    registered in the torrent meta file. These calls results in a list of peers
    that should be tried in order to exchange pieces.
    """

    def __init__(self, torrent: Torrent):
        self.tracker = HTTTPTracker(torrent)
        self.available_peers: asyncio.Queue = asyncio.Queue()
        self.peers: List[PeerConnection] = []
        self.piece_manager: PieceManager | None = None
        self.abort = False

    async def start(self) -> None:
        """
        Start downloading torrent held by this client.

        The method stops when downloading gull complete or aborted.
        """
        await self.tracker.connect()
        self.peers = [
            PeerConnection(self.available_peers, str(self.tracker.peer_id))
            for _ in range(MAX_PEERS)
        ]
        last_announce_call = None
        interval = self.tracker.interval

        while True:
            if self.piece_manager and self.piece_manager.complete:
                logging.info("Downloading complete")
                break

            if self.abort:
                logging.info("Downloading aborted!")
                break

            current = time.time()
            if not last_announce_call or (last_announce_call + interval > current):
                try:
                    self.tracker.connect()
                except TrackerError as e:
                    logging.error(e)
                    break
                last_announce_call = current
                interval = self.tracker.interval
        self.stop()

    def _empty_queue(self) -> None:
        raise NotImplementedError

    async def stop(self) -> None:
        await self.tracker.close()
        for peer in self.peers:
            peer.stop()

        if self.piece_manager:
            self.piece_manager.close()


class PieceManager:
    def __init__(self, torrent: Torrent) -> None:
        self.torrent = torrent

    @property
    def complete(self) -> bool:
        return False

    @property
    def downloaded(self) -> int:
        """
        Returns:
            int: Number of bytes download from peers
        """
        return 0

    @property
    def uploaded(self) -> int:
        """
        Returns:
            int: Number of bytes uploaded by client
        """
        return 0

    def close(self) -> None:
        """
        Close all resource used in the PieceManage such as opened files.
        """
        pass
