#!/usr/bin/env bash
# =============================================================================
# Graceful Shutdown / 安全終了シーケンス
# Called by Companion's SHUTDOWN button (after 2-step confirmation).
#
# Handles OS-level shutdown tasks: quitting applications and powering off.
# Device-specific state saving (TF1 scene store, OBS stop, ATEM black)
# is handled by Companion actions BEFORE this script runs.
#
# NOTE: Companion has a 20-second timeout for shell commands.
# Critical operations happen first; power-off is backgrounded.
#
# Usage:
#   ./scripts/shutdown-graceful.sh
#
# Environment variables:
#   PP_HOST       - ProPresenter machine IP
#   OBS_HOST      - OBS machine IP
#   SSH_USER      - SSH username
#   SHUTDOWN_REMOTE - Set to "yes" to actually shutdown remote machines
# =============================================================================

set -uo pipefail

# === CONFIGURATION ===
PP_HOST="${PP_HOST:-localhost}"
OBS_HOST="${OBS_HOST:-localhost}"
SSH_USER="${SSH_USER:-tech}"
SHUTDOWN_REMOTE="${SHUTDOWN_REMOTE:-no}"
# =====================

echo "[shutdown] Starting graceful shutdown sequence..."
echo "[shutdown] Note: TF1 scene save and OBS stop handled by Companion actions"

# --- Quit ProPresenter ---
quit_propresenter() {
    if [[ "$PP_HOST" == "localhost" || "$PP_HOST" == "127.0.0.1" ]]; then
        if [[ "$(uname)" == "Darwin" ]]; then
            echo "[shutdown] Quitting ProPresenter locally (macOS)..."
            osascript -e 'tell application "ProPresenter" to quit' 2>/dev/null || true
        fi
    else
        echo "[shutdown] Quitting ProPresenter on $PP_HOST via SSH..."
        ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            "${SSH_USER}@${PP_HOST}" \
            "osascript -e 'tell application \"ProPresenter\" to quit'" 2>/dev/null || true
    fi
}

# --- Quit OBS ---
quit_obs() {
    if [[ "$OBS_HOST" == "localhost" || "$OBS_HOST" == "127.0.0.1" ]]; then
        if [[ "$(uname)" == "Darwin" ]]; then
            echo "[shutdown] Quitting OBS locally (macOS)..."
            osascript -e 'tell application "OBS" to quit' 2>/dev/null || true
        fi
    else
        echo "[shutdown] Quitting OBS on $OBS_HOST via SSH..."
        ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            "${SSH_USER}@${OBS_HOST}" \
            "osascript -e 'tell application \"OBS\" to quit'" 2>/dev/null || true
    fi
}

# --- Shutdown remote machines ---
shutdown_remote_machines() {
    if [[ "$SHUTDOWN_REMOTE" != "yes" ]]; then
        echo "[shutdown] Remote machine shutdown DISABLED (set SHUTDOWN_REMOTE=yes to enable)"
        return
    fi

    # Only shutdown if the hosts are remote (not localhost)
    if [[ "$PP_HOST" != "localhost" && "$PP_HOST" != "127.0.0.1" ]]; then
        echo "[shutdown] Shutting down ProPresenter machine ($PP_HOST)..."
        ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            "${SSH_USER}@${PP_HOST}" \
            "sudo shutdown -h +1 'Shutdown initiated by church Stream Deck'" 2>/dev/null &
    fi

    if [[ "$OBS_HOST" != "localhost" && "$OBS_HOST" != "127.0.0.1" && "$OBS_HOST" != "$PP_HOST" ]]; then
        echo "[shutdown] Shutting down OBS machine ($OBS_HOST)..."
        ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
            "${SSH_USER}@${OBS_HOST}" \
            "sudo shutdown -h +1 'Shutdown initiated by church Stream Deck'" 2>/dev/null &
    fi
}

# --- Execute ---
quit_propresenter
quit_obs

# Brief wait for apps to close before attempting machine shutdown
sleep 2

shutdown_remote_machines

echo "[shutdown] Graceful shutdown complete."
echo "[shutdown] Applications quit. Remote shutdown: $SHUTDOWN_REMOTE"
echo "[shutdown] Display power-off handled by Companion actions."
exit 0
