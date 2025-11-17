# Tsunami Super WAV Trigger Sample Generator (Bank-Aware)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8141079.svg)](https://doi.org/10.5281/zenodo.8141079)

This script generates audio samples in WAV format specifically designed for the [Sparkfun/Robertsonics Tsunami Super WAV Trigger](https://www.robertsonics.com/tsunami/). 

## Overview

The **2025 Revision** of this tool is "Bank-Aware." It automatically generates **512 mono samples** (44.1 kHz / 16-bit) organized into four distinct instrument banks. Each track maps 1:1 to MIDI notes 0–127, allowing you to plug a MIDI controller into the Tsunami and play four different waveforms instantly on four different MIDI channels/banks.

### Bank Mapping
The script fills the first 512 tracks of the Tsunami SD card as follows:

| Bank (MIDI Ch) | Waveform | Track Range | Filename Example |
| :--- | :--- | :--- | :--- |
| **Bank 1** | Sine | 1–128 | `0001_S1 Sine_C-2.wav` |
| **Bank 2** | Triangle | 129–256 | `0129_S1 Triangle_C-2.wav` |
| **Bank 3** | Sawtooth | 257–384 | `0257_S1 Saw_C-2.wav` |
| **Bank 4** | Square | 385–512 | `0385_S1 Square_C-2.wav` |

## Requirements

- Python 3.6 or above
- Tsunami Super WAV Trigger (or any sampler reading standard WAV files)

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/bertjerred/tsunami](https://github.com/bertjerred/tsunami)
   cd tsunami

2. **Install dependencies:**
   ```bash
   pip install numpy scipy soundfile

### Usage

1. The script will generate a folder named samples_folder.
2. Inside, you will find 512 WAV files correctly numbered for Tsunami banking.
3. Copy the contents of samples_folder to the root of your Tsunami's microSD card.

## Customization

- Change the output folder as desired
- Note: file naming is unique to the Robertsonics specs. See: https://static1.squarespace.com/static/62ab6e0d1f3ea036834d4a0b/t/63c3320ae629af326157fe3a/1673736723795/Tsunami_UserGuide_20230114.pdf
- This implementation sends mono samples with "Loop" set to true and to Output #1. This can be modified. See PDF above.
- You can add or remove wave shapes
- This implementation sets the sample rate at 44100 Hz and bit depth at 16-bit, as per the WAV Trigger specs

### Acknowledgments
This script is inspired by the functionality of the Tsunami Super WAV Trigger by Sparkfun/Robertsonics,
but is NOT official or endorsed in any way by the manufacturer.
