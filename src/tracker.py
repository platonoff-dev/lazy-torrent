import random
import urllib.parse
from abc import ABC, abstractmethod
from enum import Enum

import httpx

import bencoding
from torrent import TorrentInfo

DEFAULT_NUMWANT = 30
DEFAULT_ANNOUNCE_TIMEOUT_INTERVAL = 30 * 60


class AnnounceEvent(Enum):
    STARTED = "started"
    STOPPED = "stopped"
    COMPLETED = "completed"


class AnnounceRequest:
    def __init__(
        self,
        info_hash: bytes,
        peer_id: bytes,
        port: int,
        uploaded: int,
        downloaded: int,
        left: int,
        event: AnnounceEvent,
        compact: bool = False,
        numwant: int = DEFAULT_NUMWANT,
        key: str | None = None,
        trackerid: str | None = None,
    ) -> None:
        self.info_hash = info_hash
        self.peer_id = peer_id
        self.port = port
        self.uploaded = uploaded
        self.downloaded = downloaded
        self.left = left
        self.compact = compact
        self.event = event
        self.numwant = numwant
        self.key = key
        self.trackerid = trackerid

    def urlencode(self) -> str:
        params = {}
        for key, value in self.__dict__.items():
            if value is not None:
                params[key] = value

        params.pop("compact")
        params["event"] = params["event"].value
        return urllib.parse.urlencode(params)


class TrackerResponse:
    def __init__(
        self,
        complete: int,
        incomplete: int,
        interval: int,
        min_interval: int,
        peers: bytes | list[dict],
        tracker_id: str | None,
    ):
        self.complete = complete
        self.incomplete = incomplete
        self.interval = interval
        self.min_interval = min_interval
        self._peers = self._parse_peers(peers)
        self.tracker_id = tracker_id

    @staticmethod
    def _parse_peers(peers: bytes | list[dict]) -> list[str]:
        if isinstance(peers, bytes):
            return TrackerResponse._parse_binary_peers(peers)
        else:
            return TrackerResponse._parse_dict_peers(peers)

    @staticmethod
    def _parse_binary_peers(peers: bytes) -> list[str]:
        peer_ips = []
        for i in range(0, len(peers) // 6):
            ip_bytes = peers[i * 6 : (i + 1) * 6]
            ip = ".".join(str(x) for x in ip_bytes[:4])
            port = int.from_bytes(ip_bytes[4:], "big")
            address = ip + ":" + str(port)
            peer_ips.append(address)

        return peer_ips

    @staticmethod
    def _parse_dict_peers(peers: list[dict]) -> list[str]:
        addresses = []
        for peer in peers:
            address = peer["ip"] + ":" + peer["port"]
            addresses.append(address)

        return addresses

    @property
    def peers(self) -> list[str]:
        return self._peers


class Tracker(ABC):
    _interval: int | None = None
    _min_interval: int | None = None

    def __init__(self, torrent: TorrentInfo):
        self.torrent = torrent
        self.peer_id: bytes = bytes(b"-AP0010-") + random.randbytes(12)

    @abstractmethod
    async def get_info(self) -> TrackerResponse:
        """
        Connect to tracker and retrieve meta info about the torrent
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close all network resources
        """
        pass

    @property
    def interval(self) -> int:
        return self._interval or self._min_interval or DEFAULT_ANNOUNCE_TIMEOUT_INTERVAL


class TrackerError(Exception):
    def __init__(self, status_code: int, *args: object):
        super().__init__(*args)
        self.status_code = status_code
        self.meta = args

    def __str__(self) -> str:
        return f"Failed to get tracker data. Error: {self.status_code}. Additional info: {self.meta}"


class HTTTPTracker(Tracker):
    def __init__(self, torrent: TorrentInfo):
        super().__init__(torrent)
        self._client = httpx.AsyncClient()

    async def get_info(self) -> TrackerResponse:
        """
        Connect to tracker and retrieve meta info about the torrent

        Raises:
            TrackerError: If response from tracker has not successful status code
        """
        request = AnnounceRequest(
            info_hash=self.torrent.info_hash,
            peer_id=self.peer_id,
            port=random.randint(6881, 6889),
            uploaded=0,
            downloaded=0,
            compact=True,
            left=self.torrent.size,
            event=AnnounceEvent.STARTED,
        )

        request_url = self.torrent.announce + "?" + request.urlencode()
        response = await self._client.get(request_url)
        if response.status_code != 200:
            raise TrackerError(response.status_code, await response.aread())

        decoded_response_body = bencoding.Decoder(response.read()).decode()
        if decoded_response_body.get("failure reason"):
            raise TrackerError(
                response.status_code, decoded_response_body["failure reason"]
            )

        tracker_response = TrackerResponse(
            interval=decoded_response_body["interval"],
            min_interval=decoded_response_body.get("min interval"),
            tracker_id=decoded_response_body.get("tracker id"),
            peers=decoded_response_body["peers"],
            complete=decoded_response_body["complete"],
            incomplete=decoded_response_body["incomplete"],
        )
        return tracker_response

    async def close(self) -> None:
        await self._client.aclose()


class UDPTracker(Tracker):
    def __init__(self, torrent: TorrentInfo):
        super().__init__(torrent)

    async def get_info(self) -> TrackerResponse:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError


def get_tracker(torrent: TorrentInfo) -> Tracker:
    """
    Create and return tracker object based on announce form torrent.

    Args:
        torrent Torrent: parsed torrent file

    Returns:
        Tracker: tracker object based on announce protocol. Allowed protcols
        is HTTP, UDP
    Raises:
        ValueError: If announce protocol is not supported.
    """

    if torrent.announce.startswith("http://"):
        return HTTTPTracker(torrent)
    elif torrent.announce.startswith("upd://"):
        return UDPTracker(torrent)
    else:
        raise ValueError(f"Unknown tracker protcol. Announce: {torrent.announce}")
