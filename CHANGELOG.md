# Changelog

## [1.3.0] – 2026-05-23
### Added
- 5 maintenance sensors (Descaling, Backflush, Group Head, Gaskets, Water Filter) — state is `ok / soon / due / never`, attributes: `days_since`, `shots_since`, `last_date`, `pct`; data sourced from GLP `/api/maintenance`; gracefully unavailable on older GLP versions; closes #4

## [1.2.1] – 2026-05-23
### Fixed
- Default URL changed from `http://localhost:8099` to `http://homeassistant.local:8099` — localhost doesn't resolve from HA core to the add-on container; closes #3
- Shot timestamps now parsed correctly — GLP uses Unix seconds; previous code divided by 1000 (assumed ms), causing all shot dates to appear as 1970; closes #3

## [1.2.0] – 2026-05-23
### Added
- `shots_today` sensor — counts how many shots were pulled today (HA-configured timezone); closes #2

## [1.1.0] – 2026-05-22
### Added
- `is_brewing` binary sensor via fast (2 s) polling of `/api/live/data`
- `gaggiuino_profiler_shot_completed` HA event fired on every new shot with full shot data
- Options flow: URL and poll interval configurable after setup (Settings → Integration → Configure)
- Diagnostics support for HA bug reports

### Fixed
- `last_shot_date` and `last_sync` now parsed as proper `datetime` objects (previously strings caused TIMESTAMP device class to show "unknown")

## [1.0.0] – 2026-05-22
### Added
- Initial release
- 14 sensor entities from GLP `/api/status` and `/shots.json`
- Config flow with connection validation
- HACS manifest and logo
