from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello, DevSecOps world!</h1><p>Bienvenue dans le TP sécurité web proactive.</p>"

# ---- PoC vulnérable (NE PAS EXPOSER EN PROD) ----
@app.route('/vuln-eval')
def vuln_eval():
    """
    Endpoint volontairement vulnérable pour exercice :
    /vuln-eval?expr=2+2
    """
    expr = request.args.get('expr', '')
    if not expr:
        return "Donne une expression via ?expr="
    # Danger : evaluation arbitraire !
    try:
        result = eval(expr)  # <<<<< vulnérable
        return f"Résultat: {result}"
    except Exception as e:
        abort(400, f"Erreur: {e}")
