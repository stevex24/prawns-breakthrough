from pathlib import Path

path = Path("main.js")
text = path.read_text()

Path("main_before_balalaika_player.js").write_text(text)

# 1. Preload the image after the prawn asset.
marker = '''        this.load.image(
            "prawn",
            "assets/prawn.png"
        );'''

addition = marker + '''

        this.load.image(
            "balalaikaPlayer",
            "assets/balalaika-player.png"
        );'''

if marker not in text:
    raise SystemExit("ERROR: prawn preload block not found.")

if '"balalaikaPlayer"' not in text:
    text = text.replace(marker, addition, 1)

# 2. Put musician into restaurant scene immediately after restaurant.
marker = '''        restaurant.setScale(restaurantScale);'''

addition = marker + '''

        // Subtle musician in the rear of the café.
        const balalaikaPlayer = this.add.image(
            575,
            330,
            "balalaikaPlayer"
        );

        balalaikaPlayer.setScale(0.13);
        balalaikaPlayer.setDepth(2);
'''

if marker not in text:
    raise SystemExit("ERROR: restaurant scaling block not found.")

if "const balalaikaPlayer =" not in text:
    text = text.replace(marker, addition, 1)

path.write_text(text)

print("Balalaika player added.")
print("Initial position: x=575, y=330")
print("Initial scale: 0.13")
