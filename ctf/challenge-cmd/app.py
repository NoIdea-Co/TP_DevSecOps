from flask import Flask, request, send_from_directory
import subprocess

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
    return send_from_directory('img', 'icon.png')

@app.route('/favicon.png')
def favicon_png():
    return send_from_directory('img', 'icon.png')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return send_from_directory('img', 'icon.png')

@app.route('/ping')
def ping():
    host = request.args.get('host','127.0.0.1')
    # VULN: concatenation in shell command
    try:
        output = subprocess.check_output(f"ping -c 1 {host}", shell=True, stderr=subprocess.STDOUT, timeout=5)
        content = f"<pre>{output.decode()}</pre>"
        return render_page("Résultat du ping", content, subtitle=f"Hôte : {host}")
    except subprocess.CalledProcessError as e:
        content = f"<p class=\"hint\">Erreur :</p><pre>{e.output.decode()}</pre>"
        return render_page("Échec du ping", content, subtitle=f"Hôte : {host}")
    except Exception as ex:
        content = f"<p class=\"hint\">Exception :</p><pre>{ex}</pre>"
        return render_page("Exception", content)

@app.route('/flag')
def flag():
    return open('flag.txt').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
