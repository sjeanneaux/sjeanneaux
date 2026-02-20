# Startup Manager

Eine kleine Windows-Desktopanwendung, die beim Systemstart automatisch:

- **Aufgaben** aus Google Tasks anzeigt (erledigte abhaken/erstellen)
- **heutige Kalendertermine** aus Google Calendar anzeigt
- **konfigurierte Webseiten** automatisch oder auf Knopfdruck öffnet

---

## Voraussetzungen

- Windows 10 oder 11
- Python 3.9 oder neuer
  → [python.org/downloads](https://www.python.org/downloads/)

---

## Installation

### 1. Abhängigkeiten installieren

```
pip install -r requirements.txt
```

### 2. Google-Konto einrichten

Die Anwendung greift via Google API auf Kalender und Aufgaben zu.
Hierfür wird eine eigene OAuth2-Anwendung im Google Cloud Console benötigt.

**Schritt-für-Schritt:**

1. Öffne [console.cloud.google.com](https://console.cloud.google.com)
2. Erstelle ein neues Projekt (z. B. „Startup Manager")
3. Gehe zu **APIs & Dienste → Bibliothek** und aktiviere:
   - **Google Calendar API**
   - **Google Tasks API**
4. Gehe zu **APIs & Dienste → Anmeldedaten**
5. Klicke **Anmeldedaten erstellen → OAuth-Client-ID**
   - Anwendungstyp: **Desktop-App**
   - Einen beliebigen Namen vergeben
6. Klicke auf **JSON herunterladen**
7. Benenne die Datei in **`credentials.json`** um
8. Lege sie in den **Programmordner** (neben `main.py`)

### 3. Anwendung starten

```
python main.py
```

Beim ersten Start öffnet sich ein Browserfenster zur Google-Anmeldung.
Nach der Bestätigung wird ein `token.json` erstellt – diese Datei
enthält das Zugriffstoken und wird lokal gespeichert.

---

## Autostart einrichten

1. Starte die Anwendung (`python main.py`)
2. Gehe zu **Einstellungen → Autostart ein/ausschalten**
3. Der Eintrag wird in der Windows-Registry gespeichert:
   `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

Zum Deaktivieren: denselben Menüpunkt erneut aufrufen.

---

## Webseiten konfigurieren

In der Anwendung: **Einstellungen → Webseiten verwalten...**

Für jede Webseite kann eingestellt werden:
- **Name** und **URL**
- **Beim Start automatisch öffnen** – öffnet die Seite beim Programmstart
- **Aktiv** – ob die Webseite in der Liste erscheint

Über den Button **„Ausgewählte öffnen"** / **„Alle öffnen"** können
Webseiten jederzeit manuell gestartet werden.

---

## Projektstruktur

```
startup-manager/
├── main.py              # Einstiegspunkt
├── app.py               # Haupt-GUI (tkinter)
├── google_service.py    # Google Calendar & Tasks API
├── config_manager.py    # Konfiguration lesen/schreiben
├── autostart.py         # Windows-Registry-Autostart
├── config.json          # Benutzerkonfiguration (wird automatisch angelegt)
├── credentials.json     # Google OAuth2 (manuell herunterladen, s. o.)
├── token.json           # OAuth2-Token (wird automatisch erstellt)
└── requirements.txt     # Python-Abhängigkeiten
```

---

## Tastaturbelegung

| Taste | Funktion              |
|-------|-----------------------|
| F5    | Daten aktualisieren   |

---

## Häufige Probleme

**„credentials.json nicht gefunden"**
→ Datei aus Google Cloud Console herunterladen und in den Programmordner legen.

**„Die Google-Bibliotheken sind nicht installiert"**
→ `pip install -r requirements.txt` ausführen.

**Browser öffnet sich nicht bei der Anmeldung**
→ Sicherstellen, dass ein Standardbrowser eingestellt ist.

**Aufgaben oder Termine werden nicht angezeigt**
→ F5 drücken oder prüfen, ob das Google-Konto korrekt angemeldet ist
   (Einstellungen → Google-Konto einrichten → Anmelden).
