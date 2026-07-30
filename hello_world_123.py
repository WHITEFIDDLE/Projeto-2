import os
import subprocess
import hashlib
import sqlite3

PASSWORD = "admin123"
API_KEY = "ghp_1234567890abcdef1234567890abcdef123456"

def command_injection():
    cmd = input("Digite comando: ")
    os.system(cmd)

def shell_true():
    arquivo = input("Arquivo: ")
    subprocess.call("cat " + arquivo, shell=True)

def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def sql_injection(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

def broad_exception():
    try:
        return 10 / 0
    except:
        return None