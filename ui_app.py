"""
ui_app.py
---------
CustomTkinter GUI entry point for JARVIS.

All business logic lives in the original modules:
    gemini.py | notes_manager.py | web_commands.py
    listener.py | speaker.py

This file only handles presentation and user interaction.
Run this instead of main.py for the GUI experience.
"""

import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import customtkinter as ctk

# ── Core business modules (untouched) ────────────────────────────
from config import Config
from gemini import GeminiEngine
from notes_manager import NotesManager
from web_commands import WebCommands
from listener import VoiceListener
from speaker import VoiceSpeaker
from logger import logger

# ── Theme ─────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Color palette ─────────────────────────────────────────────────
COLORS = {
    "bg_primary":    "#0a0a12",
    "bg_secondary":  "#111122",
    "bg_tertiary":   "#1a1a2e",
    "bg_card":       "#16213e",
    "accent":        "#7c3aed",
    "accent_hover":  "#9f67fa",
    "accent_light":  "#2d1b69",
    "user_bubble":   "#1e3a5f",
    "ai_bubble":     "#1a1a2e",
    "success":       "#22c55e",
    "danger":        "#ef4444",
    "warning":       "#f59e0b",
    "text_primary":  "#f1f5f9",
    "text_muted":    "#64748b",
    "text_accent":   "#a78bfa",
    "border":        "#1e1e3f",
}

FONT_FAMILY = "Segoe UI" if sys.platform == "win32" else "SF Pro Display"


# ══════════════════════════════════════════════════════════════════
#  HELPER WIDGETS
# ══════════════════════════════════════════════════════════════════

class ChatBubble(ctk.CTkFrame):
    """A single chat message rendered as a styled bubble."""

    def __init__(self, parent, text: str, sender: str, timestamp: str, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        is_user = sender == "user"

        self.grid_columnconfigure(0, weight=1)

        # Avatar + name row
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="e" if is_user else "w", pady=(0, 3))

        name_label = ctk.CTkLabel(
            header,
            text="You" if is_user else "JARVIS",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLORS["text_accent"] if not is_user else "#60a5fa",
        )
        name_label.pack(side="right" if is_user else "left", padx=(0, 6))

        ts_label = ctk.CTkLabel(
            header,
            text=timestamp,
            font=ctk.CTkFont(family=FONT_FAMILY, size=10),
            text_color=COLORS["text_muted"],
        )
        ts_label.pack(side="right" if is_user else "left")

        # Bubble
        bubble_color = COLORS["user_bubble"] if is_user else COLORS["ai_bubble"]
        bubble = ctk.CTkFrame(
            self,
            fg_color=bubble_color,
            corner_radius=14,
        )
        bubble.grid(
            row=1,
            column=0,
            sticky="e" if is_user else "w",
            padx=(80, 0) if is_user else (0, 80),
        )

        msg_label = ctk.CTkLabel(
            bubble,
            text=text,
            wraplength=420,
            justify="left",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLORS["text_primary"],
            padx=14,
            pady=10,
        )
        msg_label.pack()


class StatusBar(ctk.CTkFrame):
    """Bottom status bar showing system state."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_secondary"],
            corner_radius=0,
            height=32,
            **kwargs,
        )
        self.pack_propagate(False)

        self._dot = ctk.CTkLabel(
            self,
            text="  ",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["success"],
        )
        self._dot.pack(side="left", padx=(12, 0))

        self._label = ctk.CTkLabel(
            self,
            text="All systems online",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLORS["text_muted"],
        )
        self._label.pack(side="left", padx=4)

        self._model_label = ctk.CTkLabel(
            self,
            text=f"Model: {Config.MODEL_NAME}",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLORS["text_muted"],
        )
        self._model_label.pack(side="right", padx=14)

    def set(self, text: str, color: str = None):
        self._label.configure(text=text)
        if color:
            self._dot.configure(text_color=color)

    def ready(self):
        self.set("Ready", COLORS["success"])

    def thinking(self):
        self.set("JARVIS is thinking...", COLORS["warning"])

    def listening(self):
        self.set("Listening for voice input...", COLORS["accent"])

    def error(self, msg: str = "Error"):
        self.set(msg, COLORS["danger"])


# ══════════════════════════════════════════════════════════════════
#  TAB: AI CHAT
# ══════════════════════════════════════════════════════════════════

class ChatTab(ctk.CTkFrame):
    def __init__(self, parent, ai: GeminiEngine, speaker: VoiceSpeaker,
                 status_bar: StatusBar, executor: ThreadPoolExecutor, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg_primary"], **kwargs)
        self.ai = ai
        self.speaker = speaker
        self.status_bar = status_bar
        self.executor = executor
        self._speak_replies = False

        self._build_ui()
        self._add_bubble(
            "Hello! I am JARVIS, your AI assistant powered by Gemini. "
            "Ask me anything or use the tabs above for notes and browser control.",
            "ai",
        )

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # ── Scrollable chat area
        self.chat_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["bg_primary"],
            scrollbar_button_color=COLORS["bg_tertiary"],
        )
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self._bubble_row = 0

        # ── Input area
        input_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        input_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkTextbox(
            input_frame,
            height=56,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color=COLORS["bg_tertiary"],
            text_color=COLORS["text_primary"],
            border_width=0,
            corner_radius=10,
            wrap="word",
        )
        self.input_box.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        self.input_box.bind("<Return>", self._on_enter)
        self.input_box.bind("<Shift-Return>", lambda e: None)

        btn_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_row.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        self.speak_toggle = ctk.CTkSwitch(
            btn_row,
            text="Speak replies",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
            button_color=COLORS["accent"],
            progress_color=COLORS["accent_light"],
            command=self._toggle_speak,
        )
        self.speak_toggle.pack(side="left", padx=(0, 12))

        self.clear_btn = ctk.CTkButton(
            btn_row,
            text="Clear Chat",
            width=90,
            height=32,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color=COLORS["bg_tertiary"],
            hover_color=COLORS["bg_card"],
            text_color=COLORS["text_muted"],
            corner_radius=8,
            command=self._clear_chat,
        )
        self.clear_btn.pack(side="right", padx=(6, 0))

        self.send_btn = ctk.CTkButton(
            btn_row,
            text="Send",
            width=90,
            height=32,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=8,
            command=self._send_message,
        )
        self.send_btn.pack(side="right")

    def _on_enter(self, event):
        if not event.state & 0x1:  # Shift not held
            self._send_message()
            return "break"

    def _toggle_speak(self):
        self._speak_replies = self.speak_toggle.get()

    def _add_bubble(self, text: str, sender: str):
        ts = datetime.now().strftime("%H:%M")
        bubble = ChatBubble(
            self.chat_frame,
            text=text,
            sender=sender,
            timestamp=ts,
        )
        bubble.grid(row=self._bubble_row, column=0, sticky="ew", pady=(0, 10))
        self._bubble_row += 1
        # Scroll to bottom
        self.chat_frame.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _add_typing_indicator(self):
        self._typing_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS["ai_bubble"],
            corner_radius=14,
        )
        self._typing_frame.grid(
            row=self._bubble_row, column=0, sticky="w", pady=(0, 10)
        )
        self._typing_row = self._bubble_row
        self._bubble_row += 1

        dots_label = ctk.CTkLabel(
            self._typing_frame,
            text="JARVIS is thinking...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, slant="italic"),
            text_color=COLORS["text_muted"],
            padx=14,
            pady=10,
        )
        dots_label.pack()
        self.chat_frame.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _remove_typing_indicator(self):
        if hasattr(self, "_typing_frame"):
            self._typing_frame.destroy()

    def _send_message(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            return
        self.input_box.delete("1.0", "end")
        self._add_bubble(text, "user")
        self._add_typing_indicator()
        self.send_btn.configure(state="disabled", text="...")
        self.status_bar.thinking()
        self.executor.submit(self._fetch_reply, text)

    def _fetch_reply(self, prompt: str):
        try:
            reply = self.ai.ask_jarvis(prompt)
        except Exception as e:
            reply = f"System error: {e}"
        self.after(0, self._display_reply, reply)

    def _display_reply(self, reply: str):
        self._remove_typing_indicator()
        self._add_bubble(reply, "ai")
        self.send_btn.configure(state="normal", text="Send")
        self.status_bar.ready()
        if self._speak_replies and self.speaker:
            self.executor.submit(self.speaker.speak, reply)

    def _clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self._bubble_row = 0
        self._add_bubble("Chat cleared. How can I help you?", "ai")


# ══════════════════════════════════════════════════════════════════
#  TAB: NOTES
# ══════════════════════════════════════════════════════════════════

class NotesTab(ctk.CTkFrame):
    def __init__(self, parent, notes: NotesManager, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg_primary"], **kwargs)
        self.notes = notes
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ── Left panel: list + search
        left = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        left.grid_rowconfigure(2, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left,
            text="Saved Notes",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLORS["text_accent"],
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))

        # Search bar
        search_frame = ctk.CTkFrame(left, fg_color=COLORS["bg_tertiary"], corner_radius=8)
        search_frame.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 8))
        search_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            search_frame,
            text="  Search",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
        ).grid(row=0, column=0, padx=(6, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Filter notes...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color="transparent",
            border_width=0,
            text_color=COLORS["text_primary"],
        )
        search_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        # Notes listbox (using CTkScrollableFrame with buttons)
        self.notes_list_frame = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            scrollbar_button_color=COLORS["bg_card"],
        )
        self.notes_list_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 14))
        self.notes_list_frame.grid_columnconfigure(0, weight=1)

        # Delete button at bottom
        ctk.CTkButton(
            left,
            text="Delete Selected",
            height=34,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color="#7f1d1d",
            hover_color="#991b1b",
            text_color="#fca5a5",
            corner_radius=8,
            command=self._delete_selected,
        ).grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))

        # ── Right panel: editor
        right = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew", padx=(0, 16), pady=16)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        top_row = ctk.CTkFrame(right, fg_color="transparent")
        top_row.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))
        top_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top_row,
            text="Title",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
        ).grid(row=0, column=0, sticky="w")

        self.title_entry = ctk.CTkEntry(
            top_row,
            placeholder_text="Note title...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            height=36,
        )
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        ctk.CTkButton(
            top_row,
            text="Save Note",
            width=100,
            height=36,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=8,
            command=self._save_note,
        ).grid(row=1, column=1, padx=(10, 0), pady=(4, 0))

        ctk.CTkLabel(
            right,
            text="Content",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
        ).grid(row=0, column=0, sticky="sw", padx=14, pady=(0, 0))

        self.content_box = ctk.CTkTextbox(
            right,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color=COLORS["bg_tertiary"],
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10,
            wrap="word",
        )
        self.content_box.grid(row=1, column=0, sticky="nsew", padx=14, pady=(8, 14))

        self._selected_title = None
        self._note_buttons = {}

    def _refresh_list(self, filter_text: str = ""):
        for w in self.notes_list_frame.winfo_children():
            w.destroy()
        self._note_buttons.clear()

        raw = self.notes.list_notes()
        if "No notes" in raw:
            ctk.CTkLabel(
                self.notes_list_frame,
                text="No notes yet.\nCreate one on the right.",
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                text_color=COLORS["text_muted"],
                justify="center",
            ).pack(pady=24)
            return

        for line in raw.splitlines():
            if not line.strip() or "---" in line:
                continue
            parts = line.split(". ", 1)
            if len(parts) < 2:
                continue
            rest = parts[1]
            title = rest.split(" (Saved")[0].strip()
            if filter_text and filter_text.lower() not in title.lower():
                continue

            btn = ctk.CTkButton(
                self.notes_list_frame,
                text=title,
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["accent_light"],
                text_color=COLORS["text_primary"],
                anchor="w",
                corner_radius=8,
                height=36,
                command=lambda t=title: self._select_note(t),
            )
            btn.pack(fill="x", pady=2)
            self._note_buttons[title] = btn

    def _on_search(self, *args):
        self._refresh_list(self.search_var.get())

    def _select_note(self, title: str):
        self._selected_title = title
        raw = self.notes.read_note(title)
        for key, btn in self._note_buttons.items():
            btn.configure(
                fg_color=COLORS["accent_light"] if key == title else COLORS["bg_card"]
            )
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, title)
        self.content_box.delete("1.0", "end")
        # Extract just the content from the formatted string
        lines = raw.splitlines()
        content_lines = [l for l in lines if not l.startswith("---")]
        self.content_box.insert("1.0", "\n".join(content_lines).strip())

    def _save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_box.get("1.0", "end").strip()
        if not title:
            messagebox.showerror("Missing Title", "Please enter a title for the note.")
            return
        if not content:
            messagebox.showerror("Missing Content", "Note content cannot be empty.")
            return
        result = self.notes.save_note(title, content)
        if "Error" in result:
            messagebox.showerror("Save Failed", result)
        else:
            messagebox.showinfo("Saved", result)
            self.title_entry.delete(0, "end")
            self.content_box.delete("1.0", "end")
            self._selected_title = None
            self._refresh_list()

    def _delete_selected(self):
        if not self._selected_title:
            messagebox.showwarning("No Note Selected", "Click a note from the list first.")
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Permanently delete '{self._selected_title}'?",
        )
        if not confirm:
            return
        result = self.notes.delete_note(self._selected_title)
        if "Error" in result:
            messagebox.showerror("Delete Failed", result)
        else:
            messagebox.showinfo("Deleted", result)
            self.title_entry.delete(0, "end")
            self.content_box.delete("1.0", "end")
            self._selected_title = None
            self._refresh_list()


# ══════════════════════════════════════════════════════════════════
#  TAB: WEB & APPS
# ══════════════════════════════════════════════════════════════════

class WebTab(ctk.CTkFrame):
    def __init__(self, parent, web: WebCommands, status_bar: StatusBar, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg_primary"], **kwargs)
        self.web = web
        self.status_bar = status_bar
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Custom URL entry
        url_card = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        url_card.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        url_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            url_card,
            text="Open a Website or App",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLORS["text_accent"],
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        entry_row = ctk.CTkFrame(url_card, fg_color="transparent")
        entry_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))
        entry_row.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            entry_row,
            placeholder_text="Type a shortcut (google, github) or app name (vscode)...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            height=38,
        )
        self.url_entry.grid(row=0, column=0, sticky="ew")
        self.url_entry.bind("<Return>", lambda e: self._open_custom())

        ctk.CTkButton(
            entry_row,
            text="Open",
            width=80,
            height=38,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=8,
            command=self._open_custom,
        ).grid(row=0, column=1, padx=(10, 0))

        self.result_label = ctk.CTkLabel(
            url_card,
            text="",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["success"],
        )
        self.result_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))

        # ── Shortcut grid
        shortcuts_card = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        shortcuts_card.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        shortcuts_card.grid_columnconfigure(tuple(range(4)), weight=1)

        ctk.CTkLabel(
            shortcuts_card,
            text="Website Shortcuts",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLORS["text_accent"],
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(14, 10))

        web_shortcuts = list(self.web.shortcuts.keys())
        for i, name in enumerate(web_shortcuts):
            row = (i // 4) + 1
            col = i % 4
            ctk.CTkButton(
                shortcuts_card,
                text=name.title(),
                height=38,
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["accent_light"],
                text_color=COLORS["text_primary"],
                corner_radius=8,
                command=lambda n=name: self._open_shortcut(n),
            ).grid(row=row, column=col, padx=8, pady=4, sticky="ew")

        # ── App shortcuts
        apps_card = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        apps_card.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        apps_card.grid_columnconfigure(tuple(range(5)), weight=1)

        ctk.CTkLabel(
            apps_card,
            text="Desktop App Shortcuts",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLORS["text_accent"],
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=16, pady=(14, 10))

        app_names = list(self.web.apps.keys())
        for i, name in enumerate(app_names):
            row = (i // 5) + 1
            col = i % 5
            ctk.CTkButton(
                apps_card,
                text=name.title(),
                height=34,
                font=ctk.CTkFont(family=FONT_FAMILY, size=11),
                fg_color=COLORS["bg_tertiary"],
                hover_color=COLORS["bg_card"],
                text_color=COLORS["text_muted"],
                corner_radius=8,
                command=lambda n=name: self._open_shortcut(n),
            ).grid(row=row, column=col, padx=6, pady=3, sticky="ew")

        ctk.CTkLabel(
            apps_card,
            text="",
            height=10,
        ).grid(row=99, column=0, columnspan=5)

    def _open_shortcut(self, name: str):
        result = self.web.open_website(name)
        self._show_result(result)

    def _open_custom(self):
        text = self.url_entry.get().strip()
        if not text:
            return
        result = self.web.open_website(text)
        self._show_result(result)
        self.url_entry.delete(0, "end")

    def _show_result(self, result: str):
        is_error = "Error" in result
        self.result_label.configure(
            text=result,
            text_color=COLORS["danger"] if is_error else COLORS["success"],
        )
        self.status_bar.set(
            result,
            COLORS["danger"] if is_error else COLORS["success"],
        )


# ══════════════════════════════════════════════════════════════════
#  TAB: VOICE
# ══════════════════════════════════════════════════════════════════

class VoiceTab(ctk.CTkFrame):
    def __init__(self, parent, ai: GeminiEngine, listener: VoiceListener,
                 speaker: VoiceSpeaker, web: WebCommands,
                 status_bar: StatusBar, executor: ThreadPoolExecutor, **kwargs):
        super().__init__(parent, fg_color=COLORS["bg_primary"], **kwargs)
        self.ai = ai
        self.listener = listener
        self.speaker = speaker
        self.web = web
        self.status_bar = status_bar
        self.executor = executor
        self._listening = False
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Control card
        control_card = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        control_card.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))

        ctk.CTkLabel(
            control_card,
            text="Voice Mode",
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=COLORS["text_accent"],
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            control_card,
            text="Say 'back' to stop. Web shortcuts are voice-activated automatically.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
        ).pack(pady=(0, 16))

        self.mic_btn = ctk.CTkButton(
            control_card,
            text="Start Listening",
            width=200,
            height=50,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            corner_radius=25,
            command=self._toggle_listen,
        )
        self.mic_btn.pack(pady=(0, 20))

        self.mic_status = ctk.CTkLabel(
            control_card,
            text="Microphone idle",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
        )
        self.mic_status.pack(pady=(0, 16))

        # ── Voice transcript log
        log_card = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], corner_radius=14)
        log_card.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        log_card.grid_rowconfigure(1, weight=1)
        log_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            log_card,
            text="Voice Transcript",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLORS["text_accent"],
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.transcript_box = ctk.CTkTextbox(
            log_card,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color=COLORS["bg_tertiary"],
            text_color=COLORS["text_primary"],
            border_width=0,
            corner_radius=10,
            state="disabled",
        )
        self.transcript_box.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

    def _toggle_listen(self):
        if self._listening:
            self._listening = False
            self.mic_btn.configure(text="Start Listening", fg_color=COLORS["accent"])
            self.mic_status.configure(text="Microphone idle", text_color=COLORS["text_muted"])
            self.status_bar.ready()
        else:
            self._listening = True
            self.mic_btn.configure(text="Stop Listening", fg_color=COLORS["danger"])
            self.mic_status.configure(
                text="Listening... speak now", text_color=COLORS["success"]
            )
            self.status_bar.listening()
            self.executor.submit(self._voice_loop)

    def _voice_loop(self):
        if self.speaker:
            self.speaker.speak("Voice pipeline active. I am listening.")
        while self._listening:
            voice_text = self.listener.listen()
            if not voice_text:
                continue
            self.after(0, self._log, f"You: {voice_text}")
            if voice_text.lower() == "back":
                self.after(0, self._toggle_listen)
                break
            # Check web shortcuts
            matched = False
            for shortcut in self.web.shortcuts.keys():
                if shortcut in voice_text.lower():
                    result = self.web.open_website(shortcut)
                    self.after(0, self._log, f"JARVIS: {result}")
                    if self.speaker:
                        self.speaker.speak(result)
                    matched = True
                    break
            if matched:
                continue
            reply = self.ai.ask_jarvis(voice_text)
            self.after(0, self._log, f"JARVIS: {reply}")
            if self.speaker:
                self.executor.submit(self.speaker.speak, reply)

    def _log(self, text: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.transcript_box.configure(state="normal")
        self.transcript_box.insert("end", f"[{ts}] {text}\n\n")
        self.transcript_box.configure(state="disabled")
        self.transcript_box.see("end")


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION WINDOW
# ══════════════════════════════════════════════════════════════════

class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS — AI Desktop Assistant")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(fg_color=COLORS["bg_primary"])

        self.executor = ThreadPoolExecutor(max_workers=4)
        self._boot_and_build()

    def _boot_and_build(self):
        # ── Boot screen
        boot_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_primary"])
        boot_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(
            boot_frame,
            text="JARVIS",
            font=ctk.CTkFont(family=FONT_FAMILY, size=52, weight="bold"),
            text_color=COLORS["text_accent"],
        ).place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkLabel(
            boot_frame,
            text="AI Desktop Assistant",
            font=ctk.CTkFont(family=FONT_FAMILY, size=16),
            text_color=COLORS["text_muted"],
        ).place(relx=0.5, rely=0.47, anchor="center")

        self._boot_label = ctk.CTkLabel(
            boot_frame,
            text="Initializing systems...",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLORS["text_muted"],
        )
        self._boot_label.place(relx=0.5, rely=0.56, anchor="center")

        self._boot_bar = ctk.CTkProgressBar(
            boot_frame,
            width=300,
            mode="indeterminate",
            progress_color=COLORS["accent"],
        )
        self._boot_bar.place(relx=0.5, rely=0.62, anchor="center")
        self._boot_bar.start()

        # Boot in background thread
        self.executor.submit(self._initialize_engines, boot_frame)

    def _initialize_engines(self, boot_frame):
        engines = {}
        steps = [
            ("Connecting to Gemini AI...", "ai",       lambda: GeminiEngine()),
            ("Loading notes manager...",   "notes",    lambda: NotesManager()),
            ("Loading web commands...",    "web",      lambda: WebCommands()),
            ("Initializing microphone...", "listener", lambda: VoiceListener()),
            ("Loading voice engine...",    "speaker",  lambda: VoiceSpeaker()),
        ]
        for msg, key, factory in steps:
            self.after(0, self._boot_label.configure, {"text": msg})
            try:
                engines[key] = factory()
            except Exception as e:
                logger.warning(f"Engine '{key}' failed to load: {e}")
                engines[key] = None
            time.sleep(0.3)

        self.after(0, boot_frame.destroy)
        self.after(0, self._build_main_ui, engines)

    def _build_main_ui(self, engines: dict):
        # ── Top bar
        topbar = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], height=54, corner_radius=0)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        ctk.CTkLabel(
            topbar,
            text="JARVIS",
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=COLORS["text_accent"],
        ).pack(side="left", padx=20)

        ctk.CTkLabel(
            topbar,
            text="AI Desktop Assistant",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLORS["text_muted"],
        ).pack(side="left", padx=(0, 20))

        model_badge = ctk.CTkLabel(
            topbar,
            text=f"  {Config.MODEL_NAME}  ",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLORS["text_accent"],
            fg_color=COLORS["accent_light"],
            corner_radius=6,
        )
        model_badge.pack(side="right", padx=16)

        # ── Status bar
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill="x", side="bottom")

        # ── Tab view
        tab_view = ctk.CTkTabview(
            self,
            fg_color=COLORS["bg_primary"],
            segmented_button_fg_color=COLORS["bg_secondary"],
            segmented_button_selected_color=COLORS["accent"],
            segmented_button_selected_hover_color=COLORS["accent_hover"],
            segmented_button_unselected_color=COLORS["bg_secondary"],
            segmented_button_unselected_hover_color=COLORS["bg_tertiary"],
            text_color=COLORS["text_primary"],
            text_color_disabled=COLORS["text_muted"],
        )
        tab_view.pack(fill="both", expand=True, padx=0, pady=0)

        tab_view.add("  AI Chat  ")
        tab_view.add("  Notes  ")
        tab_view.add("  Web & Apps  ")
        tab_view.add("  Voice  ")

        # ── Chat tab
        ChatTab(
            tab_view.tab("  AI Chat  "),
            ai=engines.get("ai"),
            speaker=engines.get("speaker"),
            status_bar=self.status_bar,
            executor=self.executor,
        ).pack(fill="both", expand=True)

        # ── Notes tab
        NotesTab(
            tab_view.tab("  Notes  "),
            notes=engines.get("notes"),
        ).pack(fill="both", expand=True)

        # ── Web tab
        WebTab(
            tab_view.tab("  Web & Apps  "),
            web=engines.get("web"),
            status_bar=self.status_bar,
        ).pack(fill="both", expand=True)

        # ── Voice tab
        VoiceTab(
            tab_view.tab("  Voice  "),
            ai=engines.get("ai"),
            listener=engines.get("listener"),
            speaker=engines.get("speaker"),
            web=engines.get("web"),
            status_bar=self.status_bar,
            executor=self.executor,
        ).pack(fill="both", expand=True)

        self.status_bar.ready()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self.executor.shutdown(wait=False)
        self.destroy()


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
