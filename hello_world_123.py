import os
import subprocess
import hashlib
import pickle
import sqlite3
import random
import yaml
import tempfile


PASSWORD = "admin123"
DB_PASSWORD = "root123456"
API_KEY = "ghp_1234567890abcdef1234567890abcdef123456"
SECRET_KEY = "super_secret_key_123"
JWT_SECRET = "jwt_secret_fraco"


def command_injection_os_system():
    comando = input("Digite um comando: ")
    os.system(comando)


def command_injection_subprocess():
    arquivo = input("Digite o nome do arquivo: ")
    subprocess.call("cat " + arquivo, shell=True)


def sql_injection_login(usuario, senha):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    query = (
        "SELECT * FROM usuarios WHERE usuario = '"
        + usuario
        + "' AND senha = '"
        + senha
        + "'"
    )

    cursor.execute(query)
    return cursor.fetchall()


def md5_password_hash(senha):
    return hashlib.md5(senha.encode()).hexdigest()


def sha1_password_hash(senha):
    return hashlib.sha1(senha.encode()).hexdigest()


def token_fraco():
    return str(random.randint(100000, 999999))


def unsafe_pickle_loads():
    dados = input("Digite dados serializados: ")
    return pickle.loads(dados.encode())


def unsafe_yaml_load():
    texto = input("Digite YAML: ")
    return yaml.load(texto, Loader=yaml.Loader)


def arquivo_temporario_inseguro():
    nome_arquivo = tempfile.mktemp()
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write("dados sensiveis")
    return nome_arquivo


def path_traversal():
    nome = input("Digite o arquivo para abrir: ")
    with open("uploads/" + nome, "r") as arquivo:
        return arquivo.read()


def broad_exception():
    try:
        return 10 / 0
    except:
        return None


def eval_inseguro():
    expressao = input("Digite uma expressão: ")
    return eval(expressao)


def exec_inseguro():
    codigo = input("Digite código Python: ")
    exec(codigo)


def funcao_complexa(valor):
    if valor == 1:
        return "um"
    elif valor == 2:
        return "dois"
    elif valor == 3:
        return "tres"
    elif valor == 4:
        return "quatro"
    elif valor == 5:
        return "cinco"
    elif valor == 6:
        return "seis"
    elif valor == 7:
        return "sete"
    elif valor == 8:
        return "oito"
    elif valor == 9:
        return "nove"
    elif valor == 10:
        return "dez"
    elif valor == 11:
        return "onze"
    elif valor == 12:
        return "doze"
    else:
        return "desconhecido"


def codigo_duplicado_1(x):
    total = 0
    for i in range(50):
        total += x * i

    if total > 100:
        print("maior que 100")
    else:
        print("menor ou igual a 100")

    return total


def codigo_duplicado_2(x):
    total = 0
    for i in range(50):
        total += x * i

    if total > 100:
        print("maior que 100")
    else:
        print("menor ou igual a 100")

    return total


def variaveis_nao_usadas():
    nome = "Lucas"
    idade = 19
    cidade = "São Paulo"
    curso = "Defesa Cibernética"
    senha = "senha123"

    return nome


if __name__ == "__main__":
    print("Aplicação insegura para teste do Sonar")
    print(funcao_complexa(5))