# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-07-15

### Added
- **One-command analysis script** (`scripts/run_analysis.py`) - processes 100K+ messages in ~30 seconds, single-pass through data
- **Monthly trend tracking** - all key metrics aggregated by month for longitudinal analysis
- **Per-1k-messages normalization** - fair comparison between parties with different message volumes
- **Emotional burst detection** - identifies sequences of ≥5 consecutive negative-emotion messages with intensity scoring
- **Cross-framework correlation matrix** - Pearson correlation on monthly time series, auto-flags strong pairs (|r|>0.5)
- **Report template** (`templates/report_template.md`) - Jinja2-style placeholders for automated report generation
- **Additional metrics**: response time distribution, conversation analysis, time-of-day patterns, message length distribution, message type distribution
- **24 psychological frameworks** across 6 dimensions (A: Communication, B: Psychological Structure, C: Relationship Dynamics, D: Emotions & Needs, E: Dark Side, F: Behavioral Patterns)
- **Verified regex pattern library** (`references/verified-patterns.md`) with formula tables and threshold criteria

### Changed
- Migrated from manual `python -c` per-framework scripts to unified `run_analysis.py`
- All frequency metrics now include both absolute counts and normalized (per-1k) values

### Fixed
- `TypeError` in PAC transaction pattern counting when chaining `.get()` with `+` operator
- Bash single-quote escaping issues with Chinese regex patterns (solved by using script files)

## [1.0.0] - 2026-07-14

### Added
- Initial release with 24-framework psychological analysis system
- Framework definitions for A1-F24 with theoretical background
- Regex patterns for Chinese-language chat analysis
- Key metric calculation formulas and threshold tables
- 9 documented pitfalls from real-world usage
