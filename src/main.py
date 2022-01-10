import asyncio
from pathlib import Path

import click
from rich.prompt import Confirm

import tracker
from display import display_torrent_info
from torrent import Torrent


@click.command()
@click.argument(
    "torrent_path",
    required=True,
    type=click.Path(dir_okay=False, exists=True),
)
@click.option(
    "-y",
    "--yes",
    is_flag=True,
)
def main(torrent_path: str, yes: bool) -> None:
    torrent_file_path = Path(torrent_path)
    torrent = Torrent.parse(torrent_file_path)
    display_torrent_info(torrent)
    if not yes:
        allow_download = Confirm.ask("Allow download of this torrent", default="y")
        if not allow_download:
            print("Downloading aborted!")
            return

    http_tracker = tracker.HTTTPTracker(torrent)
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(http_tracker.connect())


if __name__ == "__main__":
    main()
