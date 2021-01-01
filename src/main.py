from display import display_torrent_info
from torrent import Torrent

if __name__ == "__main__":
    torrent = Torrent("sniper.torrent")
    display_torrent_info(torrent)
