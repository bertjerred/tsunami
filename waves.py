import os
import numpy as np
import soundfile as sf
from scipy import signal

# Set the output folder path
output_folder = 'samples_folder'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def midi_note_to_frequency(midi_note):
    return 440 * (2 ** ((midi_note - 69) / 12))

def generate_sample(midi_note, waveform_shape):
    # Generate a waveform for the sample
    sample_rate = 44100
    duration = 5  # seconds

    # Convert MIDI note to frequency
    frequency = midi_note_to_frequency(midi_note)

    # Generate waveform based on waveform_shape and frequency
    t = np.arange(sample_rate * duration)
    if waveform_shape == 'sine':
        waveform = np.sin(2 * np.pi * frequency * t / sample_rate)
    elif waveform_shape == 'square':
        waveform = np.sign(np.sin(2 * np.pi * frequency * t / sample_rate))
    elif waveform_shape == 'triangle':
        waveform = np.arcsin(np.sin(2 * np.pi * frequency * t / sample_rate))
    elif waveform_shape == 'sawtooth':
        waveform = signal.sawtooth(2 * np.pi * frequency * t / sample_rate)
    else:
        print(f"Unknown waveform shape: {waveform_shape}")
        return

    # Convert the waveform to stereo
    waveform = np.column_stack((waveform, waveform))

    # Convert the waveform to float32
    waveform = waveform.astype(np.float32)

    # Create the filename based on MIDI note number and waveform shape
    filename = f"{midi_note:04d}_L1_{waveform_shape}.wav"

    # Create the WAV file
    sf.write(os.path.join(output_folder, filename), waveform, sample_rate, format='WAV', subtype='PCM_16')

# Generate samples for all MIDI notes and waveform shapes
for waveform_shape in ['sine', 'square', 'triangle', 'sawtooth']:
    for midi_note in range(1, 129):
        generate_sample(midi_note, waveform_shape)

print("Samples generated successfully.")
