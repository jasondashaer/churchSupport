# Church Stream Deck Control System - Project Context

## Project Summary
A Bitfocus Companion + Stream Deck XL configuration for a bilingual (English/Japanese) church in Japan. The goal is to **simplify individual volunteer roles** so any volunteer can step into a technical role (slides, audio, cameras, streaming) with minimal training.

This is NOT a single-operator system. Each role gets focused, uncluttered pages showing only what that volunteer needs.

## Critical Technical Decision
`.companionconfig` files are SQLite-backed compressed exports and cannot be hand-crafted. This project provides **YAML specification files** that document every connection, page, and button so someone can recreate the configuration in Companion's web UI button-by-button. The YAML specs are the source of truth.

## Equipment & Companion Modules

| Equipment | Companion Module | Default Port | Protocol |
|-----------|-----------------|-------------|----------|
| ProPresenter | `renewedvision-propresenter` | 20404 | TCP |
| OBS Studio | `obs-studio` | 4455 | WebSocket v5 |
| Blackmagic ATEM | `bmd-atem` | 9910 | TCP |
| Yamaha TF1 | `yamaha-rcp` | 49280 | TCP/RCP |
| Wake-on-LAN | `generic-pingandwake` | N/A | UDP 9 |
| SSH (shutdown) | `generic-ssh` | 22 | SSH |

Target: **Companion v4.2.4** (latest stable)

## Stream Deck XL Grid
8 columns x 4 rows = 32 buttons per page. Zero-indexed:
```
Row 0: [0,0] [0,1] [0,2] [0,3] [0,4] [0,5] [0,6] [0,7]
Row 1: [1,0] [1,1] [1,2] [1,3] [1,4] [1,5] [1,6] [1,7]
Row 2: [2,0] [2,1] [2,2] [2,3] [2,4] [2,5] [2,6] [2,7]
Row 3: [3,0] [3,1] [3,2] [3,3] [3,4] [3,5] [3,6] [3,7]
```

## Page Organization (Role-Based)

| Pages | Role | Primary System |
|-------|------|---------------|
| 1 | Home | Role selector + startup/shutdown + connection status |
| 2-3 | Slides / スライド | ProPresenter |
| 4-5 | Audio / 音響 | Yamaha TF1 |
| 6-7 | Camera / カメラ | ATEM |
| 8-9 | Streaming / 配信 | OBS |
| 10 | Emergency / 緊急 | All systems |

## Design Principles

### Color Coding
- **Red (#CC0000)**: Danger, mute, stop, kill
- **Green (#00CC00)**: Go, active, live, unmute
- **Blue (#0066CC)**: Navigation between pages
- **Yellow (#CCCC00)**: Caution, standby, preparation
- **Gray (#666666)**: Disabled / inactive
- **ATEM tally**: Red = program (live), Green = preview

### Bilingual Labels
- Top line: English (abbreviated, max ~8 chars)
- Bottom line: Japanese (日本語)
- Product names stay in English (ProPresenter, OBS, ATEM)

### Consistent Bottom Row (every page)
- `[3,0]` Home / ホーム (blue)
- `[3,1]` Prev page in role (blue)
- `[3,2]` Next page in role (blue)
- `[3,6]` MUTE ALL / 全ミュート (red)
- `[3,7]` BLACK / ブラック (red)

### Startup/Shutdown
- Home page has STARTUP (green) and SHUTDOWN (red, 2-step confirmation) buttons
- Startup: WOL computers, power displays, launch apps, recall day-of-week presets
- Shutdown: Save TF1 scene, stop OBS, clear PP, quit apps, power off displays/computers
- Companion `internal: run shell path` for local scripts (20s timeout)
- `generic-ssh` for remote machine commands

## File Conventions
- Config specs: `config/connections.yaml`, `config/pages/pageNN-name.yaml`
- Documentation: `docs/*.md` (English primary)
- Scripts: `scripts/*.sh` (bilingual output)
- Open questions: `open-questions.md` (checkbox tracker)
- Placeholder IPs: `192.168.1.XXX` pattern (detected and skipped by scripts)
- OPEN QUESTION markers in YAML `notes` fields for unresolved items

## Key Companion Actions Reference

**ProPresenter**: `next_slide`, `previous_slide`, `clear_all`, `clear_slide`, `start_clock`, `stop_clock`, `pro7_trigger_macro`

**OBS**: `set_program_scene`, `toggle_record`, `start_record`, `stop_record`, `toggle_streaming`, `start_streaming`, `stop_streaming`, `transition`

**ATEM**: program/preview input selection per ME, auto/cut transition, upstream/downstream keyer toggle, macro execution, save/clear startup state

**Yamaha TF1**: channel mute/unmute, fader level, scene recall (RecallInc/RecallDec), scene store, DCA group control

**Internal**: `set_page`, `wait` (ms), `run shell path (local)` (20s max)

## Open Questions
See `open-questions.md` for full tracker. Critical unknowns:
- All equipment IP addresses
- ProPresenter version (determines module choice: legacy vs API)
- ATEM model and input assignments
- OBS scene names
- TF1 channel assignments and scene numbers
- TV/display brand (determines power control module)
- Network topology (same subnet? DHCP? static?)
