import tkinter as tk
from tkinter import ttk
from ui.style import C, FONT, MONO, make_btn

def build_ui(app) -> None:
    build_header(app)

    main = tk.Frame(app, bg=C["bg_dark"])
    main.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))
    main.columnconfigure(0, weight=3)
    main.columnconfigure(1, weight=2)
    main.rowconfigure(0, weight=1)

    build_left_panel(app, main)
    build_right_panel(app, main)
    build_status_bar(app)

def build_header(app) -> None:
    header = tk.Frame(app, bg=C["bg_card"], height=64)
    header.pack(fill=tk.X)
    header.pack_propagate(False)

    inner = tk.Frame(header, bg=C["bg_card"])
    inner.pack(side=tk.LEFT, fill=tk.Y, padx=20)

    tk.Label(
        inner, text="🎵",
        bg=C["bg_card"], fg=C["accent_light"],
        font=(FONT, 22),
    ).pack(side=tk.LEFT, pady=12)

    tk.Label(
        inner, text="Music Playlist Manager",
        bg=C["bg_card"], fg=C["text_white"],
        font=(FONT, 16, "bold"),
    ).pack(side=tk.LEFT, padx=(6, 0), pady=12)

    sep = tk.Frame(app, bg=C["border"], height=1)
    sep.pack(fill=tk.X)

def build_left_panel(app, parent: tk.Frame) -> None:
    left = tk.Frame(parent, bg=C["bg_dark"])
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=8)
    left.rowconfigure(1, weight=1)
    left.columnconfigure(0, weight=1)

    build_toolbar(app, left)
    build_song_list(app, left)
    build_song_actions(app, left)

def build_toolbar(app, parent: tk.Frame) -> None:
    toolbar = tk.Frame(parent, bg=C["bg_card"], pady=10, padx=12)
    toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 6))

    tk.Label(toolbar, text="🔍", bg=C["bg_card"], fg=C["accent_light"], font=(FONT, 12)).pack(side=tk.LEFT)

    search_frame = tk.Frame(toolbar, bg=C["border"], padx=1, pady=1)
    search_frame.pack(side=tk.LEFT, padx=(4, 0))

    app._search_entry = tk.Entry(
        search_frame, textvariable=app._search_var,
        bg=C["bg_input"], fg=C["text_white"],
        insertbackground=C["accent"], relief=tk.FLAT, font=(FONT, 10),
        width=22, bd=6,
    )
    app._search_entry.pack()
    app._search_var.trace_add("write", app._on_search_change)

    field_cb = ttk.Combobox(
        toolbar, textvariable=app._search_field_var,
        values=["Tên bài", "Ca sĩ", "Thể loại"],
        state="readonly", style="Dark.TCombobox", width=9, font=(FONT, 9),
    )
    field_cb.pack(side=tk.LEFT, padx=(4, 12))

    tk.Frame(toolbar, bg=C["border"], width=1, height=24).pack(side=tk.LEFT, padx=8, fill=tk.Y)

    tk.Label(toolbar, text="Sắp xếp theo:", bg=C["bg_card"], fg=C["text_muted"], font=(FONT, 9)).pack(side=tk.LEFT)

    sort_key_cb = ttk.Combobox(
        toolbar, textvariable=app._sort_key_var,
        values=["Tên bài", "Ca sĩ", "Thời lượng", "Năm"],
        state="readonly", style="Dark.TCombobox", width=10, font=(FONT, 9),
    )
    sort_key_cb.pack(side=tk.LEFT, padx=4)

    make_btn(toolbar, "▲  Sắp xếp", C["accent"], app._on_sort).pack(side=tk.LEFT, padx=(8, 0))

def build_song_list(app, parent: tk.Frame) -> None:
    list_frame = tk.Frame(parent, bg=C["bg_dark"])
    list_frame.grid(row=1, column=0, sticky="nsew")
    list_frame.rowconfigure(0, weight=1)
    list_frame.columnconfigure(0, weight=1)

    columns = ("no", "title", "artist", "duration", "genre", "year")
    app._tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Song.Treeview", selectmode="browse")

    col_config = [
        ("no",       "#",          40,  tk.CENTER),
        ("title",    "🎵  Tên bài hát", 240, tk.W),
        ("artist",   "🎤  Ca sĩ",   150, tk.W),
        ("duration", "⏱  Thời lượng", 90, tk.CENTER),
        ("genre",    "🎸  Thể loại",  110, tk.W),
        ("year",     "📅  Năm",       60,  tk.CENTER),
    ]
    for col_id, heading, width, anchor in col_config:
        app._tree.heading(col_id, text=heading, command=lambda c=col_id: app._on_header_click(c))
        app._tree.column(col_id, width=width, anchor=anchor, minwidth=40, stretch=(col_id == "title"))

    app._tree.tag_configure("odd", background=C["bg_row_alt"])
    app._tree.tag_configure("even", background=C["bg_card"])
    app._tree.tag_configure("now_playing", background=C["accent"], foreground=C["text_white"], font=(FONT, 10, "bold"))
    app._tree.tag_configure("search_hit", background="#1E3A5F", foreground=C["accent_light"])

    vsb = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=app._tree.yview, style="Dark.Vertical.TScrollbar")
    app._tree.configure(yscrollcommand=vsb.set)

    app._tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    app._tree.bind("<Double-1>", app._on_double_click)
    app._tree.bind("<<TreeviewSelect>>", app._on_select)

def build_song_actions(app, parent: tk.Frame) -> None:
    action_bar = tk.Frame(parent, bg=C["bg_card"], pady=8, padx=12)
    action_bar.grid(row=2, column=0, sticky="ew", pady=(6, 0))

    buttons = [
        ("➕  Thêm bài",   C["accent"],  app._on_add_song),
        ("✏️  Sửa",        C["bg_input"], app._on_edit_song),
        ("🗑  Xóa",        C["danger"],   app._on_delete_song),
        ("▶  Phát ngay",  C["success"],  app._on_play_selected),
    ]

    for text, color, cmd in buttons:
        make_btn(action_bar, text, color, cmd).pack(side=tk.LEFT, padx=4)

    app._dll_info_label = tk.Label(action_bar, text="", bg=C["bg_card"], fg=C["text_muted"], font=(FONT, 8))
    app._dll_info_label.pack(side=tk.RIGHT, padx=8)

def build_right_panel(app, parent: tk.Frame) -> None:
    right = tk.Frame(parent, bg=C["bg_dark"])
    right.grid(row=0, column=1, sticky="nsew", pady=8)
    right.columnconfigure(0, weight=1)

    build_now_playing(app, right)
    build_player_controls(app, right)

def build_now_playing(app, parent: tk.Frame) -> None:
    card = tk.Frame(parent, bg=C["bg_card"], pady=16, padx=16)
    card.grid(row=0, column=0, sticky="ew", pady=(0, 6))

    app._album_art_label = tk.Label(
        card, text="🎵", bg=C["accent"], fg=C["text_white"],
        font=(FONT, 32), width=3, height=1, relief=tk.FLAT,
    )
    app._album_art_label.pack()

    tk.Label(card, text="ĐANG PHÁT", bg=C["bg_card"], fg=C["text_dim"], font=(FONT, 7, "bold")).pack(pady=(10, 2))

    app._now_title_label = tk.Label(card, text="—", bg=C["bg_card"], fg=C["text_white"], font=(FONT, 13, "bold"), wraplength=260)
    app._now_title_label.pack()

    app._now_artist_label = tk.Label(card, text="", bg=C["bg_card"], fg=C["accent_light"], font=(FONT, 10))
    app._now_artist_label.pack(pady=(2, 0))

    app._now_info_label = tk.Label(card, text="", bg=C["bg_card"], fg=C["text_muted"], font=(FONT, 8))
    app._now_info_label.pack(pady=(2, 10))

    prog_frame = tk.Frame(card, bg=C["bg_card"])
    prog_frame.pack(fill=tk.X, pady=(4, 0))

    app._time_start_label = tk.Label(prog_frame, text="0:00", bg=C["bg_card"], fg=C["text_muted"], font=(MONO, 8))
    app._time_start_label.pack(side=tk.LEFT)

    app._progress_bar = ttk.Progressbar(prog_frame, variable=app._progress_val, maximum=100, style="NowPlaying.Horizontal.TProgressbar")
    app._progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)

    app._time_end_label = tk.Label(prog_frame, text="0:00", bg=C["bg_card"], fg=C["text_muted"], font=(MONO, 8))
    app._time_end_label.pack(side=tk.RIGHT)

def build_player_controls(app, parent: tk.Frame) -> None:
    ctrl = tk.Frame(parent, bg=C["bg_card"], pady=12)
    ctrl.grid(row=1, column=0, sticky="ew", pady=(0, 6))

    ctrl_inner = tk.Frame(ctrl, bg=C["bg_card"])
    ctrl_inner.pack()

    app._shuffle_btn = tk.Button(
        ctrl_inner, text="🔀", bg=C["bg_card"], fg=C["text_muted"],
        activebackground=C["bg_card"], relief=tk.FLAT, font=(FONT, 14),
        cursor="hand2", bd=0, command=app._on_shuffle,
    )
    app._shuffle_btn.grid(row=0, column=0, padx=8)

    prev_btn = tk.Button(
        ctrl_inner, text="⏮", bg=C["bg_card"], fg=C["text_white"],
        activebackground=C["border"], relief=tk.FLAT, font=(FONT, 18),
        cursor="hand2", bd=0, command=app._on_previous,
    )
    prev_btn.grid(row=0, column=1, padx=4)

    app._play_btn = tk.Button(
        ctrl_inner, text="▶", bg=C["accent"], fg=C["text_white"],
        activebackground=C["accent_hover"], activeforeground=C["text_white"],
        relief=tk.FLAT, font=(FONT, 16, "bold"), cursor="hand2", bd=0,
        width=3, pady=6, command=app._on_play_pause,
    )
    app._play_btn.grid(row=0, column=2, padx=8)

    next_btn = tk.Button(
        ctrl_inner, text="⏭", bg=C["bg_card"], fg=C["text_white"],
        activebackground=C["border"], relief=tk.FLAT, font=(FONT, 18),
        cursor="hand2", bd=0, command=app._on_next,
    )
    next_btn.grid(row=0, column=3, padx=4)

    app._repeat_btn = tk.Button(
        ctrl_inner, text="🔁", bg=C["bg_card"], fg=C["text_muted"],
        activebackground=C["bg_card"], relief=tk.FLAT, font=(FONT, 14),
        cursor="hand2", bd=0, command=app._on_repeat,
    )
    app._repeat_btn.grid(row=0, column=4, padx=8)

def build_status_bar(app) -> None:
    sb = tk.Frame(app, bg=C["bg_dark"], pady=4, padx=12)
    sb.pack(fill=tk.X, side=tk.BOTTOM)

    tk.Frame(sb, bg=C["border"], height=1).pack(fill=tk.X, pady=(0, 4))

    app._status_label = tk.Label(sb, text="Sẵn sàng", bg=C["bg_dark"], fg=C["text_muted"], font=(FONT, 8), anchor="w")
    app._status_label.pack(side=tk.LEFT)

