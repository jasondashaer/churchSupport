#!/usr/bin/env bash
# =============================================================================
# Port Availability Check / ポートチェック
# Verifies that required ports are open on each device.
#
# Usage:
#   ./scripts/port-check.sh
#
# Requires: nc (netcat) - installed by default on macOS and most Linux distros.
# =============================================================================

set -euo pipefail

# === CONFIGURATION ===
PROPRESENTER_IP="${PROPRESENTER_IP:-192.168.1.XXX}"
PROPRESENTER_PORT=20404

OBS_IP="${OBS_IP:-192.168.1.XXX}"
OBS_PORT=4455

ATEM_IP="${ATEM_IP:-192.168.1.XXX}"
ATEM_PORT=9910

YAMAHA_IP="${YAMAHA_IP:-192.168.1.XXX}"
YAMAHA_PORT=49280

SSH_IP="${SSH_IP:-192.168.1.XXX}"
SSH_PORT=22
# =====================

echo "========================================"
echo "  Port Check / ポートチェック"
echo "  $(date)"
echo "========================================"
echo ""

PASS=0
FAIL=0
SKIP=0

check_port() {
    local name="$1"
    local ip="$2"
    local port="$3"

    if [[ "$ip" == *"XXX"* ]]; then
        echo "  [SKIP] $name - $ip:$port - IP not configured / IP未設定"
        SKIP=$((SKIP + 1))
        return
    fi

    # Use nc (netcat) with 3-second timeout
    if nc -z -w 3 "$ip" "$port" 2>/dev/null; then
        echo "  [ OK ] $name - $ip:$port - Open / 開放 ✓"
        PASS=$((PASS + 1))
    else
        echo "  [FAIL] $name - $ip:$port - Closed or filtered / 閉鎖 ✗"
        FAIL=$((FAIL + 1))
    fi
}

check_port "ProPresenter (TCP)" "$PROPRESENTER_IP" "$PROPRESENTER_PORT"
check_port "OBS WebSocket" "$OBS_IP" "$OBS_PORT"
check_port "ATEM Switcher" "$ATEM_IP" "$ATEM_PORT"
check_port "Yamaha TF1 (RCP)" "$YAMAHA_IP" "$YAMAHA_PORT"
check_port "SSH Remote" "$SSH_IP" "$SSH_PORT"

echo ""
echo "----------------------------------------"
echo "  Results: $PASS open, $FAIL closed, $SKIP skipped"

if [[ $FAIL -gt 0 ]]; then
    echo ""
    echo "  WARNING: $FAIL port(s) not accessible!"
    echo "  警告: ${FAIL}個のポートにアクセスできません！"
    echo ""
    echo "  Possible causes / 考えられる原因:"
    echo "  - Device not running / デバイスが起動していない"
    echo "  - Firewall blocking / ファイアウォールでブロック"
    echo "  - Wrong IP address / IPアドレスが間違い"
    echo "  - Service not enabled / サービスが無効"
    echo "----------------------------------------"
    exit 1
fi

echo ""
echo "  All configured ports accessible."
echo "  設定済みポートすべてにアクセス可能です。"
echo "----------------------------------------"
exit 0
