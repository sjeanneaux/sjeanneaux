# Startup Manager – Claude Context

## Project Overview

A Windows desktop application that runs at startup and displays:
- **Google Tasks** – view, create, and check off tasks
- **Google Calendar** – today's events
- **Websites** – configurable list of URLs to auto-open or launch on demand

Built with Python + tkinter, integrating with Google APIs via OAuth2.

## Project Structure

```
startup-manager/
├── main.py              # Entry point – creates tkinter root and launches app
├── app.py               # Main GUI (StartupManagerApp class, tkinter)
├── google_service.py    # Google Calendar & Tasks API integration
├── config_manager.py    # Read/write config.json
├── autostart.py         # Windows Registry autostart toggle
├── config.json          # User config (websites, settings) – auto-created
├── credentials.json     # Google OAuth2 client secret (not committed)
├── token.json           # OAuth2 token cache (not committed)
├── requirements.txt     # Python dependencies
└── PTP_Workboard/       # Standalone offline Kanban/List/Table web app (HTML/JS)
```

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Google API Credentials

The app requires `credentials.json` from Google Cloud Console with Calendar API and Tasks API enabled. This file is gitignored and must be provided manually.

### Run the App

```bash
python main.py
```

On first run, a browser window opens for Google OAuth2 login. A `token.json` is created and cached locally.

## Key Technologies

- **Python 3.9+** – required
- **tkinter** – standard library GUI (comes with Python on Windows)
- **google-api-python-client** – Google API client
- **google-auth-oauthlib** – OAuth2 flow
- **google-auth-httplib2** – HTTP transport for Google auth

## Development Notes

- The app is designed for **Windows 10/11**. tkinter and registry access (autostart) are Windows-specific.
- `config.json` is automatically created on first run; do not hard-code defaults that belong there.
- Google API calls happen in background threads to avoid blocking the UI.
- Press **F5** to refresh tasks and calendar data.
- Autostart uses `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` in the Windows Registry.

## No Test Suite / No Linter Config

There is currently no automated test suite or linter configuration. Manual testing is done by running `python main.py` on Windows.

## Sensitive Files (never commit)

- `credentials.json` – Google OAuth2 client secret
- `token.json` – OAuth2 access/refresh token
