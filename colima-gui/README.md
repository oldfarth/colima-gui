# Colima Dashboard

Ein webbasiertes GUI-Steuerpult für die Verwaltung von Colima-VMs auf macOS.

**Programmierung: Hermes AI Agent** – ein autonomer KI-Assistent, entwickelt für die effiziente Verwaltung von virtuellen Maschinen.

## Funktionen

- VM-Übersicht mit Status, CPU, Arbeitsspeicher und Festplattenauslastung
- Start, Stopp, Neustart und Löschen von VMs direkt über das Web-GUI
- Docker-Container innerhalb der VMs einsehen
- Automatische Status-Erkennung (Running / Stopped / Paused)

## Voraussetzungen

- **macOS** (Apple Silicon ARM64 oder Intel)
- **Homebrew** installiert (`/opt/homebrew/bin/brew`)
- **Colima** installiert (`/opt/homebrew/bin/colima`)
- **Python 3** (über Homebrew)

## Installation

### 1. Colima-VM einrichten

Falls noch keine Colima-VM existiert, erstelle eine:

```bash
brew install --cask colima
colima start --cpu 4 --memory 8
```

### 2. Streamlit installieren

```bash
pip install streamlit
```

### 3. Repository klonen

```bash
git clone https://github.com/oldfarth/colima-gui.git
cd colima-gui
```

### 4. Dashboard starten

```bash
pip install -r requirements.txt
streamlit run app.py
```

Der Browser öffnet sich automatisch unter: **http://localhost:8501**

## Nutzung

1. **VM-Übersicht**: Zeigt alle Colima-Instanzen mit ihrem aktuellen Status.
2. **Steuern**: Verwende die Buttons `Start`, `Stop`, `Restart` oder `Delete`, um VMs zu verwalten.
3. **Container**: Docker-Container werden automatisch angezeigt, wenn die VM läuft.

## Projektstruktur

```
colima-gui/
├── app.py               # Streamlit-GUI-Hauptprogramm
├── requirements.txt     # Python-Abhängigkeiten
├── .gitignore          # Git-Auschlussdatei
└── README.md           # Diese Datei
```

## Lizenz

MIT License

## Credits

**Programmiert vom Hermes AI Agent** – ein autonomer KI-Assistent, der diesen Code vollständig erstellt hat.

---

*Erstellt mit ❤️ auf einem Mac von [oldfarth](https://github.com/oldfarth)*
