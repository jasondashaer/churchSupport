# Companion UI Walkthrough

Step-by-step guide for translating the YAML specification files into a working Companion configuration. Open the relevant YAML file alongside this guide as you work.

## Prerequisites

- Bitfocus Companion v4.2+ installed and running
- Stream Deck XL connected via USB
- Web browser open to Companion UI (default: `http://localhost:8000`)

## How to Read the YAML Spec Files

Each page YAML file (e.g., `config/pages/page02-slides-core.yaml`) contains:

```yaml
page:
  number: 2              # Companion page number
  name: "Slides - Core"  # Page name (set in Companion)
  name_jp: "スライド基本" # Japanese name (for reference)
  role: "slides"         # Which volunteer role this serves

buttons:
  - position: [1, 0]     # Row 1, Column 0 (zero-indexed)
    style:
      text_top: "◀ PREV"      # English label (top line)
      text_bottom: "前スライド" # Japanese label (bottom line)
      font_size: "18pt"
      color_text: "#FFFFFF"
      color_bg: "#CCCC00"     # Background color
    actions:
      press:
        - connection: "propresenter"  # Which module
          action: "previous_slide"     # Which action
          options: {}                  # Action parameters
    feedbacks: []
    notes: "Previous slide. Yellow = caution."
```

- **position**: `[row, col]` where row 0 is top, col 0 is left
- **style**: Visual appearance of the button
- **actions.press**: What happens when the button is pressed
- **feedbacks**: Dynamic visual changes based on device state
- **notes**: Human-readable context; `OPEN QUESTION:` marks unknowns

## Step 1: Add Connections

Open `config/connections.yaml` and add each connection in Companion:

1. Click the **Connections** tab in Companion's web UI
2. For each connection in the YAML:
   - Click **+ Add connection**
   - Search for the module name (e.g., `renewedvision-propresenter`)
   - Set the **Label** to match the YAML `label` field
   - Fill in the configuration fields:
     - **host**: IP address (use placeholder for now if unknown)
     - **port**: As specified in YAML
     - **password**: If applicable
3. Check the connection status indicator:
   - **Green circle** = connected successfully
   - **Red circle** = connection failed (check IP/port/network)
   - **Gray circle** = disabled or not yet configured

### Connection Order

Add connections in this order (matches the YAML file):
1. ProPresenter (`renewedvision-propresenter`)
2. OBS Studio (`obs-studio`)
3. ATEM Switcher (`bmd-atem`)
4. Yamaha TF1 (`yamaha-rcp`)
5. Wake-on-LAN (`generic-pingandwake`)
6. SSH (`generic-ssh`)
7. Display control (skip if TBD)
8. Smart outlet (skip if TBD)

## Step 2: Name Pages

1. Click the **Buttons** tab
2. At the top, you'll see page navigation. Click the page dropdown.
3. For each page (1-10):
   - Select the page number
   - Click the page name field
   - Enter the name from the YAML `page.name` field

Page names:
| # | Name |
|---|------|
| 1 | Home |
| 2 | Slides - Core |
| 3 | Slides - Extended |
| 4 | Audio - Core |
| 5 | Audio - Extended |
| 6 | Camera - Core |
| 7 | Camera - Extended |
| 8 | Streaming - Core |
| 9 | Streaming - Extended |
| 10 | Emergency |

## Step 3: Create Buttons

For each button in the YAML file:

### 3a: Select the Grid Position

Click the grid cell matching the `position` field. Remember:
- Grid is 8 columns (0-7) x 4 rows (0-3)
- `[0, 0]` = top-left corner
- `[3, 7]` = bottom-right corner

### 3b: Set Button Type

Most buttons are **Regular Button** (the default). Leave as-is unless the YAML specifies otherwise.

### 3c: Configure Style (Appearance)

In the button editor, go to the **Style** section:

1. **Button text**: Enter the combined EN/JP label
   - For bilingual labels, use both lines:
   - Type the English text, press Enter, type the Japanese text
   - Example: `NEXT ▶\n次スライド`
2. **Font size**: Match the YAML `font_size` value
   - Common sizes: 14pt for normal, 18pt for primary actions
3. **Text color**: Click the color picker, enter the hex value from `color_text`
4. **Background color**: Enter the hex value from `color_bg`
5. **Text alignment**: Center/Center (default) works for most buttons

### 3d: Add Press Actions

In the **Actions** section:

1. Click **Add action** under the "Press" group
2. Select the connection from the dropdown (matches YAML `connection` field)
3. Select the action (matches YAML `action` field)
4. Fill in any options from the YAML `options` field
5. Repeat for multiple actions (they execute in parallel unless separated by `internal:wait`)

**Example**: Navigation button
- Connection: `internal`
- Action: `set_page`
- Option: Page = `2`

**Example**: ProPresenter next slide
- Connection: `ProPresenter` (your connection label)
- Action: `Next Slide`
- Options: (none)

### 3e: Add Feedbacks

In the **Feedbacks** section:

1. Click **Add feedback**
2. Select the connection
3. Select the feedback type (matches YAML `feedback` field)
4. Fill in options
5. Configure **style overrides** for when the feedback is true:
   - Background color from `style_when_true.color_bg`
   - Text changes if specified

**Example**: ATEM tally (camera on program)
- Connection: `ATEM Switcher`
- Feedback: `Program Input`
- Option: Input = `1`
- Style when true: Background = `#CC0000` (red = live)

## Step 4: Multi-Step Buttons (Shutdown Confirmation)

The SHUTDOWN button on Page 1 uses a multi-step button for 2-step confirmation:

1. Click the SHUTDOWN button position `[0, 1]`
2. In the button editor, find **Step Count** or **Steps** setting
3. Set to **2 steps**
4. **Step 1**: Configure the initial appearance (red, "SHUTDOWN / 終了")
   - Press action: Advance to step 2
5. **Step 2**: Configure the confirmation state (yellow, "CONFIRM? / 確認?")
   - Press action: All shutdown actions from the YAML
6. Set **step timeout** to 5000ms (auto-resets to step 1 if not pressed)

## Step 5: Test Each Page

After building each page:

1. Look at the Stream Deck XL to verify buttons appear correctly
2. Press each navigation button to confirm page changes work
3. Check that feedback colors update (requires live connections)
4. Verify the bottom row is consistent across all pages:
   - `[3,0]` Home (blue)
   - `[3,1]` Prev in role (blue or gray if first page)
   - `[3,2]` Next in role (blue or gray if last page)
   - `[3,6]` MUTE ALL (red)
   - `[3,7]` BLACK (red)

## Step 6: Export Configuration

1. Go to the **Import/Export** tab
2. Click **Export** > **Compressed (.companionconfig)**
3. Save the file with a descriptive name, e.g., `church-japan-2026-02.companionconfig`
4. Keep a backup copy before deploying

## Tips

- **Work page by page**: Open one YAML file, build all buttons on that page, test, then move on.
- **Skip OPEN QUESTION buttons**: If a button has unresolved questions in its notes, create it with placeholder values. You can update it later.
- **Save frequently**: Companion auto-saves, but export a backup after completing each page group.
- **Test with equipment when possible**: Feedbacks only work with live connections. Test in Japan after deployment.
