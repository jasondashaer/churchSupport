#!/usr/bin/env bash
# =============================================================================
# Midweek Startup Sequence / 平日起動シーケンス
# Called by Companion for midweek services/events.
# Same as Sunday startup but logs a different service type.
#
# Device-specific preset recalls are handled by Companion actions
# (different scene/macro numbers for midweek vs Sunday).
#
# NOTE: Companion has a 20-second timeout for shell commands.
#
# Usage:
#   ./scripts/startup-midweek.sh
# =============================================================================

set -uo pipefail

# === CONFIGURATION ===
PP_HOST="${PP_HOST:-localhost}"
OBS_HOST="${OBS_HOST:-localhost}"
SSH_USER="${SSH_USER:-tech}"
PP_APP_PATH="${PP_APP_PATH:-/Applications/ProPresenter.app}"
OBS_APP_PATH="${OBS_APP_PATH:-/Applications/OBS.app}"
# =====================

SERVICE_TYPE="midweek"

echo "[startup] Starting midweek startup sequence..."
echo "[startup] Service type: $SERVICE_TYPE"

# --- Launch ProPresenter ---
if [[ "$PP_HOST" == "localhost" || "$PP_HOST" == "127.0.0.1" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "[startup] Launching ProPresenter locally..."
        open -a "$PP_APP_PATH" &
    fi
else
    echo "[startup] Launching ProPresenter on $PP_HOST via SSH..."
    ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
        "${SSH_USER}@${PP_HOST}" \
        "open -a '$PP_APP_PATH'" 2>/dev/null &
fi

# --- Launch OBS ---
if [[ "$OBS_HOST" == "localhost" || "$OBS_HOST" == "127.0.0.1" ]]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "[startup] Launching OBS locally..."
        open -a "$OBS_APP_PATH" &
    fi
else
    echo "[startup] Launching OBS on $OBS_HOST via SSH..."
    ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
        "${SSH_USER}@${OBS_HOST}" \
        "open -a '$OBS_APP_PATH'" 2>/dev/null &
fi

sleep 3

echo "[startup] Applications launched."
echo "[startup] Companion will handle midweek preset recalls."
echo "[startup] Midweek startup complete."
exit 0
