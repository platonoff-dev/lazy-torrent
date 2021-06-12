import hashlib
from pathlib import Path
from typing import List, Union

from bencoding import Decoder, Encoder


class Torrent:
    def __init__(self, filename: Union[str, Path]) -> None:
        torrent_file = Path(filename).expanduser().resolve()
        decoder = Decoder(torrent_file.read_bytes())

        metainfo = decoder.decode()

        self.announce: str = metainfo["announce"]
        self.info: dict = metainfo["info"]
        self.name: str = metainfo["info"]["name"]
        self.announce_list: List[str] = metainfo.get("announce-list")
        self.creation_date: str = metainfo.get("creation date")
        self.created_by: str = metainfo.get("created by")
        self.encoding: str = metainfo.get("encoding")
        self.publisher: str = metainfo.get("publisher")
        self.publisher: str = metainfo.get("publisher-url")
        self.comment: str = metainfo.get("comment")
        self._meta: dict = metainfo

        encoded_info = Encoder(self.info).encode()
        if not encoded_info:
            raise ValueError("`info` block not found.")
        self.info_hash = hashlib.sha1(encoded_info).digest()

    @property
    def size(self) -> int:
        if "files" in self.info:
            return sum([file["length"] for file in self.info["files"]])
        else:
            return self.info["length"]
