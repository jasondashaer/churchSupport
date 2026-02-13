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

## Why YAML Spec Files (Not Direct .companionconfig Generation)

**Key finding**: Companion's `.companionconfig` export format is a SQLite-backed compressed database. It cannot be reliably hand-crafted or programmatically generated outside of Companion.

**Chosen approach**: YAML specification files that document every connection, page, and button. An operator follows these specs to build the configuration in Companion's web UI button-by-button.

**Benefits**:
- Human-readable and version-controllable
- Can be reviewed and modified without Companion running
- Serves as living documentation of the entire configuration
- OPEN QUESTION markers make unknowns visible and trackable

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

## Open Questions Strategy

All unknowns are handled with three mechanisms:

1. **Inline markers**: YAML `notes` fields contain `OPEN QUESTION:` prefixes
2. **Centralized tracker**: `open-questions.md` has checkboxes organized by system
3. **Placeholder values**: IPs use `192.168.1.XXX` pattern that scripts detect and skip

When an answer is obtained: check the box in `open-questions.md`, update the relevant YAML files, update scripts if IPs change, and commit with a message noting which questions were resolved.
