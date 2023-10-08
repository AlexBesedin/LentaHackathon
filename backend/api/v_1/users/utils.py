import random
import string


def generate_random_code(length=8):
    """Функция генерация пароля"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
