from meta_file.meta_file import MetaFileInfo


class Torrent:
    def __init__(
        self,
        announces: list[str],
        info: dict,
        name: str,
        creation_date: str | None = None,
        created_by: str | None = None,
        encoding: str | None = None,
        publisher: str | None = None,
        publisher_url: str | None = None,
        comment: str | None = None,
    ) -> None:
        self.announces = announces
        self.info = info
        self.name = name
        self.creation_date = creation_date
        self.created_by = created_by
        self.encoding = encoding
        self.publisher = publisher
        self.publisher_url = publisher_url
        self.comment = comment
    
    @staticmethod
    def from_meta_file(meta_file: MetaFileInfo) -> 'Torrent':
        announces = set()
        announces.add(meta_file.announce)
        if meta_file.announce_list:
            for a in meta_file.announce_list:
                announces.update(a)

        return Torrent(
            announces=list(announces),
            info=meta_file.info,
            name=meta_file.name,
            creation_date=meta_file.creation_date,
            created_by = meta_file.created_by,
            encoding = meta_file.encoding,
            publisher = meta_file.publisher,
            publisher_url = meta_file.publisher_url,
            comment = meta_file.comment,
        )
    