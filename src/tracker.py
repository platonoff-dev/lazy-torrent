import random
import urllib.parse
from dataclasses import dataclass
from typing import Any, Dict, List

import httpx

import bencoding
from torrent import Torrent


class Tracker:
    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peer_id = bytes(b"-AP0010-") + random.randbytes(12)


class TrackerError(Exception):
    def __init__(self, status_code: int, *args: object) -> None:
        super().__init__(*args)


class UDPTracker(Tracker):
    pass


@dataclass
class TrackerResponse:
    def __init__(self, response_data: Dict[str, Any]):
        self.complete: int = response_data["complete"]
        self.downloaded: int = response_data["downloaded"]
        self.incomplete: int = response_data["incomplete"]
        self.interval: int = response_data["interval"]
        self.min_interval: int = response_data["min interval"]
        self.peers: List[str] = TrackerResponse.parse_peers(response_data["peers"])

    @staticmethod
    def parse_peers(peers_bytes: bytes) -> List[str]:
        ip_addresses: List[str] = []
        for i in range(len(peers_bytes) // 6):
            address = peers_bytes[i : i + 6]
            ip = ".".join(str(x) for x in address[:4])
            ip += ":" + str(int.from_bytes(address[4:], "big"))
            ip_addresses.append(ip)
        return ip_addresses


class HTTTPTracker(Tracker):
    tracker_info: TrackerResponse

    def __init__(self, torrent: Torrent):
        super().__init__(torrent)
        self._client = httpx.AsyncClient()

    async def connect(self) -> None:
        request_data = {
            "info_hash": self.torrent.info_hash,
            "peer_id": self.peer_id,
            "port": random.randint(6881, 6889),
            "uploaded": 0,
            "downloaded": 0,
            "left": self.torrent.size,
        }
        request_url = self.torrent.announce + "?" + urllib.parse.urlencode(request_data)
        response = await self._client.get(request_url, params=request_data)
        if response.status_code != 200:
            raise TrackerError(status_code=response.status_code)

        tracker_response = TrackerResponse(bencoding.Decoder(response.read()).decode())
        self.tracker_info = tracker_response

    async def close(self) -> None:
        await self.close()
