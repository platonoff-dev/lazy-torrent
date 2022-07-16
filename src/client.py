import asyncio
import logging
import time
from typing import List

from connection import PeerConnection
from torrent import TorrentInfo
from tracker import TrackerError, get_tracker

MAX_PEERS = 10


class TorrentClient:
    """
    The torrent client is the local peer that holds peer-to-peer
    connections to download and upload pieces for a given torrent.

    Once started, the client makes periodic announce calls to the tracker
    registered in the torrent meta file. These calls results in a list of peers
    that should be tried in order to exchange pieces.
    """

    def __init__(self, torrent: TorrentInfo):
        self._tracker = get_tracker(torrent)
        self._available_peers: asyncio.Queue = asyncio.Queue()
        self._peers: List[PeerConnection] = []
        self._piece_manager: PieceManager | None = None
        self._abort = False

    async def start(self) -> None:
        """
        Start downloading torrent held by this client.

        The method stops when downloading full complete or aborted.
        """
        await self._tracker.get_info()
        self._peers = [
            PeerConnection(self._available_peers, str(self._tracker.peer_id))
            for _ in range(MAX_PEERS)
        ]
        last_announce_call = None
        interval = self._tracker.interval

        while True:
            if self._piece_manager and self._piece_manager.complete:
                logging.info("Downloading complete")
                break

            if self._abort:
                logging.info("Downloading aborted!")
                break

            current = time.time()
            if not last_announce_call or (last_announce_call + interval > current):
                try:
                    self._tracker.get_info()
                except TrackerError as e:
                    logging.error(e)
                    break
                last_announce_call = current
                interval = self._tracker.interval
        self.stop()

    async def stop(self) -> None:
        await self._tracker.close()
        for peer in self._peers:
            peer.stop()

        if self._piece_manager:
            self._piece_manager.close()


class PieceManager:
    def __init__(self, torrent: TorrentInfo) -> None:
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
