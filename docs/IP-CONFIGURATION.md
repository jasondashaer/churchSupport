# Network Configuration

IP addresses, ports, and network requirements for all equipment.

## IP Address Table

Update the "Actual IP" column during on-site deployment.

| Device | Companion Module | Placeholder IP | Actual IP | Port | Protocol |
|--------|-----------------|---------------|-----------|------|----------|
| Companion PC | (host) | 192.168.1.100 | _________ | 8000 (web UI) | HTTP |
| ProPresenter | `renewedvision-propresenter` | 192.168.1.XXX | _________ | 20404 | TCP |
| OBS Studio | `obs-studio` | 192.168.1.XXX | _________ | 4455 | WebSocket |
| ATEM Switcher | `bmd-atem` | 192.168.1.XXX | _________ | 9910 | TCP |
| Yamaha TF1 | `yamaha-rcp` | 192.168.1.XXX | _________ | 49280 | TCP |
| Computer (WOL) | `generic-pingandwake` | 192.168.1.XXX | _________ | UDP 9 | WOL |
| Computer (SSH) | `generic-ssh` | 192.168.1.XXX | _________ | 22 | SSH |
| TV/Display | TBD | 192.168.1.XXX | _________ | TBD | TBD |

## Port Requirements

These ports must be open between the Companion computer and each device:

| Device | Port | Direction | Protocol | Notes |
|--------|------|-----------|----------|-------|
| ProPresenter | 20404 | Companion → PP | TCP | Enable in PP Preferences > Network |
| OBS Studio | 4455 | Companion → OBS | WebSocket | Enable in OBS Tools > WebSocket Server Settings |
| ATEM Switcher | 9910 | Companion → ATEM | TCP | Always open (network connection) |
| Yamaha TF1 | 49280 | Companion → TF1 | TCP | RCP protocol; enable in TF1 network settings |
| SSH | 22 | Companion → Target | TCP | For remote shutdown commands |
| Companion Web UI | 8000 | Browser → Companion | HTTP | For configuration (local access) |
| WOL | 9 | Companion → broadcast | UDP | Wake-on-LAN magic packet |

## Updating IPs After Deployment

### In Companion

1. Open Companion web UI (`http://localhost:8000`)
2. Go to **Connections** tab
3. Click each connection's **Edit** button
4. Update the **Host** field with the actual IP address
5. Wait for the status indicator to turn green

### In Helper Scripts

Update the environment variables or edit the default values:

```bash
# Option A: Set environment variables before running
export PROPRESENTER_IP="192.168.1.10"
export OBS_IP="192.168.1.11"
export ATEM_IP="192.168.1.12"
export YAMAHA_IP="192.168.1.13"
./scripts/network-test.sh

# Option B: Edit the default values in each script
# Look for the "=== CONFIGURATION ===" section near the top
```

## Network Requirements

### Same Subnet

All equipment **must** be on the same network subnet. Companion communicates directly with each device over TCP/UDP - there is no cloud relay.

Example valid configuration:
```
Companion PC:  192.168.1.100 / 255.255.255.0
ProPresenter:  192.168.1.101 / 255.255.255.0
OBS:           192.168.1.102 / 255.255.255.0
ATEM:          192.168.1.103 / 255.255.255.0
TF1:           192.168.1.104 / 255.255.255.0
```

### Static IPs Recommended

AV equipment should use **static IP addresses** (or DHCP reservations) to prevent addresses from changing between services. If IPs change, Companion connections will fail.

**To set up DHCP reservations:**
1. Find each device's MAC address (usually in network settings)
2. In your router/DHCP server, create a reservation mapping each MAC to a fixed IP
3. Reboot the device to confirm it gets the reserved address

### Firewall Notes

- Ensure no firewall on the Companion PC blocks outbound connections to the ports listed above
- Windows Firewall may need exceptions for Companion
- macOS may prompt to allow Companion through the firewall on first run
- If there's a network firewall/router between devices, ensure the required ports are allowed

### ATEM Special Notes

- ATEM switchers default to `192.168.10.240` which may be a different subnet
- You may need to set a temporary IP on the Companion PC (e.g., `192.168.10.100`) to access the ATEM's configuration page, then change the ATEM's IP to match your main subnet
- ATEM **cannot** be controlled via USB from Companion - must use network
- Only one control connection at a time (unless using ATEM Software Control's sharing feature)

### TF1 Special Notes

- TF1 default IP may need to be configured in the mixer's own display settings
- RCP connections require the TF1 to have network enabled (check Setup > Network on the TF1)
- Only one RCP connection at a time (StageMix uses a separate protocol)

## Network Diagram

```
                    ┌──────────────────┐
                    │  Network Switch  │
                    └────────┬─────────┘
            ┌───────┬───────┼───────┬───────┐
            │       │       │       │       │
     ┌──────┴──┐ ┌──┴───┐ ┌┴────┐ ┌┴────┐ ┌┴─────────┐
     │Companion│ │ProPre│ │ OBS │ │ATEM │ │ Yamaha   │
     │   PC    │ │senter│ │     │ │     │ │   TF1    │
     │ + SD XL │ │      │ │     │ │     │ │          │
     └─────────┘ └──────┘ └─────┘ └─────┘ └──────────┘
      .1.100      .1.XXX   .1.XXX  .1.XXX   .1.XXX
```

*(Update diagram with actual IPs after deployment)*
