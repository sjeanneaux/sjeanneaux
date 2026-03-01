# PTP Workboard

Eine schlanke, lokale Workboard-App (Mix aus Trello + Asana + Monday.com) — komplett im Browser, ohne Server, ohne Internet-Verbindung.

---

## Schnellstart

```
PTP_Workboard/
└── index.html   ← Diese Datei im Browser öffnen
```

1. Datei `index.html` im Datei-Explorer doppelklicken
   **oder** per Terminal:
   ```bash
   # macOS
   open PTP_Workboard/index.html

   # Linux
   xdg-open PTP_Workboard/index.html

   # Windows
   start PTP_Workboard/index.html
   ```
2. Die App startet sofort mit Demo-Daten (Boards **WKS_QM** und **WKS_Projekte**).

> **Hinweis:** Alle Daten leben nur im Arbeitsspeicher der Browser-Session.
> Beim Schließen des Tabs gehen nicht-exportierte Änderungen verloren.

---

## Features

### Views
| View | Beschreibung |
|------|-------------|
| **Kanban** | 5 Spalten: Backlog · Diese Woche · Heute · Waiting · Done |
| **Liste** | Sortierbare Tabelle nach Titel, Status, Owner, Due Date, Quelle |
| **Tabelle** | Erweiterte Ansicht mit Beschreibungsspalte |

### Aufgaben-Felder
| Feld | Beschreibung |
|------|-------------|
| Titel | Pflichtfeld |
| Beschreibung | Freitext, mehrzeilig |
| Owner | Name der verantwortlichen Person |
| Due Date | Fälligkeitsdatum (Ampelfarbe bei Überschreitung) |
| Status | Backlog / Diese Woche / Heute / Waiting / Done |
| Ampel | 🟢 Grün · 🟠 Orange · 🔴 Rot |
| Tags | Report · Analyse · Budget · Meeting (Mehrfachauswahl) |
| Quelle | Herkunft der Aufgabe (E-Mail, Meeting, Ticket …) |
| Board | Aufgabe einem Board zuordnen / zwischen Boards verschieben |

### Interaktion
- **Drag & Drop** — Karten im Kanban-Board zwischen Spalten ziehen
- **Klick auf Karte** — Aufgabe öffnen und bearbeiten
- **+ Button** je Spalte oder oben rechts — neue Aufgabe in diesem Status
- **✕ Button** auf Karte (sichtbar beim Hover) — schnell löschen mit Bestätigung
- **Suche** — durchsucht Titel, Beschreibung, Owner, Quelle, Tags
- **Filter** — Owner-Dropdown, Ampel-Dropdown, Tag-Buttons kombinierbar
- **Sortierung** — Klick auf Spaltenköpfe in Liste/Tabelle (2. Klick kehrt Reihenfolge um)

---

## Tastaturkürzel

| Taste | Aktion |
|-------|--------|
| `N` | Neue Aufgabe erstellen |
| `/` | Suchfeld fokussieren |
| `1` | Kanban-View |
| `2` | Listen-View |
| `3` | Tabellen-View |
| `Esc` | Modal / Suche schließen |

---

## Export & Import

### Export
1. Button **↓ Export** oben rechts klicken
2. Datei `workboard_YYYY-MM-DD.json` wird heruntergeladen
3. Datei an einem sicheren Ort speichern (z.B. Netzlaufwerk, SharePoint, lokaler Ordner)

### Import
1. Button **↑ Import** oben rechts klicken
2. Zuvor exportierte `.json`-Datei auswählen
3. Alle Boards und Aufgaben werden geladen — bisherige Session-Daten werden ersetzt

### JSON-Format
```json
{
  "version": "1.0",
  "app": "PTP_Workboard",
  "exportedAt": "2025-03-01T10:00:00.000Z",
  "boards": [
    {
      "id": "...",
      "name": "WKS_QM",
      "tasks": [
        {
          "id": "...",
          "title": "Aufgabentitel",
          "description": "...",
          "owner": "Name",
          "dueDate": "2025-03-15",
          "status": "Diese Woche",
          "ampel": "orange",
          "tags": ["Report", "Analyse"],
          "quelle": "Meeting 01.03"
        }
      ]
    }
  ]
}
```

---

## Demo-Daten

Beim ersten Start werden zwei Boards mit je 8 Beispielaufgaben geladen:

**WKS_QM** — Qualitätsmanagement-Aufgaben
Owners: S. Jeanneaux · M. Schmidt · T. Müller

**WKS_Projekte** — Projektmanagement-Aufgaben
Owners: S. Jeanneaux · K. Weber · T. Müller

Aufgaben verteilen sich über alle 5 Status-Spalten mit realistischen Due Dates relativ zum heutigen Tag.

---

## Technische Details

- **Technologie:** Reines HTML5 + CSS3 + Vanilla JavaScript — keine Abhängigkeiten
- **Datenspeicherung:** Nur `in-memory` (kein localStorage, kein IndexedDB)
- **Offline:** Vollständig offline-fähig (keine CDN-Aufrufe, keine APIs)
- **Browser-Kompatibilität:** Alle modernen Browser (Chrome, Firefox, Edge, Safari)
- **Dateigröße:** ~25 KB (alles in einer einzigen HTML-Datei)

---

## Ampel-Bedeutung

| Farbe | Bedeutung |
|-------|-----------|
| 🟢 Grün | Alles im Plan |
| 🟠 Orange | Aufmerksamkeit nötig / Verzögerungsgefahr |
| 🔴 Rot | Kritisch / Eskalation erforderlich |

Das **Due-Date-Highlighting** funktioniert automatisch:
- Heute oder früher → **rot** (überfällig)
- Innerhalb 3 Tage → **orange** (bald fällig)
- Weiter in der Zukunft → neutral

---

*PTP Workboard — Pure Frontend, kein Server, kein Internet erforderlich.*
