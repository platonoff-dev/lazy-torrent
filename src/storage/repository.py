import pickle
from sqlalchemy import select
from sqlalchemy.orm import Session

from meta_file.meta_file import MetaFileInfo
from storage.models import LoadingStatus, TorrentModel
from torrent import Torrent
from storage import engine

def add_torrent(torrent: Torrent) -> None:
    db_torrent = TorrentModel(
        announces = ",".join(torrent.announces),
        info = pickle.dumps(torrent.info),
        name = torrent.name,
        creation_date = torrent.creation_date,
        created_by = torrent.created_by,
        encoding = torrent.encoding,
        publisher = torrent.publisher,
        publisher_url = torrent.publisher_url,
        comment = torrent.comment,
        status=LoadingStatus.active,
    )
    with Session(engine) as session:
        session.add(db_torrent)
        session.commit()


def remove_torrent(id: int) -> None:
    with Session(engine) as session:
        torrent = session.get(Torrent, id)
        session.delete(torrent)
        session.commit()
        


def stop_torrent(id: int) -> None:
    with Session(engine) as session:
        torrent = session.get(TorrentModel, id)
        torrent.status = LoadingStatus.stopped
        session.commit()


def resume_torrent(id: int) -> None:
    with Session(engine) as session:
        torrent = session.get(TorrentModel, id)
        torrent.status = LoadingStatus.active
        session.commit()


def list_torrents() -> list[Torrent]:
    query = select(TorrentModel)
    torrents: list[Torrent] = []
    with Session(engine) as session:
        db_torrents = session.scalars(query).all()
        for t in db_torrents:
            torrents.append(
                Torrent(
                    announces=t.split(","),
                    info=pickle.loads(t.info),
                    name=t.name,
                    creation_date=t.creation_date,
                    created_by=t.created_by,
                    encoding=t.encoding,
                    publisher=t.publisher,
                    publisher_url=t.publisher_url,
                    comment=t.comment
                )
            ) 

    return torrents    
    