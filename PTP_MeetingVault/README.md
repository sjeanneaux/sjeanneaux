# PTP MeetingVault

Lokale Meeting-Gedächtnis-App — komplett im Browser, ohne Server, ohne Internet.
Strukturiert Meeting-Informationen aus hochgeladenen Textdateien in fünf klar getrennte Bereiche.

---

## Schnellstart

```
PTP_MeetingVault/
└── index.html   ← Diese Datei im Browser öffnen
```

1. Datei `index.html` doppelklicken **oder** per Terminal:
   ```bash
   # macOS
   open PTP_MeetingVault/index.html

   # Linux
   xdg-open PTP_MeetingVault/index.html

   # Windows
   start PTP_MeetingVault/index.html
   ```
2. **+ Neues Meeting** erstellen
3. **↑ Input importieren** — Textdateien (.txt / .md) hochladen (Mehrfach-Upload möglich)
4. Inhalte in den Tabs strukturiert erfassen

> **Hinweis:** Alle Daten leben nur im Arbeitsspeicher der Browser-Session.
> **↓ Session speichern** exportiert alle Meetings als JSON-Datei.
> **↑ Session laden** stellt eine gespeicherte Session wieder her.

---

## Workflow

### 1. Meeting anlegen
Klick auf **+ Neues Meeting** in der linken Leiste. Titel, Datum und Teilnehmer direkt oben bearbeiten.

### 2. Quelldateien importieren
Klick auf **↑ Importieren** (Header oder Meeting-Header).
Unterstützte Formate: `.txt`, `.md`
Typische Quellen: Agenda, Teilnehmerliste, Chat-Export, Notizen, Zieldokument.

Die hochgeladenen Dateien erscheinen als **Quellen-Panel** rechts — als Referenz beim Erfassen der strukturierten Daten.

### 3. Tabs ausfüllen

| Tab | Inhalt |
|-----|--------|
| **Protokoll** | Bis zu 12 Bulletpoints. `Enter` fügt neuen Punkt hinzu. |
| **Entscheidungen** | Tabelle: Entscheidung · Begründung · Owner · Deadline · Quelle |
| **Maßnahmen** | Tabelle: Maßnahme · Owner · Deadline · Status · Quelle |
| **Risiken** | Tabelle: Ampel · Risiko · Impact · Mitigation · Owner · Quelle |
| **Offene Fragen** | Bis zu 10 nummerierte Fragen |

**Quelle** im jeweiligen Datensatz = Dateiname der importierten Quelldatei (Dropdown).
Fehlende Informationen werden als `[OFFEN]` erfasst.

### 4. Exportieren

| Datei | Inhalt |
|-------|--------|
| `Minutes.md` | Protokoll + Offene Fragen als Markdown |
| `DecisionLog.csv` | Alle Entscheidungen als CSV |
| `Actions.csv` | Alle Maßnahmen als CSV |
| `Risks.csv` | Alle Risiken als CSV |
| `FollowUp_Email.md` | Fertige Follow-Up-E-Mail als Markdown |

Export-Buttons befinden sich direkt im jeweiligen Tab.

---

## Tastaturkürzel

| Taste | Aktion |
|-------|--------|
| `N` | Neues Meeting erstellen |
| `1` | Tab: Protokoll |
| `2` | Tab: Entscheidungen |
| `3` | Tab: Maßnahmen |
| `4` | Tab: Risiken |
| `5` | Tab: Offene Fragen |
| `Enter` (in Bullet) | Nächsten Punkt hinzufügen |
| `Backspace` (leerer Bullet) | Punkt löschen |
| `Esc` | Fokus aufheben |

---

## Session-Persistenz

Da die App keine automatische Speicherung vornimmt:

- **↓ Session speichern** → Alle Meetings werden als `meetingvault_YYYY-MM-DD.json` heruntergeladen
- **↑ Session laden** → Zuvor gespeicherte JSON-Datei hochladen und Session wiederherstellen

---

## Ampel-Bedeutung (Risiken)

| Farbe | Bedeutung |
|-------|-----------|
| 🟢 Grün | Geringes Risiko / unter Kontrolle |
| 🟠 Orange | Mittleres Risiko / Aufmerksamkeit erforderlich |
| 🔴 Rot | Hohes Risiko / Eskalation erforderlich |

---

## Technische Details

- **Technologie:** Reines HTML5 + CSS3 + Vanilla JavaScript — keine Abhängigkeiten
- **Datenspeicherung:** Nur `in-memory` (kein localStorage, kein IndexedDB)
- **Offline:** Vollständig offline-fähig
- **Browser:** Alle modernen Browser (Chrome, Firefox, Edge, Safari)

---

*PTP MeetingVault — Pure Frontend, kein Server, kein Internet erforderlich.*
