#import librarieszzz
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import base64
import tempfile
import wave
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for OutSystems to access the API

@app.route('/test', methods=['GET'])
def test():
    """Endpoint to test if API is running.."""
    return jsonify({"status": "API working!!!"})

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    try:
        # Check if request has the required data
        if not request.json or 'audio_base64' not in request.json:
            return jsonify({'error': 'No audio data provided'}), 400
            
        # Get base64 audio 
        audio_base64 = request.json['audio_base64']
        
        # Decode base64 audio
        audio_data = base64.b64decode(audio_base64)
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            # convert to wav file for prcessing
            with wave.open(temp_wav.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono audio
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(44100)  # Standard sample rate
                wav_file.writeframes(audio_data)
            
            # conversrion
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav.name) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                
                # cleaning
                os.unlink(temp_wav.name)
                
                return jsonify({
                    'success': True,
                    'text': text
                })
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
