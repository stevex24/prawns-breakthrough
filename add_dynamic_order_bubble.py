from pathlib import Path

path = Path("main.js")
text = path.read_text()

backup = Path("main_before_dynamic_order_bubble.js")
backup.write_text(text)

method = r'''
    showOrderBubble() {
        const bubbleX = 235;
        const bubbleY = 125;
        const bubbleWidth = 300;
        const bubbleHeight = 105;

        const bubble = this.add.graphics();

        bubble.fillStyle(0xffffff, 0.97);
        bubble.lineStyle(4, 0x222222, 1);

        bubble.fillRoundedRect(
            bubbleX,
            bubbleY,
            bubbleWidth,
            bubbleHeight,
            28
        );

        bubble.strokeRoundedRect(
            bubbleX,
            bubbleY,
            bubbleWidth,
            bubbleHeight,
            28
        );

        // Tail pointing toward the seated woman.
        bubble.fillTriangle(
            bubbleX + 115,
            bubbleY + bubbleHeight - 2,
            bubbleX + 145,
            bubbleY + bubbleHeight - 2,
            bubbleX + 130,
            bubbleY + bubbleHeight + 35
        );

        bubble.lineStyle(4, 0x222222, 1);
        bubble.lineBetween(
            bubbleX + 115,
            bubbleY + bubbleHeight,
            bubbleX + 130,
            bubbleY + bubbleHeight + 35
        );
        bubble.lineBetween(
            bubbleX + 130,
            bubbleY + bubbleHeight + 35,
            bubbleX + 145,
            bubbleY + bubbleHeight
        );

        const words = this.add.text(
            bubbleX + bubbleWidth / 2,
            bubbleY + bubbleHeight / 2 - 2,
            "I think I'll have\nthe special.",
            {
                fontFamily: "Georgia, serif",
                fontSize: "25px",
                color: "#111111",
                align: "center",
                lineSpacing: 5
            }
        );

        words.setOrigin(0.5);

        const bubbleParts = [bubble, words];

        for (const part of bubbleParts) {
            part.setAlpha(0);
            part.setScale(0.75);
            part.setDepth(20);
        }

        this.time.delayedCall(650, () => {
            this.tweens.add({
                targets: bubbleParts,
                alpha: 1,
                scale: 1,
                duration: 350,
                ease: "Back.easeOut",

                onComplete: () => {
                    this.time.delayedCall(1900, () => {
                        this.tweens.add({
                            targets: bubbleParts,
                            alpha: 0,
                            scale: 0.9,
                            duration: 300,

                            onComplete: () => {
                                bubble.destroy();
                                words.destroy();
                                this.playBreakthrough();
                            }
                        });
                    });
                }
            });
        });
    }

'''

if "    showOrderBubble() {" not in text:
    marker = "    create() {"

    if marker not in text:
        raise SystemExit(
            "ERROR: Could not find create() in main.js. No changes made."
        )

    text = text.replace(marker, method + marker, 1)

old_start = '''        this.createPosition();
        this.playBreakthrough();'''

new_start = '''        this.createPosition();
        this.showOrderBubble();'''

if old_start in text:
    text = text.replace(old_start, new_start, 1)
elif new_start not in text:
    raise SystemExit(
        "ERROR: Could not find the animation startup lines. No changes made."
    )

path.write_text(text)

print("Dynamic speech bubble installed.")
print("The bubble appears before the breakthrough begins.")
print(f"Backup saved as {backup}.")
