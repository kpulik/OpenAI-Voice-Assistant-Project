import pickle
from elevenlabs import clone, set_api_key

set_api_key("")  # Eleven labs API key here

try:
    with open('voice.pickle', 'rb') as f:
        voice = pickle.load(f)
except (OSError, IOError) as e:
    voice = clone(
        name="Sample Voice",
        description="A cloned voice for testing",
        files=[
            "path_to_audio_file_1.mp3",  # Replace with actual file paths
            "path_to_audio_file_2.mp3"
        ]
    )
    with open('voice.pickle', 'wb') as f:
        pickle.dump(voice, f)

print("Voice object created and saved successfully.")
