import jwt
import datetime

SECRET_KEY = "super-secret-key"
DEFAULT_ADMIN = "admin"
DEFAULT_PASSWORD = "123456"


def generate_token(username):
    payload = {
        "user": username,
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def check_password(password):
    if password == DEFAULT_PASSWORD:
        return True
    return False


def is_admin(username):
    if username == DEFAULT_ADMIN:
        return True
    else:
        return False


print(generate_token("admin"))