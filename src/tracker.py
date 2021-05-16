import random
import urllib.parse
from dataclasses import dataclass
from typing import Any, Dict, List

import httpx

import bencoding
from torrent import Torrent


@dataclass
class TrackerResponse:
    def __init__(self, response_data: Dict[str, Any]):
        self.complete = response_data["complete"]
        self.downloaded = response_data["downloaded"]
        self.incomplete = response_data["incomplete"]
        self.interval = response_data["interval"]
        self.min_interval = response_data["min interval"]
        self.peers = TrackerResponse.parse_peers(response_data["peers"])

    @staticmethod
    def parse_peers(peers_bytes: bytes) -> List[str]:
        pass


class Tracker:
    def __init__(self, torrent: Torrent):
        self.torrent = torrent
        self.peer_id = bytes(b"-AP0010-") + random.randbytes(12)


class UDPTracker(Tracker):
    pass


class HTTTPTracker(Tracker):
    async def get_tracker_info(self) -> None:
        request_data = {
            "info_hash": self.torrent.info_hash,
            "peer_id": self.peer_id,
            "port": random.randint(6881, 6889),
            "uploaded": 0,
            "downloaded": 0,
            "left": self.torrent.size,
            # "compact": 0,
            # "event": "started",
        }
        request_url = self.torrent.announce + "?" + urllib.parse.urlencode(request_data)
        response = httpx.get(request_url)
        bencoding.Decoder(response.read()).decode()
        print()
