# Testing Checklist / テスト確認表

Use this checklist to verify the configuration at each stage.

---

## Pre-Deployment Tests (US / Build Machine)

These tests can be done without live AV equipment.

### Companion Basics
- [ ] Companion launches and web UI loads at `http://localhost:8000`
- [ ] Stream Deck XL detected in Surfaces tab (8x4 grid)
- [ ] Surface shows "Elgato Stream Deck XL - 32 keys"

### Pages
- [ ] All 10 pages exist with correct names:
  - [ ] Page 1: Home
  - [ ] Page 2: Slides - Core
  - [ ] Page 3: Slides - Extended
  - [ ] Page 4: Audio - Core
  - [ ] Page 5: Audio - Extended
  - [ ] Page 6: Camera - Core
  - [ ] Page 7: Camera - Extended
  - [ ] Page 8: Streaming - Core
  - [ ] Page 9: Streaming - Extended
  - [ ] Page 10: Emergency

### Navigation (test on physical Stream Deck)
- [ ] Home page: All 4 role buttons navigate to correct pages (2, 4, 6, 8)
- [ ] Home page: Emergency button goes to page 10
- [ ] Every page: Home button `[3,0]` returns to page 1
- [ ] Every page: Prev `[3,1]` goes to previous page in role (or grayed if first)
- [ ] Every page: Next `[3,2]` goes to next page in role (or grayed if last)
- [ ] Every page: MUTE ALL `[3,6]` and BLACK `[3,7]` buttons are present

### Visual Check
- [ ] All buttons have visible text (EN top, JP bottom)
- [ ] Color coding is consistent:
  - Red buttons = danger/stop actions
  - Green buttons = go/active actions
  - Blue buttons = navigation
  - Yellow buttons = caution
  - Gray buttons = disabled/info

### Export
- [ ] Successfully exported `.companionconfig` file
- [ ] File size is reasonable (not 0 bytes)
- [ ] Can re-import on a fresh Companion install

---

## Post-Deployment Tests (Japan / Church)

### Network (run scripts)
```bash
./scripts/pre-service-check.sh
```
- [ ] All devices reachable (scripts/network-test.sh passes)
- [ ] All ports open (scripts/port-check.sh passes)

### Connections
- [ ] ProPresenter connection: green status
- [ ] OBS Studio connection: green status
- [ ] ATEM Switcher connection: green status
- [ ] Yamaha TF1 connection: green status
- [ ] Wake-on-LAN connection: configured
- [ ] SSH connection: configured (if needed)

---

## Per-Role Tests

### Slides Role (Pages 2-3)

**Page 2 - Core:**
- [ ] Next slide button advances ProPresenter slide
- [ ] Previous slide button goes back
- [ ] Clear slide removes current slide from output
- [ ] Clear All removes all outputs
- [ ] Logo button shows default background
- [ ] Slide counter displays current/total numbers
- [ ] Playlist buttons load correct presentations

**Page 3 - Extended:**
- [ ] Timer start/stop/reset works
- [ ] Message show/hide works
- [ ] Stage display layout switching works
- [ ] PP7 Look presets work (if applicable)

### Audio Role (Pages 4-5)

**Page 4 - Core:**
- [ ] Pastor mic mute/unmute toggles correctly
  - Green when unmuted, Red when muted
- [ ] Worship leader mic mute/unmute works
- [ ] Master output mute toggle works
- [ ] Master status indicator shows correct state
- [ ] Worship scene recall loads correct mix
- [ ] Sermon scene recall loads correct mix
- [ ] Prayer scene recall loads correct mix

**Page 5 - Extended:**
- [ ] DCA group mutes work (Vocals, Band, FX)
- [ ] Individual instrument channel mutes work
- [ ] Monitor bus mutes work
- [ ] Scene save stores to designated scene
- [ ] Scene increment/decrement navigation works

### Camera Role (Pages 6-7)

**Page 6 - Core:**
- [ ] Camera 1 button switches ATEM program to input 1
  - Button turns RED when on program (live)
  - Button turns GREEN when on preview
- [ ] Camera 2, 3, 4 buttons work similarly
- [ ] ProPresenter output button switches to PP input
- [ ] BLACK button cuts to black
- [ ] CUT transition works (instant switch)
- [ ] AUTO transition works (smooth transition)
- [ ] Preview row buttons set correct preview source

**Page 7 - Extended:**
- [ ] Transition type selection (Mix/Dip/Wipe) works
  - Active type shows green
- [ ] USK 1 toggle works (red when on air)
- [ ] DSK 1, DSK 2 toggles work
- [ ] ATEM macros execute correctly
- [ ] Transition rate buttons change duration
- [ ] Save/Clear startup state works

### Streaming Role (Pages 8-9)

**Page 8 - Core:**
- [ ] GO LIVE starts OBS streaming
  - Button turns RED when streaming
- [ ] END stops streaming
- [ ] REC starts recording
  - Button turns RED when recording
- [ ] STOP stops recording
- [ ] PAUSE pauses recording
- [ ] Scene buttons switch OBS scenes correctly
  - Active scene shows RED
- [ ] LIVE and REC indicators on row 0 reflect actual state

**Page 9 - Extended:**
- [ ] Profile switching works (Sunday/Midweek)
- [ ] Source visibility toggles work (Logo, Lower 3rd)
- [ ] OBS transition overrides work (Cut, Fade, Stinger)
- [ ] Service section scene presets work

### Emergency Page (Page 10)

- [ ] MUTE ALL mutes TF1 master output
- [ ] UNMUTE restores TF1 master output
- [ ] BLACK cuts ATEM to black
- [ ] CAM 1 recovery cuts to safe camera
- [ ] PP Clear clears all ProPresenter outputs
- [ ] PP Logo shows default logo
- [ ] OBS Stop halts streaming AND recording
- [ ] OBS Start resumes streaming AND recording
- [ ] ALL STOP executes all emergency actions simultaneously
- [ ] Individual reconnect buttons cycle connections
- [ ] Reconnect All cycles all connections

### Home Page (Page 1)

- [ ] STARTUP button triggers startup sequence
- [ ] SHUTDOWN button requires 2 presses (confirmation)
- [ ] Connection status indicators show correct colors
- [ ] Clock display shows current time
- [ ] LIVE indicator turns red when OBS is streaming
- [ ] REC indicator turns red when OBS is recording

---

## Full Service Rehearsal / 礼拝リハーサル

Walk through the entire service flow with all roles staffed:

- [ ] **Pre-service**: Run startup sequence from Home page
- [ ] **Slides volunteer**: Load today's presentation, advance through test slides
- [ ] **Audio volunteer**: Confirm all mics work, recall worship scene
- [ ] **Camera volunteer**: Switch between all cameras, test transitions
- [ ] **Streaming volunteer**: Start recording, verify scenes
- [ ] **Worship section**: Slides volunteer advances lyrics, audio has worship mix active
- [ ] **Sermon section**: Switch to sermon slides, audio recalls sermon scene
- [ ] **Prayer section**: Clear slides, audio recalls prayer/quiet scene
- [ ] **Emergency test**: Press MUTE ALL, verify audio stops; press BLACK, verify video goes black
- [ ] **Post-service**: Stop recording, run shutdown sequence

---

## Sign-Off

| Role | Tested By | Date | Notes |
|------|-----------|------|-------|
| Slides | | | |
| Audio | | | |
| Camera | | | |
| Streaming | | | |
| Emergency | | | |
| Full Rehearsal | | | |
