from pathlib import Path
import asyncio

import click
from rich.prompt import Confirm

from display import display_torrent_info
from torrent import Torrent
from tracker import HTTPTracker


@click.command()
@click.argument(
    "torrent_path",
    required=True,
    type=click.Path(dir_okay=False, exists=True),
)
@click.option(
    "-y", "--yes",
    is_flag=True,

)
def main(torrent_path: str, yes: bool) -> None:
    torrent_file = Path(torrent_path)
    torrent = Torrent(torrent_file)
    display_torrent_info(torrent)
    if not yes:
        allow_download = Confirm.ask("Allow download of this torrent", default="y")
        if not allow_download:
            print("Downloading aborted!")
            return

    tracker = HTTPTracker(torrent)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tracker.fetch())
        

if __name__ == "__main__":
    main()
