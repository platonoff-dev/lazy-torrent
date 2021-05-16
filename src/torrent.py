from pathlib import Path
from typing import Union

from bencoding import Decoder


class Torrent:
    def __init__(self, filename: Union[str, Path]) -> None:
        torrent_file = Path(filename).expanduser().resolve()
        decoder = Decoder(torrent_file.read_bytes())
        metainfo = decoder.decode()

        self.announce = metainfo["announce"]
        self.info = metainfo["info"]
        self.name = metainfo["info"]["name"]
        self.announce_list = metainfo.get("announce-list")
        self.creation_date = metainfo.get("creation date")
        self.created_by = metainfo.get("created by")
        self.encoding = metainfo.get("encoding")
        self.publisher = metainfo.get("publisher")
        self.publisher = metainfo.get("publisher-url")
        self.coment = metainfo.get("comment")
        self._meta = metainfo

    @property
    def size(self) -> int:
        if "files" in self.info:
            return sum([file["length"] for file in self.info["files"]])
        else:
            return self.info["length"]
