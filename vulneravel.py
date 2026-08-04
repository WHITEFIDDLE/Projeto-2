import os
import subprocess
import sqlite3
import hashlib
import pickle
import yaml
import tempfile
import random


# Falha: secrets hardcoded
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/prod"
API_KEY = "sk_live_123456789abcdef"
JWT_SECRET = "super-secret-jwt-key"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Falha: SQL Injection por concatenação de string
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"

    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    return result


def search_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Falha: SQL Injection via f-string
    query = f"SELECT * FROM users WHERE id = {user_id}"

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result


def ping_host(host):
    # Falha: command injection
    command = "ping -n 1 " + host

    output = subprocess.check_output(
        command,
        shell=True,
        text=True
    )

    return output


def list_directory(path):
    # Falha: command injection com os.system
    os.system("dir " + path)


def hash_password_md5(password):
    # Falha: MD5 não deve ser usado para senha
    return hashlib.md5(password.encode()).hexdigest()


def hash_password_sha1(password):
    # Falha: SHA1 também é fraco para senha
    return hashlib.sha1(password.encode()).hexdigest()


def insecure_random_token():
    # Falha: random não é adequado para token de segurança
    token = ""

    for _ in range(16):
        token += str(random.randint(0, 9))

    return token


def load_pickle_data(file_path):
    # Falha: pickle.load pode executar código malicioso se o arquivo for não confiável
    with open(file_path, "rb") as file:
        data = pickle.load(file)

    return data


def load_yaml_config(file_path):
    # Falha: yaml.load sem SafeLoader
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.Loader)

    return config


def read_file(file_name):
    # Falha: path traversal se file_name vier de usuário
    with open(file_name, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def write_temp_file(content):
    # Falha: tempfile inseguro com delete=False e conteúdo sensível
    temp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    temp.write(content)
    temp.close()

    return temp.name


def expose_environment():
    # Falha: exposição de variáveis de ambiente
    return dict(os.environ)


def dangerous_eval(expression):
    # Falha: eval executa código arbitrário
    return eval(expression)


def dangerous_exec(code):
    # Falha: exec executa código arbitrário
    exec(code)


def disabled_ssl_verification():
    import requests

    # Falha: verify=False desabilita validação TLS
    response = requests.get(
        "https://example.com",
        verify=False,
        timeout=10
    )

    return response.text


def broad_exception():
    try:
        result = 10 / 0
        return result
    except Exception:
        # Falha: captura genérica e silenciosa
        pass


def hardcoded_admin_check(username, password):
    # Falha: senha hardcoded
    if username == "admin" and password == "admin123":
        return True

    return False


def main():
    print("Security Bad Practices Demo")
    print("Token inseguro:", insecure_random_token())
    print("MD5:", hash_password_md5("admin123"))
    print("SHA1:", hash_password_sha1("admin123"))
    print("Admin:", hardcoded_admin_check("admin", "admin123"))


if __name__ == "__main__":
    main()