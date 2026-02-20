"""
config_manager.py
Verwaltet die Anwendungskonfiguration (Webseiten, Einstellungen).
"""

import json
from pathlib import Path

DEFAULT_CONFIG = {
    "websites": [
        {
            "name": "Google Mail",
            "url": "https://mail.google.com",
            "auto_open": False,
            "enabled": True
        },
        {
            "name": "Google Kalender",
            "url": "https://calendar.google.com",
            "auto_open": False,
            "enabled": True
        },
        {
            "name": "Google News",
            "url": "https://news.google.com",
            "auto_open": False,
            "enabled": False
        }
    ],
    "settings": {
        "auto_open_on_startup": False,
        "show_completed_tasks": False,
        "refresh_interval_minutes": 5,
        "window_geometry": "980x680+80+80"
    }
}


class ConfigManager:
    """Laedt und speichert die Konfiguration in config.json."""

    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.config = self._load()

    def _load(self) -> dict:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Fehlende Schlüssel mit Standardwerten auffüllen
                merged = DEFAULT_CONFIG.copy()
                merged.update(data)
                # Einstellungen ebenfalls mergen
                merged["settings"] = {**DEFAULT_CONFIG["settings"], **data.get("settings", {})}
                return merged
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "websites": [w.copy() for w in DEFAULT_CONFIG["websites"]],
            "settings": DEFAULT_CONFIG["settings"].copy()
        }

    def save(self):
        """Speichert die aktuelle Konfiguration."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get_websites(self) -> list:
        return self.config.get("websites", [])

    def set_websites(self, websites: list):
        self.config["websites"] = websites
        self.save()

    def get_settings(self) -> dict:
        return self.config.get("settings", {})

    def update_settings(self, **kwargs):
        self.config["settings"].update(kwargs)
        self.save()
