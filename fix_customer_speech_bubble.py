from pathlib import Path

path = Path("main.js")
text = path.read_text()

Path("main_before_customer_speech_fix.js").write_text(text)

replacements = {
    "        const bubbleX = 235;": "        const bubbleX = 55;",
    "        const bubbleY = 125;": "        const bubbleY = 90;",
    "        const bubbleWidth = 300;": "        const bubbleWidth = 350;",
    "        const bubbleHeight = 105;": "        const bubbleHeight = 120;",
    '''            "I think I'll have\\nthe special.",''':
    '''            "I think I'll have the\\nPrawn's Breakthrough.",''',

    '''            bubbleX + 115,
            bubbleY + bubbleHeight - 2,
            bubbleX + 145,
            bubbleY + bubbleHeight - 2,
            bubbleX + 130,
            bubbleY + bubbleHeight + 35''':
    '''            bubbleX + 115,
            bubbleY + bubbleHeight - 4,
            bubbleX + 155,
            bubbleY + bubbleHeight - 4,
            bubbleX + 85,
            bubbleY + bubbleHeight + 70''',

    '''            bubbleX + 115,
            bubbleY + bubbleHeight,
            bubbleX + 130,
            bubbleY + bubbleHeight + 35''':
    '''            bubbleX + 115,
            bubbleY + bubbleHeight,
            bubbleX + 85,
            bubbleY + bubbleHeight + 70''',

    '''            bubbleX + 130,
            bubbleY + bubbleHeight + 35,
            bubbleX + 145,
            bubbleY + bubbleHeight''':
    '''            bubbleX + 85,
            bubbleY + bubbleHeight + 70,
            bubbleX + 155,
            bubbleY + bubbleHeight'''
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(
            "ERROR: Expected bubble code was not found. main.js was not changed."
        )
    text = text.replace(old, new, 1)

path.write_text(text)

print("Moved speech bubble to the customer.")
print("Tail now points down-left toward the seated diner.")
print("Restored the Prawn's Breakthrough order.")
