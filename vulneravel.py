import os
import sqlite3
import subprocess
import hashlib
import pickle
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# Falha: secret hardcoded
app.config["SECRET_KEY"] = "minha-chave-secreta-123"

# Falha: credenciais hardcoded
DB_USER = "admin"
DB_PASSWORD = "admin123"
API_TOKEN = "token_super_secreto_123456"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

DATABASE = "app.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO users (username, password)
        SELECT 'admin', 'admin123'
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE username = 'admin'
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return """
    <h1>Vulnerable Python App</h1>
    <p>Aplicação simples com falhas intencionais.</p>

    <ul>
        <li>/login?username=admin&password=admin123</li>
        <li>/search?q=&lt;script&gt;alert(1)&lt;/script&gt;</li>
        <li>/ping?host=127.0.0.1</li>
        <li>/hash?password=teste123</li>
        <li>/read-file?name=vulnerable_app.py</li>
        <li>/debug</li>
    </ul>
    """


@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Falha: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "message": "Login realizado",
            "user": user
        })

    return jsonify({
        "status": "error",
        "message": "Usuário ou senha inválidos"
    })


@app.route("/search")
def search():
    q = request.args.get("q", "")

    # Falha: XSS refletido
    return f"""
    <h1>Busca</h1>
    <p>Você pesquisou por: {q}</p>
    """


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Falha: command injection
    command = f"ping -n 1 {host}"

    output = subprocess.check_output(
        command,
        shell=True,
        text=True
    )

    return f"<pre>{output}</pre>"


@app.route("/hash")
def hash_password():
    password = request.args.get("password", "")

    # Falha: MD5 é fraco para senha
    password_hash = hashlib.md5(password.encode()).hexdigest()

    return jsonify({
        "password": password,
        "hash": password_hash
    })


@app.route("/read-file")
def read_file():
    file_name = request.args.get("name", "vulnerable_app.py")

    # Falha: path traversal / leitura de arquivo sem validação
    with open(file_name, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    return f"<pre>{content}</pre>"


@app.route("/deserialize", methods=["POST"])
def deserialize():
    payload = request.json.get("payload", "")

    # Falha: desserialização insegura
    decoded = base64.b64decode(payload)
    obj = pickle.loads(decoded)

    return jsonify({
        "message": "Objeto desserializado",
        "object": str(obj)
    })


@app.route("/debug")
def debug():
    # Falha: exposição de informações sensíveis
    return jsonify({
        "environment": dict(os.environ),
        "db_user": DB_USER,
        "db_password": DB_PASSWORD,
        "api_token": API_TOKEN,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "flask_secret": app.config["SECRET_KEY"]
    })


if __name__ == "__main__":
    init_db()

    # Falha: debug ativo em aplicação web
    app.run(host="0.0.0.0", port=5000, debug=True)