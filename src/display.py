from datetime import datetime
from typing import Dict, List

from rich import print

from torrent import Torrent


def generate_file_tree(dir_structure: Dict[str, dict], parent_prefix: str = "") -> str:
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
    dimensions = ["B", "KiB", "Mib", "GiB", "TiB"]

    current_dim = 0
    size = float(number_bytes)
    while size > 1024:
        size /= 1024
        current_dim += 1

    return f"{number_bytes:.3f} {dimensions[current_dim]}"


def display_torrent_info(torrent: Torrent) -> None:
    created_at = datetime.fromtimestamp(torrent.info["creation date"])
    files = []
    if torrent.info["info"].get("files"):
        files += ["/".join(file["path"]) for file in torrent.info["info"]["files"]]
    else:
        files.append(torrent.info["info"]["name"])
    file_structure = _generate_directory_tree(torrent.info["info"]["name"], files)
    print(
        f"[yellow bold]Torrent: [green]{torrent.info['info']['name']} \"{torrent.info['comment']}\""
    )
    print(f"[yellow bold]Tracker: [green]{torrent.info['announce']}")
    print(f"[yellow bold]Created: [green]{torrent.info['created by']} ({created_at})")
    print(f"[yellow bold]Publisher: [green]{torrent.info.get('publisher')}")
    print(f"[yellow bold]Size: [green]{_generate_size(torrent.size)}")
    print(f"[yellow bold]Files: \n[green]{generate_file_tree(file_structure)}")
