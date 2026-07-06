import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.song import Song
from models.playlist import Playlist
from models.player import Player
from ui.app import MusicApp

SAMPLE_SONGS = [
    Song("Có Chắc Yêu Là Đây",    "Sơn Tùng M-TP",  199, "V-Pop",   2020),
    Song("Waiting For You",         "MONO",            214, "V-Pop",   2022),
    Song("Chạy Ngay Đi",            "Sơn Tùng M-TP",  252, "V-Pop",   2018),
    Song("Người Lạ Ơi",             "Karik & Orange",  248, "V-Pop",  2018),
    Song("Bắt Đầu Từ Hôm Nay",     "Phương Ly",       228, "V-Pop",   2019),
    Song("Từng Quen",               "HIEUTHUHAI",      193, "V-Pop",   2023),
    Song("Nấu Ăn Cho Mà Nghe",     "Pháo",            247, "V-Pop",   2021),
    Song("Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "V.A",   180, "V-Pop",   2015),
    Song("Anh Sẽ Ổn",              "GREY D",          205, "V-Pop",   2020),
    Song("Có Không Giữ Mất Đừng Tìm", "Trịnh Đình Quang", 237, "V-Pop", 2021),
    Song("Blinding Lights",         "The Weeknd",      200, "Synth-pop", 2019),
    Song("As It Was",               "Harry Styles",    167, "Pop",       2022),
    Song("Anti-Hero",               "Taylor Swift",    200, "Pop",       2022),
    Song("Flowers",                 "Miley Cyrus",     200, "Pop",       2023),
    Song("Kill Bill",               "SZA",             153, "R&B",       2022),
    Song("Calm Down",               "Rema & Selena Gomez", 239, "Afrobeats", 2022),
    Song("Unholy",                  "Sam Smith",       156, "Pop",       2022),
    Song("Cruel Summer",            "Taylor Swift",    178, "Pop",       2019),
    Song("Levitating",              "Dua Lipa",        203, "Disco-pop", 2020),
    Song("Shape of You",            "Ed Sheeran",      234, "Pop",       2017),
]


def load_sample_data(player: Player) -> None:
    for song in SAMPLE_SONGS:
        player.add_song(song)


def main() -> None:
    playlist_info = Playlist(
        name="🎵 PTTKGT Playlist — Nhóm 5",
        description="Playlist demo cho bài tập lớn môn Phân Tích Thiết Kế Giải Thuật"
    )
    player = Player(playlist_info)
    load_sample_data(player)
    app = MusicApp(player)
    app.mainloop()


if __name__ == "__main__":
    main()
