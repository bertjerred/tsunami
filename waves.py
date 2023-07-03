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

def generate_sample(file_number, waveform_shape):
    # Generate a waveform for the sample
    sample_rate = 44100
    duration = 1  # seconds

    # Convert file number to string format with leading zeros if needed
    file_number_str = str(file_number).zfill(4)

    # Define the filename based on file number and waveform shape
    filename = f"{file_number_str}_L1_{waveform_shape}.wav"

    # Calculate frequency based on file number and waveform shape
    if waveform_shape == 'sine':
        cycle_index = (file_number - 1) % 128
        midi_note = cycle_index + 21  # Adjusting the range to correspond to MIDI notes 21-148
        frequency = midi_note_to_frequency(midi_note)
    elif waveform_shape == 'sawtooth':
        cycle_index = (file_number - 1) % 128
        midi_note = cycle_index + 20  # Adjusting the range to correspond to MIDI notes 20-147
        frequency = midi_note_to_frequency(midi_note)
    elif waveform_shape == 'square':
        cycle_index = (file_number - 1) % 128
        midi_note = cycle_index + 21  # Adjusting the range to correspond to MIDI notes 21-148
        frequency = midi_note_to_frequency(midi_note)
    elif waveform_shape == 'triangle':
        cycle_index = (file_number - 1) % 128
        midi_note = cycle_index + 21  # Adjusting the range to correspond to MIDI notes 21-148
        frequency = midi_note_to_frequency(midi_note)
    elif waveform_shape == 'noise':
        frequency = np.random.uniform(20, 20000)  # Random frequency between 20 Hz and 20 kHz
    else:
        raise ValueError(f"Unknown waveform shape: {waveform_shape}")

    # Generate waveform based on waveform_shape and frequency
    t = np.arange(sample_rate * duration)
    if waveform_shape == 'sine':
        waveform = np.sin(2 * np.pi * frequency * t / sample_rate)
    elif waveform_shape == 'sawtooth':
        waveform = signal.sawtooth(2 * np.pi * frequency * t / sample_rate)
    elif waveform_shape == 'square':
        waveform = signal.square(2 * np.pi * frequency * t / sample_rate)
    elif waveform_shape == 'triangle':
        waveform = signal.sawtooth(2 * np.pi * frequency * t / sample_rate, width=0.5)
    elif waveform_shape == 'noise':
        waveform = np.random.uniform(-1, 1, sample_rate * duration)
    else:
        raise ValueError(f"Unknown waveform shape: {waveform_shape}")

    # Convert the waveform to float32
    waveform = waveform.astype(np.float32)

    # Create the WAV file
    sf.write(os.path.join(output_folder, filename), waveform, sample_rate, format='WAV', subtype='PCM_16')

# Define the waveform shapes
waveform_shapes = ['sine', 'sawtooth', 'square', 'triangle', 'noise']

# Define the number of files per waveform shape
files_per_waveform = 128

# Generate samples for each waveform shape
for waveform_shape in waveform_shapes:
    start_file = (waveform_shapes.index(waveform_shape) * files_per_waveform) + 1
    end_file = start_file + files_per_waveform
    for file_number in range(start_file, end_file):
        generate_sample(file_number, waveform_shape)

print("Samples generated successfully.")
