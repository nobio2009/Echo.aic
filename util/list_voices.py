import pyttsx3

def list_voices():
    """List all available voices on the system."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("Available voices:")
    for index, voice in enumerate(voices):
        print(f"\nVoice {index}:")
        print(f"  Name: {voice.name}")
        print(f"  ID: {voice.id}")
        print(f"  Language(s): {voice.languages}")
        print(f"  Gender: {voice.gender}")
        print(f"  Age: {voice.age}")

if __name__ == "__main__":
    list_voices()
