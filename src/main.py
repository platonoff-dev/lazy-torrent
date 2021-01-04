from pathlib import Path

import click
from rich.prompt import Confirm

from display import display_torrent_info
from torrent import Torrent


@click.command()
@click.argument(
    "torrent_path",
    required=True,
    type=click.Path(dir_okay=False, exists=True),
)
def main(torrent_path: str) -> None:
    torrent_file = Path(torrent_path)
    torrent = Torrent(torrent_file)
    display_torrent_info(torrent)
    allow_download = Confirm.ask("Allow download of this torrent", default="y")
    if allow_download:
        torrent.download()
    else:
        print("Downloading aborted!")


if __name__ == "__main__":
    main()
