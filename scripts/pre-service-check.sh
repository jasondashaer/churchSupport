#!/usr/bin/env bash
# =============================================================================
# Pre-Service Check / 礼拝前チェック
# Run this 15 minutes before service starts.
# Combines network test + port check + reminder checklist.
#
# Usage:
#   ./scripts/pre-service-check.sh
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "╔════════════════════════════════════════╗"
echo "║  Pre-Service Check / 礼拝前チェック    ║"
echo "║  $(date)           ║"
echo "╚════════════════════════════════════════╝"
echo ""

# --- Step 1: Network ---
echo "━━━ Step 1: Network / ネットワーク ━━━"
if [[ -x "$SCRIPT_DIR/network-test.sh" ]]; then
    "$SCRIPT_DIR/network-test.sh" || true
else
    echo "  [WARN] network-test.sh not found or not executable"
    echo "  Run: chmod +x scripts/network-test.sh"
fi
echo ""

# --- Step 2: Ports ---
echo "━━━ Step 2: Ports / ポート ━━━"
if [[ -x "$SCRIPT_DIR/port-check.sh" ]]; then
    "$SCRIPT_DIR/port-check.sh" || true
else
    echo "  [WARN] port-check.sh not found or not executable"
    echo "  Run: chmod +x scripts/port-check.sh"
fi
echo ""

# --- Step 3: Reminder Checklist ---
echo "━━━ Step 3: Manual Checklist / 手動チェックリスト ━━━"
echo ""
echo "  Companion / Companion:"
echo "    [ ] Companion is running at http://localhost:8000"
echo "        Companionが起動中 (http://localhost:8000)"
echo "    [ ] Stream Deck XL is connected (check USB)"
echo "        Stream Deck XLが接続済み (USB確認)"
echo "    [ ] All connection indicators are GREEN"
echo "        すべての接続インジケーターが緑色"
echo ""
echo "  ProPresenter / ProPresenter:"
echo "    [ ] ProPresenter is running"
echo "        ProPresenterが起動中"
echo "    [ ] Today's presentation/playlist is loaded"
echo "        今日のプレゼンテーションが読み込み済み"
echo "    [ ] Network Link enabled (Preferences > Network)"
echo "        ネットワーク接続が有効 (設定 > ネットワーク)"
echo ""
echo "  OBS Studio / OBS Studio:"
echo "    [ ] OBS is running"
echo "        OBSが起動中"
echo "    [ ] WebSocket server enabled (Tools > WebSocket)"
echo "        WebSocketサーバーが有効 (ツール > WebSocket)"
echo "    [ ] Correct scene collection loaded"
echo "        正しいシーンコレクションが読み込み済み"
echo "    [ ] Stream key configured (if streaming today)"
echo "        ストリームキーが設定済み (配信する場合)"
echo ""
echo "  ATEM / ATEM:"
echo "    [ ] ATEM is powered on"
echo "        ATEMの電源がON"
echo "    [ ] All cameras connected and showing video"
echo "        すべてのカメラが接続済みで映像が表示されている"
echo "    [ ] Correct inputs assigned"
echo "        正しい入力が割り当て済み"
echo ""
echo "  Yamaha TF1 / Yamaha TF1:"
echo "    [ ] TF1 is powered on"
echo "        TF1の電源がON"
echo "    [ ] Correct scene recalled for today's service"
echo "        今日の礼拝用のシーンがリコール済み"
echo "    [ ] All microphones tested (tap test)"
echo "        すべてのマイクがテスト済み (タップテスト)"
echo "    [ ] Speakers powered on"
echo "        スピーカーの電源がON"
echo ""
echo "  General / その他:"
echo "    [ ] Service order/run sheet available"
echo "        礼拝の進行表が準備済み"
echo "    [ ] All volunteer positions staffed"
echo "        すべてのボランティアポジションに人員配置済み"
echo "    [ ] Each volunteer knows their role pages"
echo "        各ボランティアが自分のページを理解している"
echo ""
echo "╔════════════════════════════════════════╗"
echo "║  Check complete! / チェック完了！       ║"
echo "║  Ready for service / 礼拝準備完了       ║"
echo "╚════════════════════════════════════════╝"
