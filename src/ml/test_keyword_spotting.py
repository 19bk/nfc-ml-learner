from keyword_spotting import KeywordSpotter
import time

def custom_callback(keyword):
    """Custom callback function to demonstrate how to handle detected keywords."""
    print(f"\n🎯 Detected word: {keyword}")
    print("Playing feedback audio...")
    # The default callback will handle playing the audio file

def main():
    print("Starting Keyword Spotting Test")
    print("=============================")
    print("This test will listen for the following keywords:")
    print("- lion")
    print("- tiger")
    print("- elephant")
    print("- giraffe")
    print("- monkey")
    print("\nSpeak one of these words to test the system.")
    print("Press Ctrl+C to stop the test.")
    print("=============================\n")
    
    try:
        # Initialize the keyword spotter
        spotter = KeywordSpotter()
        
        # Start listening with our custom callback
        spotter.start_listening(callback=custom_callback)
        
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    except Exception as e:
        print(f"\nError during test: {str(e)}")
    finally:
        print("\nTest completed.")

if __name__ == "__main__":
    main() 