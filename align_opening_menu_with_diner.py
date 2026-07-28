from pathlib import Path

path = Path("main.js")
text = path.read_text()

backup = Path("main_before_menu_alignment.js")
backup.write_text(text)

replacements = {
    # Start directly over the menu in the diner's hands.
    "const menu = this.add.container(445, 430);":
    "const menu = this.add.container(430, 445);",

    # Make the menu initially match the small, angled illustrated menu.
    "menu.setScale(0.08, 0.78);":
    "menu.setScale(0.28, 0.42);",

    "menu.setAlpha(0);":
    "menu.setAlpha(0.88);",

    "menu.setAngle(-4);":
    "menu.setAngle(-11);",

    # Open and lift it more gradually.
    "duration: 700,":
    "duration: 850,",

    # The opened menu should drift upward toward the viewer.
    "y: menu.y - 25,":
    "x: menu.x + 20,\n                        y: menu.y - 95,",

    "scaleX: 1.08,":
    "scaleX: 1.18,",

    "scaleY: 1.08,":
    "scaleY: 1.18,",

    "duration: 450,":
    "duration: 650,"
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(
            f"ERROR: Expected code not found:\n{old}\n"
            "main.js was not changed."
        )

    text = text.replace(old, new, 1)

path.write_text(text)

print("Aligned opening menu with the diner's illustrated menu.")
print("The menu now begins small and tilted near her hands.")
print("Backup saved as:", backup)
