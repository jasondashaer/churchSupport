# Design Decisions

This document explains the rationale behind key architectural and design choices in this project.

## Why Role-Based Pages (Not Service-Flow Pages)

**Rejected approach**: Organize pages by service section (Pre-Service, Worship, Sermon, Prayer, etc.) where one operator controls all systems during each section.

**Chosen approach**: Organize pages by volunteer role (Slides, Audio, Camera, Streaming) where each volunteer sees only their system's controls.

**Rationale**: This project is designed to simplify individual volunteer roles, not consolidate control under a single operator. A slides volunteer shouldn't need to see audio faders, and a camera operator shouldn't navigate through lyric controls. Role-based pages keep each interface focused and uncluttered, reducing the learning curve for new volunteers.

| Pages | Role | Primary System |
|-------|------|---------------|
| 1 | Home | Navigation + Startup/Shutdown |
| 2-3 | Slides / スライド | ProPresenter |
| 4-5 | Audio / 音響 | Yamaha TF1 |
| 6-7 | Camera / カメラ | ATEM |
| 8-9 | Streaming / 配信 | OBS |
| 10 | Emergency / 緊急 | All systems |

## Why YAML Spec Files

**Original assumption**: Companion's `.companionconfig` export format is a SQLite-backed compressed database that cannot be programmatically generated. This turned out to be incorrect — Companion v4.2+ supports importing pretty-formatted JSON via its Import/Export UI.

**Chosen approach**: YAML specification files as the canonical source of truth, with a converter script (`scripts/yaml-to-companion.py`) that generates Companion-importable JSON. The YAML can also be followed manually as a button-by-button guide.

**Benefits**:
- Human-readable and version-controllable
- Can be reviewed and modified without Companion running
- Serves as living documentation of the entire configuration
- OPEN QUESTION markers make unknowns visible and trackable
- Automated conversion eliminates tedious manual button creation

## Bilingual Label Strategy

**Chosen approach**: Dual-language labels on every button.
- Top line: English (abbreviated, max ~8 characters)
- Bottom line: Japanese (日本語)

**Why not separate profiles?** Separate English and Japanese profiles would require maintaining two copies of every configuration change. Dual labels work for everyone immediately.

**Why not a language toggle?** A Companion variable-based language switcher is technically possible but adds significant complexity. Dual labels are simpler to build, maintain, and debug. Can upgrade to a toggle system later if needed.

**Product names stay in English**: ProPresenter, OBS, ATEM, TF1 are brand/product names and are kept in English regardless of language context. Technical abbreviations (CAM, MIC, REC) also use English as they are international standards.

## Color Coding

Colors follow broadcast industry standards:

| Color | Hex | Meaning | Japanese |
|-------|-----|---------|----------|
| Red | #CC0000 | Danger, mute, stop, live/program | 危険・ミュート・停止 |
| Green | #00CC00 | Go, active, unmute, preview | 実行・アクティブ |
| Blue | #0066CC | Navigation between pages | ナビゲーション |
| Yellow | #CCCC00 | Caution, standby, preparation | 注意・スタンバイ |
| Gray | #666666 | Disabled, inactive, informational | 無効・非アクティブ |

**ATEM tally standard**: Red = program (currently live on air), Green = preview (next up). This is the universal broadcast tally convention.

## Consistent Bottom Row

Every page (1-10) has an identical bottom row (row 3) layout:

```
[3,0] Home    [3,1] ◀ Prev   [3,2] Next ▶   ...   [3,6] MUTE ALL   [3,7] BLACK
ホーム         ◀ 前ページ      次ページ ▶           全ミュート        ブラック
(blue)         (blue)          (blue)                (red)             (red)
```

**Rationale**: Navigation on the left, safety controls on the right. Operators build muscle memory: bottom-left = where am I going, bottom-right = emergency stop. The MUTE ALL and BLACK buttons are available on EVERY page so a volunteer doesn't need to navigate away to handle an emergency.

## Startup/Shutdown Design

**Startup**: A single STARTUP button on the Home page triggers a multi-action sequence:
1. Wake-on-LAN to power on computers
2. Wait for boot
3. Launch applications via shell scripts
4. Recall day-appropriate presets on TF1, ATEM, OBS

**Shutdown**: Uses Companion's multi-step button feature for 2-step confirmation:
- First press: Button changes to yellow "CONFIRM? / 確認?"
- Second press within 5 seconds: Executes graceful shutdown sequence
- No second press: Resets automatically (prevents accidental shutdown)

**Why not auto-start?** Automatic time-based startup is possible via Companion triggers but is deferred to Phase 2. Manual startup ensures a human is present and aware that systems are coming online.

## Documentation Language Strategy

**Chosen approach**: English-primary documentation with a Japanese setup guide for the core deployment workflow.

- `docs/SETUP-GUIDE-EN.md` — English (primary, most detailed)
- `docs/セットアップガイド.md` — Japanese (complete setup guide translation)
- `docs/OPERATOR-QUICK-REFERENCE.md` — Bilingual (used during services by Japanese-speaking volunteers)
- `docs/TROUBLESHOOTING.md` — Bilingual section headers for emergency reference

**Rationale**: Technical documentation (module names, Companion UI labels, API actions) is English-native, so English remains the primary language for builder-facing docs. However, the setup guide is translated to Japanese since the church is in Japan and local volunteers may lead future deployments. The operator quick reference is bilingual because it is used in real-time during services.

## Custom Variables on Home Page

The Home page (Page 1, Row 2) displays three custom Companion variables alongside live status indicators:

| Position | Variable | Purpose |
|----------|----------|---------|
| [2,0] | `$(internal:time_hms)` | Current time (built-in) |
| [2,1] | `$(internal:custom_service_day)` | Service type: sunday / midweek |
| [2,2]-[2,3] | OBS streaming/recording | Live status feedback (built-in) |
| [2,5] | `$(internal:custom_service_phase)` | Service phase: pre, worship, sermon, etc. |
| [2,7] | `$(internal:custom_startup_status)` | System status with color feedback |

**Rationale**: At-a-glance status is critical on the Home page since all volunteers pass through it. The `startup_status` variable turns green when all systems are online and red on error, providing immediate visual confirmation. The `service_day` and `service_phase` variables help volunteers confirm they have the right presets loaded.

## Why a YAML-to-JSON Converter

**Original assumption**: `.companionconfig` files are SQLite-backed compressed exports that cannot be programmatically generated.

**Discovery**: Companion v4.2+ actually supports importing **pretty-formatted JSON** configs via its Import/Export UI. The internal format is a structured JSON object with `pages`, `instances`, and `custom_variables` sections.

**Solution**: `scripts/yaml-to-companion.py` reads all YAML spec files and generates a Companion-importable `.companionconfig` JSON file. This eliminates the tedious manual process of recreating every button through the web UI.

**Design for iterative refinement**: Companion's internal JSON schema is not formally documented. The converter isolates all field name assumptions into a `FIELD_MAP` dictionary at the top of the script. When testing against a real Companion instance reveals mismatches, you change one line — not the entire script.

**YAML specs remain the source of truth**: The converter is a one-way transformation. Edits are always made in YAML, then re-converted. This preserves the human-readable, version-controllable benefits of the YAML approach while eliminating the manual build step.

**Validation built in**: The script includes a `--validate-only` mode that checks all YAML files for errors (missing fields, invalid colors, unknown connections) without generating output. This catches spec mistakes before they reach Companion.

## Why a Separate Parameters File

**Problem**: The original connections.yaml mixed equipment topology (what connects where) with device-specific details (IPs, passwords, ports). Users had to edit YAML spec files to change an IP address, and there was no way to express "ProPresenter and OBS run on the same machine" — you'd have to duplicate the IP in two places.

**Solution**: `config/parameters.yaml` separates three concerns:
1. **Machines** — physical computers/devices and their IP addresses
2. **Assignments** — which app runs on which machine
3. **Connection settings** — module-specific config (passwords, ports, model selection)

**Key benefit**: When ProPresenter and OBS are on the same PC, you define the IP once under a machine name, then assign both apps to that machine. Change the IP in one place and both connections update.

The converter merges `parameters.yaml` settings with complete module config defaults (every field populated) so that Companion can save connections immediately after import — no missing-field errors.

## Open Questions Strategy

All unknowns are handled with three mechanisms:

1. **Inline markers**: YAML `notes` fields contain `OPEN QUESTION:` prefixes
2. **Centralized tracker**: `open-questions.md` has checkboxes organized by system
3. **Placeholder values**: IPs use `192.168.1.XXX` pattern that scripts detect and skip

When an answer is obtained: check the box in `open-questions.md`, update the relevant YAML files, update scripts if IPs change, and commit with a message noting which questions were resolved.
