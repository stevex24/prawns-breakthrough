from pathlib import Path

path = Path("main.js")
text = path.read_text()

backup = Path("main_before_opening_menu.js")
backup.write_text(text)

method = r'''
    showMenuOpeningThenFocus() {
        // Temporary menu drawn in Phaser.
        // Later this can be replaced with the illustrated concept menu.
        const menu = this.add.container(445, 430);
        menu.setDepth(15);

        const pages = this.add.graphics();

        pages.fillStyle(0xf8efd7, 1);
        pages.lineStyle(4, 0x5b3a22, 1);

        // Left and right pages.
        pages.fillRoundedRect(-150, -105, 145, 210, 12);
        pages.strokeRoundedRect(-150, -105, 145, 210, 12);

        pages.fillRoundedRect(5, -105, 145, 210, 12);
        pages.strokeRoundedRect(5, -105, 145, 210, 12);

        // Center fold.
        pages.lineBetween(0, -100, 0, 100);

        const heading = this.add.text(
            77,
            -70,
            "TODAY'S\nSPECIAL",
            {
                fontFamily: "Georgia, serif",
                fontSize: "19px",
                color: "#5b2418",
                align: "center",
                fontStyle: "bold"
            }
        );

        heading.setOrigin(0.5);

        const item = this.add.text(
            77,
            20,
            "Prawn's\nBreakthrough",
            {
                fontFamily: "Georgia, serif",
                fontSize: "18px",
                color: "#111111",
                align: "center"
            }
        );

        item.setOrigin(0.5);

        const leftPage = this.add.text(
            -77,
            0,
            "CHECKMATE\nCAFÉ",
            {
                fontFamily: "Georgia, serif",
                fontSize: "18px",
                color: "#3c2a1c",
                align: "center",
                fontStyle: "bold"
            }
        );

        leftPage.setOrigin(0.5);

        menu.add([pages, heading, item, leftPage]);

        // Begin nearly closed, as though opening around its center fold.
        menu.setScale(0.08, 0.78);
        menu.setAlpha(0);
        menu.setAngle(-4);

        this.tweens.add({
            targets: menu,
            alpha: 1,
            scaleX: 1,
            scaleY: 1,
            angle: 0,
            duration: 700,
            ease: "Back.easeOut",

            onComplete: () => {
                this.time.delayedCall(750, () => {
                    this.tweens.add({
                        targets: menu,
                        y: menu.y - 25,
                        scaleX: 1.08,
                        scaleY: 1.08,
                        duration: 450,
                        ease: "Sine.easeInOut",

                        onComplete: () => {
                            this.focusMenuThenPlay();

                            this.tweens.add({
                                targets: menu,
                                alpha: 0,
                                duration: 450,

                                onComplete: () => {
                                    menu.destroy(true);
                                }
                            });
                        }
                    });
                });
            }
        });
    }

'''

if "    showMenuOpeningThenFocus() {" not in text:
    marker = "    focusMenuThenPlay() {"

    if marker not in text:
        raise SystemExit(
            "ERROR: focusMenuThenPlay() was not found. No changes made."
        )

    text = text.replace(marker, method + marker, 1)

bubble_start = text.find("    showOrderBubble() {")
create_start = text.find("    create() {", bubble_start)

if bubble_start == -1 or create_start == -1:
    raise SystemExit(
        "ERROR: Could not isolate showOrderBubble(). No changes made."
    )

bubble_block = text[bubble_start:create_start]

if "this.showMenuOpeningThenFocus();" not in bubble_block:
    if "this.focusMenuThenPlay();" not in bubble_block:
        raise SystemExit(
            "ERROR: focusMenuThenPlay() call was not found "
            "inside showOrderBubble(). No changes made."
        )

    bubble_block = bubble_block.replace(
        "this.focusMenuThenPlay();",
        "this.showMenuOpeningThenFocus();",
        1
    )

    text = text[:bubble_start] + bubble_block + text[create_start:]

path.write_text(text)

print("Opening-menu transition installed.")
print("The diner now opens a temporary menu before the camera zoom.")
print("Backup saved as:", backup)
