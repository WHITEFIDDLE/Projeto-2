from flask import Flask, request, render_template_string, jsonify
import sqlite3
import subprocess
import os
import hashlib
import pickle
import base64

app = Flask(__name__)

# Falha: secret hardcoded
app.config["SECRET_KEY"] = "admin-secret-key-123"

# Falha: credenciais hardcoded
DB_USER = "admin"
DB_PASSWORD = "password123"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

DATABASE = "demo.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO users (username, password, email)
        SELECT 'admin', 'admin123', 'admin@example.com'
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE username = 'admin'
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return """
    <h1>Vulnerable Demo App</h1>
    <p>Aplicação intencionalmente vulnerável para testar scanners.</p>

    <ul>
        <li><a href="/login?username=admin&password=admin123">SQL Injection test</a></li>
        <li><a href="/search?q=<script>alert(1)</script>">XSS test</a></li>
        <li><a href="/ping?host=127.0.0.1">Command Injection test</a></li>
        <li><a href="/hash?password=teste123">Weak Hash test</a></li>
        <li><a href="/debug">Debug Info Exposure</a></li>
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
            "message": "Login realizado com sucesso",
            "user": user
        })

    return jsonify({
        "status": "error",
        "message": "Credenciais inválidas"
    })


@app.route("/search")
def search():
    query = request.args.get("q", "")

    # Falha: XSS refletido
    template = f"""
    <h1>Resultado da busca</h1>
    <p>Você pesquisou por: {query}</p>
    """

    return render_template_string(template)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Falha: command injection
    command = f"ping -n 1 {host}"

    result = subprocess.check_output(
        command,
        shell=True,
        text=True,
        stderr=subprocess.STDOUT
    )

    return f"<pre>{result}</pre>"


@app.route("/hash")
def weak_hash():
    password = request.args.get("password", "")

    # Falha: uso de MD5 para senha
    hashed = hashlib.md5(password.encode()).hexdigest()

    return jsonify({
        "password": password,
        "md5": hashed
    })


@app.route("/deserialize", methods=["POST"])
def insecure_deserialize():
    data = request.json.get("payload", "")

    # Falha: desserialização insegura
    decoded = base64.b64decode(data)
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
        "secret_key": app.config["SECRET_KEY"],
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY
    })


@app.route("/redirect")
def open_redirect():
    next_url = request.args.get("next", "https://example.com")

    # Falha: open redirect
    return f"""
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url={next_url}" />
        </head>
        <body>
            Redirecionando para {next_url}
        </body>
    </html>
    """


@app.route("/file")
def file_read():
    file_name = request.args.get("name", "README.md")

    # Falha: path traversal / leitura insegura de arquivo
    with open(file_name, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    return f"<pre>{content}</pre>"


if __name__ == "__main__":
    init_db()

    # Falha: debug ativo
    app.run(host="0.0.0.0", port=5000, debug=True)