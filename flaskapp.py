import pickle
from flask import Flask, request, send_file, render_template
import openai
import elevenlabs
from elevenlabs import play
import os
from dotenv import load_dotenv

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")  # import ElevenLabs key from .env file that you will need to create
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"
VOICE_PICKLE_FILE = 'voice.pickle'
RESPONSE_AUDIO_FILE = 'response_elevenlabs.mp3'
messages = [{"role": "system", "content": "Your initial prompt here"}]

def get_voice_from_pickle(file_path):
    """Loads and returns a voice object from a pickle file."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except (OSError, IOError) as e:
        print(f"Error loading voice from pickle: {e}")
        return None

def get_response_text_from_model(messages):
    """Sends the messages to the OpenAI model and returns the generated response."""
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages
    )
    return response['choices'][0]['message']['content']

def write_audio_to_file(response_text, voice, file_path):
    """Writes the audio version of the response_text to the file_path."""
    audio = elevenlabs.generate(
        text=response_text,
        voice=voice,
        model='eleven_monolingual_v1'
    )
    with open(file_path, 'wb') as f:
        f.write(audio)

@app.route('/')
def home():
    """Returns the homepage."""
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def process_message():
    """Processes the user message and returns an audio file with the response."""
    user_message = request.form['message']
    messages.append({"role": "user", "content": user_message})
    
    response_text = get_response_text_from_model(messages)
    messages.append({"role": "assistant", "content": response_text})
    
    voice = get_voice_from_pickle(VOICE_PICKLE_FILE)
    if voice:
        write_audio_to_file(response_text, voice, RESPONSE_AUDIO_FILE)
        return send_file(RESPONSE_AUDIO_FILE, mimetype='audio/mp3')
    else:
        return "Error: Voice not found", 500

def main():
    """Sets the API keys and starts the server."""
    elevenlabs.set_api_key(API_KEY)
    openai.api_key = OPENAI_API_KEY
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()