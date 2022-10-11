from sqlalchemy import Column, Integer, VARCHAR, String, JSON, PickleType
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Torrent(Base):
    __tablename__ = "torrents"

    id = Column(Integer, primary_key=True)
    announce = Column(String(500), nullable=False)
    info = Column(PickleType, nullable=False)
    name = Column(String(200), nullable=False)
    announce_list = Column(PickleType)
    creation_date = Column(String(100))
    created_by = Column(String(100))
    encoding = Column(String(100))
    publisher = Column(String(100))
    publisher_url = Column(String(100))
    comment = Column(String(100))
