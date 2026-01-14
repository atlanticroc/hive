# STORY-001: Research and Access METAR Data Sources (Completed)

**Points**: 2 | **Sprint**: 1 | **Status**: Done
**Started**: 2026-01-13 | **Completed**: 2026-01-14
**Labels**: research

## User Story

As a Data Engineer,
I want to identify and gain access to reliable METAR data sources,
So that I can acquire 20+ years of historical weather data for LPMA.

## Acceptance Criteria

- [x] Iowa State University ASOS-AWOS-METAR API access documented (endpoints, authentication, rate limits)
- [x] NOAA Aviation Weather Center historical data endpoints identified and tested
- [x] API access confirmed for 2005-2024 date range (earliest available: 2005)
- [x] Data schema documented: timestamp, wind speed, wind direction, gusts, visibility, temp, pressure, runway
- [x] Sample data retrieved and validated

## Completion Notes

- **Date range adjustment**: Earliest available LPMA data is from 2005 (not 2004)
- Implementation by Codex: `src/metar_samples.py` fetcher script
- Two sources identified and documented: IEM (primary, historical), AWC (secondary, current)
- No authentication required for either API

## Tasks Completed

- [x] Identify IEM (Iowa Environmental Mesonet) as primary data source
- [x] Identify AWC (Aviation Weather Center) as secondary source
- [x] Create `src/metar_samples.py` fetcher script
- [x] Test IEM API with LPMA station
- [x] Document API endpoints and parameters
- [x] Confirm no rate limits or authentication required

## Research Summary

### Iowa State IEM (Primary - Historical)
- Endpoint: `https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py`
- Supports full historical range via `sts`/`ets` params
- CSV format, no auth required
- Earliest LPMA data: 2005

### NOAA AWC (Secondary - Current)
- Endpoint: `https://aviationweather.gov/api/data/dataserver`
- Supports `startTime`/`endTime` or `hoursBeforeNow`
- JSON/CSV/XML formats, no auth required
