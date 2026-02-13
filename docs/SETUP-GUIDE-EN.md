# Setup Guide (English)

Complete instructions for building and deploying the Stream Deck configuration.

## Prerequisites

- [ ] **Bitfocus Companion** v4.2+ installed ([download](https://bitfocus.io/companion))
- [ ] **Stream Deck XL** connected via USB (8x4 = 32 buttons)
- [ ] Network access to all AV equipment (or placeholder IPs for pre-deployment)
- [ ] This repository cloned/downloaded to the build machine

## Phase 1: Install Companion

1. Download Companion from [bitfocus.io/companion](https://bitfocus.io/companion)
2. Install for your operating system (macOS, Windows, or Linux)
3. Launch Companion
4. Open a web browser to `http://localhost:8000`
5. Verify the web UI loads with the Companion dashboard

## Phase 2: Configure Surface

1. Connect the Stream Deck XL via USB
2. In Companion, go to the **Surfaces** tab
3. Verify the Stream Deck XL appears (should show "Elgato Stream Deck XL - 32 keys")
4. Set the surface name to `Church-Main` (optional but helpful)
5. Confirm the grid shows 8 columns x 4 rows

## Phase 3: Add Connections

Follow `config/connections.yaml` to add each module connection.

See `docs/COMPANION-UI-WALKTHROUGH.md` for detailed step-by-step instructions.

**Connection summary:**

| # | Module | Label | IP | Port |
|---|--------|-------|-----|------|
| 1 | `renewedvision-propresenter` | ProPresenter | See IP-CONFIGURATION.md | 20404 |
| 2 | `obs-studio` | OBS Studio | See IP-CONFIGURATION.md | 4455 |
| 3 | `bmd-atem` | ATEM Switcher | See IP-CONFIGURATION.md | 9910 |
| 4 | `yamaha-rcp` | Yamaha TF1 | See IP-CONFIGURATION.md | 49280 |
| 5 | `generic-pingandwake` | Wake-on-LAN | Target computer IP | N/A |
| 6 | `generic-ssh` | SSH Remote Control | Target computer IP | 22 |

Connections 7-8 (Display, Smart Outlet) are TBD pending equipment confirmation.

## Phase 4: Build Pages

For each of the 10 pages, open the corresponding YAML file and create every button as specified.

**Recommended build order:**
1. Page 1 (Home) - establishes the role selector and status layout
2. Page 10 (Emergency) - the bottom-row safety buttons reference this
3. Page 2 (Slides Core) - most commonly used role page
4. Pages 4, 6, 8 (other core role pages)
5. Pages 3, 5, 7, 9 (extended role pages)

For detailed button creation instructions, see `docs/COMPANION-UI-WALKTHROUGH.md`.

### Page files:

| Page | YAML File |
|------|-----------|
| 1 | `config/pages/page01-home.yaml` |
| 2 | `config/pages/page02-slides-core.yaml` |
| 3 | `config/pages/page03-slides-extended.yaml` |
| 4 | `config/pages/page04-audio-core.yaml` |
| 5 | `config/pages/page05-audio-extended.yaml` |
| 6 | `config/pages/page06-camera-core.yaml` |
| 7 | `config/pages/page07-camera-extended.yaml` |
| 8 | `config/pages/page08-stream-core.yaml` |
| 9 | `config/pages/page09-stream-extended.yaml` |
| 10 | `config/pages/page10-emergency.yaml` |

## Phase 5: Test

Run through `docs/TESTING-CHECKLIST.md` to verify:
- All pages exist with correct names
- Navigation buttons work across all pages
- Connection status indicators show correct colors
- Actions trigger correctly (requires live equipment)
- Bottom row is consistent on every page

If testing without live equipment, verify:
- All buttons have correct text and colors
- Navigation between pages works
- Buttons are in the correct grid positions

## Phase 6: Export

1. Go to Companion's **Import/Export** tab
2. Click **Export**
3. Select **Compressed (.companionconfig)** format
4. Save as `church-japan-YYYY-MM.companionconfig`
5. Make a backup copy

## Phase 7: Deploy at Church in Japan

1. Install Companion on the church's computer
2. Connect Stream Deck XL via USB
3. Import the `.companionconfig` file:
   - Go to **Import/Export** tab
   - Click **Import**
   - Select the exported file
   - Choose **Full Import** (replaces all existing config)
4. **Update IP addresses** for all connections:
   - Go to **Connections** tab
   - For each connection, update the IP address to the actual device IP
   - See `docs/IP-CONFIGURATION.md` for the address table
5. **Update helper scripts**:
   - Edit IP addresses in `scripts/network-test.sh` and `scripts/port-check.sh`
   - Or set environment variables (see script headers for details)
6. **Run pre-service check**:
   ```bash
   chmod +x scripts/*.sh
   ./scripts/pre-service-check.sh
   ```
7. Test each role's pages with the actual equipment
8. Walk through `docs/TESTING-CHECKLIST.md` again with live connections

## Phase 8: Train Volunteers

1. Show each volunteer their role's pages (2 pages per role)
2. Demonstrate the bottom-row convention (nav left, safety right)
3. Practice the MUTE ALL and BLACK emergency buttons
4. Give each volunteer a copy of `docs/OPERATOR-QUICK-REFERENCE.md`
5. Do a full service rehearsal with all roles staffed

## Ongoing Maintenance

- **Before each service**: Run `scripts/pre-service-check.sh`
- **After changes**: Export a new `.companionconfig` backup
- **When resolving open questions**: Update YAML specs, `open-questions.md`, and rebuild affected buttons
- **Version control**: Commit changes to this repository with notes on what changed
