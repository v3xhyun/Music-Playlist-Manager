import tkinter as tk
from tkinter import ttk
from models.player import RepeatMode

C = {
    "bg_dark":     "#0D0D1A",
    "bg_card":     "#1A1A2E",
    "bg_input":    "#16213E",
    "bg_row_alt":  "#14142B",
    "accent":      "#7C3AED",
    "accent_light":"#A78BFA",
    "accent_hover":"#6D28D9",
    "now_playing": "#F59E0B",
    "text_white":  "#F0F0FF",
    "text_muted":  "#8888AA",
    "text_dim":    "#555577",
    "border":      "#2D2D4E",
    "success":     "#10B981",
    "danger":      "#EF4444",
    "warning":     "#F59E0B",
    "gradient1":   "#7C3AED",
    "gradient2":   "#DB2777",
}

FONT  = "Segoe UI"
MONO  = "Consolas"

REPEAT_ICONS = {
    RepeatMode.NONE: ("🔁", C["text_muted"]),
    RepeatMode.ONE:  ("🔂", C["accent_light"]),
    RepeatMode.ALL:  ("🔁", C["accent_light"]),
}

def apply_ttk_styles(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "Song.Treeview",
        background=C["bg_card"],
        foreground=C["text_white"],
        fieldbackground=C["bg_card"],
        rowheight=36,
        font=(FONT, 10),
        borderwidth=0,
    )
    style.configure(
        "Song.Treeview.Heading",
        background=C["bg_dark"],
        foreground=C["text_muted"],
        font=(FONT, 9, "bold"),
        relief=tk.FLAT,
        borderwidth=0,
    )
    style.map(
        "Song.Treeview",
        background=[("selected", C["accent"])],
        foreground=[("selected", C["text_white"])],
    )
    style.map("Song.Treeview.Heading",
              background=[("active", C["border"])])

    style.configure(
        "Dark.Vertical.TScrollbar",
        background=C["border"],
        troughcolor=C["bg_dark"],
        arrowcolor=C["text_muted"],
        borderwidth=0,
    )

    style.configure(
        "Dark.TCombobox",
        fieldbackground=C["bg_input"],
        background=C["bg_input"],
        foreground=C["text_white"],
        arrowcolor=C["accent_light"],
        bordercolor=C["border"],
        darkcolor=C["bg_input"],
        lightcolor=C["bg_input"],
    )
    style.map("Dark.TCombobox",
              fieldbackground=[("readonly", C["bg_input"])],
              background=[("readonly", C["bg_input"])])

    style.configure(
        "NowPlaying.Horizontal.TProgressbar",
        background=C["accent"],
        troughcolor=C["border"],
        borderwidth=0,
        thickness=4,
    )

def darken(hex_color: str, amount: int = 20) -> str:
    try:
        r = max(0, int(hex_color[1:3], 16) - amount)
        g = max(0, int(hex_color[3:5], 16) - amount)
        b = max(0, int(hex_color[5:7], 16) - amount)
        return f"#{r:02X}{g:02X}{b:02X}"
    except Exception:
        return hex_color

def make_btn(parent, text: str, color: str, command) -> tk.Button:
    btn = tk.Button(
        parent, text=text,
        bg=color, fg=C["text_white"],
        activebackground=color,
        activeforeground=C["text_white"],
        relief=tk.FLAT,
        font=(FONT, 9, "bold"),
        padx=10, pady=5,
        cursor="hand2", bd=0,
        command=command,
    )
    btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=darken(c)))
    btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    return btn
