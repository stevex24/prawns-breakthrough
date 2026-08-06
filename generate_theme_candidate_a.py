from pathlib import Path
import math
import wave

SAMPLE_RATE = 44_100
TEMPO = 108
EIGHTH_NOTE = 60 / TEMPO / 2

FREQUENCIES = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "Bb4": 466.16,
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "F5": 698.46,
    "R": 0.0,
}

# Light Italian-style 6/8 candidate:
# lyrical opening, repetition with variation, and a brighter ending.
MELODY = [
    ("F4", 1), ("A4", 1), ("C5", 2), ("A4", 1), ("G4", 1),
    ("F4", 1), ("G4", 1), ("A4", 2), ("C5", 1), ("A4", 1),

    ("G4", 1), ("A4", 1), ("Bb4", 2), ("A4", 1), ("G4", 1),
    ("F4", 2), ("E4", 1), ("F4", 3),

    ("F4", 1), ("A4", 1), ("C5", 2), ("D5", 1), ("C5", 1),
    ("Bb4", 1), ("A4", 1), ("G4", 2), ("A4", 1), ("Bb4", 1),

    ("C5", 1), ("D5", 1), ("E5", 2), ("D5", 1), ("C5", 1),
    ("A4", 1), ("G4", 1), ("F4", 4),
]

# Simple 6/8 accompaniment: bass note followed by two light chord pulses.
BARS = [
    ("F4", ["F4", "A4", "C5"]),
    ("F4", ["F4", "A4", "C5"]),
    ("Bb4", ["F4", "Bb4", "D5"]),
    ("F4", ["F4", "A4", "C5"]),
    ("F4", ["F4", "A4", "C5"]),
    ("Bb4", ["G4", "Bb4", "D5"]),
    ("C4", ["G4", "C5", "E5"]),
    ("F4", ["F4", "A4", "C5"]),
]


def envelope(position: int, total: int) -> float:
    attack = max(1, int(total * 0.06))
    release = max(1, int(total * 0.15))

    if position < attack:
        return position / attack

    if position >= total - release:
        return max(0.0, (total - position) / release)

    return 1.0


def tone(frequency: float, duration: float, volume: float) -> list[float]:
    count = int(SAMPLE_RATE * duration)

    if frequency == 0:
        return [0.0] * count

    samples = []

    for index in range(count):
        time = index / SAMPLE_RATE
        env = envelope(index, count)

        # Fundamental plus a quiet second harmonic for a softer,
        # clarinet/accordion-like synthesized timbre.
        value = (
            math.sin(2 * math.pi * frequency * time)
            + 0.22 * math.sin(4 * math.pi * frequency * time)
        )

        samples.append(volume * env * value)

    return samples


def mix(target: list[float], source: list[float], start: int) -> None:
    required = start + len(source)

    if required > len(target):
        target.extend([0.0] * (required - len(target)))

    for index, value in enumerate(source):
        target[start + index] += value


melody_duration = sum(units for _, units in MELODY) * EIGHTH_NOTE
audio = [0.0] * int((melody_duration + 0.5) * SAMPLE_RATE)

cursor = 0

for note, units in MELODY:
    duration = units * EIGHTH_NOTE
    sound = tone(FREQUENCIES[note], duration, 0.24)
    mix(audio, sound, cursor)
    cursor += len(sound)

# Add a restrained 6/8 accompaniment.
bar_duration = 6 * EIGHTH_NOTE

for bar_index, (bass, chord) in enumerate(BARS):
    bar_start = int(bar_index * bar_duration * SAMPLE_RATE)

    bass_frequency = FREQUENCIES[bass] / 2
    mix(
        audio,
        tone(bass_frequency, 2 * EIGHTH_NOTE, 0.10),
        bar_start,
    )

    for beat in (2, 4):
        pulse_start = bar_start + int(beat * EIGHTH_NOTE * SAMPLE_RATE)

        for chord_note in chord:
            mix(
                audio,
                tone(FREQUENCIES[chord_note], 1.5 * EIGHTH_NOTE, 0.035),
                pulse_start,
            )

# Prevent clipping.
peak = max(abs(sample) for sample in audio) or 1.0
normalizer = min(1.0, 0.88 / peak)

pcm = bytearray()

for sample in audio:
    value = int(max(-1.0, min(1.0, sample * normalizer)) * 32767)
    pcm.extend(value.to_bytes(2, byteorder="little", signed=True))

output = Path("assets/checkmate-cafe-theme-a.wav")

with wave.open(str(output), "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)
    wav.writeframes(pcm)

print(f"Created {output}")
print(f"Duration: {len(audio) / SAMPLE_RATE:.1f} seconds")
