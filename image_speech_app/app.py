from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filepath)
            return f"Image {image.filename} uploaded successfully!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)