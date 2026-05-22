# Changelog

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
