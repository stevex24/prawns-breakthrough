from pathlib import Path

path = Path("main.js")
text = path.read_text()

Path("main_before_piece_rebalance.js").write_text(text)

# Restore calmer prawn movement.
old_scuttle = '''            // Exaggerated comic scuttle:
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

new_scuttle = '''            // Simple comic rocking motion.
            const scuttle = this.tweens.add({
                targets: piece,
                angle: {
                    from: -7,
                    to: 7
                },
                duration: 105,
                yoyo: true,
                repeat: -1,
                ease: "Sine.easeInOut"
            });'''

if old_scuttle in text:
    text = text.replace(old_scuttle, new_scuttle, 1)

# Remove scale reset if it was added only for squash/stretch.
text = text.replace(
'''                    scuttle.stop();
                    piece.setAngle(0);
                    piece.setScale(1);
                    resolve();''',
'''                    scuttle.stop();
                    piece.setAngle(0);
                    resolve();''',
1
)

# Make prawns modestly sized.
text = text.replace(
    "prawn.setDisplaySize(50, 50);",
    "prawn.setDisplaySize(46, 46);",
    1
)

# Make kings fill more of their squares.
text = text.replace(
    'fontSize: "48px",',
    'fontSize: "58px",',
    1
)

path.write_text(text)

print("Restored restrained prawn scuttle.")
print("Prawns set to 46×46.")
print("Kings increased to 58px.")
print("Backup: main_before_piece_rebalance.js")
