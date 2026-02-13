#!/usr/bin/env bash
# =============================================================================
# Sunday Startup Sequence / 日曜起動シーケンス
# Called by Companion's "internal: run shell path" action from the STARTUP button.
#
# This script handles application launching and OS-level startup tasks.
# Device-specific preset recalls (TF1 scene, ATEM macro, OBS profile)
# are handled by Companion actions, not this script.
#
# NOTE: Companion has a 20-second timeout for shell commands.
# Long-running tasks should be backgrounded.
#
# Usage:
#   ./scripts/startup-sunday.sh
#
# Environment variables (optional):
#   PP_HOST       - ProPresenter machine IP (if remote)
#   OBS_HOST      - OBS machine IP (if remote)
#   SSH_USER      - SSH username for remote machines
#   PP_APP_PATH   - Path to ProPresenter application
#   OBS_APP_PATH  - Path to OBS application
# =============================================================================

set -uo pipefail

# === CONFIGURATION ===
PP_HOST="${PP_HOST:-localhost}"
OBS_HOST="${OBS_HOST:-localhost}"
SSH_USER="${SSH_USER:-tech}"
PP_APP_PATH="${PP_APP_PATH:-/Applications/ProPresenter.app}"
OBS_APP_PATH="${OBS_APP_PATH:-/Applications/OBS.app}"
# =====================

DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday
SERVICE_TYPE="sunday"

echo "[startup] Starting Sunday startup sequence..."
echo "[startup] Day of week: $DAY_OF_WEEK"
echo "[startup] Service type: $SERVICE_TYPE"

# --- Launch ProPresenter ---
launch_propresenter() {
    if [[ "$PP_HOST" == "localhost" || "$PP_HOST" == "127.0.0.1" ]]; then
        # Local launch
        if [[ "$(uname)" == "Darwin" ]]; then
            echo "[startup] Launching ProPresenter locally (macOS)..."
            open -a "$PP_APP_PATH" &
        else
            echo "[startup] OPEN QUESTION: ProPresenter launch command for this OS"
            echo "[startup] Skipping ProPresenter launch"
        fi
    else
        # Remote launch via SSH
        echo "[startup] Launching ProPresenter on $PP_HOST via SSH..."
        # Background the SSH command to avoid blocking
        ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            "${SSH_USER}@${PP_HOST}" \
            "open -a '$PP_APP_PATH'" 2>/dev/null &
    fi
}

# --- Launch OBS ---
launch_obs() {
    if [[ "$OBS_HOST" == "localhost" || "$OBS_HOST" == "127.0.0.1" ]]; then
        # Local launch
        if [[ "$(uname)" == "Darwin" ]]; then
            echo "[startup] Launching OBS locally (macOS)..."
            open -a "$OBS_APP_PATH" &
        else
            echo "[startup] OPEN QUESTION: OBS launch command for this OS"
            echo "[startup] Skipping OBS launch"
        fi
    else
        # Remote launch via SSH
        echo "[startup] Launching OBS on $OBS_HOST via SSH..."
        ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            "${SSH_USER}@${OBS_HOST}" \
            "open -a '$OBS_APP_PATH'" 2>/dev/null &
    fi
}

# --- Execute ---
launch_propresenter
launch_obs

# Wait briefly for apps to start initializing
sleep 3

echo "[startup] Applications launched."
echo "[startup] Companion will handle preset recalls (TF1 scene, ATEM macro, OBS profile)."
echo "[startup] Sunday startup complete."
exit 0
