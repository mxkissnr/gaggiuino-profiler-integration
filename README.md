# Gaggiuino Local Profiler — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Exposes [Gaggiuino Local Profiler](https://github.com/mxkissnr/gaggiuino-local-profiler) data as Home Assistant sensors.

## Requirements

- [Gaggiuino Local Profiler](https://github.com/mxkissnr/gaggiuino-local-profiler) add-on installed and running
- Home Assistant 2024.1.0 or newer

## Installation

### HACS (recommended)

1. Open HACS → **Integrations** → ⋮ → **Custom repositories**
2. Add `https://github.com/mxkissnr/gaggiuino-profiler-integration` as **Integration**
3. Search for *Gaggiuino Local Profiler* and install
4. Restart Home Assistant

### Manual

1. Copy `custom_components/gaggiuino_profiler/` into your `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for *Gaggiuino Local Profiler*
3. Enter the URL of your GLP instance (e.g. `http://homeassistant.local:8099`)

## Sensors

| Entity | Description | Unit |
|--------|-------------|------|
| Machine Status | `online` / `error` | — |
| Shot Count | Total shots synced | shots |
| Last Shot Profile | Profile name | — |
| Last Shot Score | Manual score | — |
| Last Shot Date | Timestamp | — |
| Last Shot Duration | Shot duration | s |
| Last Shot Avg Pressure | Average extraction pressure | bar |
| Last Shot Yield | Output weight | g |
| Last Shot Brew Ratio | Yield ÷ dose | — |
| Last Shot Dose | Input dose | g |
| Last Shot Coffee | Bean annotation | — |
| Last Shot Grinder | Grinder annotation | — |
| Last Sync | Last sync timestamp | — |
| Machine Hostname | Gaggiuino hostname | — |

## Links

- [Add-on repository](https://github.com/mxkissnr/gaggiuino-local-profiler)
- [Issues](https://github.com/mxkissnr/gaggiuino-profiler-integration/issues)
