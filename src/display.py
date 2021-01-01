from datetime import datetime
from typing import Dict

from rich import print

from torrent import Torrent

# def generate_file_tree(dir_structure: Dict[str, dict]):
#     display_filename_prefix_middle = "├──"
#     display_filename_prefix_last = "└──"
#     display_parent_prefix_middle = "    "
#     display_parent_prefix_last = "│   "
# TODO: Finish tree string generator


def _generate_directory_tree(torrent: Torrent) -> Dict[str, dict]:
    name = torrent.info["info"]["name"]
    files = []
    if torrent.info["info"].get("files"):
        files += [file["path"][0] for file in torrent.info["info"]["files"]]
    else:
        files.append(torrent.info["info"]["name"])

    tree: Dict[str, dict] = {name: {}}
    root = tree[name]
    for path in files:
        parts = path.split("/")
        current = root
        for part in parts:
            if not current.get(part):
                current[part] = {}
    return tree


def display_torrent_info(torrent: Torrent) -> None:
    created_at = datetime.fromtimestamp(torrent.info["creation date"])
    files = []
    if torrent.info["info"].get("files"):
        files += [file["path"][0] for file in torrent.info["info"]["files"]]
    else:
        files.append(torrent.info["info"]["name"])

    print(
        f"[yellow bold]Torrent: [green]{torrent.info['info']['name']} \"{torrent.info['comment']}\""
    )
    print(f"[yellow bold]Tracker: [green]{torrent.info['announce']}")
    print(f"[yellow bold]Created: [green]{torrent.info['created by']} ({created_at})")
    print(f"[yellow bold]Publisher: [green]{torrent.info.get('publisher')}")
    print(f"[yellow bold]Files: \n\t[green]{files}")
