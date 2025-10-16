# app/app.py
from flask import Flask, request, abort, current_app
import ast
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello, DevSecOps world!</h1><p>Bienvenue dans le TP sécurité web proactive.</p>"

# ---- SAFE evaluator for arithmetic expressions ----
ALLOWED_AST_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.USub, ast.UAdd, ast.Load, ast.Tuple, ast.List
}

def is_safe_node(node):
    return type(node) in ALLOWED_AST_NODES

def safe_eval_arith(expr: str):
    """
    Évalue de manière sûre des expressions arithmétiques simples comme '2+2' ou '3*(4+1)'.
    Lève ValueError si l'expression contient un noeud non autorisé.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except Exception as e:
        raise ValueError("Expression invalide")

    # Walk AST and ensure only allowed nodes
    for node in ast.walk(parsed):
        if not is_safe_node(node):
            raise ValueError("Usage non autorisé dans l'expression")
    # Use eval on compiled AST (safe because nodes are controlled)
    compiled = compile(parsed, filename="<ast>", mode="eval")
    return eval(compiled, {"__builtins__": {}})

# ---- POC endpoint: gated by env var and safe mode ----
@app.route('/vuln-eval')
def vuln_eval():
    """
    Endpoint sécurisé pour évaluer EXPR arithmétique :
    /vuln-eval?expr=2+2

    Le endpoint PoC n'est actif que si la variable d'environnement ENABLE_POC est 'true'.
    """
    enable = os.getenv("ENABLE_POC", "false").lower()
    if enable not in ("1", "true", "yes"):
        abort(404)

    expr = request.args.get('expr', '')
    if not expr:
        return "Donne une expression via ?expr="
    try:
        result = safe_eval_arith(expr)
        return f"Résultat: {result}"
    except ValueError as e:
        abort(400, str(e))
    except Exception:
        abort(400, "Erreur lors de l'évaluation")
