from utils.detection import analyze_image
from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "C:\\AI_ML\\uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page
@app.route('/')
def home():
    return render_template("index.html")

# Upload route
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    report = analyze_image(filepath)

    return render_template("index.html", message=report)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)