from flask import Flask, render_template, url_for, request, redirect, send_file
from PIL import Image
import os

app = Flask(__name__)

# Create directories for uploads and processed files
uploader_file = "uploaders"
processed_file = "processed"
os.makedirs(uploader_file, exist_ok=True)
os.makedirs(processed_file, exist_ok=True)

app.config['uploader_file'] = uploader_file


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "No file uploaded.", 400

    # Validate file type
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
        return "Invalid file type. Please upload an image.", 400

    file_path = os.path.join(app.config['uploader_file'], file.filename)
    file.save(file_path)

    processed_file_path = os.path.join(processed_file, file.filename)
    with Image.open(file_path) as image_convt:
        image_convt.save(processed_file_path, "JPEG", quality=50)

    return redirect(url_for('result', filename=file.filename))


@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)


@app.route('/download/<filename>')
def download_file(filename):
    processed_filepath = os.path.join(processed_file, filename)
    if not os.path.exists(processed_filepath):
        return "File not found.", 404
    return send_file(processed_filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
