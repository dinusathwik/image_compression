from fileinput import filename

from flask import Flask, render_template,url_for,request,redirect
# from werkzeug.utils import secure_filename
import os
import PIL as img

app = Flask(__name__)

uploader_file = "uploaders"
processed_file = "processed"
os.mkdir(uploader_file,exit_ok(True))
os.mkdir(processed_file,exit_ok(True))
app.config['uploader_file']= uploader_file

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload',method=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(app.config['uploader_file'], file.filename)
    file.save(file_path)

    processed_file_path = os.path.join(processed_file, file.filename)
    with img.open(file_path) as image_convt:
        image_convt.save(processed_file_path, "JPEG" ,quality=50)
    return redirect(url_for('result',filename=file.filename))

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    processed_filepath = os.path.join(processed_file, filename)
    return send_file(processed_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

