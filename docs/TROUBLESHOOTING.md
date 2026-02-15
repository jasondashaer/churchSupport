# Troubleshooting / トラブルシューティング

Common issues and their solutions, organized by symptom.

---

## Connection Issues / 接続の問題

### All connections show red / すべての接続が赤い

**Likely cause**: Network issue between Companion PC and the equipment.

1. Run `./scripts/network-test.sh` to check if devices are reachable
2. Check that the Companion PC and all devices are on the same network/subnet
3. Verify network cable connections (try a different port on the switch)
4. Check if the Companion PC's firewall is blocking outbound connections
5. Restart the network switch

### ProPresenter connection red / ProPresenter接続が赤い

**Common symptoms and fixes:**

#### "Unexpected Server Response: 404" / サーバー応答エラー: 404

This is the most common ProPresenter connection error. Three possible causes:

**Cause 1: No controller password set (most common)**
The legacy module requires a non-empty controller password. Without it, ProPresenter's WebSocket endpoint returns 404.
1. Open ProPresenter > Settings > Network
2. Under "ProPresenter Remote", check "Controller"
3. **Set a non-empty password** in the controller password field
4. Enter the same password in `config/parameters.yaml` under `connection_settings.propresenter.password`
5. Re-run the converter and reimport, or update manually in Companion's Connections tab

**Cause 2: ProPresenter v21+ (Remote Classic removed)**
Starting with ProPresenter v21, the legacy "Remote Classic" API was removed entirely. The WebSocket endpoint no longer exists.
1. Check your ProPresenter version: ProPresenter > About
2. If v21 or newer, you **must** switch to the API module:
   - In `config/parameters.yaml`, change `module` to `"renewedvision-propresenter-api"`
   - Re-run the converter and reimport

**Cause 3: Wrong port number**
ProPresenter assigns a **random port** each time it launches unless you lock it.
1. Open ProPresenter > Settings > Network
2. Note the port number displayed
3. To lock it: type the number back into the field and press Enter
4. Update the port in `config/parameters.yaml`

#### Connection goes green then red after ~5 seconds / 接続が一瞬緑になってすぐ赤になる

This typically means TCP connects (green) but the WebSocket handshake fails (red). See the 404 causes above.

#### General ProPresenter troubleshooting / 一般的なトラブルシューティング

1. **Verify PP is running**: ProPresenter must be open and running
2. **Check Network is enabled**: ProPresenter > Settings > Network > "Enable Network" must be ON
3. **Check port**: The port in Companion must match what ProPresenter shows (it is NOT fixed at 20404)
4. **Localhost**: If PP runs on the same machine as Companion, use `127.0.0.1` as the IP
5. **Firewall**: Ensure the PP computer's firewall allows inbound on the configured port
6. **Restart**: Close and reopen ProPresenter, then toggle the connection in Companion (disable/wait/enable)

#### Which module should I use? / どのモジュールを使うべき?

| ProPresenter Version | Recommended Module |
|---------------------|-------------------|
| PP 6 | `renewedvision-propresenter` (legacy) |
| PP 7.0 - 7.8 | `renewedvision-propresenter` (legacy) |
| PP 7.9 - 20 | `renewedvision-propresenter-api` (recommended) |
| PP 21+ | `renewedvision-propresenter-api` (required) |

### OBS connection red / OBS接続が赤い

1. **Verify OBS is running**: OBS Studio must be open
2. **Check WebSocket Server**: In OBS: Tools > WebSocket Server Settings
   - Verify "Enable WebSocket server" is checked
   - Port matches (default: 4455)
   - If authentication is enabled, password must match Companion config
3. **OBS version**: Must be OBS 28+ for WebSocket v5 protocol
4. **Restart**: Close and reopen OBS, toggle connection in Companion

### ATEM connection red / ATEM接続が赤い

1. **Verify ATEM is powered on** and connected to the network
2. **Check IP address**: ATEM Mini defaults to `192.168.10.240` which may be on a different subnet
   - Access ATEM settings via ATEM Software Control to change IP
3. **Firmware**: Must be >= 7.5.2 (update via ATEM Software Control)
4. **USB control**: Companion does NOT support USB connections to ATEM - must use network
5. **Single connection**: Only one controller can connect at a time. If ATEM Software Control is open, it may be blocking Companion
6. **Restart**: Power cycle the ATEM, toggle connection in Companion

### Yamaha TF1 connection red / TF1接続が赤い

1. **Verify TF1 is powered on** and network cable connected
2. **Check RCP setting**: On TF1: Setup > Network > RCP must be enabled
3. **Port**: Must be 49280 (default Yamaha RCP port)
4. **Single connection**: Only one RCP client at a time. If TF Editor is connected, disconnect it first
5. **TF Editor won't work**: The Companion module requires the physical hardware - TF Editor (software emulator) is not supported
6. **Restart**: Toggle connection in Companion

---

## Button Issues / ボタンの問題

### Button not doing anything / ボタンが反応しない

1. **Check connection**: Is the relevant connection green? If red, fix the connection first
2. **Check action**: In Companion web UI, click the button and verify:
   - An action is assigned to the "Press" group
   - The correct connection is selected
   - Action options are filled in correctly
3. **Check OPEN QUESTION**: The button may have placeholder values that need updating
4. **Test in Companion UI**: Click the "Test" button in the action editor to trigger the action manually

### Feedback not updating / フィードバックが更新されない

1. **Connection must be active**: Feedbacks only work when the connection is green
2. **Check feedback config**: In Companion, verify the feedback options match the actual device state
3. **Polling delay**: Some feedbacks poll periodically - wait a few seconds for updates
4. **Module limitation**: Some feedback types may not be supported by the current module version

### Wrong button color / ボタンの色が違う

1. **Feedback override**: A feedback condition may be changing the color. Check what feedbacks are configured
2. **Step state**: Multi-step buttons (like SHUTDOWN) change appearance between steps. The button may be stuck on a non-default step - press it or wait for timeout
3. **Reconfigure**: Compare the button's style settings with the YAML spec

---

## Audio Issues / 音声の問題

### No sound / 音が出ない

1. **Check MUTE ALL**: Was the master mute accidentally pressed? Check `[3,6]` on any page
2. **Check channel mutes**: In Audio pages, verify key channels are unmuted (green, not red)
3. **Check TF1 scene**: Recall a known-good scene (e.g., Worship or Default)
4. **Physical check**: Verify speakers are powered on and connected
5. **TF1 direct**: Check the TF1 mixer's own display for mute/level status

### Feedback shows wrong mute state / ミュート表示が実際と違う

1. **Connection lag**: Toggle the mute button twice to resync
2. **Channel ID mismatch**: The YAML channel IDs (e.g., `InCh/001`) must match the TF1's actual channel numbering
3. **Reconnect**: Disable and re-enable the TF1 connection in Companion

---

## Video Issues / 映像の問題

### Black screen on output / 出力が真っ暗

1. **Check BLACK button**: Was `[3,7]` accidentally pressed? Press a camera input button to recover
2. **Check ATEM input**: On the Camera page, press CAM 1 to switch to a known input
3. **Physical check**: Verify cameras are powered on and connected to ATEM inputs
4. **ATEM direct**: Check the ATEM's own multiview output to see what's on each input

### Tally colors not showing / タリーの色が表示されない

1. **ATEM connection**: Must be green for tally feedback to work
2. **Input numbers**: The YAML input numbers must match the actual ATEM input assignments
3. **Multiple feedbacks**: Each camera button has both program (red) and preview (green) feedbacks - verify both are configured

---

## Streaming Issues / 配信の問題

### Can't start stream / 配信を開始できない

1. **OBS connection**: Must be green
2. **Stream key**: Verify OBS has a valid stream key configured (Settings > Stream)
3. **Internet**: Verify internet connectivity on the OBS machine
4. **OBS error**: Check OBS's own status bar for error messages

### Recording not starting / 録画が開始されない

1. **Output path**: Verify OBS's recording output path exists and has write permissions
2. **Disk space**: Check available disk space on the recording drive
3. **OBS settings**: Verify recording settings in OBS (Settings > Output > Recording)

---

## Startup/Shutdown Issues / 起動・終了の問題

### Startup sequence doesn't complete / 起動シーケンスが完了しない

1. **WOL not working**: Verify target computers have WOL enabled in BIOS/UEFI
2. **Script timeout**: Companion's `run shell path` has a 20-second timeout. Long startup sequences may need to background tasks
3. **SSH failure**: Verify SSH credentials and that the target machine has SSH enabled
4. **App not launching**: Check the startup script output for errors

### Shutdown button does nothing / 終了ボタンが反応しない

1. **2-step confirmation**: Press once to see "CONFIRM?" (yellow), then press again within 5 seconds
2. **Step timeout**: If the button shows "CONFIRM?" but resets before you can press again, you may need to increase the timeout
3. **Connection required**: Shutdown actions require active connections to the equipment

---

## Emergency Procedures / 緊急時の手順

### Companion crashes / Companionがクラッシュした

1. Relaunch Companion application
2. Configuration auto-loads from the last saved state
3. Verify Stream Deck XL reconnects (check Surfaces tab)
4. All connections should auto-reconnect

### Stream Deck disconnects / Stream Deckが切断された

1. Unplug the USB cable
2. Wait 5 seconds
3. Plug it back in
4. Companion should auto-detect and restore the layout

### Everything is broken / すべてが動かない

1. **Don't panic** / 慌てないでください
2. **Manual control**: Each device can be operated directly:
   - ProPresenter: Use the computer's keyboard/mouse
   - OBS: Use the OBS window directly
   - ATEM: Use ATEM Software Control or the hardware panel
   - TF1: Use the mixer's physical controls
3. **Restart Companion**: Close and reopen Companion
4. **Restart Stream Deck**: Unplug and replug USB
5. **Check network**: Run `./scripts/network-test.sh`
6. **Reimport config**: If the configuration is corrupted, reimport from the `.companionconfig` backup
