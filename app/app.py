from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello, DevSecOps world!</h1><p>Bienvenue dans le TP sécurité web proactive.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
