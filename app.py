#imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import tempfile
import wave
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for OutSystems to access the API

# Add allowed audio formats
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/test', methods=['GET'])
def test():
    """Simple GET endpoint to test if API is running"""
    return jsonify({"status": "💯YES API WORKING!!!!!!👍"})

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    try:
        # Check if request has the audio file
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
            
        audio_file = request.files['audio']
        
        # Validate if file was selected
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Validate file format
        if not allowed_file(audio_file.filename):
            return jsonify({'error': f'File format not supported. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Read the audio data from formdata
        audio_data = audio_file.read()
        
        # Create temporary WAV file 
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            try:
                # Temp data to WAV file
                with wave.open(temp_wav.name, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono audio
                    wav_file.setsampwidth(2)  # 2 bytes per sample
                    wav_file.setframerate(44100)  # Standard sample rate
                    wav_file.writeframes(audio_data)
                
                # Convert
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_wav.name) as source:
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio)
                    
                    return jsonify({
                        'success': True,
                        'text': text
                    })
            finally:
                #sure clean resources after everything
                if os.path.exists(temp_wav.name):
                    os.unlink(temp_wav.name)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=False)
