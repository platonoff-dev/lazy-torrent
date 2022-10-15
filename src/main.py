from pathlib import Path
import click


from display.display import render
from meta_file.meta_file import MetaFileInfo
from storage import repository
from torrent import Torrent

@click.group()
def cli() -> None:
    pass

@cli.command
def start() -> None:
    pass

@cli.command
@click.argument(
    "torrent_path",
    required=True,
    type=click.Path(dir_okay=False, exists=True),
)
def download(torrent_path: str) -> None: 
    torrent_file_path = Path(torrent_path)
    meta_info = MetaFileInfo.parse(torrent_file_path)
    repository.add_torrent(Torrent.from_meta_file(meta_info))
    repository.stop_torrent(1)
    repository.resume_torrent(1)

@cli.command
def display() -> None:
    render()

if __name__ == "__main__":
    cli()
