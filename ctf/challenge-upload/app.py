from flask import Flask, request, redirect, url_for, send_from_directory
import os
import subprocess
import urllib.parse

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
                <link rel=\"icon\" type=\"image/png\" href=\"/favicon.ico?v=1\" />
                <link rel=\"shortcut icon\" type=\"image/png\" href=\"/favicon.ico?v=1\" />
                <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/favicon.png?v=1\" />
                <link rel=\"apple-touch-icon\" href=\"/apple-touch-icon.png?v=1\" />
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
# On élargit volontairement les extensions pour le besoin du CTF (vulnérable)
ALLOWED_EXT = {'png','jpg','jpeg','gif','svg','txt','log','md','html','htm','php'}

@app.route('/')
def index():
    return send_from_directory('.', 'app.html')


@app.route('/app.js')
def app_js():
    return send_from_directory('.', 'app.js')


@app.route('/style.css')
def style_css():
    return send_from_directory('.', 'style.css')

@app.route('/favicon.ico')
def favicon():
    # sert l'icône depuis le volume monté /app/img
    return send_from_directory('img', 'icon.png')

@app.route('/favicon.png')
def favicon_png():
    return send_from_directory('img', 'icon.png')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory('img', 'icon.png')

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
        qfn = urllib.parse.quote(filename)
        link = f"/uploads/{qfn}"
        content = f"<p>Fichier enregistré : <code>{path}</code></p><p>Accès : <a class=\"btn btn-primary\" href=\"{link}\">{link}</a></p>"
        return render_page("Téléversement réussi", content)
    else:
        return render_page("Téléversement", "<p>Extension non autorisée.</p>")

@app.route('/uploads/<path:filename>')
def uploads(filename):
    # On laisse le serveur livrer directement le fichier, mais on fournit aussi une petite page d’info
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return render_page("Fichier introuvable", f"<p>Le fichier <code>{filename}</code> n’existe pas.</p>")
    ext = filename.rsplit('.',1)[1].lower() if '.' in filename else ''
    preview = []
    # Bouton de téléchargement toujours disponible
    qfn = urllib.parse.quote(filename)
    preview.append(f'<p><a class="btn btn-primary" href="/raw/{qfn}">Télécharger</a></p>')
    # Interprétation selon le type
    if ext in {'png','jpg','jpeg','gif','svg'}:
        # Afficher l'image directement
        preview.insert(0, f'<div class="preview"><img src="/raw/{qfn}" alt="{filename}" style="max-width:100%; border-radius:10px"/></div>')
    elif ext in {'html','htm'}:
        # Afficher via iframe pour rendre le HTML
        preview.insert(0, f'<div class="preview" style="height:420px"><iframe src="/raw/{qfn}" style="width:100%;height:100%;border:1px solid rgba(255,255,255,.08);border-radius:10px"></iframe></div>')
    elif ext in {'txt','log','md'}:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as fh:
                data = fh.read()
        except Exception as e:
            data = f"(impossible de lire le fichier: {e})"
        preview.insert(0, f'<pre style="white-space:pre-wrap">{data}</pre>')
    elif ext == 'php':
        # Exécuter le fichier PHP avec php-cli (intentionnellement vulnérable pour le CTF)
        try:
            proc = subprocess.run(["php", file_path], capture_output=True, text=True, timeout=5)
            out = proc.stdout or ''
            err = proc.stderr or ''
            code = proc.returncode
            php_block = f"<h3>Sortie PHP (code {code})</h3><pre>{out}</pre>"
            if err:
                php_block += f"<h4>Erreurs</h4><pre>{err}</pre>"
        except Exception as e:
            php_block = f"<p class=\"hint\">Erreur d'exécution PHP: {e}</p>"
        preview.insert(0, php_block)
    else:
        preview.insert(0, '<p class="hint">Aperçu non disponible pour ce type de fichier.</p>')

    info = f"<p>Fichier: <code>{filename}</code></p>" + ''.join(preview)
    return render_page("Aperçu", info, subtitle="Interprétation automatique selon le type (vulnérable)")


@app.route('/raw/<path:filename>')
def raw(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/secret')
def secret():
    return open('flag.txt').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
