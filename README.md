<p align="center">
  <img src="custom_components/gaggiuino_profiler/logo.png" alt="Gaggiuino Local Profiler" width="120"/>
</p>

<h1 align="center">Gaggiuino Local Profiler — Home Assistant Integration</h1>

<p align="center">
  <a href="https://github.com/mxkissnr/gaggiuino-profiler-integration/releases">
    <img src="https://img.shields.io/github/v/tag/mxkissnr/gaggiuino-profiler-integration?color=%23f59e0b&label=Version&style=flat-square" alt="Version"/>
  </a>
  <a href="https://github.com/custom-components/hacs">
    <img src="https://img.shields.io/badge/HACS-Custom-orange?style=flat-square" alt="HACS Custom"/>
  </a>
  <img src="https://img.shields.io/badge/Home%20Assistant-2024.1%2B-41bdf5?logo=home-assistant&style=flat-square" alt="HA Version"/>
  <img src="https://img.shields.io/badge/Polling-local-6b7280?style=flat-square" alt="Local Polling"/>
</p>

<p align="center">
  Bindet den <a href="https://github.com/mxkissnr/gaggiuino-local-profiler">Gaggiuino Local Profiler</a> als native HA-Entities ein —<br/>
  Maschinenstatus, Shotdaten und Live-Brühstatus direkt in Home Assistant.
</p>

---

## ⚡ Schnellinstallation via HACS

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=mxkissnr&repository=gaggiuino-profiler-integration&category=integration">
  <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Integration via HACS hinzufügen" height="40"/>
</a>

---

## ✨ Was diese Integration macht

| | Feature | Beschreibung |
|---|---|---|
| ☕ | **Brühstatus** | Binary Sensor aktualisiert sich alle 2 Sekunden — ideal als Automations-Trigger |
| 📊 | **14 Shot-Sensoren** | Profil, Score, Dauer, Druck, Yield, Ratio, Dose, Kaffee, Grinder u.v.m. |
| 🔔 | **Shot-Event** | HA-Event `gaggiuino_profiler_shot_completed` mit allen Shotdaten nach jedem Bezug |
| ⚙️ | **Konfigurierbar** | URL und Poll-Interval jederzeit über *Einstellungen → Integration → Konfigurieren* anpassbar |
| 🔍 | **Diagnose** | HA-Diagnostics-Export für einfache Fehlerberichte |

---

## 🚀 Installation

### HACS (empfohlen)

1. Button oben klicken — oder: HACS → Integrationen → ⋮ → **Benutzerdefinierte Repositories**
2. URL `https://github.com/mxkissnr/gaggiuino-profiler-integration` als **Integration** hinzufügen
3. Nach *Gaggiuino Local Profiler* suchen und installieren
4. Home Assistant neu starten

### Manuell

1. Den Ordner `custom_components/gaggiuino_profiler/` in das Verzeichnis `config/custom_components/` kopieren
2. Home Assistant neu starten

---

## ⚙️ Einrichtung

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. Nach *Gaggiuino Local Profiler* suchen
3. URL des GLP-Add-ons eingeben, z. B.:
   ```
   http://homeassistant.local:8099
   ```
   Die Integration testet die Verbindung direkt — bei Fehler erscheint eine Fehlermeldung.

### Optionen nach der Einrichtung anpassen

**Einstellungen → Geräte & Dienste → Gaggiuino Local Profiler → Konfigurieren**

| Option | Standard | Beschreibung |
|---|---|---|
| URL | *(eingegebene URL)* | URL des GLP-Add-ons |
| Poll-Interval | `60` | Aktualisierungsintervall in Sekunden (10–300) |

---

## 📋 Entities

### Sensoren

| Entity | Beschreibung | Einheit |
|---|---|---|
| Machine Status | `online` / `error` | — |
| Shot Count | Gesamtzahl der gespeicherten Shots | shots |
| Last Shot Profile | Name des Extraktionsprofils | — |
| Last Shot Score | Automatischer 0–100-Score | — |
| Last Shot Date | Zeitstempel des letzten Shots | — |
| Last Shot Duration | Bezugsdauer | s |
| Last Shot Avg Pressure | Durchschnittlicher Extraktionsdruck | bar |
| Last Shot Yield | Ausbeute (Output-Gewicht) | g |
| Last Shot Brew Ratio | Yield ÷ Dose | — |
| Last Shot Dose | Einwaage (Input-Gewicht) | g |
| Last Shot Coffee | Kaffee-Annotation | — |
| Last Shot Grinder | Grinder-Annotation | — |
| Last Sync | Zeitstempel der letzten Synchronisation | — |
| Machine Hostname | Hostname des Gaggiuino-Controllers | — |

### Binary Sensor

| Entity | Beschreibung | Aktualisierung |
|---|---|---|
| Brewing | `true` während eines aktiven Bezugs | alle 2 Sekunden |

---

## 🔔 HA-Event: `gaggiuino_profiler_shot_completed`

Nach jedem abgeschlossenen Bezug feuert die Integration automatisch dieses Event. Es enthält alle relevanten Shotdaten:

```yaml
event_type: gaggiuino_profiler_shot_completed
data:
  shot_id: 54
  profile: "Adaptive"
  duration_s: 28.4
  yield_g: 42.1
  dose_g: 18.0
  ratio: 2.34
  avg_pressure: 8.72
  score: 87
  coffee: "Ethiopia Yirgacheffe"
  grinder: "DF64"
```

### Automationsbeispiele

**Benachrichtigung nach jedem Shot:**
```yaml
automation:
  trigger:
    platform: event
    event_type: gaggiuino_profiler_shot_completed
  action:
    service: notify.mobile_app
    data:
      title: "☕ Shot abgeschlossen"
      message: >
        {{ trigger.event.data.profile }} –
        {{ trigger.event.data.duration_s }}s,
        Ratio 1:{{ trigger.event.data.ratio }}
```

**Licht nach Bezug dimmen:**
```yaml
automation:
  trigger:
    platform: state
    entity_id: binary_sensor.gaggiuino_local_profiler_brewing
    from: "on"
    to: "off"
  action:
    service: light.turn_on
    target:
      entity_id: light.kueche
    data:
      brightness_pct: 30
```

**Shot in Google Sheets loggen (via Webhook):**
```yaml
automation:
  trigger:
    platform: event
    event_type: gaggiuino_profiler_shot_completed
  action:
    service: rest_command.log_shot
    data:
      shot_id: "{{ trigger.event.data.shot_id }}"
      profile: "{{ trigger.event.data.profile }}"
      yield_g: "{{ trigger.event.data.yield_g }}"
```

---

## 🏗️ Architektur

```
Home Assistant
├── GlpDataCoordinator  (60 s, konfigurierbar)
│   ├── GET /api/status    → Maschinenstatus, shotCount, lastSync
│   └── GET /shots.json    → Shotdaten, Annotationen, Datapoints
│
├── GlpLiveCoordinator  (2 s)
│   └── GET /api/live/data → isLive (Brühstatus)
│
└── Event Bus
    └── gaggiuino_profiler_shot_completed  (bei neuer shot_id)
```

---

## 🔍 Diagnose

Bei Problemen: **Einstellungen → Geräte & Dienste → Gaggiuino Local Profiler → Gerät → Diagnose herunterladen**

Die Diagnosedatei enthält die aktuellen Coordinator-Daten (ohne sensible Informationen) und erleichtert das Melden von Issues.

---

<p align="center">
  <a href="CHANGELOG.md">📋 Changelog</a> ·
  <a href="https://github.com/mxkissnr/gaggiuino-local-profiler">🔧 GLP Add-on</a> ·
  <a href="https://github.com/mxkissnr/gaggiuino-profiler-integration/issues">🐛 Issues</a>
</p>
