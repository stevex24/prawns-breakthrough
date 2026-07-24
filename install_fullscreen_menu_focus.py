from pathlib import Path

path = Path("main.js")
text = path.read_text()

backup = Path("main_before_fullscreen_menu_focus.js")
backup.write_text(text)

method = r'''
    focusMenuThenPlay() {
        const camera = this.cameras.main;

        const menuCenterX =
            this.boardX + 4 * this.squareSize;

        const menuCenterY =
            this.boardY + 4 * this.squareSize;

        camera.pan(
            menuCenterX,
            menuCenterY,
            1000,
            "Sine.easeInOut"
        );

        camera.zoomTo(
            1.65,
            1000,
            "Sine.easeInOut"
        );

        this.time.delayedCall(1250, () => {
            this.playBreakthrough();
        });
    }

'''

if "    focusMenuThenPlay() {" not in text:
    marker = "    showOrderBubble() {"

    if marker not in text:
        raise SystemExit(
            "ERROR: showOrderBubble() was not found. No changes made."
        )

    text = text.replace(marker, method + marker, 1)

bubble_start = text.find("    showOrderBubble() {")
create_start = text.find("    create() {", bubble_start)

if bubble_start == -1 or create_start == -1:
    raise SystemExit(
        "ERROR: Could not isolate showOrderBubble(). No changes made."
    )

bubble_block = text[bubble_start:create_start]

if "this.focusMenuThenPlay();" not in bubble_block:
    if "this.playBreakthrough();" not in bubble_block:
        raise SystemExit(
            "ERROR: playBreakthrough() call was not found inside "
            "showOrderBubble(). No changes made."
        )

    bubble_block = bubble_block.replace(
        "this.playBreakthrough();",
        "this.focusMenuThenPlay();",
        1
    )

    text = (
        text[:bubble_start]
        + bubble_block
        + text[create_start:]
    )

path.write_text(text)

print("Installed full-screen menu focus.")
print("The bubble now calls focusMenuThenPlay().")
print("Backup saved as:", backup)
