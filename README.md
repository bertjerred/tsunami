# Tsunami Super WAV Trigger Sample Generator

This script generates audio samples in WAV format for use with the Sparkfun/Robertsonics Tsunami Super WAV Trigger (https://www.robertsonics.com/tsunami/). Each sample corresponds to a MIDI note and a selected waveform shape, allowing you to create a wide range of audio samples.

## Introduction

The Tsunami Super WAV Trigger is a powerful audio playback device that allows you to trigger and play back high-quality audio samples. This script generates audio samples in WAV format that can be used with the Tsunami Super WAV Trigger. The samples are created for different MIDI notes and waveform shapes, providing flexibility in creating various sounds and tones.

## Requirements

- Python 3.6 or above
- NumPy library
- SciPy library
- SoundFile library
- Tsunami Super WAV Trigger connected to your audio playback system

## Usage

### Clone the repository
git clone https://github.com/your-username/tsunami-sample-generator.git

### Navigate to the project directory
cd tsunami-sample-generator

### Install the required libraries
pip install numpy scipy soundfile

### Connect the Tsunami Super WAV Trigger to your audio playback system

### Run the script
python tsunami_sample_generator.py

The script will generate audio samples for all MIDI notes and waveform shapes
The samples will be saved in the 'samples_folder' directory
Transfer the generated WAV files to the Tsunami Super WAV Trigger according to the device's documentation

## Customization
Adjust the sample_rate and duration variables in the code to modify the audio quality and duration of the generated samples.
Modify the waveform shapes (sine, square, triangle, sawtooth) to create different audio characteristics.
Customize the output folder path (output_folder) to specify the location where the generated samples will be saved.

### Acknowledgments
This script is inspired by the functionality of the Tsunami Super WAV Trigger by Sparkfun/Robertsonics.
