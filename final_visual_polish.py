from pathlib import Path

path = Path("main.js")
text = path.read_text()

Path("main_before_final_visual_polish.js").write_text(text)

# ---------------------------------------------------------
# 1. Replace letter K with real chess king symbols.
# ---------------------------------------------------------

old_king = '''    makeKing(squareName, color) {
        const position = this.square(squareName);

        const king = this.add.text(
            position.x,
            position.y,
            "K",
            {
                fontSize: "36px",
                color: color,
                fontStyle: "bold"
            }
        );

        king.setOrigin(0.5);

        return king;
    }'''

new_king = '''    makeKing(squareName, color) {
        const position = this.square(squareName);

        const isWhite = color === "#ffffff";

        const king = this.add.text(
            position.x,
            position.y,
            isWhite ? "♔" : "♚",
            {
                fontFamily: "Georgia, serif",
                fontSize: "48px",
                color: color,
                stroke: isWhite ? "#222222" : "#eeeeee",
                strokeThickness: 1
            }
        );

        king.setOrigin(0.5);

        return king;
    }'''

if old_king not in text:
    raise SystemExit("ERROR: makeKing() block not found.")

text = text.replace(old_king, new_king, 1)

# ---------------------------------------------------------
# 2. Change only the menu dish and customer's order.
#    Keep the project's Prawn's Breakthrough title untouched.
# ---------------------------------------------------------

old_menu = '''            "Prawn's\\nBreakthrough",'''
new_menu = '''            "HOUSE\\nSPECIAL",'''

if old_menu not in text:
    raise SystemExit("ERROR: menu item text not found.")

text = text.replace(old_menu, new_menu, 1)

old_dialogue = '''            "I think I'll try the\\nPrawn's Breakthrough.",'''
new_dialogue = '''            "I think I'll try the\\nHouse Special.",'''

if old_dialogue not in text:
    raise SystemExit("ERROR: diner dialogue not found.")

text = text.replace(old_dialogue, new_dialogue, 1)

# ---------------------------------------------------------
# 3. More comic prawn scuttle.
#    Does not interfere with the x/y movement tween.
# ---------------------------------------------------------

old_scuttle = '''            // A tiny repeated rocking motion suggests comic crawling.
            const scuttle = this.tweens.add({
                targets: piece,
                angle: {
                    from: -6,
                    to: 6
                },
                duration: 110,
                yoyo: true,
                repeat: -1
            });'''

new_scuttle = '''            // Exaggerated comic scuttle:
            // rock rapidly while alternately squashing and stretching.
            const scuttle = this.tweens.add({
                targets: piece,
                angle: {
                    from: -14,
                    to: 14
                },
                scaleX: {
                    from: 0.92,
                    to: 1.08
                },
                scaleY: {
                    from: 1.06,
                    to: 0.90
                },
                duration: 85,
                yoyo: true,
                repeat: -1,
                ease: "Sine.easeInOut"
            });'''

if old_scuttle not in text:
    raise SystemExit("ERROR: current scuttle tween not found.")

text = text.replace(old_scuttle, new_scuttle, 1)

# Reset scale as well as angle after each move.
old_reset = '''                    scuttle.stop();
                    piece.setAngle(0);
                    resolve();'''

new_reset = '''                    scuttle.stop();
                    piece.setAngle(0);
                    piece.setScale(1);
                    resolve();'''

if old_reset not in text:
    raise SystemExit("ERROR: movement reset block not found.")

text = text.replace(old_reset, new_reset, 1)

path.write_text(text)

print("Installed:")
print("  - real chess king symbols")
print("  - House Special menu/order wording")
print("  - stronger comic prawn scuttle")
print("Backup: main_before_final_visual_polish.js")
