from flask import Flask, request, redirect, url_for, send_from_directory
import os

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
def render_page(title: str, inner_html: str, subtitle: str | None = None) -> str:
        sub = f'<p class="subtitle">{subtitle}</p>' if subtitle else ''
        return f"""
        <!DOCTYPE html>
        <html lang=\"fr\">
            <head>
                <meta charset=\"UTF-8\" />
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
                <link rel=\"stylesheet\" href=\"/style.css\" />
                <title>{title}</title>
                <script defer src=\"/app.js\"></script>
            </head>
            <body>
                <header class=\"site-header\"><div class=\"container\"><div class=\"brand\">CTF — Sécurité Web</div></div></header>
                <main class=\"centered\"><div class=\"container\"><section class=\"card\">
                    <h1 class=\"title\">{title}</h1>
                    {sub}
                    {inner_html}
                    <div class=\"actions\" style=\"margin-top:14px\"><a class=\"btn btn-secondary\" href=\"/\">Retour</a></div>
                </section></div></main>
            </body>
        </html>
        """
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXT = {'png','jpg','jpeg','txt'}

@app.route('/')
def index():
    return send_from_directory('.', 'app.html')


@app.route('/app.js')
def app_js():
    return send_from_directory('.', 'app.js')


@app.route('/style.css')
def style_css():
    return send_from_directory('.', 'style.css')

def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    if not f:
        return render_page("Téléversement", "<p>Aucun fichier reçu.</p>")
    filename = f.filename
    # VULN: save without sanitization and allow .txt to be served
    if allowed(filename):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        link = f"/uploads/{filename}"
        content = f"<p>Fichier enregistré : <code>{path}</code></p><p>Accès : <a class=\"btn btn-primary\" href=\"{link}\">{link}</a></p>"
        return render_page("Téléversement réussi", content)
    else:
        return render_page("Téléversement", "<p>Extension non autorisée.</p>")

@app.route('/uploads/<path:filename>')
def uploads(filename):
    # On laisse le serveur livrer directement le fichier, mais on fournit aussi une petite page d’info
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return render_page("Fichier introuvable", f"<p>Le fichier <code>{filename}</code> n’existe pas.</p>")
    info = f"<p>Fichier: <code>{filename}</code></p><p><a class=\"btn btn-primary\" href=\"/raw/{filename}\">Télécharger</a></p>"
    return render_page("Aperçu", info, subtitle="Servi tel quel par l’application")


@app.route('/raw/<path:filename>')
def raw(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/secret')
def secret():
    return open('flag.txt').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
