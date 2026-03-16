# NFC-ML-Learner

Offline edge ML vocabulary learning device for rural Kenya and refugee camp classrooms.

This project helps children practice vocabulary with NFC tagged cards, offline speech recognition, and spoken feedback that runs on the device itself. It is built for classrooms where internet access is unreliable and the hardware needs to stay affordable, portable, and easy to use.

![Demo](docs/demo.gif)

## Why Edge ML

The device processes speech on the hardware itself instead of sending audio to the cloud. That makes it a better fit for schools and learning spaces where connectivity is limited and the system still needs to work every day.

## What It Does

A child taps an NFC tagged card, for example a picture of a lion, against the device. The system looks up the tag, says the word aloud, spells it letter by letter, and gives audio reinforcement. The child can then **say the word back** and the on device keyword spotter listens for the correct answer in real time.

The full pipeline runs offline on low cost hardware. It is designed for early literacy practice, small group learning, and bilingual content such as English and Kiswahili.

## Tech Stack

| Layer            | Technology                              |
|------------------|-----------------------------------------|
| Keyword Spotting | Picovoice Porcupine (TinyML, on-device) |
| Text-to-Speech   | pyttsx3 (offline WAV generation)        |
| Audio I/O        | PyAudio (real-time mic capture)         |
| NFC Simulation   | JSON tag-to-word mapping                |
| Target Hardware  | ESP32 / Raspberry Pi                    |
| Language         | Python 3.13                             |

## Architecture

```
NFC Tag Scan
     |
     v
nfc_word_map.json   -- maps tag IDs to vocabulary words
     |
     v
generate_tts.py     -- pre-generates "<word>. <spelling>. Great job!" WAV files
     |
     v
data/audio/*.wav    -- cached audio, no runtime TTS needed
     |
     v
keyword_spotting.py -- Porcupine listens for the child to repeat the word
     |
     v
Audio feedback      -- plays the corresponding WAV on successful detection
```

All inference happens locally. No cloud calls, no network dependency. The Porcupine engine processes raw PCM frames from the microphone at the hardware sample rate and returns keyword indices in constant time.

## Key Features

- **On-device ML inference** -- Picovoice Porcupine runs keyword detection directly on the microphone stream with sub-100ms latency
- **Offline-first design** -- TTS audio is pre-generated and cached as WAV files; no runtime synthesis or network calls
- **NFC-to-curriculum mapping** -- vocabulary is data-driven via JSON; adding a new word means adding one key-value pair and regenerating audio
- **Extensible callback system** -- `KeywordSpotter.start_listening(callback=fn)` accepts any handler, decoupling detection from response logic
- **Hardware-portable** -- architected for ESP32/Raspberry Pi deployment with solar power and SD-card content updates

## Suggested Use Cases

- English and Kiswahili word drills with reusable tagged cards
- Community learning programmes that need offline, portable teaching aids
- Refugee camp classrooms with limited or no internet access
- Small group vocabulary practice with immediate spoken feedback

## Project Structure

```
nfc-ml-learner/
  src/
    ml/
      keyword_spotting.py      # Porcupine-based realtime keyword detector
      generate_tts.py          # Offline TTS audio generation pipeline
      nfc_word_map.json        # NFC tag ID -> word mapping
      test_keyword_spotting.py # Integration test harness
    app/
      simulate_nfc.py          # NFC scan simulator for development
  data/
    audio/                     # Pre-generated WAV files (lion.wav, etc.)
  requirements.txt
```

## Quick Start

```bash
# Clone and set up
git clone https://github.com/19bk/nfc-ml-learner.git
cd nfc-ml-learner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate vocabulary audio files
python src/ml/generate_tts.py

# Set your Picovoice access key
export PICOVOICE_ACCESS_KEY="your-key-here"

# Run keyword spotting (speak "lion", "tiger", "elephant", "giraffe", or "monkey")
python src/ml/keyword_spotting.py

# Run the test harness
python src/ml/test_keyword_spotting.py

# Run the terminal demo (no hardware or API keys needed)
python scripts/demo_simulate.py
```

## Current Vocabulary

| NFC Tag ID | Word     |
|------------|----------|
| nfc_001    | lion     |
| nfc_002    | tiger    |
| nfc_003    | elephant |
| nfc_004    | giraffe  |
| nfc_005    | monkey   |

Adding words: insert a new entry in `src/ml/nfc_word_map.json`, then re-run `generate_tts.py`.

## License

MIT
