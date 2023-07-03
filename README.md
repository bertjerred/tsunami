# Tsunami Super WAV Trigger Sample Generator

This script generates audio samples in WAV format for use with the Sparkfun/Robertsonics Tsunami Super WAV Trigger (https://www.robertsonics.com/tsunami/). Each sample corresponds to a MIDI note and a selected waveform shape, allowing you to create a wide range of audio samples.

## Introduction

The Tsunami Super WAV Trigger is a powerful audio playback device that allows you to trigger and play back high-quality audio samples. This script generates audio samples in WAV format that can be used with the Tsunami Super WAV Trigger. The samples are created for different MIDI notes and waveform shapes, providing flexibility in creating various sounds and tones.

## Requirements

- Python 3.6 or above
- NumPy library
- SciPy library
- SoundFile library
- Tsunami Super WAV Trigger (though these WAV files could be used in other contexts just as easily)
  
## Usage

### Clone the repository
git clone https://github.com/bertjerred/tsunami

### Navigate to the project directory
cd tsunami

### Install the required libraries
pip install numpy scipy soundfile

### Run the script
python waves.py

The script will generate audio samples for all MIDI notes and waveform shapes
The samples will be saved in the 'samples_folder' directory
Transfer the generated WAV files to the Tsunami Super WAV Trigger according to the device's documentation

## Customization
Change the output folder as desired

Note: file naming is unique to the Robertsonics specs. See: https://static1.squarespace.com/static/62ab6e0d1f3ea036834d4a0b/t/63c3320ae629af326157fe3a/1673736723795/Tsunami_UserGuide_20230114.pdf

This implementation sends samples with "Loop" set to true and to Output #1. This can be modified. See PDF above.

You can add more wave shapes, too.

### Acknowledgments
This script is inspired by the functionality of the Tsunami Super WAV Trigger by Sparkfun/Robertsonics,
but is NOT official or endorsed in any way by the manufacturer.
