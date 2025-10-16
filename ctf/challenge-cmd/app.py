from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h2>Ping tool</h2>
    <form action="/ping" method="GET">
      Host: <input name="host" value="127.0.0.1">
      <input type="submit" value="Ping">
    </form>
    '''

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
