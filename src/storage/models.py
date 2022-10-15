import enum
from sqlalchemy import Column, Integer, String, Enum, BLOB, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class LoadingStatus(enum.Enum):
    active = 0
    stopped = 1
    paused = 2


class TorrentModel(Base):  # type: ignore
    __tablename__ = "torrents"

    id = Column(Integer, primary_key=True)
    announces = Column(Text, nullable=False, comment="Coma-separated list of announces")
    info = Column(BLOB, nullable=False)
    name = Column(String(200), nullable=False)
    status = Column(Enum(LoadingStatus), nullable=False)
    creation_date = Column(String(100))
    created_by = Column(String(100))
    encoding = Column(String(20))
    publisher = Column(String(100))
    publisher_url = Column(String(100))
    comment = Column(String(100))
