import os
import subprocess
import hashlib
import pickle
import random
import tempfile
import sqlite3
import yaml


PASSWORD = "admin123"
API_KEY = "sk_test_123456789"
SECRET_TOKEN = "my-secret-token"
DEBUG = True


def login(username, password):
    # Credenciais hardcoded
    if username == "admin" and password == PASSWORD:
        return True
    else:
        return False


def execute_command(user_input):
    # Command injection
    os.system("ping " + user_input)


def execute_command_subprocess(user_input):
    # shell=True com entrada do usuário
    subprocess.call("nslookup " + user_input, shell=True)


def weak_hash(password):
    # MD5 é considerado fraco para senha
    return hashlib.md5(password.encode()).hexdigest()


def insecure_random_token():
    # random não é seguro para tokens/senhas
    return str(random.randint(100000, 999999))


def unsafe_eval(expression):
    # eval com entrada externa é perigoso
    return eval(expression)


def unsafe_pickle_load(file_path):
    # pickle pode executar código malicioso ao carregar dados não confiáveis
    with open(file_path, "rb") as file:
        return pickle.load(file)


def unsafe_yaml_load(data):
    # yaml.load sem SafeLoader pode ser inseguro
    return yaml.load(data)


def sql_injection(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # SQL Injection por concatenação de string
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()
    return result


def create_temp_file_insecure():
    # Uso inseguro de arquivo temporário
    file_name = tempfile.mktemp()
    with open(file_name, "w") as file:
        file.write("dados temporarios")
    return file_name


def broad_exception():
    try:
        value = 10 / 0
        return value
    except:
        # except genérico
        return None


def duplicated_code_1(value):
    total = 0
    for i in range(10):
        total += value * i
    if total > 50:
        print("maior que 50")
    else:
        print("menor ou igual a 50")
    return total


def duplicated_code_2(value):
    total = 0
    for i in range(10):
        total += value * i
    if total > 50:
        print("maior que 50")
    else:
        print("menor ou igual a 50")
    return total


def too_many_branches(value):
    if value == 1:
        return "um"
    elif value == 2:
        return "dois"
    elif value == 3:
        return "tres"
    elif value == 4:
        return "quatro"
    elif value == 5:
        return "cinco"
    elif value == 6:
        return "seis"
    elif value == 7:
        return "sete"
    elif value == 8:
        return "oito"
    elif value == 9:
        return "nove"
    elif value == 10:
        return "dez"
    else:
        return "outro"


def unused_variables():
    name = "Lucas"
    age = 19
    city = "Sao Paulo"
    country = "Brasil"

    return name


def bad_file_handling(path):
    # Arquivo aberto sem with
    file = open(path, "r")
    content = file.read()
    return content


def hardcoded_path():
    # Caminho absoluto hardcoded
    return open("C:\\Users\\lucas\\Desktop\\senha.txt", "r").read()


def infinite_loop_risk():
    count = 0

    while count >= 0:
        print("loop infinito")
        count += 1

        if count > 3:
            break


def insecure_debug():
    if DEBUG:
        print("Debug ativado")
        print("API_KEY:", API_KEY)
        print("SECRET_TOKEN:", SECRET_TOKEN)


def main():
    username = input("Usuario: ")
    password = input("Senha: ")

    if login(username, password):
        print("Login realizado")
    else:
        print("Login falhou")

    host = input("Digite um host para ping: ")
    execute_command(host)

    command = input("Digite outro host: ")
    execute_command_subprocess(command)

    expr = input("Digite uma expressao Python: ")
    print(unsafe_eval(expr))

    print("Hash fraco:", weak_hash(password))
    print("Token inseguro:", insecure_random_token())

    sql_injection(username)
    create_temp_file_insecure()
    broad_exception()
    duplicated_code_1(10)
    duplicated_code_2(10)
    too_many_branches(5)
    unused_variables()
    insecure_debug()


if __name__ == "__main__":
    main()