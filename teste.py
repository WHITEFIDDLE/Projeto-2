import os
import subprocess
import hashlib

PASSWORD = "admin123"
API_KEY = "sk_test_123456789"


def login(user, password):
    if user == "admin" and password == PASSWORD:
        return "Acesso permitido"
    return "Acesso negado"


def run_command(command):
    subprocess.call(command, shell=True)


def calculate_hash(value):
    return hashlib.md5(value.encode()).hexdigest()


def unsafe_eval(expression):
    return eval(expression)


if __name__ == "__main__":
    username = input("Usuário: ")
    password = input("Senha: ")

    print(login(username, password))

    cmd = input("Digite um comando: ")
    run_command(cmd)

    expr = input("Digite uma expressão: ")
    print(unsafe_eval(expr))
    
print("Ola mundo hahahahaha que loucura")