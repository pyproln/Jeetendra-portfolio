from flask import Flask, render_template, request
import os
import easyocr
from PIL import Image
import pyttsx3
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
# import uuid

load_dotenv()

vision_key = os.getenv('AZURE_VISION_KEY')
vision_endpoint = os.getenv('AZURE_VISION_ENDPOINT')


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
AUDIO_FOLDER = 'static/audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ✅ Initialize EasyOCR reader globally
reader = easyocr.Reader(['en'])

# ✅ Route for initial page load
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

# ✅ Route for image upload and OCR
@app.route('/upload', methods = ['POST'])
def upload_image():
    if 'image' not in request.files:
        return render_template('index.html', message='No image uploaded.')

    image = request.files['image']
    if image.filename == '':
        return render_template('index.html', message='No selected file.')

    mode = request.form.get('mode', 'ocr')  # default to OCR
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)


    # Run OCR
    extracted_text = extract_text(filepath)

    # Fallback to captioning if OCR fails
    if mode == 'ocr':
        extracted_text = extract_text(filepath)
    else:
        extracted_text = generate_caption(filepath)

    return render_template('index.html', message='Image uploaded successfully.', extracted_text=extracted_text, image_filename = filename)

# route to Dashboard
@app.route('/dashboard')
def dashboard():
    # Dummy stats for now
    stats = {
        'total_uploads': 12,
        'ocr_count': 7,
        'caption_count': 5,
        'speech_triggered': 10
    }
    return render_template('dashboard.html', stats=stats)



# New route to speak
@app.route('/speak', methods=['POST'])
def speak_text():
    text = request.form.get('text')
    if not text:
        return render_template('index.html', message='No text to speak.')

    engine = pyttsx3.init()
    # filename = f"{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], 'speech.mp3')
    if os.path.exists(audio_path):
        os.remove(audio_path)
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    return render_template('index.html', message='Speech generated.', extracted_text=text, audio_file='audio/speech.mp3')

# Setup client  So. this is key setup over here and then a variable above which gets the details from an other file .env which is git ignored
vision_client = ComputerVisionClient(
    endpoint=vision_endpoint,
    credentials=CognitiveServicesCredentials(vision_key)
)

import traceback

def generate_caption(image_path):
    try:
        with open(image_path, "rb") as image_stream:
            analysis = vision_client.analyze_image_in_stream(
                image_stream,
                visual_features=["DESCRIPTION"]
            )
        if analysis.description and analysis.description.captions:
            return analysis.description.captions[0].text
        else:
            return "No description available."
    except Exception as e:
        print("Azure Vision API error:", e)
        traceback.print_exc()
        return "Captioning failed due to an error."




# OCR function using EasyOCR
def extract_text(image_path):
    result = reader.readtext(image_path, detail=0)
    return ' '.join(result)

# ✅ Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

