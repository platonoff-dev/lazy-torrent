import time

from rich.table import Table
from rich.live import Live

from meta_file.meta_file import MetaFileInfo

def generate_table(torrents: list[MetaFileInfo]) -> Table:
    table = Table(expand=True)
    table.add_column("Name")
    table.add_column("Size")
    table.add_column("Status")
    table.add_column("Speed")
    table.add_column("Seeds/Peers")

    for torrent in torrents:
        table.add_row(
            torrent.name,
            str(torrent.size),
            "ACTIVE",  # TODO: use actual data
            "0 MiB/s",  # TODO: use actual data
            "0.0", # TODO: use actual data
        )

    return table


def render() -> None:
    table = generate_table()

    with Live(table, screen=True) as live:
        for _ in range(40):
            time.sleep(0.4)
