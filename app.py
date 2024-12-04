#imports
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
    """Simple endpoint to test if API is running"""
    return jsonify({"status": "API is working"})

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    try:
        # Check if request has the required data
        if not request.json or 'audio_base64' not in request.json:
            return jsonify({'error': 'No audio data provided'}), 400
            
        # Get base64 audio from request
        audio_base64 = request.json['audio_base64']
        
        # Decode base64 audio
        audio_data = base64.b64decode(audio_base64)
        
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            # Write audio data to WAV file
            with wave.open(temp_wav.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono audio
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(44100)  # Standard sample rate
                wav_file.writeframes(audio_data)
            
            # Use speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav.name) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                
                # Clean up temporary file
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
