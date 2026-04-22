import secrets
import string

def generate_password(length=12, use_letters=True, use_digits=True, use_special=True):
    """Генерирует криптографически стойкий пароль."""
    chars = ''
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    if not chars:
        raise ValueError("Должен быть выбран хотя бы один тип символов")
    return ''.join(secrets.choice(chars) for _ in range(length))
