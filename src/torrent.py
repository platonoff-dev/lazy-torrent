import hashlib
from pathlib import Path
from typing import List, Union

from bencoding import Decoder, Encoder


class Torrent:
    def __init__(
        self,
        announce: str,
        info: dict,
        name: str,
        announce_list: List[str],
        creation_date: str,
        created_by: str,
        encoding: str,
        publisher: str,
        publisher_url: str,
        comment: str,
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

    def parse(filename: Union[str, Path]) -> 'Torrent':
        torrent_file = Path(filename).expanduser().resolve()
        decoder = Decoder(torrent_file.read_bytes())
        metainfo = decoder.decode()

        return Torrent(
            metainfo["announce"],
            metainfo["info"],
            metainfo["info"]["name"],
            metainfo.get("announce-list"),
            metainfo.get("creation date"),
            metainfo.get("created by"),
            metainfo.get("encoding"),
            metainfo.get("publisher"),
            metainfo.get("publisher-url"),
            metainfo.get("comment")
        )

    @property
    def size(self) -> int:
        if "files" in self.info:
            return sum([file["length"] for file in self.info["files"]])
        else:
            return self.info["length"]

    @property
    def info_hash(self):
        encoded_info = Encoder(self.info).encode()
        if not encoded_info:
            raise ValueError("`info` block not found.")
        return hashlib.sha1(encoded_info).hexdigest()
