#!/usr/bin/env python3
"""
Startup Manager
===============
Startet beim Systemstart, zeigt Aufgaben und Kalendertermine,
und öffnet konfigurierte Webseiten.

Verwendung:
    python main.py

Unter Windows kann die Anwendung über
    Einstellungen → Autostart ein/ausschalten
automatisch beim Anmelden gestartet werden.
"""

import sys
import tkinter as tk


def main():
    root = tk.Tk()
    try:
        from app import StartupManagerApp
        StartupManagerApp(root)
        root.mainloop()
    except Exception as exc:
        import traceback
        from tkinter import messagebox
        messagebox.showerror(
            "Startfehler",
            f"Die Anwendung konnte nicht gestartet werden:\n\n{exc}\n\n"
            f"{traceback.format_exc()}",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
