import json
import os
import pyttsx3
from pathlib import Path
import time

def setup_tts_engine():
    """Initialize and configure the TTS engine."""
    engine = pyttsx3.init()
    # Set properties for better quality
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    return engine

def generate_single_audio(engine, text, output_file):
    """Generate a single audio file."""
    try:
        engine.save_to_file(text, str(output_file))
        engine.runAndWait()
        # Add a small delay to ensure file is written
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Error generating audio for '{text}': {str(e)}")
        return False

def generate_audio_files():
    """Generate audio files for all words in the NFC word map."""
    # Create audio directory if it doesn't exist
    audio_dir = Path("data/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the NFC word map
    with open("src/ml/nfc_word_map.json", "r") as f:
        word_map = json.load(f)
    
    # Initialize TTS engine
    engine = setup_tts_engine()
    
    # Generate audio for each word
    success_count = 0
    for nfc_id, word in word_map.items():
        # Create the full sentence
        sentence = f"{word}. {'. '.join(word.upper())}. Great job!"
        
        # Generate and save the audio file
        output_file = audio_dir / f"{word}.wav"
        print(f"Generating audio for: {sentence}")
        
        if generate_single_audio(engine, sentence, output_file):
            success_count += 1
            print(f"✓ Successfully generated {output_file}")
        else:
            print(f"✗ Failed to generate {output_file}")
    
    print(f"\nAudio generation complete! Successfully generated {success_count} out of {len(word_map)} files.")

if __name__ == "__main__":
    generate_audio_files() 