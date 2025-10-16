from flask import Flask, request, redirect, url_for, send_from_directory
import os

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXT = {'png','jpg','jpeg','txt'}

@app.route('/')
def index():
    return '''
    <h2>Upload</h2>
    <form method="POST" enctype="multipart/form-data" action="/upload">
      File: <input type="file" name="file"><br>
      <input type="submit" value="Upload">
    </form>
    '''

def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    if not f:
        return "No file"
    filename = f.filename
    # VULN: save without sanitization and allow .txt to be served
    if allowed(filename):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        return f"Saved to {path}. Access at /uploads/{filename}"
    else:
        return "Extension not allowed"

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/secret')
def secret():
    return open('flag.txt').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
