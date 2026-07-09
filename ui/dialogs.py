from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.song import Song


COLORS = {
    "bg_dark":    "#0D0D1A",
    "bg_card":    "#1A1A2E",
    "bg_input":   "#16213E",
    "accent":     "#7C3AED",
    "accent_hover":"#6D28D9",
    "text_white": "#F0F0FF",
    "text_muted": "#8888AA",
    "border":     "#2D2D4E",
    "success":    "#10B981",
    "danger":     "#EF4444",
}

FONT_FAMILY = "Segoe UI"


class SongDialog(tk.Toplevel):
    def __init__(self, parent, title: str = "Thêm bài hát",
                 song: Optional["Song"] = None):
        super().__init__(parent)
        self.result = None
        self._song = song

        self.title(title)
        self.configure(bg=COLORS["bg_dark"])
        self.resizable(False, False)
        self.grab_set()  # Modal

        self.geometry(self._center_geometry(parent, 480, 500))

        self._build_ui(title)
        self._fill_existing(song)

        self.bind("<Return>", lambda e: self._on_confirm())
        self.bind("<Escape>", lambda e: self._on_cancel())

        self.wait_window()

    def _center_geometry(self, parent, w: int, h: int) -> str:
        parent.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        return f"{w}x{h}+{x}+{y}"

    def _build_ui(self, dialog_title: str) -> None:
        header = tk.Frame(self, bg=COLORS["accent"], pady=16)
        header.pack(fill=tk.X)
        tk.Label(
            header, text=f"🎵  {dialog_title}",
            bg=COLORS["accent"], fg=COLORS["text_white"],
            font=(FONT_FAMILY, 14, "bold")
        ).pack()

        body = tk.Frame(self, bg=COLORS["bg_dark"], padx=28, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("Tên bài hát *", "title",    "Nhập tên bài hát..."),
            ("Ca sĩ / Nghệ sĩ *", "artist", "Nhập tên ca sĩ..."),
            ("Thời lượng (giây) *", "duration", "Ví dụ: 210"),
            ("Thể loại", "genre",   "Pop, Rock, R&B..."),
            ("Năm phát hành", "year", "Ví dụ: 2024"),
        ]

        self._entries: dict[str, tk.Entry] = {}

        for label_text, field_key, placeholder in fields:
            tk.Label(
                body, text=label_text,
                bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
                font=(FONT_FAMILY, 9),
                anchor="w"
            ).pack(fill=tk.X, pady=(8, 2))

            entry_frame = tk.Frame(body, bg=COLORS["border"], pady=1, padx=1)
            entry_frame.pack(fill=tk.X)

            entry = tk.Entry(
                entry_frame,
                bg=COLORS["bg_input"],
                fg=COLORS["text_white"],
                insertbackground=COLORS["accent"],
                relief=tk.FLAT,
                font=(FONT_FAMILY, 10),
                bd=6,
            )
            entry.pack(fill=tk.X)

            entry._placeholder = placeholder
            entry._has_placeholder = True
            entry.insert(0, placeholder)
            entry.config(fg=COLORS["text_muted"])

            def on_focus_in(e, ent=entry):
                if ent._has_placeholder:
                    ent.delete(0, tk.END)
                    ent.config(fg=COLORS["text_white"])
                    ent._has_placeholder = False

            def on_focus_out(e, ent=entry):
                if not ent.get():
                    ent.insert(0, ent._placeholder)
                    ent.config(fg=COLORS["text_muted"])
                    ent._has_placeholder = True

            entry.bind("<FocusIn>",  on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

            self._entries[field_key] = entry

        btn_frame = tk.Frame(self, bg=COLORS["bg_dark"], padx=28, pady=16)
        btn_frame.pack(fill=tk.X)

        cancel_btn = tk.Button(
            btn_frame, text="Hủy",
            bg=COLORS["bg_card"], fg=COLORS["text_muted"],
            activebackground=COLORS["border"], activeforeground=COLORS["text_white"],
            relief=tk.FLAT, font=(FONT_FAMILY, 10),
            padx=20, pady=8, cursor="hand2",
            command=self._on_cancel,
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(8, 0))

        confirm_btn = tk.Button(
            btn_frame, text="✓  Xác nhận",
            bg=COLORS["accent"], fg=COLORS["text_white"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_white"],
            relief=tk.FLAT, font=(FONT_FAMILY, 10, "bold"),
            padx=20, pady=8, cursor="hand2",
            command=self._on_confirm,
        )
        confirm_btn.pack(side=tk.RIGHT)

        for btn, hover_bg, normal_bg in [
            (cancel_btn, COLORS["border"], COLORS["bg_card"]),
            (confirm_btn, COLORS["accent_hover"], COLORS["accent"]),
        ]:
            btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=normal_bg: b.config(bg=c))

    def _fill_existing(self, song: Optional["Song"]) -> None:
        if song is None:
            return

        def set_field(key: str, value: str):
            entry = self._entries[key]
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
            entry.config(fg=COLORS["text_white"])
            entry._has_placeholder = False

        set_field("title",    song.title)
        set_field("artist",   song.artist)
        set_field("duration", song.duration)
        set_field("genre",    song.genre)
        set_field("year",     song.year)

    def _get_value(self, key: str) -> str:
        entry = self._entries[key]
        if entry._has_placeholder:
            return ""
        return entry.get().strip()

    def _on_confirm(self) -> None:
        title, artist, dur_str = (self._get_value(k) for k in ("title", "artist", "duration"))

        for val, name in [(title, "tên bài hát"), (artist, "tên ca sĩ"), (dur_str, "thời lượng")]:
            if not val:
                messagebox.showwarning("Thiếu thông tin", f"Vui lòng nhập {name}!", parent=self)
                return

        try:
            duration = int(dur_str)
            if duration <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Lỗi", "Thời lượng phải là số nguyên dương!", parent=self)
            return

        year_str = self._get_value("year")
        self.result = {
            "title": title, "artist": artist, "duration": duration,
            "genre": self._get_value("genre") or "Unknown",
            "year": int(year_str) if year_str.isdigit() else 2024
        }
        self.destroy()

    def _on_cancel(self) -> None:
        self.result = None
        self.destroy()


class ConfirmDialog(tk.Toplevel):
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent)
        self.result = False
        self.title(title)
        self.configure(bg=COLORS["bg_dark"])
        self.resizable(False, False)
        self.grab_set()

        w, h = 380, 180
        parent.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Icon + message
        inner = tk.Frame(self, bg=COLORS["bg_dark"], padx=24, pady=20)
        inner.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            inner, text="⚠️  " + message,
            bg=COLORS["bg_dark"], fg=COLORS["text_white"],
            font=(FONT_FAMILY, 10), wraplength=330, justify=tk.LEFT
        ).pack(anchor="w")

        btn_frame = tk.Frame(inner, bg=COLORS["bg_dark"])
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(16, 0))

        no_btn = tk.Button(
            btn_frame, text="Hủy",
            bg=COLORS["bg_card"], fg=COLORS["text_muted"],
            relief=tk.FLAT, font=(FONT_FAMILY, 10),
            padx=16, pady=6, cursor="hand2",
            command=lambda: self._close(False)
        )
        no_btn.pack(side=tk.RIGHT, padx=(8, 0))

        yes_btn = tk.Button(
            btn_frame, text="Xác nhận xóa",
            bg=COLORS["danger"], fg=COLORS["text_white"],
            activebackground="#DC2626",
            relief=tk.FLAT, font=(FONT_FAMILY, 10, "bold"),
            padx=16, pady=6, cursor="hand2",
            command=lambda: self._close(True)
        )
        yes_btn.pack(side=tk.RIGHT)

        self.bind("<Escape>", lambda e: self._close(False))
        self.wait_window()

    def _close(self, value: bool) -> None:
        self.result = value
        self.destroy()
