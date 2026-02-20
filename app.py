"""
app.py
Haupt-GUI des Startup Managers (tkinter).
Layout: Header | [Aufgaben | Termine] | Webseiten | Statusleiste
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import threading
from datetime import datetime

from config_manager import ConfigManager
from google_service import GoogleService

# Farben (Windows-inspiriert)
C = {
    "bg":          "#ffffff",
    "bg2":         "#f3f2f1",
    "accent":      "#0078d4",
    "success":     "#107c10",
    "error":       "#a4262c",
    "text":        "#201f1e",
    "text2":       "#605e5c",
    "done":        "#a19f9d",
    "border":      "#edebe9",
}

FONT_BODY   = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_TIME   = ("Segoe UI", 10, "bold")

WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
            "Freitag", "Samstag", "Sonntag"]
MONTHS   = ["Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"]


class StartupManagerApp:
    """Haupt-Anwendungsfenster."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.config = ConfigManager()
        self.google = GoogleService()

        # Zustand
        self._task_vars: dict[str, tuple[tk.BooleanVar, str]] = {}
        self._website_vars: dict[str, tk.BooleanVar] = {}
        self._refresh_job = None

        self._setup_window()
        self._apply_style()
        self._build_gui()
        self._load_data()

        # Ggf. Webseiten automatisch öffnen
        if self.config.get_settings().get("auto_open_on_startup"):
            self.root.after(1500, self._auto_open_websites)

        # Periodische Aktualisierung planen
        self._schedule_refresh()

    # ------------------------------------------------------------------ #
    #  Fenster / Stil                                                       #
    # ------------------------------------------------------------------ #

    def _setup_window(self):
        self.root.title("Startup Manager")
        self.root.configure(bg=C["bg"])
        geo = self.config.get_settings().get("window_geometry", "980x680+80+80")
        self.root.geometry(geo)
        self.root.minsize(720, 500)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<F5>", lambda _: self._load_data())

    def _apply_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(".",
                    background=C["bg"],
                    foreground=C["text"],
                    font=FONT_BODY)
        s.configure("Section.TLabelframe",
                    background=C["bg"],
                    relief="flat")
        s.configure("Section.TLabelframe.Label",
                    font=FONT_BOLD,
                    foreground=C["accent"],
                    background=C["bg"])
        s.configure("Accent.TButton",
                    background=C["accent"],
                    foreground="white")
        s.map("Accent.TButton",
              background=[("active", "#106ebe")])

    # ------------------------------------------------------------------ #
    #  GUI-Aufbau                                                           #
    # ------------------------------------------------------------------ #

    def _build_gui(self):
        self._build_menu()

        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill=tk.BOTH, expand=True)

        self._build_header(outer)

        ttk.Separator(outer).pack(fill=tk.X, pady=(6, 10))

        # Haupt-Bereich: Aufgaben + Termine nebeneinander
        mid = ttk.Frame(outer)
        mid.pack(fill=tk.BOTH, expand=True)
        mid.columnconfigure(0, weight=1)
        mid.columnconfigure(1, weight=1)
        mid.rowconfigure(0, weight=1)

        self._build_todo_panel(mid)
        self._build_calendar_panel(mid)

        ttk.Separator(outer).pack(fill=tk.X, pady=(10, 6))

        self._build_website_panel(outer)

        # Statusleiste
        self._status_var = tk.StringVar(value="Bereit")
        ttk.Label(self.root,
                  textvariable=self._status_var,
                  foreground=C["text2"],
                  font=FONT_SMALL,
                  padding=(8, 2)).pack(side=tk.BOTTOM, fill=tk.X)

    def _build_menu(self):
        bar = tk.Menu(self.root)
        self.root.config(menu=bar)

        # Datei
        m = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Datei", menu=m)
        m.add_command(label="Aktualisieren  F5", command=self._load_data)
        m.add_separator()
        m.add_command(label="Beenden", command=self._on_close)

        # Einstellungen
        m = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Einstellungen", menu=m)
        m.add_command(label="Webseiten verwalten...", command=self._open_website_settings)
        m.add_command(label="Google-Konto einrichten...", command=self._open_google_settings)
        m.add_separator()
        m.add_command(label="Autostart ein/ausschalten", command=self._toggle_autostart)

        # Hilfe
        m = tk.Menu(bar, tearoff=0)
        bar.add_cascade(label="Hilfe", menu=m)
        m.add_command(label="Über Startup Manager", command=self._show_about)

    def _build_header(self, parent):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X)

        now = datetime.now()
        greeting = (
            "Guten Morgen!"  if now.hour < 12 else
            "Guten Tag!"     if now.hour < 18 else
            "Guten Abend!"
        )
        ttk.Label(row, text=greeting, font=FONT_TITLE).pack(side=tk.LEFT)

        date_str = (
            f"{WEEKDAYS[now.weekday()]}, "
            f"{now.day}. {MONTHS[now.month - 1]} {now.year}"
        )
        ttk.Label(row, text=date_str, font=FONT_SMALL,
                  foreground=C["text2"]).pack(side=tk.RIGHT, anchor=tk.S)

    # --- Aufgaben-Panel ---

    def _build_todo_panel(self, parent):
        frame = ttk.LabelFrame(parent, text=" Aufgaben ",
                               style="Section.TLabelframe", padding=8)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        # Toolbar – pack, damit kein pack/grid-Konflikt entsteht
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 6))
        ttk.Button(toolbar, text="+ Neue Aufgabe",
                   command=self._add_task).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Aktualisieren",
                   command=self._load_data).pack(side=tk.RIGHT)

        # Scrollbarer Bereich (intern pack-basiert)
        self._todo_canvas, self._todo_inner = self._scrollable_frame(frame)

    # --- Kalender-Panel ---

    def _build_calendar_panel(self, parent):
        frame = ttk.LabelFrame(parent, text=" Termine heute ",
                               style="Section.TLabelframe", padding=8)
        frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        self._cal_canvas, self._cal_inner = self._scrollable_frame(frame)

    # --- Webseiten-Panel ---

    def _build_website_panel(self, parent):
        frame = ttk.LabelFrame(parent, text=" Webseiten ",
                               style="Section.TLabelframe", padding=8)
        frame.pack(fill=tk.X)

        self._website_check_frame = ttk.Frame(frame)
        self._website_check_frame.pack(fill=tk.X, pady=(0, 8))
        self._rebuild_website_checks()

        btns = ttk.Frame(frame)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Ausgewählte öffnen",
                   command=self._open_selected_websites).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(btns, text="Alle öffnen",
                   command=self._open_all_websites).pack(side=tk.LEFT)
        ttk.Button(btns, text="Verwalten...",
                   command=self._open_website_settings).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------ #
    #  Hilfsmethoden                                                        #
    # ------------------------------------------------------------------ #

    def _scrollable_frame(self, parent) -> tuple[tk.Canvas, ttk.Frame]:
        """Erstellt einen scrollbaren Inhaltsbereich und gibt (Canvas, InnerFrame) zurück."""
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        canvas = tk.Canvas(container, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)

        inner.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)

        return canvas, inner

    def _set_status(self, msg: str):
        self._status_var.set(msg)

    # ------------------------------------------------------------------ #
    #  Daten laden                                                          #
    # ------------------------------------------------------------------ #

    def _load_data(self):
        if not self.google.is_configured:
            self._show_not_configured()
            return
        self._set_status("Daten werden geladen...")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        try:
            events = self.google.get_today_events()
            tasks  = self.google.get_tasks(
                self.config.get_settings().get("show_completed_tasks", False)
            )
            self.root.after(0, lambda: self._render_calendar(events))
            self.root.after(0, lambda: self._render_todos(tasks))
            self.root.after(0, lambda: self._set_status(
                f"Zuletzt aktualisiert: {datetime.now().strftime('%H:%M')}"
            ))
        except Exception as exc:
            self.root.after(0, lambda: self._set_status(f"Fehler: {exc}"))
            self.root.after(0, lambda: messagebox.showerror(
                "Fehler beim Laden", str(exc), parent=self.root
            ))

    def _show_not_configured(self):
        for frame in (self._todo_inner, self._cal_inner):
            for w in frame.winfo_children():
                w.destroy()
        msg = "Google-Konto nicht eingerichtet.\n\nEinstellungen → Google-Konto einrichten..."
        for frame in (self._todo_inner, self._cal_inner):
            ttk.Label(frame, text=msg, foreground=C["text2"],
                      justify=tk.CENTER).pack(pady=24, padx=8)
        self._set_status("Google-Konto nicht konfiguriert")

    # ------------------------------------------------------------------ #
    #  Aufgaben rendern                                                     #
    # ------------------------------------------------------------------ #

    def _render_todos(self, tasks: list):
        for w in self._todo_inner.winfo_children():
            w.destroy()
        self._task_vars.clear()

        if not tasks:
            ttk.Label(self._todo_inner,
                      text="Keine offenen Aufgaben",
                      foreground=C["text2"]).pack(pady=20)
            return

        for task in tasks:
            self._add_task_row(task)

    def _add_task_row(self, task: dict):
        row = ttk.Frame(self._todo_inner)
        row.pack(fill=tk.X, pady=2, padx=4)

        var = tk.BooleanVar(value=task["status"] == "completed")
        self._task_vars[task["id"]] = (var, task["tasklist_id"])

        cb = ttk.Checkbutton(
            row, variable=var,
            command=lambda t=task, v=var: self._toggle_task(t, v)
        )
        cb.pack(side=tk.LEFT)

        # Titel + ggf. Fälligkeitsdatum
        label_text = task["title"]
        if task.get("due"):
            try:
                dt = datetime.fromisoformat(task["due"].replace("Z", "+00:00"))
                label_text += f"  [{dt.strftime('%d.%m.')}]"
            except ValueError:
                pass

        color = C["done"] if task["status"] == "completed" else C["text"]
        ttk.Label(row, text=label_text, foreground=color).pack(side=tk.LEFT, padx=(4, 0))

        # Notiz als Tooltip (einfache Label-Zeile)
        if task.get("notes"):
            note_short = task["notes"][:60] + ("…" if len(task["notes"]) > 60 else "")
            ttk.Label(row, text=note_short, foreground=C["text2"],
                      font=FONT_SMALL).pack(side=tk.LEFT, padx=(8, 0))

    # ------------------------------------------------------------------ #
    #  Kalender rendern                                                     #
    # ------------------------------------------------------------------ #

    def _render_calendar(self, events: list):
        for w in self._cal_inner.winfo_children():
            w.destroy()

        if not events:
            ttk.Label(self._cal_inner,
                      text="Keine Termine heute",
                      foreground=C["text2"]).pack(pady=20)
            return

        for event in events:
            self._add_event_row(event)

    def _add_event_row(self, event: dict):
        row = ttk.Frame(self._cal_inner)
        row.pack(fill=tk.X, pady=5, padx=4)

        # Zeit parsen
        start_raw = event.get("start", "")
        if "T" in start_raw:
            try:
                dt = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
                time_str = dt.strftime("%H:%M")
            except ValueError:
                time_str = start_raw[:5]
        else:
            time_str = "Ganztag"

        ttk.Label(row, text=time_str, width=8,
                  foreground=C["accent"], font=FONT_TIME).pack(side=tk.LEFT)
        ttk.Label(row, text=event["summary"],
                  font=FONT_BODY).pack(side=tk.LEFT, padx=(4, 0))

        if event.get("location"):
            loc = event["location"]
            if len(loc) > 30:
                loc = loc[:28] + "…"
            ttk.Label(row, text=f"  @ {loc}",
                      foreground=C["text2"],
                      font=FONT_SMALL).pack(side=tk.LEFT)

    # ------------------------------------------------------------------ #
    #  Aufgaben-Aktionen                                                    #
    # ------------------------------------------------------------------ #

    def _toggle_task(self, task: dict, var: tk.BooleanVar):
        self._set_status("Aufgabe wird gespeichert…")
        completed = var.get()

        def _do():
            try:
                self.google.update_task_status(
                    task["tasklist_id"], task["id"], completed
                )
                self.root.after(0, lambda: self._set_status("Aufgabe gespeichert"))
            except Exception as exc:
                self.root.after(0, lambda: self._set_status(f"Fehler: {exc}"))

        threading.Thread(target=_do, daemon=True).start()

    def _add_task(self):
        if not self.google.is_configured:
            messagebox.showwarning(
                "Nicht konfiguriert",
                "Bitte zuerst das Google-Konto einrichten.\n"
                "Einstellungen → Google-Konto einrichten...",
                parent=self.root
            )
            return

        title = simpledialog.askstring(
            "Neue Aufgabe", "Aufgabentitel:", parent=self.root
        )
        if not title or not title.strip():
            return

        def _create():
            try:
                lists = self.google.get_task_lists()
                if not lists:
                    raise RuntimeError("Keine Aufgabenlisten im Google-Konto gefunden.")
                self.google.create_task(lists[0]["id"], title.strip())
                self.root.after(0, self._load_data)
            except Exception as exc:
                self.root.after(0, lambda: messagebox.showerror(
                    "Fehler", str(exc), parent=self.root
                ))

        threading.Thread(target=_create, daemon=True).start()

    # ------------------------------------------------------------------ #
    #  Webseiten                                                            #
    # ------------------------------------------------------------------ #

    def _rebuild_website_checks(self):
        for w in self._website_check_frame.winfo_children():
            w.destroy()
        self._website_vars.clear()

        websites = [s for s in self.config.get_websites() if s.get("enabled", True)]
        if not websites:
            ttk.Label(self._website_check_frame,
                      text="Keine Webseiten konfiguriert – Einstellungen → Webseiten verwalten",
                      foreground=C["text2"]).pack(side=tk.LEFT)
            return

        for site in websites:
            var = tk.BooleanVar(value=site.get("auto_open", False))
            self._website_vars[site["url"]] = var
            ttk.Checkbutton(
                self._website_check_frame,
                text=site["name"],
                variable=var
            ).pack(side=tk.LEFT, padx=(0, 14))

    def _open_selected_websites(self):
        opened = 0
        for url, var in self._website_vars.items():
            if var.get():
                webbrowser.open(url)
                opened += 1
        if opened:
            self._set_status(f"{opened} Webseite(n) geöffnet")
        else:
            messagebox.showinfo("Hinweis", "Keine Webseite ausgewählt.", parent=self.root)

    def _open_all_websites(self):
        sites = [s for s in self.config.get_websites() if s.get("enabled", True)]
        if not sites:
            messagebox.showinfo("Hinweis", "Keine Webseiten konfiguriert.", parent=self.root)
            return
        for s in sites:
            webbrowser.open(s["url"])
        self._set_status(f"{len(sites)} Webseite(n) geöffnet")

    def _auto_open_websites(self):
        for site in self.config.get_websites():
            if site.get("enabled", True) and site.get("auto_open", False):
                webbrowser.open(site["url"])

    # ------------------------------------------------------------------ #
    #  Dialoge / Einstellungen                                              #
    # ------------------------------------------------------------------ #

    def _open_website_settings(self):
        WebsiteSettingsDialog(self.root, self.config, self._rebuild_website_checks)

    def _open_google_settings(self):
        GoogleSettingsDialog(self.root, self.google, self._load_data)

    def _toggle_autostart(self):
        try:
            from autostart import toggle_autostart
            enabled = toggle_autostart()
            state = "aktiviert" if enabled else "deaktiviert"
            messagebox.showinfo("Autostart", f"Autostart wurde {state}.", parent=self.root)
        except Exception as exc:
            messagebox.showerror("Autostart-Fehler", str(exc), parent=self.root)

    def _show_about(self):
        messagebox.showinfo(
            "Über Startup Manager",
            "Startup Manager v1.0\n\n"
            "Zeigt Aufgaben und Kalendertermine beim Systemstart.\n"
            "Öffnet konfigurierte Webseiten automatisch.\n\n"
            "Technologie: Python 3 · tkinter · Google APIs",
            parent=self.root
        )

    # ------------------------------------------------------------------ #
    #  Periodische Aktualisierung                                           #
    # ------------------------------------------------------------------ #

    def _schedule_refresh(self):
        minutes = self.config.get_settings().get("refresh_interval_minutes", 5)
        ms = max(1, minutes) * 60 * 1000
        self._refresh_job = self.root.after(ms, self._periodic_refresh)

    def _periodic_refresh(self):
        self._load_data()
        self._schedule_refresh()

    # ------------------------------------------------------------------ #
    #  Fenster schließen                                                    #
    # ------------------------------------------------------------------ #

    def _on_close(self):
        if self._refresh_job:
            self.root.after_cancel(self._refresh_job)
        self.config.update_settings(window_geometry=self.root.geometry())
        self.root.destroy()


# ====================================================================== #
#  Dialoge                                                                 #
# ====================================================================== #

class WebsiteSettingsDialog(tk.Toplevel):
    """Dialog zum Verwalten der Webseiten-Liste."""

    def __init__(self, parent, config: ConfigManager, refresh_cb):
        super().__init__(parent)
        self.config = config
        self.refresh_cb = refresh_cb
        self.title("Webseiten verwalten")
        self.geometry("560x380")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self._build()
        self.wait_window()

    def _build(self):
        f = ttk.Frame(self, padding=14)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text="Webseiten verwalten",
                  font=FONT_BOLD).pack(anchor=tk.W)
        ttk.Separator(f).pack(fill=tk.X, pady=8)

        # Liste
        lf = ttk.Frame(f)
        lf.pack(fill=tk.BOTH, expand=True)
        self._lb = tk.Listbox(lf, selectmode=tk.SINGLE,
                              font=FONT_BODY, activestyle="dotbox")
        sb = ttk.Scrollbar(lf, command=self._lb.yview)
        self._lb.config(yscrollcommand=sb.set)
        self._lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self._refresh_list()

        # Buttons
        bf = ttk.Frame(f)
        bf.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(bf, text="Hinzufügen", command=self._add).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(bf, text="Bearbeiten", command=self._edit).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(bf, text="Entfernen",  command=self._remove).pack(side=tk.LEFT)
        ttk.Button(bf, text="Schließen",  command=self.destroy).pack(side=tk.RIGHT)

    def _refresh_list(self):
        self._lb.delete(0, tk.END)
        for s in self.config.get_websites():
            tags = []
            if s.get("auto_open"):   tags.append("Auto")
            if not s.get("enabled", True): tags.append("Deaktiviert")
            suffix = f"  [{', '.join(tags)}]" if tags else ""
            self._lb.insert(tk.END, f"{s['name']}{suffix}  –  {s['url']}")

    def _add(self):
        d = WebsiteDialog(self)
        if d.result:
            sites = self.config.get_websites()
            sites.append(d.result)
            self.config.set_websites(sites)
            self._refresh_list()
            self.refresh_cb()

    def _edit(self):
        sel = self._lb.curselection()
        if not sel:
            return
        sites = self.config.get_websites()
        d = WebsiteDialog(self, sites[sel[0]])
        if d.result:
            sites[sel[0]] = d.result
            self.config.set_websites(sites)
            self._refresh_list()
            self.refresh_cb()

    def _remove(self):
        sel = self._lb.curselection()
        if not sel:
            return
        sites = self.config.get_websites()
        del sites[sel[0]]
        self.config.set_websites(sites)
        self._refresh_list()
        self.refresh_cb()


class WebsiteDialog(tk.Toplevel):
    """Dialog zum Hinzufügen/Bearbeiten einer Webseite."""

    def __init__(self, parent, site: dict = None):
        super().__init__(parent)
        self.result = None
        self.title("Webseite " + ("bearbeiten" if site else "hinzufügen"))
        self.geometry("420x230")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build(site)
        self.wait_window()

    def _build(self, site):
        f = ttk.Frame(self, padding=14)
        f.pack(fill=tk.BOTH, expand=True)
        f.columnconfigure(1, weight=1)

        # Name
        ttk.Label(f, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self._name = tk.StringVar(value=site["name"] if site else "")
        ttk.Entry(f, textvariable=self._name).grid(row=0, column=1, sticky=tk.EW, pady=5)

        # URL
        ttk.Label(f, text="URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self._url = tk.StringVar(value=site["url"] if site else "https://")
        ttk.Entry(f, textvariable=self._url).grid(row=1, column=1, sticky=tk.EW, pady=5)

        # Optionen
        self._auto = tk.BooleanVar(value=site.get("auto_open", False) if site else False)
        ttk.Checkbutton(f, text="Beim Start automatisch öffnen",
                        variable=self._auto).grid(row=2, column=0, columnspan=2,
                                                  sticky=tk.W, pady=3)

        self._enabled = tk.BooleanVar(value=site.get("enabled", True) if site else True)
        ttk.Checkbutton(f, text="Aktiv",
                        variable=self._enabled).grid(row=3, column=0, columnspan=2,
                                                     sticky=tk.W)

        # Buttons
        bf = ttk.Frame(f)
        bf.grid(row=4, column=0, columnspan=2, pady=(14, 0))
        ttk.Button(bf, text="OK",        command=self._ok).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(bf, text="Abbrechen", command=self.destroy).pack(side=tk.LEFT)

    def _ok(self):
        name = self._name.get().strip()
        url  = self._url.get().strip()
        if not name or not url:
            messagebox.showwarning("Pflichtfeld", "Name und URL sind erforderlich.", parent=self)
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.result = {
            "name":      name,
            "url":       url,
            "auto_open": self._auto.get(),
            "enabled":   self._enabled.get(),
        }
        self.destroy()


class GoogleSettingsDialog(tk.Toplevel):
    """Dialog zur Google-OAuth2-Einrichtung."""

    def __init__(self, parent, google: GoogleService, refresh_cb):
        super().__init__(parent)
        self.google = google
        self.refresh_cb = refresh_cb
        self.title("Google-Konto einrichten")
        self.geometry("540x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self._build()
        self.wait_window()

    def _build(self):
        f = ttk.Frame(self, padding=16)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text="Google-Konto einrichten",
                  font=FONT_BOLD).pack(anchor=tk.W)
        ttk.Separator(f).pack(fill=tk.X, pady=8)

        # Bibliotheks-Check
        if not self.google.is_available:
            ttk.Label(
                f,
                text=(
                    "Die Google-Bibliotheken sind nicht installiert.\n\n"
                    "Bitte ausführen:\n"
                    "    pip install google-api-python-client\n"
                    "                google-auth-httplib2\n"
                    "                google-auth-oauthlib"
                ),
                foreground=C["error"],
                justify=tk.LEFT,
                font=FONT_BODY,
            ).pack(anchor=tk.W)
            ttk.Button(f, text="Schließen", command=self.destroy).pack(pady=10)
            return

        # Status
        if self.google.is_configured:
            status_text = "credentials.json gefunden  ✓"
            status_color = C["success"]
        else:
            status_text = "credentials.json NICHT gefunden"
            status_color = C["error"]

        ttk.Label(f, text=f"Status: {status_text}",
                  foreground=status_color).pack(anchor=tk.W, pady=(0, 8))

        instructions = (
            "Schritt-für-Schritt-Anleitung:\n\n"
            "1. Öffnen Sie console.cloud.google.com\n"
            "2. Neues Projekt erstellen\n"
            "3. APIs aktivieren:\n"
            "     • Google Calendar API\n"
            "     • Google Tasks API\n"
            "4. OAuth2-Zugangsdaten erstellen (Typ: Desktop-App)\n"
            "5. credentials.json herunterladen\n"
            "6. Datei in den Programmordner legen\n"
            "7. Unten auf 'Anmelden' klicken – Browser öffnet sich"
        )
        ttk.Label(f, text=instructions,
                  justify=tk.LEFT,
                  foreground=C["text2"],
                  font=FONT_SMALL).pack(anchor=tk.W, pady=(0, 12))

        bf = ttk.Frame(f)
        bf.pack(fill=tk.X)
        if self.google.is_configured:
            ttk.Button(bf, text="Anmelden / Token erneuern",
                       command=self._authenticate).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(bf, text="Schließen", command=self.destroy).pack(side=tk.LEFT)

    def _authenticate(self):
        try:
            self.google.authenticate()
            messagebox.showinfo("Erfolg", "Anmeldung erfolgreich!", parent=self)
            self.refresh_cb()
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Anmeldung fehlgeschlagen", str(exc), parent=self)
