"""
autostart.py
Verwaltet den Windows-Autostart via Registry.
Funktioniert nur unter Windows.
"""

import sys
from pathlib import Path


def _get_app_command() -> str:
    """Gibt den Startbefehl der Anwendung zurück."""
    if getattr(sys, "frozen", False):
        # Als .exe kompiliert
        return f'"{sys.executable}"'
    else:
        script = str(Path(__file__).parent / "main.py")
        return f'"{sys.executable}" "{script}"'


def toggle_autostart() -> bool:
    """
    Schaltet den Windows-Autostart um.
    Gibt True zurück wenn jetzt aktiviert, False wenn deaktiviert.
    Wirft RuntimeError wenn nicht unter Windows.
    """
    if sys.platform != "win32":
        raise RuntimeError("Autostart wird nur unter Windows unterstützt.")

    import winreg  # nur Windows

    app_name = "StartupManager"
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        reg_path,
        0,
        winreg.KEY_ALL_ACCESS,
    )

    try:
        winreg.QueryValueEx(key, app_name)
        # Eintrag existiert -> entfernen (deaktivieren)
        winreg.DeleteValue(key, app_name)
        winreg.CloseKey(key)
        return False
    except FileNotFoundError:
        # Kein Eintrag -> hinzufügen (aktivieren)
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, _get_app_command())
        winreg.CloseKey(key)
        return True


def is_autostart_enabled() -> bool:
    """Gibt True zurück wenn der Autostart-Eintrag in der Registry vorhanden ist."""
    if sys.platform != "win32":
        return False
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ,
        )
        winreg.QueryValueEx(key, "StartupManager")
        winreg.CloseKey(key)
        return True
    except Exception:
        return False
