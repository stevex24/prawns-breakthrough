from pathlib import Path

path = Path("main.js")
text = path.read_text()

# Ensure the sprite is loaded.
commented_load = '''        // this.load.image(
        //     "prawn",
        //     "assets/prawn.png"
        // );'''

active_load = '''        this.load.image(
            "prawn",
            "assets/prawn.png"
        );'''

if commented_load in text:
    text = text.replace(commented_load, active_load, 1)
elif active_load not in text:
    restaurant_load = '''        this.load.image(
            "restaurant",
            "assets/restaurant-panel.png"
        );'''

    replacement = restaurant_load + '''

        this.load.image(
            "prawn",
            "assets/prawn.png"
        );'''

    if restaurant_load not in text:
        raise SystemExit("ERROR: Could not locate preload image block.")

    text = text.replace(restaurant_load, replacement, 1)

old_function = '''    makePawn(squareName, color) {
        const position = this.square(squareName);

        let pawn;

        if (this.textures.exists("prawn")) {
            pawn = this.add.sprite(
                position.x,
                position.y,
                "prawn"
            );

            pawn.setDisplaySize(44, 44);
        } else {
            pawn = this.add.circle(
                position.x,
                position.y,
                18,
                color
            );

            pawn.setStrokeStyle(2, 0x000000);
        }

        return pawn;
    }'''

new_function = '''    makePawn(squareName, color, usePrawn = false) {
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

if old_function not in text:
    raise SystemExit("ERROR: Could not locate the current makePawn() function.")

text = text.replace(old_function, new_function, 1)

text = text.replace(
    'whiteA: this.makePawn("a5", 0xffffff),',
    'whiteA: this.makePawn("a5", 0xffffff, true),'
)
text = text.replace(
    'whiteB: this.makePawn("b5", 0xffffff),',
    'whiteB: this.makePawn("b5", 0xffffff, true),'
)
text = text.replace(
    'whiteC: this.makePawn("c5", 0xffffff),',
    'whiteC: this.makePawn("c5", 0xffffff, true),'
)

backup = Path("main_before_installing_prawn.js")
if not backup.exists():
    backup.write_text(path.read_text())

path.write_text(text)

print("Installed prawn sprite support.")
print("White pawns are now prawns; black pawns remain circles.")
