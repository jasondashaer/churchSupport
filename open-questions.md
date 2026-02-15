# Open Questions / 未解決事項

Track all unknowns that need resolution before the configuration can be finalized.
When an answer is obtained: check the box, note the answer, and update the relevant YAML spec files.

## Status Key
- [ ] Unresolved
- [x] Resolved

---

## ProPresenter
- [x] What version of ProPresenter is installed? (6, 7, or 7.9+) → **ProPresenter 21+**
  - Using `renewedvision-propresenter-api` module (REQUIRED for PP 21+, legacy Remote Classic was removed)
  - Set in `config/parameters.yaml` under `connection_settings.propresenter.module`
- [x] IP address of the ProPresenter computer → `127.0.0.1` (same machine as Companion)
- [x] Is ProPresenter on the same machine as Companion? → Yes
- [ ] Are presentations organized by playlist or folder?
- [ ] What playlists/presentations are used each Sunday? (worship lyrics, sermon slides, announcements, etc.)
- [ ] Is the ProPresenter stage display used? What layout?
- [ ] Are ProPresenter timers/clocks used during service?

## OBS Studio
- [x] IP address of the OBS computer (same machine as ProPresenter? separate?) → `127.0.0.1` (same machine)
- [ ] OBS version (must be 28+ for WebSocket v5)
- [ ] WebSocket password (if set)
- [ ] What scenes currently exist? What should be created?
  - Examples: Wide Shot, Pastor Cam, Lyrics/Slides, Announcements, Starting Soon, BRB, Ending
- [ ] What sources are configured in each scene?
- [ ] Is streaming active? To which platform? (YouTube, Facebook, etc.)
- [ ] Is recording active? Output path and format?
- [ ] Are there OBS profiles for different service types?

## Blackmagic ATEM Switcher
- [ ] ATEM model (Mini, Mini Pro, Television Studio, 1 M/E, 2 M/E, etc.)
- [ ] Firmware version (must be >= 7.5.2)
- [ ] IP address (default: 192.168.10.240)
- [ ] Number of available inputs
- [ ] Input assignment map:
  - Input 1: ? (Camera 1 - wide?)
  - Input 2: ? (Camera 2 - pulpit?)
  - Input 3: ? (ProPresenter output?)
  - Input 4+: ?
- [ ] How many cameras does the church actually have?
- [ ] Are upstream/downstream keyers used?
- [ ] Preferred transition type and duration (cut, mix, dip?)
- [ ] Are any ATEM macros currently programmed?

## Yamaha TF1 Mixer
- [ ] IP address of the TF1
- [ ] Channel assignment map:
  - Ch 1: ? (Pastor wireless mic?)
  - Ch 2: ? (Worship leader mic?)
  - Ch 3-16: ? (Instruments, playback, etc.)
- [ ] DCA group assignments:
  - DCA 1: ? (All vocals?)
  - DCA 2: ? (All instruments?)
  - DCA 3-8: ?
- [ ] Scene numbers for service presets:
  - Sunday Worship scene: ?
  - Sunday Sermon scene: ?
  - Midweek scene: ?
  - Default/safe scene: ?
- [ ] Are User Defined Keys programmed on the console?
- [ ] Monitor mix setup (how many monitor sends, who gets what)

## Network
- [ ] Network subnet at the church in Japan (192.168.x.0/24?)
- [ ] DHCP or static IPs for AV equipment?
- [ ] Is there a dedicated AV VLAN or network segment?
- [ ] Are there firewall rules that might block Companion traffic?
- [ ] Internet connection available for streaming?
- [ ] What is the network switch/router model?

## Startup/Shutdown
- [x] Are ProPresenter and OBS on the same machine or different machines? → Same machine as Companion
- [ ] What TV/display brand and model? (determines control module: Samsung, LG, etc.)
- [ ] Are there smart outlets or a PDU in use? Brand/model?
- [x] Is the Companion computer the same as the ProPresenter computer? → Yes, all on one machine
- [ ] Are computers set up for Wake-on-LAN? (requires BIOS/UEFI setting)
- [ ] Do computers have SSH enabled? (needed for remote shutdown)
- [ ] What OS do the computers run? (macOS, Windows, Linux?)
- [ ] What applications need to auto-launch on startup?

## Service Flow
- [ ] Exact typical Sunday service order (or does it vary week to week?)
- [ ] Number of worship songs typically performed
- [ ] Does the church do communion? How often? (may need a page/buttons)
- [ ] Are video clips played during service? (media playback needs)
- [ ] Is the service bilingual simultaneously or alternating languages?
- [ ] Are there midweek services or events that use the same equipment?
- [ ] How is the service order communicated to the tech team each week?

## Hardware
- [ ] Has the Stream Deck XL been purchased yet?
- [ ] Is there a budget for additional hardware (smart outlets, cameras, etc.)?
- [ ] Current pain points in service operation that this should address first
