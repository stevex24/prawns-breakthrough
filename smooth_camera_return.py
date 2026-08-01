from pathlib import Path

path = Path("main.js")
text = path.read_text()

backup = Path("main_before_smooth_camera_return.js")
backup.write_text(text)

old = """            this.time.delayedCall(
                1200,
                resolve
            );"""

new = """            this.time.delayedCall(
                1200,
                () => {

                    this.tweens.add({
                        targets: camera,
                        zoom: 1.02,
                        duration: 180,
                        yoyo: true,
                        ease: "Sine.easeInOut",

                        onComplete: resolve
                    });

                }
            );"""

if old not in text:
    raise SystemExit(
        "ERROR: returnToRestaurant() ending not found."
    )

text = text.replace(old, new, 1)

path.write_text(text)

print("Installed smoother camera landing.")
print("Backup:", backup)
