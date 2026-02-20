"""
google_service.py
Kapselt den Zugriff auf Google Calendar und Google Tasks API.
"""

import threading
from datetime import datetime, timezone
from pathlib import Path

# Prüfen ob Google-Bibliotheken installiert sind
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

# Benötigte OAuth2-Berechtigungen
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/tasks",
]


class GoogleService:
    """Verwaltet Authentifizierung und Datenabruf von Google APIs."""

    def __init__(self):
        self._base = Path(__file__).parent
        self._credentials_path = self._base / "credentials.json"
        self._token_path = self._base / "token.json"
        self._calendar = None
        self._tasks = None
        self._lock = threading.Lock()

    # --- Zustandsabfragen ---

    @property
    def is_available(self) -> bool:
        """True wenn die Google-Bibliotheken installiert sind."""
        return AVAILABLE

    @property
    def is_configured(self) -> bool:
        """True wenn credentials.json vorhanden ist."""
        return AVAILABLE and self._credentials_path.exists()

    @property
    def is_authenticated(self) -> bool:
        """True wenn ein gültiges Token vorliegt."""
        return self._calendar is not None and self._tasks is not None

    # --- Authentifizierung ---

    def authenticate(self):
        """
        Führt den OAuth2-Flow durch.
        Öffnet beim ersten Mal den Browser zur Google-Anmeldung.
        """
        if not self.is_configured:
            raise RuntimeError(
                "credentials.json nicht gefunden.\n"
                "Bitte Google API-Zugangsdaten einrichten (siehe README)."
            )

        creds = None
        if self._token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self._token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self._credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self._token_path, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

        with self._lock:
            self._calendar = build("calendar", "v3", credentials=creds)
            self._tasks = build("tasks", "v1", credentials=creds)

    def _ensure_authenticated(self):
        """Stellt sicher, dass eine aktive Verbindung besteht."""
        if not self.is_authenticated:
            self.authenticate()

    # --- Kalender ---

    def get_today_events(self) -> list:
        """
        Gibt alle Termine des heutigen Tages zurück.
        Rückgabe: Liste von dicts mit 'summary', 'start', 'end', 'location'.
        """
        self._ensure_authenticated()

        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        result = self._calendar.events().list(
            calendarId="primary",
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = []
        for item in result.get("items", []):
            events.append({
                "summary": item.get("summary", "(Kein Titel)"),
                "start": item["start"].get("dateTime", item["start"].get("date", "")),
                "end": item["end"].get("dateTime", item["end"].get("date", "")),
                "location": item.get("location", ""),
                "description": item.get("description", ""),
            })
        return events

    # --- Tasks ---

    def get_task_lists(self) -> list:
        """Gibt alle Aufgabenlisten zurück."""
        self._ensure_authenticated()
        result = self._tasks.tasklists().list(maxResults=100).execute()
        return result.get("items", [])

    def get_tasks(self, show_completed: bool = False) -> list:
        """
        Gibt alle Aufgaben aus allen Listen zurück.
        Rückgabe: Liste von dicts mit 'id', 'tasklist_id', 'title', 'status', 'due', 'notes'.
        """
        self._ensure_authenticated()
        task_lists = self.get_task_lists()

        all_tasks = []
        for tl in task_lists:
            params = {
                "tasklist": tl["id"],
                "showCompleted": show_completed,
                "showHidden": show_completed,
                "maxResults": 100,
            }
            result = self._tasks.tasks().list(**params).execute()
            for task in result.get("items", []):
                if task.get("status") == "completed" and not show_completed:
                    continue
                if task.get("deleted"):
                    continue
                all_tasks.append({
                    "id": task["id"],
                    "tasklist_id": tl["id"],
                    "tasklist_name": tl.get("title", ""),
                    "title": task.get("title", "(Kein Titel)"),
                    "status": task.get("status", "needsAction"),
                    "due": task.get("due", ""),
                    "notes": task.get("notes", ""),
                })

        return all_tasks

    def update_task_status(self, tasklist_id: str, task_id: str, completed: bool):
        """Markiert eine Aufgabe als erledigt oder offen."""
        self._ensure_authenticated()
        task = self._tasks.tasks().get(tasklist=tasklist_id, task=task_id).execute()
        task["status"] = "completed" if completed else "needsAction"
        if completed:
            task["completed"] = datetime.now(timezone.utc).isoformat()
        else:
            task.pop("completed", None)
        self._tasks.tasks().update(
            tasklist=tasklist_id, task=task_id, body=task
        ).execute()

    def create_task(self, tasklist_id: str, title: str, notes: str = ""):
        """Erstellt eine neue Aufgabe in der angegebenen Liste."""
        self._ensure_authenticated()
        body = {"title": title}
        if notes:
            body["notes"] = notes
        return self._tasks.tasks().insert(tasklist=tasklist_id, body=body).execute()
