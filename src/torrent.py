import hashlib
from pathlib import Path
from typing import List, Union

from bencoding import Decoder, Encoder


class TorrentInfo:
    def __init__(
        self,
        announce: str,
        info: dict,
        name: str,
        announce_list: List[str] | None,
        creation_date: str | None,
        created_by: str | None,
        encoding: str | None,
        publisher: str | None,
        publisher_url: str | None,
        comment: str | None,
    ) -> None:
        self.announce = announce
        self.info = info
        self.name = name
        self.announce_list = announce_list
        self.creation_date = creation_date
        self.created_by = created_by
        self.encoding = encoding
        self.publisher = publisher
        self.publisher_url = publisher_url
        self.comment = comment

    @staticmethod
    def parse(filename: Union[str, Path]) -> "TorrentInfo":
        torrent_file = Path(filename).expanduser().resolve()
        decoder = Decoder(torrent_file.read_bytes())
        metainfo = decoder.decode()

        return TorrentInfo(
            announce=metainfo["announce"],
            info=metainfo["info"],
            name=metainfo["info"]["name"],
            announce_list=metainfo.get("announce-list"),
            creation_date=metainfo.get("creation date"),
            created_by=metainfo.get("created by"),
            encoding=metainfo.get("encoding"),
            publisher=metainfo.get("publisher"),
            publisher_url=metainfo.get("publisher-url"),
            comment=metainfo.get("comment"),
        )

    @property
    def size(self) -> int:
        if "files" in self.info:
            return sum([file["length"] for file in self.info["files"]])
        else:
            return self.info["length"]

    @property
    def info_hash(self) -> bytes:
        encoded_info = Encoder(self.info).encode()
        if not encoded_info:
            raise ValueError("`info` block not found.")
        return hashlib.sha1(encoded_info).digest()
