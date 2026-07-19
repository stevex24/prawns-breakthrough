from pathlib import Path

path = Path("main.js")
text = path.read_text()

backup = Path("main_before_scuttling_prawns.js")
backup.write_text(text)

old_make_pawn = '''    makePawn(squareName, color, usePrawn = false) {
        const position = this.square(squareName);

        if (usePrawn && this.textures.exists("prawn")) {
            const prawn = this.add.image(
                position.x,
                position.y,
                "prawn"
            );

            prawn.setDisplaySize(50, 50);

            return prawn;
        }

        const pawn = this.add.circle(
            position.x,
            position.y,
            18,
            color
        );

        pawn.setStrokeStyle(2, 0x000000);

        return pawn;
    }'''

new_make_pawn = '''    makePawn(squareName, color, usePrawn = false) {
        const position = this.square(squareName);

        if (usePrawn && this.textures.exists("prawn")) {
            const prawn = this.add.image(
                position.x,
                position.y,
                "prawn"
            );

            prawn.setDisplaySize(50, 50);

            // Black's prawns use the same artwork with a dark tint.
            if (color === 0x333333) {
                prawn.setTint(0x596273);
            }

            return prawn;
        }

        const pawn = this.add.circle(
            position.x,
            position.y,
            18,
            color
        );

        pawn.setStrokeStyle(2, 0x000000);

        return pawn;
    }'''

old_move_piece = '''    movePiece(piece, destination, duration = 700) {
        const target = this.square(destination);

        return new Promise(resolve => {
            this.tweens.add({
                targets: piece,
                x: target.x,
                y: target.y,
                duration: duration,
                ease: "Sine.easeInOut",
                onComplete: resolve
            });
        });
    }'''

new_move_piece = '''    movePiece(piece, destination, duration = 700) {
        const target = this.square(destination);

        return new Promise(resolve => {
            // A tiny repeated rocking motion suggests comic crawling.
            const scuttle = this.tweens.add({
                targets: piece,
                angle: {
                    from: -6,
                    to: 6
                },
                duration: 110,
                yoyo: true,
                repeat: -1
            });

            this.tweens.add({
                targets: piece,
                x: target.x,
                y: target.y,
                duration: duration,
                ease: "Sine.easeInOut",

                onComplete: () => {
                    scuttle.stop();
                    piece.setAngle(0);
                    resolve();
                }
            });
        });
    }'''

if old_make_pawn not in text:
    raise SystemExit(
        "ERROR: Current makePawn() function was not found. No changes made."
    )

if old_move_piece not in text:
    raise SystemExit(
        "ERROR: Current movePiece() function was not found. No changes made."
    )

text = text.replace(old_make_pawn, new_make_pawn, 1)
text = text.replace(old_move_piece, new_move_piece, 1)

# Enable prawn artwork for all three Black pawns.
text = text.replace(
    'blackA: this.makePawn("a7", 0x333333),',
    'blackA: this.makePawn("a7", 0x333333, true),'
)
text = text.replace(
    'blackB: this.makePawn("b7", 0x333333),',
    'blackB: this.makePawn("b7", 0x333333, true),'
)
text = text.replace(
    'blackC: this.makePawn("c7", 0x333333),',
    'blackC: this.makePawn("c7", 0x333333, true),'
)

path.write_text(text)

print("Updated main.js successfully.")
print("All six pawns now use prawn artwork.")
print("Black prawns are tinted dark.")
print("Moving prawns now scuttle.")
print(f"Backup: {backup}")
