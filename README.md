# Church Stream Deck Control System

A Bitfocus Companion + Stream Deck XL configuration for a bilingual (English/Japanese) church in Japan. Simplifies volunteer technical roles so anyone can run slides, audio, cameras, or streaming with minimal training.

## What This Is

This project provides **YAML specification files**, a **converter script**, and **documentation** for building a complete Bitfocus Companion configuration. The YAML specs are the source of truth; the converter (`scripts/yaml-to-companion.py`) generates a `.companionconfig` JSON file that can be imported directly into Companion's UI — no manual button-by-button recreation needed.

## Equipment Controlled

| System | Equipment | Role |
|--------|-----------|------|
| Presentation | ProPresenter | Slides / Lyrics volunteer |
| Audio | Yamaha TF1 mixer | Audio / Sound volunteer |
| Video | Blackmagic ATEM switcher | Camera volunteer |
| Streaming | OBS Studio | Streaming volunteer |

## Directory Structure

```
config/
  connections.yaml          # All Companion module connections
  parameters.yaml           # Equipment IPs, ports, passwords (edit this first!)
  pages/
    page01-home.yaml        # Role selector + startup/shutdown
    page02-slides-core.yaml # Slides - core controls
    page03-slides-extended.yaml # Slides - extended
    page04-audio-core.yaml      # Audio - core controls
    page05-audio-extended.yaml  # Audio - extended
    page06-camera-core.yaml     # Camera - core controls
    page07-camera-extended.yaml # Camera - extended
    page08-stream-core.yaml     # Streaming - core controls
    page09-stream-extended.yaml # Streaming - extended
    page10-emergency.yaml   # Emergency / panic
  variables.yaml            # Custom Companion variables
  triggers.yaml             # Automated triggers
docs/
  SETUP-GUIDE-EN.md         # English setup guide
  セットアップガイド.md       # Japanese setup guide / 日本語セットアップガイド
  IP-CONFIGURATION.md       # Network configuration template
  TESTING-CHECKLIST.md      # Verification steps
  TROUBLESHOOTING.md        # Common issues and solutions
  OPERATOR-QUICK-REFERENCE.md # Bilingual cheat sheet
  COMPANION-UI-WALKTHROUGH.md # Step-by-step UI guide
  DESIGN-DECISIONS.md       # Rationale documentation
scripts/
  yaml-to-companion.py      # YAML → Companion JSON converter
  network-test.sh           # Ping all equipment
  port-check.sh             # Check required ports
  pre-service-check.sh      # Combined pre-service validation
  startup-sunday.sh         # Sunday startup sequence
  startup-midweek.sh        # Midweek startup sequence
  shutdown-graceful.sh      # Graceful shutdown
output/                     # Generated configs (gitignored)
```

## Quick Start

### Option A: Automated (recommended)

1. Install [Bitfocus Companion](https://bitfocus.io/companion) v4.2+
2. Connect Stream Deck XL via USB
3. Edit `config/parameters.yaml` with your equipment IPs, ports, and passwords
4. Generate the config:
   ```bash
   python3 scripts/yaml-to-companion.py --verbose
   ```
5. In Companion, go to **Import/Export** → **Import** → select `output/church-config.companionconfig`
6. Verify connections are green in the **Connections** tab
7. Test with `docs/TESTING-CHECKLIST.md`

### Option B: Manual

1. Install [Bitfocus Companion](https://bitfocus.io/companion) v4.2+
2. Connect Stream Deck XL via USB
3. Follow `docs/SETUP-GUIDE-EN.md` (English) or `docs/セットアップガイド.md` (日本語) to build the configuration button-by-button
4. Update IP addresses per `docs/IP-CONFIGURATION.md`
5. Test with `docs/TESTING-CHECKLIST.md`
6. Export `.companionconfig` for deployment

## Open Questions

See `open-questions.md` for equipment details that need to be confirmed before finalizing the configuration.
