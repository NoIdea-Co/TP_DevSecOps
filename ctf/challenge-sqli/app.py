from flask import Flask, request, render_template_string, send_from_directory
import sqlite3

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

DB = 'sqli.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
    c.execute("DELETE FROM users;")
    c.execute("INSERT INTO users(username,password) VALUES ('alice','alicepass'), ('bob','bobpass');")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'app.html')


@app.route('/app.js')
def app_js():
    return send_from_directory('.', 'app.js')


@app.route('/style.css')
def style_css():
    return send_from_directory('.', 'style.css')

@app.route('/login')
def login():
    uname = request.args.get('username','')
    pwd = request.args.get('password','')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        if uname and not pwd:
            # Étape 1: si seul le username est fourni, on fait une recherche vulnérable (LIKE) pour énumérer
            # VULN: concaténation non paramétrée sur LIKE
            query_enum = f"SELECT username FROM users WHERE username LIKE '%{uname}%';"
            c.execute(query_enum)
            rows = c.fetchall()
            if rows:
                items = ''.join(f"<li><code>{u[0]}</code></li>" for u in rows)
                content = f"<p>Utilisateurs trouvés :</p><ul>{items}</ul>"
            else:
                content = "<p>Aucun utilisateur correspondant.</p>"
            hint = "<p class=\"hint\">Indice : utilisez ces informations pour la suite.</p>"
            return render_page("Énumération d’utilisateurs", content + hint, subtitle=f"Motif : {uname}")
        else:
            # Étape 2: username paramétré, mot de passe injectable
            # Important: on encadre la condition du mot de passe pour éviter que OR '1'='1' n'échappe au filtre username
            query = "SELECT username FROM users WHERE username = ? AND (password = '" + pwd + "');"
            c.execute(query, (uname,))
            row = c.fetchone()
            if row:
                username = str(row[0])
                if username.lower() == 'bob':
                    # Cas Bob: page similaire mais sans flag, on donne un indice supplémentaire
                    content = (
                        f"<p class=\"subtitle\">Bienvenue, <strong>{username}</strong> !</p>"
                        f"<p class=\"hint\">Indice : ce compte ne dispose pas des droits nécessaires. Vérifiez peut‑être un autre utilisateur…</p>"
                    )
                    return render_page("Connexion réussie", content)
                else:
                    # Cas standard (ex: alice): on affiche le flag
                    try:
                        flag = open('flag.txt').read().strip()
                    except Exception:
                        flag = '(flag indisponible)'
                    content = (
                        f"<p class=\"subtitle\">Bienvenue, <strong>{username}</strong> !</p>"
                        f"<p><strong>Flag :</strong> <code>{flag}</code></p>"
                        f"<p class=\"hint\">Astuce : essayez aussi de contourner l’authentification.</p>"
                    )
                    return render_page("Connexion réussie", content)
            else:
                content = "<p>Identifiants invalides. Réessayez…</p>"
                return render_page("Échec de connexion", content)
    except Exception as e:
        content = f"<p class=\"hint\">Erreur SQL :</p><pre>{e}</pre>"
        return render_page("Erreur", content)
    finally:
        conn.close()

@app.route('/flag')
def flag():
    # endpoint qui retourne le flag si on parvient à bypasser l'auth
    return open('flag.txt').read()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
