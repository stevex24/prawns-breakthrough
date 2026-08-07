from pathlib import Path
import math
import wave

SR = 44100
TEMPO = 116
EIGHTH = 60 / TEMPO / 2

FREQ = {
    "C4":261.63, "D4":293.66, "E4":329.63, "F4":349.23,
    "G4":392.00, "A4":440.00, "Bb4":466.16,
    "C5":523.25, "D5":587.33, "E5":659.25, "F5":698.46
}

# Candidate B:
# A stronger repeated opening gesture, then an answering phrase.
MELODY = [
    ("F4",1), ("G4",1), ("A4",1), ("C5",3),
    ("A4",1), ("G4",1), ("F4",1), ("A4",3),

    ("F4",1), ("G4",1), ("A4",1), ("C5",2), ("D5",1),
    ("C5",1), ("A4",1), ("G4",1), ("F4",3),

    ("A4",1), ("Bb4",1), ("C5",1), ("D5",3),
    ("C5",1), ("Bb4",1), ("A4",1), ("C5",3),

    ("D5",1), ("C5",1), ("A4",1), ("G4",2), ("A4",1),
    ("G4",1), ("E4",1), ("F4",4),
]


def tone(freq, duration, volume=.25):
    n = int(SR * duration)
    result = []

    for i in range(n):
        t = i / SR

        attack = min(1.0, i / max(1, int(.04*n)))
        release = min(1.0, (n-i) / max(1, int(.14*n)))
        env = min(attack, release)

        # Warm synthesized lead.
        value = (
            math.sin(2*math.pi*freq*t)
            + .18*math.sin(4*math.pi*freq*t)
        )

        result.append(volume * env * value)

    return result


audio = []

for note, units in MELODY:
    audio.extend(tone(FREQ[note], units * EIGHTH))

peak = max(abs(x) for x in audio) or 1
scale = min(1, .88/peak)

pcm = bytearray()

for x in audio:
    sample = int(max(-1, min(1, x*scale))*32767)
    pcm.extend(sample.to_bytes(2, "little", signed=True))

out = Path("assets/checkmate-cafe-theme-b.wav")

with wave.open(str(out), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SR)
    wav.writeframes(pcm)

print("Created:", out)
print("Duration:", round(len(audio)/SR, 1), "seconds")
