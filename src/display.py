from datetime import datetime
from typing import Dict, List

from rich import print

from torrent import Torrent


def generate_file_tree(dir_structure: Dict[str, dict], parent_prefix: str = "") -> str:
    """Generate directory tree string for command line printing based on structure"""
    display_filename_prefix_middle = "├──"
    display_filename_prefix_last = "└──"
    display_parent_prefix_middle = "    "
    display_parent_prefix_last = "│   "
    res = ""
    key_list = list(dir_structure.keys())

    for key, value in dir_structure.items():
        prefix = parent_prefix
        new_parent_prefix = parent_prefix

        if key == key_list[-1]:
            prefix += display_filename_prefix_last
            new_parent_prefix += display_parent_prefix_middle
        else:
            prefix += display_filename_prefix_middle
            new_parent_prefix += display_parent_prefix_last

        res += prefix + key + "\n"
        if value:
            res += generate_file_tree(value, new_parent_prefix)
    return res


def _generate_directory_tree(name: str, files: List[str]) -> Dict[str, dict]:
    tree: Dict[str, dict] = {name: {}}
    root = tree[name]
    for path in files:
        parts = path.split("/")
        current = root
        for part in parts:
            if not current.get(part):
                current[part] = {}
                current = current[part]
    return tree


def _generate_size(number_bytes: int) -> str:
    """Convert count of bytest to human readable for with dimension"""
    dimensions = ["B", "KiB", "Mib", "GiB", "TiB"]

    current_dim = 0
    size = float(number_bytes)
    while size > 1024:
        size /= 1024
        current_dim += 1

    return f"{size:.3f} {dimensions[current_dim]}"


def display_torrent_info(torrent: Torrent) -> None:
    """Pretty print torrent basic info for confirmation of download"""
    created_at = datetime.fromtimestamp(torrent.creation_date)
    files = []
    if torrent.info.get("files"):
        files += ["/".join(file["path"]) for file in torrent.info["files"]]
    else:
        files.append(torrent.info["name"])
    file_structure = _generate_directory_tree(torrent.info["name"], files)

    print(f'[yellow bold]Torrent: [green]{torrent.name} "{torrent.comment}"')
    print(f"[yellow bold]Tracker: [green]{torrent.announce}")
    print(f"[yellow bold]Created: [green]{torrent.created_by} ({created_at})")
    print(f"[yellow bold]Publisher: [green]{torrent.publisher}")
    print(f"[yellow bold]Size: [green]{_generate_size(torrent.size)}")
    print(f"[yellow bold]Files: \n[green]{generate_file_tree(file_structure)}")
