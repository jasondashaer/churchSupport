#!/usr/bin/env bash
# =============================================================================
# Network Connectivity Test / ネットワーク接続テスト
# Pings all AV equipment to verify network reachability.
#
# Usage:
#   ./scripts/network-test.sh
#
# Configuration:
#   Set IP addresses via environment variables or edit defaults below.
#   Placeholder IPs (containing "XXX") are automatically skipped.
# =============================================================================

set -euo pipefail

# === CONFIGURATION - UPDATE THESE IPs ===
PROPRESENTER_IP="${PROPRESENTER_IP:-192.168.1.XXX}"
OBS_IP="${OBS_IP:-192.168.1.XXX}"
ATEM_IP="${ATEM_IP:-192.168.1.XXX}"
YAMAHA_IP="${YAMAHA_IP:-192.168.1.XXX}"
COMPANION_IP="${COMPANION_IP:-127.0.0.1}"
# =========================================

# Detect OS for ping syntax
if [[ "$(uname)" == "Darwin" ]]; then
    PING_CMD="ping -c 2 -W 2"
elif [[ "$(uname)" == "Linux" ]]; then
    PING_CMD="ping -c 2 -W 2"
else
    # Windows Git Bash / WSL
    PING_CMD="ping -n 2 -w 2000"
fi

echo "========================================"
echo "  Network Test / ネットワークテスト"
echo "  $(date)"
echo "========================================"
echo ""

PASS=0
FAIL=0
SKIP=0

test_device() {
    local name="$1"
    local ip="$2"

    if [[ "$ip" == *"XXX"* ]]; then
        echo "  [SKIP] $name ($ip) - IP not configured / IP未設定"
        SKIP=$((SKIP + 1))
        return
    fi

    if $PING_CMD "$ip" > /dev/null 2>&1; then
        echo "  [ OK ] $name ($ip) - Reachable / 到達可能 ✓"
        PASS=$((PASS + 1))
    else
        echo "  [FAIL] $name ($ip) - Unreachable / 到達不可 ✗"
        FAIL=$((FAIL + 1))
    fi
}

test_device "Companion PC" "$COMPANION_IP"
test_device "ProPresenter" "$PROPRESENTER_IP"
test_device "OBS Studio" "$OBS_IP"
test_device "ATEM Switcher" "$ATEM_IP"
test_device "Yamaha TF1" "$YAMAHA_IP"

echo ""
echo "----------------------------------------"
echo "  Results: $PASS passed, $FAIL failed, $SKIP skipped"

if [[ $SKIP -gt 0 ]]; then
    echo "  NOTE: $SKIP devices have placeholder IPs."
    echo "  Update IPs in this script or set environment variables."
    echo "  注意: ${SKIP}台のIPが未設定です。"
fi

if [[ $FAIL -gt 0 ]]; then
    echo ""
    echo "  WARNING: $FAIL device(s) unreachable!"
    echo "  警告: ${FAIL}台に到達できません！"
    echo "----------------------------------------"
    exit 1
fi

echo ""
echo "  All configured devices reachable."
echo "  設定済みデバイスすべてに到達可能です。"
echo "----------------------------------------"
exit 0
