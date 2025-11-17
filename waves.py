"""
Tsunami Super WAV Trigger Sample Generator (Bank-Aware, 2025 Revision)

- Generates 4 x 128 = 512 mono samples at 44.1 kHz / 16-bit:
  Bank 0: Sine      (tracks 1–128)
  Bank 1: Triangle  (tracks 129–256)
  Bank 2: Sawtooth  (tracks 257–384)
  Bank 3: Square    (tracks 385–512)

- Each track maps 1:1 to MIDI notes 0–127 inside its bank.
  For example, in Bank 0 (sine):
    MIDI note 0  -> Track 1   -> "0001_S1 Sine_C-2.wav"
    MIDI note 60 -> Track 61  -> "0061_S1 Sine_C4.wav"

- Filenames follow Tsunami rules:
    <trackNumber>[_FN] <Description>.wav
  where:
    _F  = S (single-shot) by default
    N   = 1 (output 1) by default

- Waveforms are rendered at reduced gain (default -10.5 dBFS ≈ 0.3)
  for safe polyphony on the Tsunami mix bus.

Dependencies:
    pip install numpy scipy soundfile
"""

import os
from dataclasses import dataclass
from typing import Callable, Dict, List

import numpy as np
import soundfile as sf
from scipy import signal

# ===== User-tweakable settings =================================================

OUTPUT_FOLDER = "samples_folder"      # Where WAVs will be written
SAMPLE_RATE = 44100                   # Tsunami spec
DURATION_SECONDS = 1.0                # Per sample
MASTER_GAIN = 0.3                     # Linear gain (≈ -10.5 dBFS)
PLAYBACK_SUFFIX = "_S1"               # _S1 = single-shot on output 1, _L1 = loop on output 1
BIT_DEPTH_SUBTYPE = "PCM_16"          # 16-bit integer

# Waveforms in bank order. Each bank = one instrument.
WAVEFORMS_IN_BANK_ORDER: List[str] = ["sine", "triangle", "saw", "square"]

# ===== Helpers =================================================================


def ensure_output_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def midi_note_to_frequency(midi_note: int) -> float:
    """Standard MIDI pitch to frequency (A4=440, note 69)."""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


NOTE_NAMES = ["C", "C#","D","D#","E","F","F#","G","G#","A","A#","B"]


def midi_note_to_name(midi_note: int) -> str:
    """
    Returns something like 'C4', 'F#3', etc.
    MIDI 60 -> C4 by convention.
    """
    pitch_class = midi_note % 12
    octave = (midi_note // 12) - 1
    return f"{NOTE_NAMES[pitch_class]}{octave}"


# ===== Waveform generators =====================================================


def gen_sine(phase: np.ndarray, _: float) -> np.ndarray:
    return np.sin(phase)


def gen_triangle(phase: np.ndarray, _: float) -> np.ndarray:
    # 0..2π -> triangle in [-1,1]
    return signal.sawtooth(phase, width=0.5)


def gen_saw(phase: np.ndarray, _: float) -> np.ndarray:
    return signal.sawtooth(phase)


def gen_square(phase: np.ndarray, _: float) -> np.ndarray:
    return signal.square(phase)


WAVEFORM_GENERATORS: Dict[str, Callable[[np.ndarray, float], np.ndarray]] = {
    "sine": gen_sine,
    "triangle": gen_triangle,
    "saw": gen_saw,
    "square": gen_square,
}


# ===== Envelope ================================================================


def simple_fade_envelope(num_samples: int, fade_fraction: float = 0.01) -> np.ndarray:
    """
    Apply a short fade-in/out to avoid clicks at boundaries.
    fade_fraction is the proportion of total samples used for each fade.
    """
    fade_len = max(1, int(num_samples * fade_fraction))
    env = np.ones(num_samples, dtype=np.float32)

    # Linear fades
    fade_in = np.linspace(0.0, 1.0, fade_len, endpoint=True, dtype=np.float32)
    fade_out = np.linspace(1.0, 0.0, fade_len, endpoint=True, dtype=np.float32)

    env[:fade_len] *= fade_in
    env[-fade_len:] *= fade_out
    return env


# ===== Core generation logic ===================================================


@dataclass
class BankSpec:
    index: int        # 0-based MIDI bank index
    waveform_name: str


def track_number_for(bank_index: int, midi_note: int) -> int:
    """
    Tsunami MIDI mapping:

    Bank 0: MIDI note 0..127 -> tracks 1..128
    Bank 1: MIDI note 0..127 -> tracks 129..256
    ...
    """
    return bank_index * 128 + midi_note + 1


def filename_for(track_number: int, note_name: str, waveform_label: str) -> str:
    """
    Formats filenames as:

        0001_S1 Sine_C4.wav

    which obeys: <trackNumber>[_FN] <anything>.wav
    """
    track_str = str(track_number).zfill(4)
    return f"{track_str}{PLAYBACK_SUFFIX} {waveform_label}_{note_name}.wav"


def generate_waveform(
    waveform_name: str,
    midi_note: int,
    sample_rate: int,
    duration_sec: float,
) -> np.ndarray:
    num_samples = int(sample_rate * duration_sec)
    t = np.arange(num_samples, dtype=np.float64) / sample_rate
    freq = midi_note_to_frequency(midi_note)

    phase = 2.0 * np.pi * freq * t
    generator = WAVEFORM_GENERATORS[waveform_name]
    raw = generator(phase, freq).astype(np.float32)

    # Apply anti-click envelope + master gain for Tsunami headroom
    env = simple_fade_envelope(num_samples)
    out = raw * env * MASTER_GAIN

    # Safety clamp
    np.clip(out, -1.0, 1.0, out=out)
    return out


def generate_bank(bank: BankSpec, output_folder: str) -> None:
    print(f"Generating bank {bank.index} – {bank.waveform_name}...")
    for midi_note in range(128):
        track_num = track_number_for(bank.index, midi_note)
        note_name = midi_note_to_name(midi_note)
        waveform = generate_waveform(
            waveform_name=bank.waveform_name,
            midi_note=midi_note,
            sample_rate=SAMPLE_RATE,
            duration_sec=DURATION_SECONDS,
        )
        filename = filename_for(
            track_number=track_num,
            note_name=note_name,
            waveform_label=bank.waveform_name.capitalize(),
        )
        path = os.path.join(output_folder, filename)
        sf.write(path, waveform, SAMPLE_RATE, format="WAV", subtype=BIT_DEPTH_SUBTYPE)


def main() -> None:
    ensure_output_folder(OUTPUT_FOLDER)

    banks: List[BankSpec] = [
        BankSpec(index=i, waveform_name=name)
        for i, name in enumerate(WAVEFORMS_IN_BANK_ORDER)
    ]

    for bank in banks:
        generate_bank(bank, OUTPUT_FOLDER)

    print("✅ Tsunami samples generated successfully.")
    print(
        f"- Output folder: {os.path.abspath(OUTPUT_FOLDER)}\n"
        f"- Banks generated: {len(banks)} (0–{len(banks)-1})\n"
        f"- Tracks total: {len(banks) * 128}"
    )


if __name__ == "__main__":
    main()
