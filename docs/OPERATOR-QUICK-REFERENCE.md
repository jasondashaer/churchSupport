# Operator Quick Reference / オペレーター早見表

A bilingual cheat sheet for service-day operation.

---

## Page Map / ページ一覧

| Page | Role / 担当 | System / システム |
|------|------------|-----------------|
| **1** | Home / ホーム | Role selector + Startup/Shutdown |
| **2** | Slides / スライド | ProPresenter (core) |
| **3** | Slides+ / スライド+ | ProPresenter (timers, messages) |
| **4** | Audio / 音響 | Yamaha TF1 (core) |
| **5** | Audio+ / 音響+ | Yamaha TF1 (instruments, monitors) |
| **6** | Camera / カメラ | ATEM (core) |
| **7** | Camera+ / カメラ+ | ATEM (keyers, macros) |
| **8** | Stream / 配信 | OBS (core) |
| **9** | Stream+ / 配信+ | OBS (sources, profiles) |
| **10** | Emergency / 緊急 | All systems (panic buttons) |

---

## Color Guide / 色の説明

| Color / 色 | Meaning / 意味 |
|------------|---------------|
| **Red / 赤** | Danger, mute, stop, LIVE / 危険・ミュート・停止・ライブ |
| **Green / 緑** | Go, active, unmute, preview / 実行・アクティブ・解除・プレビュー |
| **Blue / 青** | Navigation / ページ移動 |
| **Yellow / 黄** | Caution, standby, confirmation / 注意・待機・確認 |
| **Gray / 灰** | Disabled, informational / 無効・情報表示 |

---

## Bottom Row (Every Page) / 最下段（全ページ共通）

```
┌────────┬────────┬────────┬────┬────┬────┬──────────┬────────┐
│  Home  │◀ Prev  │ Next ▶ │    │    │    │ MUTE ALL │ BLACK  │
│ ホーム │◀ 前    │ 次 ▶   │    │    │    │全ミュート│ブラック│
│ (blue) │(blue)  │(blue)  │    │    │    │  (RED)   │ (RED)  │
└────────┴────────┴────────┴────┴────┴────┴──────────┴────────┘
 [3,0]    [3,1]    [3,2]                    [3,6]      [3,7]
```

- **MUTE ALL / 全ミュート**: Instantly mutes all audio output (master). Press again to unmute on Audio page.
- **BLACK / ブラック**: Instantly cuts video to black screen. Switch to a camera on Camera page to recover.

---

## Slides Volunteer / スライド担当

**Your pages: 2 and 3 / あなたのページ: 2と3**

### Key Buttons / 重要なボタン:
| Button / ボタン | What it does / 機能 |
|----------------|-------------------|
| **NEXT ▶ / 次スライド** | Advance to next slide / 次のスライドに進む |
| **◀ PREV / 前スライド** | Go back one slide / 前のスライドに戻る |
| **Clear / クリア** | Remove current slide from screen / 画面からスライドを消去 |
| **Clear All / 全消去** | Remove everything from screen / 画面から全てを消去 |
| **Logo / ロゴ** | Show default logo image / デフォルトロゴ画像を表示 |
| **Worship / 賛美** | Load worship lyrics playlist / 賛美の歌詞プレイリストを読み込む |
| **Sermon / メッセージ** | Load sermon slides / メッセージスライドを読み込む |

### Typical Flow / 通常の流れ:
1. Press **Worship / 賛美** to load lyrics
2. Use **NEXT ▶** to advance through songs
3. Press **Sermon / メッセージ** when sermon starts
4. Use **NEXT ▶** for sermon slides
5. Press **Clear All / 全消去** when done

---

## Audio Volunteer / 音響担当

**Your pages: 4 and 5 / あなたのページ: 4と5**

### Key Buttons / 重要なボタン:
| Button / ボタン | What it does / 機能 |
|----------------|-------------------|
| **Pastor / 牧師マイク** | Toggle pastor mic mute / 牧師マイクのミュート切替 |
| **Worship / 賛美リード** | Toggle worship leader mic / 賛美リーダーマイク切替 |
| **Master / マスター** | Toggle master output mute / マスター出力ミュート切替 |
| **Worship Scene / 賛美シーン** | Load worship audio mix / 賛美用ミックスを呼出 |
| **Sermon Scene / 説教シーン** | Load sermon audio mix / 説教用ミックスを呼出 |
| **Prayer Scene / 祈りシーン** | Load prayer audio mix / 祈り用ミックスを呼出 |

### Color Guide / 色の見方:
- **Green / 緑** = Mic is ON (unmuted) / マイクON（ミュート解除）
- **Red / 赤** = Mic is MUTED / マイクミュート中

### Typical Flow / 通常の流れ:
1. Recall **Worship Scene** before worship starts
2. Unmute mics as needed (green = on)
3. Recall **Sermon Scene** when sermon starts
4. Mute worship mics, unmute pastor
5. Recall **Prayer Scene** for quiet moments

---

## Camera Volunteer / カメラ担当

**Your pages: 6 and 7 / あなたのページ: 6と7**

### Key Buttons / 重要なボタン:
| Button / ボタン | What it does / 機能 |
|----------------|-------------------|
| **CAM 1-4 / カメラ1-4** | Switch to camera (LIVE) / カメラに切り替え（ライブ） |
| **PP Out / PP映像** | Switch to ProPresenter output / PP映像に切り替え |
| **CUT / カット** | Instant switch / 即座に切り替え |
| **AUTO / オート** | Smooth transition / スムーズな切り替え |
| **PVW 1-4 / プレビュー** | Preview a camera (not live yet) / カメラをプレビュー |

### Color Guide / 色の見方:
- **Red / 赤** = Camera is LIVE (on program) / カメラがライブ中（放送中）
- **Green / 緑** = Camera is on PREVIEW (next up) / カメラがプレビュー中（次）

### Typical Flow / 通常の流れ:
1. Start on **CAM 1** (wide shot)
2. During worship: switch between **CAM 1** (wide) and **PP Out** (lyrics)
3. During sermon: switch between **CAM 2** (speaker) and **PP Out** (slides)
4. Use **AUTO** for smooth transitions, **CUT** for quick switches

---

## Streaming Volunteer / 配信担当

**Your pages: 8 and 9 / あなたのページ: 8と9**

### Key Buttons / 重要なボタン:
| Button / ボタン | What it does / 機能 |
|----------------|-------------------|
| **GO LIVE / 配信開始** | Start streaming / 配信を開始する |
| **END / 配信停止** | Stop streaming / 配信を停止する |
| **REC / 録画開始** | Start recording / 録画を開始する |
| **STOP / 録画停止** | Stop recording / 録画を停止する |
| **Wide / ワイド** | Wide shot scene / ワイドショットシーン |
| **Speaker / スピーカー** | Speaker camera scene / スピーカーカメラシーン |
| **Slides / スライド** | Slides scene / スライドシーン |

### Color Guide / 色の見方:
- **Red / 赤** on GO LIVE = Currently streaming / 現在配信中
- **Red / 赤** on REC = Currently recording / 現在録画中

### Typical Flow / 通常の流れ:
1. Select **Starting / 開始前** scene before service
2. Press **GO LIVE / 配信開始** and **REC / 録画開始**
3. Switch scenes as service progresses
4. Press **END / 配信停止** and **STOP / 録画停止** after service

---

## Emergency / 緊急時

If something goes wrong during service:

| Problem / 問題 | Solution / 解決策 |
|---------------|-----------------|
| Audio feedback/noise | Press **MUTE ALL / 全ミュート** (bottom row of ANY page) |
| Wrong video showing | Press **BLACK / ブラック** (bottom row), then switch to correct camera |
| Need to stop everything | Go to Page 10 (Emergency), press **ALL STOP / 全停止** |
| Connection lost | Go to Page 10 (Emergency), press the reconnect button for that system |

**Remember / 覚えておくこと**: MUTE ALL and BLACK are on the bottom row of EVERY page. You don't need to navigate to a special page to use them.
