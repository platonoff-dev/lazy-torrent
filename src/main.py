from pathlib import Path
import click


from display.display import render
from torrent import TorrentInfo
from storage import repository

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
    torrent = TorrentInfo.parse(torrent_file_path)
    repository.add_torrent(torrent)

@cli.command
def display() -> None:
    render()

if __name__ == "__main__":
    cli()
