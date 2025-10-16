from flask import Flask, request, send_from_directory
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'app.html')


@app.route('/app.css')
def app_css():
    return send_from_directory('.', 'app.css')


@app.route('/app.js')
def app_js():
    return send_from_directory('.', 'app.js')

@app.route('/ping')
def ping():
    host = request.args.get('host','127.0.0.1')
    # VULN: concatenation in shell command
    try:
        output = subprocess.check_output(f"ping -c 1 {host}", shell=True, stderr=subprocess.STDOUT, timeout=5)
        return f"<pre>{output.decode()}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"
    except Exception as ex:
        return f"Exception: {ex}"

@app.route('/flag')
def flag():
    return open('flag.txt').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
