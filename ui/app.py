from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List

from models.player import Player, RepeatMode
from models.song import Song
from data_structures.node import Node
from ui.dialogs import SongDialog, ConfirmDialog

from ui.style import C, REPEAT_ICONS, apply_ttk_styles
from ui.layout import build_ui

class MusicApp(tk.Tk):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.player.add_observer(self._on_player_update)

        self._search_nodes: Optional[List[Node]] = None
        self._highlight_ids: list[str] = []
        self._sort_key_var    = tk.StringVar(value="Tên bài")
        self._search_var      = tk.StringVar()
        self._search_field_var = tk.StringVar(value="Tên bài")

        self._progress_val = tk.DoubleVar(value=0.0)
        self._sim_seconds  = 0
        self._sim_running  = False

        self._setup_window()
        apply_ttk_styles(self)
        build_ui(self)

        self._refresh_song_list()
        self._update_now_playing()

    def _setup_window(self) -> None:
        self.title("🎵 Music Playlist Manager")
        self.configure(bg=C["bg_dark"])
        self.minsize(1100, 650)

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = 1200, 720
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_player_update(self) -> None:
        self._refresh_song_list()
        self._update_controls()
        self._update_now_playing()

    def _refresh_song_list(self, highlight_nodes: Optional[List[Node]] = None) -> None:
        selected_iid = None
        sel = self._tree.selection()
        if sel:
            selected_iid = sel[0]

        self._tree.delete(*self._tree.get_children())

        current_node = self.player.current
        
        nodes_to_display = self.player.songs if highlight_nodes is None else highlight_nodes

        for i, node in enumerate(nodes_to_display):
            song = node.data
            tags = []

            if node is current_node:
                tags = ["now_playing"]
            elif highlight_nodes is not None:
                tags = ["search_hit"]
            else:
                tags = ["even" if i % 2 == 0 else "odd"]

            iid = song.song_id
            self._tree.insert(
                "", tk.END,
                iid=iid,
                values=(i + 1, song.title, song.artist, song.duration_str(), song.genre, song.year),
                tags=tags,
            )

        if selected_iid and self._tree.exists(selected_iid):
            self._tree.selection_set(selected_iid)

        if current_node and self._tree.exists(current_node.data.song_id):
            self._tree.see(current_node.data.song_id)

        n = self.player.total_songs
        d = self.player.total_duration_str
        self._dll_info_label.config(text=f"DLL: {n} nút | Tổng: {d}")

    def _update_now_playing(self) -> None:
        song = self.player.current_song
        if song:
            if getattr(self, "_last_played_song_id", None) != song.song_id:
                self._now_title_label.config(text=song.title)
                self._now_artist_label.config(text=song.artist)
                self._now_info_label.config(text=f"{song.genre}  •  {song.year}")
                self._time_end_label.config(text=song.duration_str())
                self._sim_seconds = 0
                self._progress_val.set(0.0)
                self._time_start_label.config(text="0:00")
                self._last_played_song_id = song.song_id
        else:
            self._now_title_label.config(text="—")
            self._now_artist_label.config(text="Chưa có bài nào được chọn")
            self._now_info_label.config(text="")
            self._time_end_label.config(text="0:00")
            self._progress_val.set(0.0)
            self._last_played_song_id = None

    def _update_controls(self) -> None:
        if self.player.is_shuffled:
            self._shuffle_btn.config(fg=C["accent_light"])
        else:
            self._shuffle_btn.config(fg=C["text_muted"])

        icon, color = REPEAT_ICONS[self.player.repeat_mode]
        self._repeat_btn.config(text=icon, fg=color)

    def _set_status(self, msg: str, color: str = None) -> None:
        self._status_label.config(text=msg, fg=color or C["text_muted"])

    def _tick_progress(self) -> None:
        if not self._sim_running:
            return

        song = self.player.current_song
        if song and song.duration > 0:
            self._sim_seconds = min(self._sim_seconds + 1, song.duration)
            pct = (self._sim_seconds / song.duration) * 100
            self._progress_val.set(pct)

            m = self._sim_seconds // 60
            s = self._sim_seconds % 60
            self._time_start_label.config(text=f"{m}:{s:02d}")

            if self._sim_seconds >= song.duration:
                self._sim_seconds = 0
                self.player.next_song()

        self.after(1000, self._tick_progress)

    def _on_double_click(self, event) -> None:
        node = self._get_selected_node()
        if node:
            self.player.play(node)
            self._sim_seconds = 0
            if not self._sim_running:
                self._sim_running = True
                self._tick_progress()
            self._play_btn.config(text="⏸")
            self._set_status(f"▶  Đang phát: {node.data.title} — {node.data.artist}", C["success"])

    def _on_select(self, event) -> None:
        pass

    def _on_header_click(self, column: str) -> None:
        self._sort_key_var.set(column)
        self._on_sort()

    def _get_selected_node(self) -> Optional[Node]:
        sel = self._tree.selection()
        if not sel:
            return None
        song_id = sel[0]
        return self.player.songs.find_by_id(song_id)

    def _on_add_song(self) -> None:
        dlg = SongDialog(self, title="➕  Thêm bài hát mới")
        if dlg.result:
            song = Song(**dlg.result)
            node = self.player.add_song(song)
            self._set_status(f"✓  Đã thêm: {song.title} — {song.artist}", C["success"])

    def _on_edit_song(self) -> None:
        node = self._get_selected_node()
        if not node:
            messagebox.showinfo("Chưa chọn bài", "Vui lòng chọn bài hát cần sửa!")
            return
        dlg = SongDialog(self, title="✏️  Chỉnh sửa bài hát", song=node.data)
        if dlg.result:
            self.player.edit_song(node, **dlg.result)
            self._set_status(f"✓  Đã cập nhật: {node.data.title}", C["success"])

    def _on_delete_song(self) -> None:
        node = self._get_selected_node()
        if not node:
            messagebox.showinfo("Chưa chọn bài", "Vui lòng chọn bài hát cần xóa!")
            return
        dlg = ConfirmDialog(self, title="Xác nhận xóa", message=f'Bạn có chắc muốn xóa bài\n"{node.data.title}"?')
        if dlg.result:
            song = self.player.remove_song(node)
            self._set_status(f"🗑  Đã xóa: {song.title}", C["danger"])

    def _on_play_selected(self) -> None:
        node = self._get_selected_node()
        if not node:
            node = self.player.songs.head
        if node:
            self.player.play(node)
            self._sim_seconds = 0
            if not self._sim_running:
                self._sim_running = True
                self._tick_progress()
            self._play_btn.config(text="⏸")
            self._set_status(f"▶  Đang phát: {node.data.title} — {node.data.artist}", C["success"])

    def _on_play_pause(self) -> None:
        selected = self._get_selected_node()
        # Nếu người dùng đã chọn một bài và bài đó KHÁC với bài đang phát
        if selected and selected is not self.player.current:
            self.player.play(selected)
            self._sim_seconds = 0
            if not self._sim_running:
                self._sim_running = True
                self._tick_progress()
            self._play_btn.config(text="⏸")
            self._set_status(f"▶  Đang phát: {selected.data.title}", C["success"])
            return

        if self.player.current is None:
            node = selected if selected else self.player.songs.head
            if node:
                self.player.play(node)
                self._sim_seconds = 0
                if not self._sim_running:
                    self._sim_running = True
                    self._tick_progress()
                self._play_btn.config(text="⏸")
                self._set_status(f"▶  Đang phát: {node.data.title}", C["success"])
        else:
            self._sim_running = not self._sim_running
            if self._sim_running:
                self._play_btn.config(text="⏸")
                self._tick_progress()
                self._set_status("▶  Tiếp tục phát", C["success"])
            else:
                self._play_btn.config(text="▶")
                self._set_status("⏸  Tạm dừng", C["text_muted"])

    def _on_next(self) -> None:
        node = self.player.next_song()
        self._sim_seconds = 0
        if node:
            if not self._sim_running:
                self._sim_running = True
                self._tick_progress()
            self._play_btn.config(text="⏸")
            self._set_status(f"⏭  Next: {node.data.title} — {node.data.artist}", C["accent_light"])
        else:
            self._set_status("Đã hết playlist", C["text_muted"])

    def _on_previous(self) -> None:
        node = self.player.previous_song()
        self._sim_seconds = 0
        if node:
            if not self._sim_running:
                self._sim_running = True
                self._tick_progress()
            self._play_btn.config(text="⏸")
            self._set_status(f"⏮  Previous: {node.data.title} — {node.data.artist}", C["accent_light"])

    def _on_shuffle(self) -> None:
        is_on = self.player.toggle_shuffle()
        status = "🔀  Shuffle BẬT" if is_on else "🔀  Shuffle TẮT (khôi phục thứ tự)"
        self._set_status(status, C["accent_light"] if is_on else C["text_muted"])

    def _on_repeat(self) -> None:
        mode = self.player.toggle_repeat()
        labels = {
            RepeatMode.NONE: "🔁  Repeat TẮT",
            RepeatMode.ONE:  "🔂  Repeat 1 bài",
            RepeatMode.ALL:  "🔁  Repeat toàn bộ",
        }
        self._set_status(labels[mode], C["accent_light"])

    def _on_search_change(self, *args) -> None:
        keyword = self._search_var.get().strip()
        if not keyword:
            self._refresh_song_list()
            self._set_status("Sẵn sàng")
            return

        field_vn = self._search_field_var.get()
        field_map = {"Tên bài": "title", "Ca sĩ": "artist", "Thể loại": "genre"}
        field = field_map.get(field_vn, "title")
        
        results = self.player.search(keyword, field)
        self._refresh_song_list(highlight_nodes=results)

        if results:
            self._set_status(f"🔍  Tìm thấy {len(results)} kết quả cho '{keyword}' trong [{field_vn}]", C["accent_light"])
        else:
            self._set_status(f"🔍  Không tìm thấy kết quả cho '{keyword}'", C["danger"])

    def _on_sort(self) -> None:
        key_vn  = self._sort_key_var.get()
        key_map = {"Tên bài": "title", "Ca sĩ": "artist", "Thời lượng": "duration", "Năm": "year"}
        key = key_map.get(key_vn, "title")

        result = self.player.sort(key, "merge")

        self._set_status(f"▲  Đã sắp xếp theo [{key_vn}] | {result['count']} bài | {result['time_ms']} ms", C["warning"])

    def _on_close(self) -> None:
        self._sim_running = False
        self.destroy()
