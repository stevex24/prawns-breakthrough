#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/prawns-breakthrough"

if [[ ! -f main.js ]]; then
    echo "ERROR: main.js not found in $(pwd)"
    exit 1
fi

cp main.js "main_before_special_order_$(date +%Y%m%d_%H%M%S).js"

python3 <<'PY'
from pathlib import Path
import re

path = Path("main.js")
text = path.read_text()

start_marker = "// BEGIN SPECIAL ORDER OVERLAY"
end_marker = "// END SPECIAL ORDER OVERLAY"

# Remove an earlier installation so this script is safe to rerun.
if start_marker in text and end_marker in text:
    pattern = re.compile(
        re.escape(start_marker)
        + r".*?"
        + re.escape(end_marker)
        + r"\n?",
        re.DOTALL,
    )
    text = pattern.sub("", text)

# Replace likely versions of the old spoken order.
old_lines = [
    "I'll have Prawn's Breakthrough.",
    'I’ll have Prawn’s Breakthrough.',
    "I'll have the Prawn's Breakthrough.",
    'I’ll have the Prawn’s Breakthrough.',
]

for old in old_lines:
    text = text.replace(old, "I'll have the special.")

overlay_code = r'''
// BEGIN SPECIAL ORDER OVERLAY
function addSpecialOrderOverlay(scene) {
    const depth = 1000;

    // --------------------------------------------------------
    // Customer speech bubble
    // --------------------------------------------------------
    const bubbleX = 55;
    const bubbleY = 38;
    const bubbleWidth = 265;
    const bubbleHeight = 72;

    const bubble = scene.add.graphics().setDepth(depth);

    bubble.fillStyle(0xffffff, 0.98);
    bubble.lineStyle(3, 0x242424, 1);

    bubble.fillRoundedRect(
        bubbleX,
        bubbleY,
        bubbleWidth,
        bubbleHeight,
        15
    );

    bubble.strokeRoundedRect(
        bubbleX,
        bubbleY,
        bubbleWidth,
        bubbleHeight,
        15
    );

    // Speech-bubble tail.
    bubble.fillStyle(0xffffff, 0.98);
    bubble.fillTriangle(
        bubbleX + 66,
        bubbleY + bubbleHeight - 1,
        bubbleX + 99,
        bubbleY + bubbleHeight - 1,
        bubbleX + 78,
        bubbleY + bubbleHeight + 25
    );

    bubble.lineStyle(3, 0x242424, 1);
    bubble.beginPath();
    bubble.moveTo(
        bubbleX + 66,
        bubbleY + bubbleHeight - 1
    );
    bubble.lineTo(
        bubbleX + 78,
        bubbleY + bubbleHeight + 25
    );
    bubble.lineTo(
        bubbleX + 99,
        bubbleY + bubbleHeight - 1
    );
    bubble.strokePath();

    scene.add.text(
        bubbleX + 24,
        bubbleY + 22,
        "I'll have the special.",
        {
            fontFamily: "Georgia, serif",
            fontSize: "22px",
            color: "#161616",
            fontStyle: "italic"
        }
    ).setDepth(depth + 1);

    // --------------------------------------------------------
    // Checkmate Café menu
    // --------------------------------------------------------
    const menuX = 515;
    const menuY = 42;
    const menuWidth = 245;
    const menuHeight = 205;

    const menu = scene.add.graphics().setDepth(depth);

    // Wooden outer frame.
    menu.fillStyle(0x684323, 1);
    menu.fillRoundedRect(
        menuX,
        menuY,
        menuWidth,
        menuHeight,
        12
    );

    // Dark chalkboard interior.
    menu.fillStyle(0x18352f, 1);
    menu.fillRoundedRect(
        menuX + 10,
        menuY + 10,
        menuWidth - 20,
        menuHeight - 20,
        8
    );

    menu.lineStyle(2, 0xe0bd74, 1);
    menu.strokeRoundedRect(
        menuX + 15,
        menuY + 15,
        menuWidth - 30,
        menuHeight - 30,
        6
    );

    scene.add.text(
        menuX + menuWidth / 2,
        menuY + 25,
        "CHECKMATE CAFÉ",
        {
            fontFamily: "Georgia, serif",
            fontSize: "19px",
            fontStyle: "bold",
            color: "#f4df9b"
        }
    )
        .setOrigin(0.5, 0)
        .setDepth(depth + 1);

    scene.add.text(
        menuX + menuWidth / 2,
        menuY + 72,
        "TODAY'S SPECIAL",
        {
            fontFamily: "Georgia, serif",
            fontSize: "17px",
            color: "#ffd866"
        }
    )
        .setOrigin(0.5, 0)
        .setDepth(depth + 1);

    scene.add.text(
        menuX + menuWidth / 2,
        menuY + 112,
        "Prawn's\nBreakthrough",
        {
            fontFamily: "Georgia, serif",
            fontSize: "27px",
            fontStyle: "bold",
            color: "#ffffff",
            align: "center",
            lineSpacing: 4
        }
    )
        .setOrigin(0.5, 0)
        .setDepth(depth + 1);
}
// END SPECIAL ORDER OVERLAY
'''

# Insert the helper before the scene class when possible.
class_match = re.search(r"\bclass\s+\w+\s+extends\s+Phaser\.Scene", text)

if class_match:
    text = (
        text[:class_match.start()]
        + overlay_code
        + "\n"
        + text[class_match.start():]
    )
else:
    text = overlay_code + "\n" + text

# Add the call immediately inside create(). Its high depth ensures
# that later-created restaurant objects do not obscure it.
create_pattern = re.compile(r"(create\s*\(\s*\)\s*\{)")

if not create_pattern.search(text):
    raise SystemExit(
        "Could not find create() in main.js; no changes written."
    )

text = create_pattern.sub(
    r"\1\n        addSpecialOrderOverlay(this);",
    text,
    count=1,
)

path.write_text(text)
print("Updated main.js successfully.")
PY

# Check JavaScript syntax when Node is available.
if command -v node >/dev/null 2>&1; then
    node --check main.js
    echo "JavaScript syntax check passed."
fi

# Initialize Git only if this directory is not already a repository.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git init
fi

# Supply local commit identity only when none is configured.
if ! git config user.name >/dev/null; then
    git config user.name "Cloud Shell User"
fi

if ! git config user.email >/dev/null; then
    git config user.email "${USER:-cloudshell}@users.noreply.github.com"
fi

git add main.js install_special_order_scene.sh
git commit -m "Add daily special menu and customer order"

echo
echo "Committed successfully."
echo "Start the preview with:"
echo "  python3 -m http.server 8000"
