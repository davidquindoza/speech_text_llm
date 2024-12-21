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
        print("=== Request received ===")
        
        # Print request
        print("Files in request:", request.files)
        print("Form data:", request.form)
        
        if 'audio' not in request.files:
            print("No audio file in request.files")
            return jsonify({'error': 'No audio file provided'}), 400
            
        audio_file = request.files['audio']
        print(f"Filename: {audio_file.filename}")
        print(f"Content Type: {audio_file.content_type}")

     # Convert directly without saving temp file
        recognizer = sr.Recognizer()
        
        # Read audio file directly from request
        audio_data = sr.AudioFile(io.BytesIO(audio_file.read()))
        
        with audio_data as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
        
        return jsonify({
            'success': True,
            'message': 'Audio processed successfully',
            'filename': audio_file.filename,
            'content_type': audio_file.content_type,
            'text': text
        })
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
