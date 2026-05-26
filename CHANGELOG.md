# Changelog

## [1.8.0] – 2026-05-26
### Added
- `machine_temperature` and `machine_target_temperature` sensors — read from `/api/preheat` (`temp` and `targetTemp` fields); device class `temperature`, unit °C, state class `measurement`; requires GLP add-on v1.51.0+; closes #12

## [1.7.0] – 2026-05-26
### Added
- REST API proxy views at `/api/glp/orders/*` and `/api/glp/shots/*` — the integration now registers three `HomeAssistantView` endpoints that forward requests to the GLP add-on using the coordinator's URL and API token; allows the GLP Order Card to access the orders API via `hass.fetchWithAuth` without requiring a Supervisor ingress session; closes #13

## [1.6.0] – 2026-05-25
### Added
- New `Maintenance Grinders` sensor — aggregates all grinder cleaning entries from GLP v1.40.0 into a single worst-status sensor; per-grinder status, days_since, shots_since, last_date, and pct are exposed as state attributes keyed by grinder name; closes #10

## [1.5.1] – 2026-05-25
### Changed
- API token is now fully automatic — fetched from GLP `/api/status` on every coordinator update, no user input required; `api_token` config field removed; closes #9

## [1.5.0] – 2026-05-25
### Added
- Optional API token support: new `api_token` field in setup and options flow; if set, all requests to GLP include the `X-GLP-Token` header; closes #8

## [1.4.2] – 2026-05-24
### Fixed
- Security: config flow now rejects non-http/https URLs before attempting a connection, preventing SSRF via schemes like `file://` or custom internal addresses; applies to both initial setup and options reconfigure

## [1.4.1] – 2026-05-24
### Added
- `machine_status` sensor now exposes `switch_entity` as a state attribute (sourced from GLP `/api/status`), allowing the Lovelace card to auto-detect the smart plug without manual config; closes #6

## [1.4.0] – 2026-05-24
### Added
- Preheat sensors: `binary_sensor.…preheat_ready`, `sensor.…preheat_elapsed` (s), `sensor.…preheat_remaining` (s) — sourced from GLP `/api/preheat`; gracefully unavailable on older GLP versions; closes #5

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
