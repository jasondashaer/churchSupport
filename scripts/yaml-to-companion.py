#!/usr/bin/env python3
"""
YAML-to-Companion JSON Converter
=================================
Converts this project's YAML page specifications into a Bitfocus Companion v4
importable JSON configuration file.

Usage:
    python3 scripts/yaml-to-companion.py                        # Generate config
    python3 scripts/yaml-to-companion.py --validate-only        # Validate only
    python3 scripts/yaml-to-companion.py --dump-sample          # Generate sample for comparison
    python3 scripts/yaml-to-companion.py --output path/to/file  # Custom output path

Requirements:
    PyYAML >= 6.0  (install with: pip install pyyaml)

The generated JSON file can be imported via Companion's Import/Export UI:
    1. Open Companion web UI (http://localhost:8000)
    2. Go to Import/Export tab
    3. Click Import, select the generated file
    4. Remap connections if IP addresses differ
    5. Verify button layout on each page

IMPORTANT: The Companion JSON schema is not formally documented. This script
reconstructs the format from Companion's TypeScript source. Some field names
may need adjustment after testing with a real Companion instance. All mappings
are isolated in FIELD_MAP and the mapping functions for easy tuning.
"""

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "ERROR: PyYAML is required but not installed.\n"
        "Install with: pip install pyyaml\n"
        "エラー: PyYAMLが必要です。pip install pyyaml でインストールしてください。"
    )

# =============================================================================
# SECTION 1: Constants & Configuration
# =============================================================================

FORMAT_VERSION = 6
EXPORT_TYPE = "full"
COMPANION_BUILD = "yaml-converter-v1.0"

GRID_ROWS = 4
GRID_COLS = 8

GRID_SIZE = {
    "minColumn": 0,
    "maxColumn": GRID_COLS - 1,
    "minRow": 0,
    "maxRow": GRID_ROWS - 1,
}

# Font size mapping: YAML string -> Companion integer
FONT_SIZE_MAP = {
    "auto": "auto",
    "7pt": 7,
    "14pt": 14,
    "18pt": 18,
    "24pt": 24,
    "30pt": 30,
    "44pt": 44,
}

# Companion format field names - adjust these if import testing reveals mismatches.
# Each entry maps a conceptual field to its actual name in the Companion JSON.
FIELD_MAP = {
    "action_type_key": "type",
    "action_type_value": "action",
    "feedback_type_value": "feedback",
    "action_id_key": "id",
    "action_def_key": "definitionId",
    "action_conn_key": "connectionId",
    "action_opts_key": "options",
    "press_key": "down",
    "release_key": "up",
    "style_bgcolor": "bgcolor",
    "style_color": "color",
    "style_text": "text",
    "style_size": "size",
}

# Internal action name mapping: our YAML names -> Companion internal action IDs.
# These may need adjustment after testing with a real Companion instance.
INTERNAL_ACTION_MAP = {
    "set_page": "button_page_set",
    "wait": "action_delay",
    "run_shell_path": "shell_path",
    "button_step": "button_step",
    "connection_disable": "instance_control_disable",
    "connection_enable": "instance_control_enable",
}

# Internal action option remapping: our YAML option names -> Companion option names
INTERNAL_OPTION_MAP = {
    "set_page": {"page": "page"},
    "wait": {"duration_ms": "delay"},
    "run_shell_path": {"path": "path"},
    "button_step": {"step": "step"},
    "connection_disable": {"connection_id": "instance_id"},
    "connection_enable": {"connection_id": "instance_id"},
}


# =============================================================================
# SECTION 2: Mapping Layer
# =============================================================================

def hex_to_companion_color(hex_str):
    """Convert '#RRGGBB' hex color to Companion decimal integer.

    Examples:
        '#CC0000' -> 13369344
        '#FFFFFF' -> 16777215
        '#000000' -> 0
    """
    if not hex_str or not isinstance(hex_str, str):
        return 0
    hex_str = hex_str.strip().lstrip("#")
    # Handle 3-digit shorthand
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    if len(hex_str) != 6:
        return 0
    try:
        return int(hex_str, 16)
    except ValueError:
        return 0


def font_size_to_companion(size_str):
    """Convert '14pt' style string to Companion integer."""
    if not size_str:
        return 14
    return FONT_SIZE_MAP.get(str(size_str), 14)


def text_contains_expression(text):
    """Check if button text contains Companion variable expressions like $(...)."""
    return "$(" in text if text else False


def build_button_text(yaml_style):
    """Combine text_top and text_bottom with newline separator."""
    top = yaml_style.get("text_top", "")
    bottom = yaml_style.get("text_bottom", "")
    if top and bottom:
        return f"{top}\\n{bottom}"
    return top or bottom


def build_button_style(yaml_style):
    """Map YAML style block to Companion ButtonStyleProperties."""
    text = build_button_text(yaml_style)
    return {
        FIELD_MAP["style_text"]: text,
        "textExpression": text_contains_expression(text),
        FIELD_MAP["style_size"]: font_size_to_companion(
            yaml_style.get("font_size", "14pt")
        ),
        "alignment": "center:center",
        "pngalignment": "center:center",
        FIELD_MAP["style_color"]: hex_to_companion_color(
            yaml_style.get("color_text", "#FFFFFF")
        ),
        FIELD_MAP["style_bgcolor"]: hex_to_companion_color(
            yaml_style.get("color_bg", "#000000")
        ),
        "show_topbar": "default",
        "png64": None,
    }


def remap_action_options(action_name, options, connection_name):
    """Remap action option keys for internal actions."""
    if connection_name != "internal":
        return dict(options) if options else {}
    opt_map = INTERNAL_OPTION_MAP.get(action_name, {})
    if not opt_map or not options:
        return dict(options) if options else {}
    remapped = {}
    for k, v in options.items():
        remapped[opt_map.get(k, k)] = v
    return remapped


def build_action(yaml_action, connection_map):
    """Map a single YAML action to a Companion ActionEntityModel."""
    conn_name = yaml_action.get("connection", "internal")
    action_name = yaml_action.get("action", "")

    # Resolve connection ID
    if conn_name == "internal":
        conn_id = "internal"
        def_id = INTERNAL_ACTION_MAP.get(action_name, action_name)
    else:
        conn_id = connection_map.get(conn_name, conn_name)
        def_id = action_name

    options = remap_action_options(
        action_name, yaml_action.get("options", {}), conn_name
    )

    return {
        FIELD_MAP["action_type_key"]: FIELD_MAP["action_type_value"],
        FIELD_MAP["action_id_key"]: str(uuid.uuid4()),
        FIELD_MAP["action_def_key"]: def_id,
        FIELD_MAP["action_conn_key"]: conn_id,
        "headline": None,
        FIELD_MAP["action_opts_key"]: options,
        "disabled": False,
        "upgradeIndex": None,
    }


def build_feedback_style(yaml_feedback):
    """Build Companion feedback style override and inversion flag.

    Returns (style_dict, is_inverted).
    """
    style_true = yaml_feedback.get("style_when_true", {})
    style_false = yaml_feedback.get("style_when_false", {})
    is_inverted = False

    # If only style_when_false provided, invert the feedback
    if style_false and not style_true:
        style_true = style_false
        is_inverted = True

    result = {}
    if "color_bg" in style_true:
        result[FIELD_MAP["style_bgcolor"]] = hex_to_companion_color(
            style_true["color_bg"]
        )
    if "color_text" in style_true:
        result[FIELD_MAP["style_color"]] = hex_to_companion_color(
            style_true["color_text"]
        )
    # Handle text overrides in feedback styles
    text_parts = []
    if "text_top" in style_true:
        text_parts.append(style_true["text_top"])
    if "text_bottom" in style_true:
        text_parts.append(style_true["text_bottom"])
    if text_parts:
        result[FIELD_MAP["style_text"]] = "\\n".join(text_parts)

    return result, is_inverted


def build_feedback(yaml_feedback, connection_map):
    """Map a YAML feedback to a Companion FeedbackEntityModel."""
    conn_name = yaml_feedback.get("connection", "internal")
    if conn_name == "internal":
        conn_id = "internal"
    else:
        conn_id = connection_map.get(conn_name, conn_name)

    style, is_inverted = build_feedback_style(yaml_feedback)

    return {
        FIELD_MAP["action_type_key"]: FIELD_MAP["feedback_type_value"],
        FIELD_MAP["action_id_key"]: str(uuid.uuid4()),
        FIELD_MAP["action_def_key"]: yaml_feedback.get("feedback", ""),
        FIELD_MAP["action_conn_key"]: conn_id,
        "headline": None,
        FIELD_MAP["action_opts_key"]: yaml_feedback.get("options", {}),
        "disabled": False,
        "upgradeIndex": None,
        "isInverted": is_inverted,
        "style": style,
    }


def build_step(yaml_press_actions, connection_map, step_name=""):
    """Build a Companion step object from a list of press actions."""
    actions = [build_action(a, connection_map) for a in (yaml_press_actions or [])]
    return {
        "action_sets": {
            FIELD_MAP["press_key"]: actions,
            FIELD_MAP["release_key"]: [],
        },
        "options": {
            "runWhileHeld": [],
            "name": step_name,
        },
    }


def build_control(yaml_button, connection_map):
    """Build a complete Companion button control from a YAML button definition."""
    style = build_button_style(yaml_button.get("style", {}))
    feedbacks = [
        build_feedback(f, connection_map)
        for f in yaml_button.get("feedbacks", [])
    ]

    step_count = yaml_button.get("step_count", 1)
    is_multistep = step_count >= 2

    # Build steps
    steps = {}
    press_actions = yaml_button.get("actions", {}).get("press", [])
    step1_id = str(uuid.uuid4())
    steps[step1_id] = build_step(press_actions, connection_map, "")

    if is_multistep:
        step2_actions = yaml_button.get("step_2_actions", {}).get("press", [])
        step2_id = str(uuid.uuid4())
        steps[step2_id] = build_step(step2_actions, connection_map, "Confirm")

    # Button options
    options = {
        "rotaryActions": False,
    }
    if is_multistep:
        options["stepProgression"] = "auto"
        timeout = yaml_button.get("step_2_timeout_ms", 5000)
        options["stepAutoProgressTimeout"] = timeout
    else:
        options["stepProgression"] = "auto"

    return {
        "type": "button",
        "options": options,
        "style": style,
        "feedbacks": feedbacks,
        "steps": steps,
        "localVariables": [],
    }


# =============================================================================
# SECTION 3: Structure Builders
# =============================================================================

def build_connections(yaml_connections):
    """Build Companion instances dict and connection_map from connections.yaml.

    Returns (instances_dict, connection_map).
    """
    connection_map = {"internal": "internal"}
    instances = {}

    for i, conn in enumerate(yaml_connections):
        conn_id = conn.get("id", "")
        module = conn.get("module", "TBD")

        # Skip TBD modules (display, pdu) - they have no valid module
        if module == "TBD":
            continue

        conn_uuid = str(uuid.uuid4())
        connection_map[conn_id] = conn_uuid

        config = conn.get("config", {})

        instances[conn_uuid] = {
            "instance_type": module,
            "label": conn.get("label", conn_id),
            "config": config,
            "enabled": conn.get("enabled", True),
            "isFirstInit": False,
            "lastUpgradeIndex": -1,
            "sortOrder": i,
        }

    return instances, connection_map


def build_custom_variables(yaml_variables):
    """Convert variables.yaml custom_variables to Companion CustomVariablesModel."""
    result = {}
    for i, var in enumerate(yaml_variables or []):
        name = var.get("name", "")
        if not name:
            continue
        result[name] = {
            "description": var.get("description", ""),
            "defaultValue": var.get("default", ""),
            "persistCurrentValue": False,
            "sortOrder": i,
        }
    return result


def build_page(yaml_page_data, connection_map):
    """Build a complete Companion page from parsed YAML page data."""
    page_meta = yaml_page_data.get("page", {})
    page_name = page_meta.get("name", "Unnamed")

    controls = {}
    for button in yaml_page_data.get("buttons", []):
        pos = button.get("position", [0, 0])
        row = str(pos[0])
        col = str(pos[1])

        if row not in controls:
            controls[row] = {}

        controls[row][col] = build_control(button, connection_map)

    return {
        "name": page_name,
        "controls": controls,
        "gridSize": dict(GRID_SIZE),
    }


def build_full_export(pages_dict, instances, custom_variables):
    """Assemble the top-level Companion export structure."""
    return {
        "version": FORMAT_VERSION,
        "type": EXPORT_TYPE,
        "companionBuild": COMPANION_BUILD,
        "pages": pages_dict,
        "instances": instances,
        "custom_variables": custom_variables,
    }


# =============================================================================
# SECTION 4: Validation
# =============================================================================

class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.info.append(msg)

    @property
    def has_errors(self):
        return len(self.errors) > 0

    def print_report(self):
        print(f"\nValidation Results / バリデーション結果:")
        print(f"  ERRORS:   {len(self.errors)}")
        print(f"  WARNINGS: {len(self.warnings)}")
        print(f"  INFO:     {len(self.info)}")
        print()
        for e in self.errors:
            print(f"  [ERROR] {e}")
        for w in self.warnings:
            print(f"  [WARN]  {w}")
        for i in self.info:
            print(f"  [INFO]  {i}")
        print()


def validate_button(button, page_file, known_connections, result):
    """Validate a single button definition."""
    pos = button.get("position")
    if not pos or not isinstance(pos, list) or len(pos) != 2:
        result.error(f"{page_file}: Button missing valid position field")
        return

    row, col = pos
    label = f"[{row},{col}]"

    if not (0 <= row <= GRID_ROWS - 1):
        result.error(f"{page_file}: Button {label} row {row} out of range (0-{GRID_ROWS-1})")
    if not (0 <= col <= GRID_COLS - 1):
        result.error(f"{page_file}: Button {label} col {col} out of range (0-{GRID_COLS-1})")

    style = button.get("style", {})
    if not style:
        result.warn(f"{page_file}: Button {label} has no style defined")

    # Validate color formats
    for color_field in ["color_bg", "color_text"]:
        val = style.get(color_field, "")
        if val and not (isinstance(val, str) and val.startswith("#") and len(val) == 7):
            result.warn(f"{page_file}: Button {label} {color_field} '{val}' may not be valid hex")

    # Validate font size
    fs = style.get("font_size", "")
    if fs and fs not in FONT_SIZE_MAP:
        result.warn(f"{page_file}: Button {label} font_size '{fs}' not in known sizes")

    # Validate connection references in actions
    for action in button.get("actions", {}).get("press", []):
        conn = action.get("connection", "")
        if conn and conn not in known_connections and conn != "internal":
            result.error(f"{page_file}: Button {label} action references unknown connection '{conn}'")

    # Validate connection references in feedbacks
    for fb in button.get("feedbacks", []):
        conn = fb.get("connection", "")
        if conn and conn not in known_connections and conn != "internal":
            result.error(f"{page_file}: Button {label} feedback references unknown connection '{conn}'")

    # Check for OPEN QUESTION markers
    notes = str(button.get("notes", ""))
    if "OPEN QUESTION" in notes:
        result.warn(f"{page_file}: Button {label} has OPEN QUESTION in notes")

    # Multi-step validation
    step_count = button.get("step_count", 1)
    if step_count >= 2:
        if not button.get("step_2_actions"):
            result.warn(f"{page_file}: Button {label} has step_count={step_count} but no step_2_actions")
        if not button.get("step_2_timeout_ms"):
            result.note(f"{page_file}: Button {label} multi-step without timeout (will use default)")

    # Display-only buttons (no actions)
    press_actions = button.get("actions", {}).get("press", [])
    if not press_actions:
        result.note(f"{page_file}: Button {label} has no press actions (display-only)")


def validate_page(page_data, page_file, known_connections, result):
    """Validate a complete page YAML file."""
    page_meta = page_data.get("page", {})
    if not page_meta.get("number"):
        result.error(f"{page_file}: Missing page number")
    if not page_meta.get("name"):
        result.warn(f"{page_file}: Missing page name")

    buttons = page_data.get("buttons", [])
    if not buttons:
        result.warn(f"{page_file}: No buttons defined")
        return

    # Check for duplicate positions
    positions = []
    for button in buttons:
        pos = button.get("position")
        if pos:
            pos_tuple = tuple(pos)
            if pos_tuple in positions:
                result.error(f"{page_file}: Duplicate button position [{pos[0]},{pos[1]}]")
            positions.append(pos_tuple)

    for button in buttons:
        validate_button(button, page_file, known_connections, result)


def validate_connections(yaml_connections, result):
    """Validate connections.yaml."""
    for conn in yaml_connections:
        conn_id = conn.get("id", "unknown")
        config = conn.get("config", {})
        host = config.get("host", "")
        if "XXX" in str(host):
            result.warn(f"connections.yaml: '{conn_id}' has placeholder IP ({host})")

        notes = conn.get("notes", [])
        oq_count = sum(1 for n in (notes or []) if "OPEN QUESTION" in str(n))
        if oq_count:
            result.warn(f"connections.yaml: '{conn_id}' has {oq_count} OPEN QUESTION(s)")


def validate_all(pages_data, yaml_connections, yaml_variables, result):
    """Run all validation checks."""
    known_connections = {"internal"}
    for conn in yaml_connections:
        known_connections.add(conn.get("id", ""))

    validate_connections(yaml_connections, result)

    for page_file, page_data in pages_data:
        validate_page(page_data, page_file, known_connections, result)


# =============================================================================
# SECTION 5: File I/O
# =============================================================================

def load_yaml_file(path):
    """Load and parse a YAML file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"ERROR: Failed to parse YAML file: {path}", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)


def load_all_pages(pages_dir):
    """Discover and load all page YAML files, sorted by name.

    Returns list of (filename, parsed_data) tuples.
    """
    pages_path = Path(pages_dir)
    if not pages_path.is_dir():
        print(f"ERROR: Pages directory not found: {pages_dir}", file=sys.stderr)
        sys.exit(1)

    page_files = sorted(pages_path.glob("page*.yaml"))
    if not page_files:
        print(f"ERROR: No page*.yaml files found in {pages_dir}", file=sys.stderr)
        sys.exit(1)

    result = []
    for pf in page_files:
        data = load_yaml_file(pf)
        result.append((pf.name, data))

    return result


def write_json_output(data, output_path):
    """Write the Companion JSON config file."""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =============================================================================
# SECTION 6: CLI Entry Point
# =============================================================================

def generate_sample():
    """Generate a minimal sample config for format comparison."""
    conn_map = {"internal": "internal", "sample_module": str(uuid.uuid4())}

    sample_button = {
        "position": [0, 0],
        "style": {
            "text_top": "SAMPLE",
            "text_bottom": "サンプル",
            "font_size": "14pt",
            "color_text": "#FFFFFF",
            "color_bg": "#0066CC",
        },
        "actions": {
            "press": [
                {
                    "connection": "internal",
                    "action": "set_page",
                    "options": {"page": 2},
                }
            ]
        },
        "feedbacks": [],
    }

    sample_feedback_button = {
        "position": [0, 1],
        "style": {
            "text_top": "STATUS",
            "text_bottom": "状態",
            "font_size": "14pt",
            "color_text": "#FFFFFF",
            "color_bg": "#666666",
        },
        "actions": {"press": []},
        "feedbacks": [
            {
                "connection": "sample_module",
                "feedback": "connection_status",
                "options": {},
                "style_when_true": {"color_bg": "#00CC00"},
                "style_when_false": {"color_bg": "#CC0000"},
            }
        ],
    }

    sample_multistep = {
        "position": [0, 2],
        "style": {
            "text_top": "CONFIRM",
            "text_bottom": "確認",
            "font_size": "14pt",
            "color_text": "#FFFFFF",
            "color_bg": "#CC0000",
        },
        "actions": {
            "press": [
                {
                    "connection": "internal",
                    "action": "button_step",
                    "options": {"step": 2},
                }
            ]
        },
        "feedbacks": [],
        "step_count": 2,
        "step_2_style": {"color_bg": "#CCCC00", "color_text": "#000000"},
        "step_2_actions": {
            "press": [
                {
                    "connection": "internal",
                    "action": "set_page",
                    "options": {"page": 1},
                }
            ]
        },
        "step_2_timeout_ms": 5000,
    }

    controls = {
        "0": {
            "0": build_control(sample_button, conn_map),
            "1": build_control(sample_feedback_button, conn_map),
            "2": build_control(sample_multistep, conn_map),
        }
    }

    sample_export = {
        "version": FORMAT_VERSION,
        "type": EXPORT_TYPE,
        "companionBuild": COMPANION_BUILD,
        "pages": {
            "1": {
                "name": "Sample Page",
                "controls": controls,
                "gridSize": dict(GRID_SIZE),
            }
        },
        "instances": {
            conn_map["sample_module"]: {
                "instance_type": "generic-module",
                "label": "Sample Module",
                "config": {"host": "192.168.1.100"},
                "enabled": True,
                "isFirstInit": False,
                "lastUpgradeIndex": -1,
                "sortOrder": 0,
            }
        },
        "custom_variables": {
            "sample_var": {
                "description": "A sample variable",
                "defaultValue": "hello",
                "persistCurrentValue": False,
                "sortOrder": 0,
            }
        },
    }

    return sample_export


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert church YAML specs to Companion JSON config.\n"
        "教会YAMLスペックからCompanion JSON設定を生成します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config-dir",
        default=None,
        help="Path to config/ directory (default: auto-detect from script location)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: output/church-config.companionconfig)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate YAML files, don't generate output",
    )
    parser.add_argument(
        "--dump-sample",
        action="store_true",
        help="Generate a minimal sample config for format comparison",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed conversion progress",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit non-zero)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    if args.config_dir:
        config_dir = Path(args.config_dir)
    else:
        config_dir = project_root / "config"

    output_path = args.output or str(project_root / "output" / "church-config.companionconfig")

    # Handle --dump-sample
    if args.dump_sample:
        sample = generate_sample()
        sample_path = args.output or str(project_root / "output" / "sample-config.json")
        write_json_output(sample, sample_path)
        print(f"Sample config written to: {sample_path}")
        print("Compare this against a real Companion JSON export to verify format.")
        return

    # Load YAML files
    if args.verbose:
        print("Loading configuration files...")
        print(f"  Config directory: {config_dir}")

    connections_path = config_dir / "connections.yaml"
    variables_path = config_dir / "variables.yaml"
    pages_dir = config_dir / "pages"

    connections_data = load_yaml_file(connections_path)
    variables_data = load_yaml_file(variables_path)
    pages_data = load_all_pages(pages_dir)

    yaml_connections = connections_data.get("connections", [])
    yaml_variables = variables_data.get("custom_variables", [])

    if args.verbose:
        print(f"  Loaded {len(yaml_connections)} connections")
        print(f"  Loaded {len(yaml_variables)} custom variables")
        print(f"  Loaded {len(pages_data)} page files")

    # Validate
    result = ValidationResult()
    validate_all(pages_data, yaml_connections, yaml_variables, result)
    result.print_report()

    if result.has_errors:
        print("Validation failed with errors. Fix errors before generating config.")
        print("バリデーションエラーがあります。設定生成前にエラーを修正してください。")
        sys.exit(1)

    if args.strict and result.warnings:
        print("Strict mode: warnings treated as errors.")
        sys.exit(1)

    if args.validate_only:
        if not result.has_errors:
            print("Validation passed. YAML specs are valid.")
            print("バリデーション成功。YAMLスペックは有効です。")
        return

    # Build Companion JSON
    if args.verbose:
        print("Building Companion configuration...")

    instances, connection_map = build_connections(yaml_connections)

    if args.verbose:
        print(f"  Built {len(instances)} connection instances")
        for friendly_id, comp_uuid in connection_map.items():
            if friendly_id != "internal":
                print(f"    {friendly_id} -> {comp_uuid[:8]}...")

    custom_variables = build_custom_variables(yaml_variables)

    pages_dict = {}
    total_buttons = 0
    for page_file, page_data in pages_data:
        page_num = page_data.get("page", {}).get("number", 0)
        page_name = page_data.get("page", {}).get("name", "Unnamed")
        page_result = build_page(page_data, connection_map)
        pages_dict[str(page_num)] = page_result

        button_count = sum(len(cols) for cols in page_result["controls"].values())
        total_buttons += button_count
        if args.verbose:
            print(f"  Page {page_num}: {page_name} ({button_count} buttons)")

    full_export = build_full_export(pages_dict, instances, custom_variables)

    # Write output
    write_json_output(full_export, output_path)

    print(f"\nConfig generated successfully! / 設定ファイルの生成に成功しました！")
    print(f"  Output: {output_path}")
    print(f"  Pages:  {len(pages_dict)}")
    print(f"  Buttons: {total_buttons}")
    print(f"  Connections: {len(instances)}")
    print(f"  Variables: {len(custom_variables)}")
    print()
    print("Next steps / 次のステップ:")
    print("  1. Open Companion web UI (http://localhost:8000)")
    print("  2. Go to Import/Export tab")
    print("  3. Import this file")
    print("  4. Remap connections to actual device IPs")
    print("  5. Verify button layout on each page")


if __name__ == "__main__":
    main()
