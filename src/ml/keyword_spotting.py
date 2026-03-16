import pvporcupine
import pyaudio
import struct
import json
import os
from pathlib import Path

class KeywordSpotter:
    def __init__(self, access_key=None):
        """
        Initialize the keyword spotter.
        Args:
            access_key: Picovoice access key (required for production)
        """
        self.access_key = access_key or os.getenv('PICOVOICE_ACCESS_KEY')
        if not self.access_key:
            raise ValueError("Picovoice access key is required. Set PICOVOICE_ACCESS_KEY environment variable or pass it to the constructor.")
        
        # Initialize Porcupine
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keywords=['lion', 'tiger', 'elephant', 'giraffe', 'monkey']  # Using our NFC word map keywords
        )
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        
        # Load word map for feedback
        self.word_map = self._load_word_map()
        
    def _load_word_map(self):
        """Load the NFC word map for keyword feedback."""
        with open("src/ml/nfc_word_map.json", "r") as f:
            return json.load(f)
    
    def start_listening(self, callback=None):
        """
        Start listening for keywords.
        Args:
            callback: Function to call when a keyword is detected
        """
        print("Listening for keywords...")
        try:
            while True:
                pcm = self.stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    keyword = self.porcupine.keywords[keyword_index]
                    print(f"Detected keyword: {keyword}")
                    
                    if callback:
                        callback(keyword)
                    else:
                        self._default_callback(keyword)
                        
        except KeyboardInterrupt:
            print("\nStopping keyword detection...")
        finally:
            self.cleanup()
    
    def _default_callback(self, keyword):
        """Default callback that plays the corresponding audio file."""
        audio_file = Path(f"data/audio/{keyword}.wav")
        if audio_file.exists():
            os.system(f"afplay {audio_file}")
        else:
            print(f"Audio file not found for keyword: {keyword}")
    
    def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'stream'):
            self.stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()

def main():
    """Main function to demonstrate keyword spotting."""
    try:
        spotter = KeywordSpotter()
        spotter.start_listening()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 