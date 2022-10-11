from sqlalchemy.orm import Session

from torrent import TorrentInfo
from storage.models import Torrent
from storage import engine

def add_torrent(torrent: TorrentInfo) -> None:
    torrent = Torrent(
        announce = torrent.announce,
        info = torrent.info,
        name = torrent.name,
        announce_list = torrent.announce_list,
        creation_date = torrent.creation_date,
        created_by = torrent.created_by,
        encoding = torrent.encoding,
        publisher = torrent.publisher,
        publisher_url = torrent.publisher_url,
        comment = torrent.comment,
    )
    with Session(engine) as session:
        session.add(torrent)
        session.commit()
